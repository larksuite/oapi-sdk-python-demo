"""
获取部门下所有用户列表，使用到两个OpenAPI：
1. [获取子部门列表](https://open.feishu.cn/document/server-docs/contact-v3/department/children)
2. [获取部门直属用户列表](https://open.feishu.cn/document/server-docs/contact-v3/user/find_by_department)
"""

import lark_oapi as lark
from lark_oapi.api.contact.v3 import *


class ListUserByDepartmentRequest(object):
    def __init__(self) -> None:
        super().__init__()
        self.department_id: Optional[str] = None  # open_department_id，必填


class ListUserByDepartmentResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.children_department_response: Optional[ChildrenDepartmentResponseBody] = None
        self.find_by_department_user_response: List[User] = []


# 获取部门下所有用户列表
def list_user_by_department(client: lark.Client, request: ListUserByDepartmentRequest) -> BaseResponse:
    # 获取子部门列表
    children_department_req = ChildrenDepartmentRequest.builder() \
        .department_id_type("open_department_id") \
        .department_id(request.department_id) \
        .fetch_child(True) \
        .build()

    children_department_resp = client.contact.v3.department.children(children_department_req)

    if not children_department_resp.success():
        lark.logger.error(
            f"client.contact.v3.department.children failed, "
            f"code: {children_department_resp.code}, "
            f"msg: {children_department_resp.msg}, "
            f"log_id: {children_department_resp.get_log_id()}")
        return children_department_resp

    # 获取部门直属用户列表
    users = []
    open_department_ids = [request.department_id]
    for i in children_department_resp.data.items:
        open_department_ids.append(i.open_department_id)

    for id in open_department_ids:
        find_by_department_user_req = FindByDepartmentUserRequest.builder() \
            .department_id(id) \
            .build()

        find_by_department_user_resp = client.contact.v3.user.find_by_department(find_by_department_user_req)

        if not find_by_department_user_resp.success():
            lark.logger.error(
                f"client.contact.v3.user.find_by_department failed, "
                f"code: {find_by_department_user_resp.code}, "
                f"msg: {find_by_department_user_resp.msg}, "
                f"log_id: {find_by_department_user_resp.get_log_id()}")
            return find_by_department_user_resp

        users.extend(find_by_department_user_resp.data.items)

    # 返回结果
    response = ListUserByDepartmentResponse()
    response.code = 0
    response.msg = "success"
    response.children_department_response = children_department_resp.data
    response.find_by_department_user_response = users

    return response

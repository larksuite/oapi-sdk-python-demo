"""
创建多维表格同时添加数据表，使用到两个OpenAPI：
1. [创建多维表格](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app/create)
2. [新增一个数据表](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table/create)
"""

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


class CreateAppAndTablesRequest(object):
    def __init__(self) -> None:
        super().__init__()
        self.name: Optional[str] = None  # 多维表格名称，必填
        self.folder_token: Optional[str] = None  # 多维表格归属文件夹，必填
        self.tables: List[ReqTable] = []  # 数据表，不填则不创建


class CreateAppAndTablesResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.create_app_response: Optional[CreateAppResponseBody] = None
        self.create_app_tables_response: Optional[CreateAppTableResponseBody] = None


# 创建多维表格同时添加数据表
def create_app_and_tables(client: lark.Client, request: CreateAppAndTablesRequest) -> BaseResponse:
    # 创建多维表格
    create_app_req = CreateAppRequest.builder() \
        .request_body(ReqApp.builder()
                      .name(request.name)
                      .folder_token(request.folder_token)
                      .build()) \
        .build()

    create_app_resp = client.bitable.v1.app.create(create_app_req)

    if not create_app_resp.success():
        lark.logger.error(
            f"client.bitable.v1.app.create failed, "
            f"code: {create_app_resp.code}, "
            f"msg: {create_app_resp.msg}, "
            f"log_id: {create_app_resp.get_log_id()}")
        return create_app_resp

    # 添加数据表
    option = lark.RequestOption.builder().headers({"X-Tt-Logid": create_app_resp.get_log_id()}).build()
    tables = []
    for table in request.tables:
        create_app_table_req = CreateAppTableRequest.builder() \
            .app_token(create_app_resp.data.app.app_token) \
            .request_body(CreateAppTableRequestBody.builder()
                          .table(table)
                          .build()) \
            .build()

        create_app_table_resp = client.bitable.v1.app_table.create(create_app_table_req, option)

        if not create_app_table_resp.success():
            lark.logger.error(
                f"client.bitable.v1.app_table.create failed, "
                f"code: {create_app_table_resp.code}, "
                f"msg: {create_app_table_resp.msg}, "
                f"log_id: {create_app_table_resp.get_log_id()}")
            return create_app_table_resp

        tables.append(create_app_table_resp.data)

    # 返回结果
    response = CreateAppAndTablesResponse()
    response.code = 0
    response.msg = "success"
    response.create_app_response = create_app_resp.data
    response.create_app_tables_response = tables

    return response

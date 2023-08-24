"""
复制粘贴某个范围的单元格数据，使用到两个OpenAPI：
1. [读取单个范围](https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range)
2. [向单个范围写入数据](https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/write-data-to-a-single-range)
"""
import json
from typing import Optional, Dict

import lark_oapi as lark


class CopyAndPasteByRangeRequest(object):
    def __init__(self) -> None:
        self.spreadsheetToken: Optional[str] = None  # 表格token，必填
        self.src_range: Optional[str] = None  # 来源范围，必填
        self.dst_range: Optional[str] = None  # 目标范围，必填


class CopyAndPasteRangeResponse(lark.BaseResponse):
    def __init__(self):
        super().__init__()
        self.read_response: Optional[Dict] = None
        self.write_response: Optional[Dict] = None


# 复制粘贴某个范围的单元格数据
def copy_and_paste_range(client: lark.Client, request: CopyAndPasteByRangeRequest) -> lark.BaseResponse:
    # 读取单个范围
    read_req: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.GET) \
        .uri(f"/open-apis/sheets/v2/spreadsheets/{request.spreadsheetToken}/values/{request.src_range}") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .build()

    read_resp = client.request(read_req)

    if not read_resp.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, "
            f"code: {read_resp.code}, "
            f"msg: {read_resp.msg}, "
            f"log_id: {read_resp.get_log_id()}")
        return read_resp

    # 向单个范围写入数据
    option = lark.RequestOption.builder().headers({"X-Tt-Logid": read_resp.get_log_id()}).build()
    read_data = json.loads(str(read_resp.raw.content, lark.UTF_8)).get("data")
    body = {
        "valueRange": {
            "range": request.dst_range,
            "values": read_data.get("valueRange").get("values"),
        }
    }
    write_req: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.PUT) \
        .uri(f"/open-apis/sheets/v2/spreadsheets/{request.spreadsheetToken}/values") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .body(body) \
        .build()

    write_resp = client.request(write_req, option)

    if not write_resp.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, "
            f"code: {write_resp.code}, "
            f"msg: {write_resp.msg}, "
            f"log_id: {write_resp.get_log_id()}")
        return write_resp

    # 返回结果
    response = CopyAndPasteRangeResponse()
    response.code = 0
    response.msg = "success"
    response.read_response = read_data
    response.write_response = json.loads(str(write_resp.raw.content, lark.UTF_8)).get("data")

    return response

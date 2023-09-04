"""
下载指定范围单元格的所有素材列表，使用到两个OpenAPI：
1. [读取单个范围](https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range)
2. [下载素材](https://open.feishu.cn/document/server-docs/docs/drive-v1/media/download)
"""

import json

import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


class DownloadMediaByRangeRequest(object):
    def __init__(self) -> None:
        self.spreadsheetToken: Optional[str] = None  # 表格token，必填
        self.range: Optional[str] = None  # 单元格范围，必填


class DownloadMediaByRangeResponse(lark.BaseResponse):
    def __init__(self):
        super().__init__()
        self.read_response: Optional[Dict] = None
        self.download_media_response: List[DownloadMediaResponse] = []


# 下载指定范围单元格的所有素材列表
def download_media_by_range(client: lark.Client, request: DownloadMediaByRangeRequest):
    # 读取单个范围
    read_req: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.GET) \
        .uri(f"/open-apis/sheets/v2/spreadsheets/{request.spreadsheetToken}/values/{request.range}") \
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

    # 下载文件
    read_data = json.loads(str(read_resp.raw.content, lark.UTF_8)).get("data")
    tokens = _parse_file_token(read_data.get("valueRange").get("values"), [])
    option = lark.RequestOption.builder().headers({"X-Tt-Logid": read_resp.get_log_id()}).build()
    files = []

    for token in tokens:
        download_media_req = DownloadMediaRequest.builder() \
            .file_token(token) \
            .build()

        download_media_resp = client.drive.v1.media.download(download_media_req, option)

        if not download_media_resp.success():
            lark.logger.error(
                f"client.drive.v1.media.download failed, "
                f"code: {read_resp.code}, "
                f"msg: {read_resp.msg}, "
                f"log_id: {read_resp.get_log_id()}")
            return download_media_resp

        files.append(download_media_resp)

    # 返回结果
    response = DownloadMediaByRangeResponse()
    response.code = 0
    response.msg = "success"
    response.read_response = read_data
    response.download_media_response = files

    return response


def _parse_file_token(values: List[Any], tokens: List[str]) -> List[str]:
    if values is None or len(values) == 0:
        return tokens
    for i in values:
        if isinstance(i, List):
            _parse_file_token(i, tokens)
        elif isinstance(i, dict) and "fileToken" in i:
            tokens.append(i.get("fileToken"))

    return tokens

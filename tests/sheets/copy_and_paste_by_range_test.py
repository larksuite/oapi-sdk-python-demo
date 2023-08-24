from client import client
from composite_api.sheets.copy_and_paste_by_range import *

req = CopyAndPasteByRangeRequest()
req.spreadsheetToken = "T90VsUqrYhrnGCtBKS3cLCgQnih"
req.src_range = "53988e!A1:B5"
req.dst_range = "53988e!C1:D5"

resp = copy_and_paste_range(client, req)
print(lark.JSON.marshal(resp, indent=4))

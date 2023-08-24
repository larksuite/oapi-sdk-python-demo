from client import client
from composite_api.sheets.download_media_by_range import *

req = DownloadMediaByRangeRequest()
req.spreadsheetToken = "T90VsUqrYhrnGCtBKS3cLCgQnih"
req.range = "53988e!A1:A7"

resp = download_media_by_range(client, req)
for i in resp.download_media_response:
    f = open(f"/Users/bytedance/Desktop/{i.file_name}", "wb")
    f.write(i.file.read())
    f.close()


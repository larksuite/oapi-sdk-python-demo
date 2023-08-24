from client import client
from composite_api.im.send_file import *

req = SendFileRequest()
req.file_type = "pdf"
req.file_name = "demo.pdf"
req.file = open("/Users/bytedance/Desktop/demo.pdf", "rb")
req.receive_id_type = "open_id"
req.receive_id = "ou_a79a0f82add14976e3943f4deb17c3fa"

resp = send_file(client, req)
print(lark.JSON.marshal(resp, indent=4))

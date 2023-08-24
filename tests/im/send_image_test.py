from client import client
from composite_api.im.send_image import *

req = SendImageRequest()
req.image = open("/Users/bytedance/Desktop/demo.png", "rb")
req.receive_id_type = "open_id"
req.receive_id = "ou_a79a0f82add14976e3943f4deb17c3fa"

resp = send_image(client, req)
print(lark.JSON.marshal(resp, indent=4))

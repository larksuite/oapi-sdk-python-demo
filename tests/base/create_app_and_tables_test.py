from client import client
from composite_api.base.create_app_and_tables import *

req = CreateAppAndTablesRequest()
req.name = "这是多维表格"
req.folder_token = "Y9LhfoWNZlKxWcdsf2fcPP0SnXc"
req.tables = [
    ReqTable.builder()
    .name("这是数据表1")
    .fields([AppTableCreateHeader.builder().field_name("field1").type(1).build(),
             AppTableCreateHeader.builder().field_name("field2").type(2).build()])
    .build(),
    ReqTable.builder()
    .name("这是数据表2")
    .fields([AppTableCreateHeader.builder().field_name("field3").type(5).build(),
             AppTableCreateHeader.builder().field_name("field4").type(13).build()])
    .build(),
]

resp = create_app_and_tables(client, req)
print(lark.JSON.marshal(resp, indent=4))

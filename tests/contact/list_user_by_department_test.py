from lark_oapi import JSON

from client import client
from composite_api.contact.list_user_by_department import ListUserByDepartmentRequest, list_user_by_department

req = ListUserByDepartmentRequest()
req.department_id = 0

resp = list_user_by_department(client, req)
print(JSON.marshal(resp, indent=4))

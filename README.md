# 飞书开放接口使用示例
* 针对多 API 串行调用场景，封装 API [组合函数](./composite_api)，减少开发者对接 API 个数，提高开发效率；
* 针对常见业务场景，封装可直接运行的 [Quick-Start](./quick_start)，帮助开发者快速上手 API 接入。

## 组合函数
目前提供以下组合函数：
* 消息
  * [发送文件消息](./composite_api/im/send_file.py)
  * [发送图片消息](./composite_api/im/send_image.py)
* 通讯录
  * [获取部门下所有用户列表](./composite_api/contact/list_user_by_department.py)
* 多维表格
  * [创建多维表格同时添加数据表](./composite_api/base/create_app_and_tables.py)
* 电子表格
  * [复制粘贴某个范围的单元格数据](./composite_api/sheets/copy_and_paste_by_range.py)
  * [下载指定范围单元格的所有素材列表](./composite_api/sheets/download_media_by_range.py)


## Quick-Start
目前提供以下场景的运行示例：
* [机器人自动拉群报警](./quick_start/robot) ([开发教程](https://open.feishu.cn/document/home/message-development-tutorial/introduction))
  

## License
MIT

## 加入讨论群
[_单击_](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=575k28fa-2c12-400a-80c0-2d8924e00d38)加入讨论群
import json
import uuid

import requests

from pylychee.apps.feishu import AccessToken

# todo testcases
# todo 帮助文档

class Messages:
    """ 消息管理 """

    def send(self, text, receive_ids=[], ):
        """ 发送消息。文档地址:https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
            @参数:receive_id:            消息接收者的ID
            @参数:text:                  发送内容
        """
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
        headers = AccessToken.tenant_headers()
        content = {'text': text}
        for user_id in receive_ids:
            payload = json.dumps({
                "receive_id": user_id,
                "msg_type": "text",
                "content": json.dumps(content),
                "uuid": uuid.uuid4().hex,
            })
            response = requests.post(url, headers=headers, data=payload, timeout=15)
            if response.status_code != 200:
                raise Exception(f'{response.text}')

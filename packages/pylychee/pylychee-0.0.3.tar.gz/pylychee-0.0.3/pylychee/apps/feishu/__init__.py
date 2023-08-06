import os

import requests
import yaml


class AccessToken:
    """ 访问凭证 """

    @classmethod
    def tenant_access_token(cls):
        """ 自建应用获取 tenant_access_token """
        if not hasattr(cls, '_tenant_access_token'):
            settings = os.environ.get("PYLYCHEE_SETTINGS")
            config = yaml.load(open(settings).read(), Loader=yaml.CLoader)
            payload = {
                "app_id": config['feishu']['app_id'],
                "app_secret": config['feishu']['app_secret'],
            }
            r = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', payload)
            cls._tenant_access_token = r.json()['tenant_access_token']

        return cls._tenant_access_token

    @classmethod
    def tenant_headers(cls):
        """ 应用的身份请求头 """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {cls.tenant_access_token()}'
        }
        return headers

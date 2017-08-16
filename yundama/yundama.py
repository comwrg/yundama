# coding=utf-8
"""
@author: comwrg
@license: MIT
@time : 2017/08/15 18:23
@desc : yundama api
        HOME URL: http://www.yundama.com/
        Reference: https://github.com/ResolveWang/weibospider/blob/master/utils/code_verification.py.
"""

import requests
import time

class Yundama:
    _API_URL = 'http://api.yundama.com/api.php'

    def __init__(self, user, pwd, app_id='3510', app_key='7281f8452aa559cdad6673684aa8f575'):
        """

        :type app_id: str
        :type app_key: str
        """
        self._user = user
        self._pwd = pwd
        self._app_id = app_id
        self._app_key = app_key

        # To check account whether correct
        self.balance()

    def upload(self, img, code_type, timeout=1000):
        """Upload image and server will return an id for the image.

        :param code_type: URL: http://www.yundama.com/price.html
        :type code_type: int
        :type timeout: int
        :type img: bytes
        :return: return an id for the image
        :rtype: int
        """
        r = requests.post(
                url=self._API_URL,
                data={
                    'method'  : 'upload',
                    'username': self._user,
                    'password': self._pwd,
                    'appid'   : self._app_id,
                    'appkey'  : self._app_key,
                    'codetype': str(code_type),
                    'timeout' : str(timeout),
                },
                files={
                    'file': img,
                },
        )
        # {"ret":0,"cid":1492625614,"text":""}
        return r.json()['cid']

    def result(self, cid):
        """Get image identify result.

        :param cid: an id for the image
        :return: image identify result
        :rtype: str
        """
        r = requests.post(
                url=self._API_URL,
                data={
                    'method'  : 'result',
                    'username': self._user,
                    'password': self._pwd,
                    'appid'   : self._app_id,
                    'appkey'  : self._app_key,
                    'cid'     : str(cid),
                },
        )
        # {"ret":0,"cid":1492625614,"text":"BKQY"}
        return r.json()['text']

    def result_loop(self, cid):
        """Keep the loop until server returns image identify result."""
        while True:
            r = self.result(cid)
            if r: return r
            time.sleep(1)

    def balance(self):
        """Get account balance.

        :return: If success return balance, else throws exception.
        """
        r = requests.post(
                url=self._API_URL,
                data={
                    'method'  : 'balance',
                    'username': self._user,
                    'password': self._pwd,
                    'appid'   : self._app_id,
                    'appkey'  : self._app_key,
                },
        )
        j = r.json()
        if j['ret'] == 0:
            return j['balance']
        else:
            raise Exception('ACCOUNT INCORRECT')

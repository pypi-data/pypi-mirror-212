import random
import os
import sys
import time
import requests


class ChatGLMClient:
    name = 'default'

    config = {}

    def __init__(self, params: dict = {}) -> None:
        super().__init__()
        self.config = params

    def send_request(self, url: str, data):
        """
        send request
        :param url:
        :param data:
        :return:
        """
        try:
            headers = {
                "Content-Type": "application/json;charset=UTF-8"
            }
            response = requests.post(url, headers=headers, json=data)
            response.encoding = 'utf-8'
            # print(response.status_code)
            return response.json()

        except Exception as e:
            print(e)
            return False

    def chat(self, data: dict):
        """
        进行 chat 调用
        :param data:
        :return:
        """
        data.setdefault("max_length", 40960)
        prompt_length = len(data.get('prompt', ''))
        start_time = time.time()
        result = self.send_request(url=self.config['api_host'], data=data)
        response_length = len(result.get('response', ''))
        work_time = time.time() - start_time
        info = {
            'prompt_length': prompt_length,
            'response_length': response_length,
            'work_time': work_time,
            'response': result.get('response'),
        }

        return result, info

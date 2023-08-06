import time
import unittest
import inspect
from chatglmclient.tests.test_base import BasicsTestCase
from chatglmclient.chatglm_client import ChatGLMClient


class IOTestCase(BasicsTestCase):

    def test_time_ms(self):
        # url = "http://192.168.1.233:5000"

        client = ChatGLMClient(params={'api_host': "http://192.168.1.233:5000"})

        prompts = [
            {
                "prompt": "一只狗有几条腿",
                "history": []
            },
            {
                "prompt": "一只鸡有几条腿",
                "history": []
            },
            {
                "prompt": "一只螃蟹有几条腿",
                "history": []
            },
        ]

        for prompt in prompts:
            result, info = client.chat(prompt)
            print(
                result,
                info,
                info['response']
            )

        self.assertTrue(True, 'test_time_ms')


if __name__ == '__main__':
    unittest.main()

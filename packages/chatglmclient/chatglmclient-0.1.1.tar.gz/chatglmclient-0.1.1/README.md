# chatglmclient

ChatGLM Client，对 api 访问进行封装，方便调用

### 构建

在项目文件夹中运行以下命令

```shell
python setup.py sdist bdist_wheel
```

### 上传：

```shell
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
或
python -m twine upload dist/*
```

按照提示，输入pypi的用户名、密码，就可以成功了。若中途提示有些库没有安装，则使用pip安装一下，需要用到twine库。

### 使用

#### 安装或更新

pip3 install chatglmclient
pip3 install --upgrade chatglmclient

#### 代码使用

```python
from chatglmclient.chatglm_client import ChatGLMClient

client = ChatGLMClient(params={'api_host': "http://192.168.1.111:5000"})

prompt = {
    "prompt": "一只狗有几条腿",
    "history": []
}
result, info = client.chat(prompt)
print(
    result,
    info,
)

```
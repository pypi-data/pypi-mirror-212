# pwproxy

<hr>

> 基于playwright实现mitmproxy的核心功能:请求拦截,响应篡改<br>

优点

1. 基于playwright，直接调用本地浏览器，不用以设置代理的方式启动浏览器, mitmproxy必须以冷启动设置代理的方法启动本地浏览器才能实现拦截
2. 不需要考虑安全证书的问题

# 安装

`pip install pwproxy`

# 使用

<hr>
目录结构:<br>

```python
├─run.py
├─demo.py
```

```python
# run.py
from pwproxy.run import Run

Run.run("demo.py", url="http://example.com/")
```

```python
# demo.py
from playwright.sync_api import Route


def replace_resp(route: Route):
    if "http://example.com/" in route.request.url:
        response = route.fetch()
        body = response.text()
        body = body.replace("Example Domain", "Goodo")
        route.fulfill(
            body=body
        )

addons = [
    replace_resp
]
```



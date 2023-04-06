# Pandora

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/pengzhile/pandora)](https://github.com/pengzhile/pandora/issues)
[![Commits](https://img.shields.io/github/last-commit/pengzhile/pandora/master)](https://github.com/pengzhile/pandora/commits/master)
[![PyPi](https://img.shields.io/pypi/v/pandora-chatgpt.svg)](https://pypi.python.org/pypi/pandora-chatgpt)
[![Downloads](https://static.pepy.tech/badge/pandora-chatgpt)](https://pypi.python.org/pypi/pandora-chatgpt)

[![PyPi workflow](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml)
[![Docker workflow](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml)

### `潘多拉`，一个不只是命令行的`ChatGPT`。

### 实现了网页版`ChatGPT`的主要操作。能过`Cloudflare`，理论上速度还可以。

## 为什么要用

1. 高峰期能绕过官方限制，继续使用。
2. 应答速度直逼`PLUS`，白嫖用户的福音。
3. 官方故障的时候，它可能还是能跑。
4. 多模式：网页/命令行/API，私有化部署。
5. 不会像官方那样无故断线、报错。

## 界面截图

  <details>

  <summary>

  ![alt Screenshot5](https://github.com/pengzhile/pandora/raw/master/doc/images/s05.png)
  ![alt Screenshot10](https://github.com/pengzhile/pandora/raw/master/doc/images/s10.jpeg)

  </summary>

  ![alt Screenshot1](https://github.com/pengzhile/pandora/raw/master/doc/images/s01.png)
  ![alt Screenshot2](https://github.com/pengzhile/pandora/raw/master/doc/images/s02.png)
  ![alt Screenshot3](https://github.com/pengzhile/pandora/raw/master/doc/images/s03.png)
  ![alt Screenshot4](https://github.com/pengzhile/pandora/raw/master/doc/images/s04.png)
  ![alt Screenshot6](https://github.com/pengzhile/pandora/raw/master/doc/images/s06.png)
  ![alt Screenshot11](https://github.com/pengzhile/pandora/raw/master/doc/images/s11.jpeg)

  </details>

## 如何运行

* Python版本目测起码要`3.7`

* pip安装运行

  ```shell
  pip install pandora-chatgpt
  pandora
  ```
  * 如果你想支持`gpt-3.5-turbo`模式：

    ```shell
    pip install 'pandora-chatgpt[api]'
    pandora
    ```
  * 如果你想启用`cloud`模式：

    ```shell
    pip install 'pandora-chatgpt[cloud]'
    pandora-cloud
    ```

* 编译运行

  ```shell
  pip install .
  pandora
  ```
  
  * 如果你想支持`gpt-3.5-turbo`模式：

    ```shell
    pip install '.[api]'
    pandora
    ```
  
  * 如果你想启用`cloud`模式：

    ```shell
    pip install '.[cloud]'
    pandora-cloud
    ```

* Docker Hub运行

  ```shell
  docker pull pengzhile/pandora
  docker run -it --rm pengzhile/pandora
  ```

* Docker编译运行

  ```shell
  docker build -t pandora .
  docker run -it --rm pandora
  ```

* 输入用户名密码登录即可，登录密码理论上不显示出来，莫慌。
* 简单而粗暴，不失优雅。

## 程序参数

* 可通过 `pandora --help` 查看。
* `-p` 或 `--proxy` 指定代理，格式：`protocol://user:pass@ip:port`。
* `-t` 或 `--token_file` 指定一个存放`Access Token`的文件，使用`Access Token`登录。
* `-s` 或 `--server` 以`http`服务方式启动，格式：`ip:port`。
* `-a` 或 `--api` 使用`gpt-3.5-turbo`API请求，**你可能需要向`OpenAI`支付费用**。
* `-l` 或 `--local` 使用本地环境登录，**你可能需要一个合适的代理IP以避免账号被风控！**
* `--sentry` 启用`sentry`框架来发送错误报告供作者查错，敏感信息**不会被发送**。
* `-v` 或 `--verbose` 显示调试信息，且出错时打印异常堆栈信息，供查错使用。

## Docker环境变量

* `PANDORA_ACCESS_TOKEN` 指定`Access Token`字符串。
* `PANDORA_PROXY` 指定代理，格式：`protocol://user:pass@ip:port`。
* `PANDORA_SERVER` 以`http`服务方式启动，格式：`ip:port`。
* `PANDORA_API` 使用`gpt-3.5-turbo`API请求，**你可能需要向`OpenAI`支付费用**。
* `PANDORA_LOGIN_LOCAL` 使用本地环境登录，**你可能需要一个合适的代理IP以避免账号被风控！**
* `PANDORA_SENTRY` 启用`sentry`框架来发送错误报告供作者查错，敏感信息**不会被发送**。
* `PANDORA_VERBOSE` 显示调试信息，且出错时打印异常堆栈信息，供查错使用。
* 使用Docker方式，设置环境变量即可，无视上述`程序参数`。

## 关于 Access Token

* 使用`Access Token`方式登录，可以无代理直连。
* [这个服务](https://chat.gateway.do/auth) 可以帮你安全有效拿到`Access Token`，无论是否第三方登录。
* 其中`accessToken`字段的那一长串内容即是`Access Token`。
* `Access Token`可以复制保存，其有效期目前为`1个月`。
* 不要泄露你的`Access Token`，使用它可以操纵你的账号。

## HTTP服务文档

* 如果你以`http`服务方式启动，现在你可以打开一个极简版的`ChatGPT`了。通过你指定的`http://ip:port`来访问。
* API文档见：[doc/HTTP-API.md](https://github.com/pengzhile/pandora/blob/master/doc/HTTP-API.md)

## 操作命令

* 对话界面**连敲两次**`Enter`发送你的输入给`ChatGPT`。
* 对话界面使用`/?`可以打印支持的操作命令。
* `/title` 重新设置当前对话的标题。
* `/select` 回到选择会话界面。
* `/reload` 重新加载当前会话所有内容，`F5`你能懂吧。
* `/regen` 如果对`ChatGPT`当前回答不满意，可以让它重新回答。
* `/continue` 让`ChatGPT`继续输出回复的剩余部分。
* `/edit` 编辑你之前的一个提问。
* `/new` 直接开启一个新会话。
* `/del` 删除当前会话，回到会话选择界面。
* `/token` 打印当前的`Access Token`，也许你用得上，但不要泄露。
* `/clear` 清屏，应该不用解释。
* `/version` 打印`Pandora`的版本信息。
* `/exit` 退出`潘多拉`。

## 高阶设置

* 本部分内容不理解的朋友，**请勿擅动！**
* 环境变量 `OPENAI_API_PREFIX` 可以替换OpenAI Api的前缀`https://api.openai.com`。
* 环境变量 `CHATGPT_API_PREFIX` 可以替换ChatGPT Api的前缀`https://chat.gateway.do`。
* 如果你想持久存储`Docker`中`Pandora`产生的数据，你可以挂载宿主机目录至`/data`。
* 如果你在国内使用`pip`安装缓慢，可以考虑切换至腾讯的源：```pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple```
* 镜像同步版本可能不及时，如果出现这种情况建议切换至官方源：```pip config set global.index-url https://pypi.org/simple```
* 默认使用`sqlite3`存储会话数据，如果你希望更换至`mysql`，可以这么做：
  * 执行```pip install PyMySQL```安装驱动。
  * 设置环境变量：`DATABASE_URI`为类似`mysql+pymysql://user:pass@localhost/dbname`的连接字符串。
* 环境变量指定`OPENAI_EMAIL`可以替代登录输入用户名，`OPENAI_PASSWORD`则可以替代输入密码。

## Cloud模式

* 搭建一个跟官方很像的`ChatGPT`服务，不能说很像，只能说一样。
* 该模式使用`pandora-cloud`启动，前提是你如前面所说安装好了。
* Docker环境变量：`PANDORA_CLOUD` 启动`cloud`模式。
* 该模式参数含义与普通模式相同，可`--help`查看。

## 使用Cloudflare Workers代理

* 如果你感觉默认的`https://chat.gateway.do`在你那里可能被墙了，可以使用如下方法自行代理。
* 你需要一个`Cloudflare`账号，如果没有，可以[注册](https://dash.cloudflare.com/sign-up)一个。
* 登录后，点击`Workers`，然后点击`Create a Worker`，填入服务名称后点击`创建服务`。
* 点开你刚才创建的服务，点击`快速编辑`按钮，贴入下面的代码，然后点击`保存并部署`。
  ```javascript
  export default {
    async fetch(request, env) {
      const url = new URL(request.url);
      url.host = 'chat.gateway.do';
      return fetch(new Request(url, request))
    }
  }
  ```
* 点击`触发器`选项卡，可以添加自定义访问域名。
* 参考`高阶设置`中的环境变量使用你的服务地址进行替换。
* 这里有一个示例代理地址：`https://chat1.gateway.do`。

## 其他说明

* 项目是站在其他巨人的肩膀上，感谢！
* 报错、BUG之类的提出`Issue`，我会修复。
* 因为之后`ChatGPT`的API变动，我可能不会跟进修复。
* 喜欢的可以给颗星，都是老朋友了。
* 不影响`PHP是世界上最好的编程语言！`
 
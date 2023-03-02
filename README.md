# Pandora

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/pengzhile/pandora)](https://github.com/pengzhile/pandora/issues)
[![Commits](https://img.shields.io/github/last-commit/pengzhile/pandora/master)](https://github.com/pengzhile/pandora/commits/master)
[![PyPi](https://img.shields.io/pypi/v/pandora-chatgpt.svg)](https://pypi.python.org/pypi/pandora-chatgpt)
[![Downloads](https://static.pepy.tech/badge/pandora-chatgpt)](https://pypi.python.org/pypi/pandora-chatgpt)

[![PyPi workflow](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml)
[![Docker workflow](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml)

[English](https://github.com/pengzhile/pandora/blob/master/doc/README.en.md)

### `潘多拉`，一个命令行的`ChatGPT`。

### 实现了网页版`ChatGPT`的主要操作。能过`Cloudflare`，理论上速度还可以。

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
  pip install Pandora-ChatGPT
  pandora
  ```

* 编译运行

  ```shell
  pip install .
  pandora
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
* `-v` 或 `--verbose` 显示调试信息，且出错时打印异常堆栈信息，供查错使用。

## Docker环境变量

* `PANDORA_ACCESS_TOKEN` 指定`Access Token`字符串。
* `PANDORA_PROXY` 指定代理，格式：`protocol://user:pass@ip:port`。
* `PANDORA_SERVER` 以`http`服务方式启动，格式：`ip:port`。
* `PANDORA_VERBOSE` 显示调试信息，且出错时打印异常堆栈信息，供查错使用。
* 使用Docker方式，设置环境变量即可，无视上述`程序参数`。

## 关于 Access Token

* 使用`Access Token`方式登录，可以无代理直连。
* 通常使用`Google`或`Microsoft`账号登录`ChatGPT`的人会用到
* 首先正常登录`ChatGPT`，不管是账号密码，还是`Google`或是`Microsoft`。
* 登录成功到聊天页面后打开：`https://chat.openai.com/api/auth/session`。
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
* `/edit` 编辑你之前的一个提问。
* `/new` 直接开启一个新会话。
* `/del` 删除当前会话，回到会话选择界面。
* `/token` 打印当前的`Access Token`，也许你用得上，但不要泄露。
* `/clear` 清屏，应该不用解释。
* `/version` 打印`Pandora`的版本信息。
* `/exit` 退出`潘多拉`。

## 其他说明

* 项目是站在其他巨人的肩膀上，感谢！
* 报错、BUG之类的提出`Issue`，我会修复。
* 因为之后`ChatGPT`的API变动，我可能不会跟进修复。
* 喜欢的可以给颗星，都是老朋友了。
* 不影响`PHP是世界上最好的编程语言！`
 
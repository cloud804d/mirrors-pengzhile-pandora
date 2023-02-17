# Pandora

### `潘多拉`，一个命令行的`ChatGPT`。
### 实现了网页版`ChatGPT`的主要操作。能过`Cloudflare`，理论上速度还可以。

## 如何运行：

* `Python`版本目测起码要`3.7`

* `pip`安装运行

	```shell
	pip install Pandora-ChatGPT
	pandora
	```
  
* 编译运行
 
    ```shell
    python setup.py install
    pandora
    ```

* `Docker`运行：

    ```shell
    docker build -t pandora .
    docker run -it --rm pandora
    ```

* 输入用户名密码登录即可，登录密码理论上不显示出来，莫慌。
* 简单而粗暴，不失优雅。

## 程序参数

* 可通过 `pandora --help` 查看。
* `-p` 或 `--proxy` 指定代理，格式：`http://user:pass@ip:port`。
* `-t` 或 `--access_token` 使用`Access Token`登录，提示输入`Access Token`。

## 操作命令

* 对话界面**连敲两次**`Enter`发送你的输入给`ChatGPT`。
* 对话界面使用`/?`可以打印支持的操作命令。
* `/title` 重新设置当前对话的标题。
* `/select` 回到选择会话界面。
* `/reload` 重新加载当前会话所有内容，`F5`你能懂吧。
* `/regen` 如果对`ChatGPT`当前回答不满意，可以让它重新回答。
* `/new` 直接开启一个新会话。
* `/del` 删除当前会话，回到会话选择界面。
* `/token` 打印当前的`Access Token`，也许你用得上，但不要泄露。
* `/clear` 清屏，应该不用解释。
* `/exit` 退出`潘多拉`。

## 其他说明
* 项目是站在其他巨人的肩膀上，感谢！
* 报错、BUG之类的提出`Issue`，我会修复。
* 因为之后`ChatGPT`的API变动，我可能不会跟进修复。
* 喜欢的可以给颗星，都是老朋友了。
* 没有英文的`README`，能力有限，抱歉！
* 不影响`PHP是世界上最好的编程语言！`
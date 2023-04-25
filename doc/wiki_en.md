<br />

<p align="center">
  <h3 align="center">Pandora</h3>
  <p align="center">
Pandora, talking with ChatGPT in command lines, and with more surprises.
    <br />
    <a href="https://github.com/pengzhile/pandora/blob/master/doc/wiki.md"><strong>Wiki in 中文 »</strong></a>
    <br />
    <br />
    <a href="https://chat.zhile.io">Demo View</a>
    ·
    <a href="https://github.com/pengzhile/pandora/issues">Bug Report</a>
    ·
    <a href="https://github.com/pengzhile/pandora/issues">Feature Request</a>
  </p>
</p>

## Table of Contents

- [Make it run](#make-it-run)
- [Start parameters](#start-parameters)
- [Docker](#docker)
- [Access Token things](#access-token-things)
- [HTTP RESTful API](#http-restful-api)
- [Commands](#commands)
- [Cloud mode](#cloud-mode)

## Make it run

* Python version no less than `3.7`

* install from `pip`

  ```shell
  pip install pandora-chatgpt
  pandora
  ```
  * `gpt-3.5-turbo` mode:

    ```shell
    pip install 'pandora-chatgpt[api]'
    pandora
    ```
  * `cloud` mode:

    ```shell
    pip install 'pandora-chatgpt[cloud]'
    pandora-cloud
    ```

* install from source

  ```shell
  pip install .
  pandora
  ```
  
  * `gpt-3.5-turbo` mode:

    ```shell
    pip install '.[api]'
    pandora
    ```
  
  * `cloud` mode:

    ```shell
    pip install '.[cloud]'
    pandora-cloud
    ```

* Docker Hub

  ```shell
  docker pull pengzhile/pandora
  docker run -it --rm pengzhile/pandora
  ```

* Docker build

  ```shell
  docker build -t pandora .
  docker run -it --rm pandora
  ```

* login with your credentials

* stay simple, stay naive, stay elegant

## Start parameters

*  `pandora --help` for help text.
* `-p` or `--proxy` for setting the proxy. the value should be`protocol://user:pass@ip:port`.
* `-t` or `--token_file` for indicating the file that stores `Access Token`. You will login with access token if this option is in use.
* `-s` or `--server` starts the HTTP server, by which you could open a web page and interact with it in a fancy UI. the value should be`ip:port`.
* `-a` or `--api` use `gpt-3.5-turbo` API in backend. **NOTICE: you will be charged if this option is in use.** 
* `--tokens_file` indicating a file storing multiple `Access Token`s. The file content should be like`{"key": "token"}`.
* `--threads` specify the number of server workers, default is `8`, and for cloud mode, it is `4`.
* `--sentry` sending error messages to author for improving Pandora. **Sensitive information won't be leaked.**
* `-v` or `--verbose` for verbose debugging messages.

## Docker

These docker environment variables will override start parameters.

* `PANDORA_ACCESS_TOKEN` =`Access Token` string.
* `PANDORA_TOKENS_FILE` = the path of file which keeps `Access Token`s.
* `PANDORA_PROXY` =`protocol://user:pass@ip:port`.
* `PANDORA_SERVER` =`ip:port`.
* `PANDORA_API`  for using `gpt-3.5-turbo` API. **NOTICE: you will be charged if this option is in use.** 
* `PANDORA_SENTRY` for sending error messages to author to improve Pandora. **Sensitive information won't be leaked.**
* `PANDORA_VERBOSE` for verbose debugging messages.

## Access Token things

* no need for proxy if login with `Access Token`.
* you could obtain your access token safely with [this service](https://ai.fakeopen.com/auth).
* `Access Token` has a expiration time as `1 month`, you could save it and keep using within this period.
* leaking your `Access Token` will lead to loss of your account.

## HTTP RESTful API

* if you start Pandora with `-s`/`--server`/`PANDORA_SERVER`, you could access a web UI with `http://ip:port`.
* you could switch access token by passing a different one with `http://ip:port/?token=xxx`.
* API documents: [doc/HTTP-API.md](https://github.com/pengzhile/pandora/blob/master/doc/HTTP-API.md)

## Commands 

* **double** `Enter` to send prompt to `ChatGPT`.
* `/?` for help text.
* `/title` for setting the title of current conversation.
* `/select` back to conversation choosing page.
* `/reload` for refreshing.
* `/regen` for regenerating answers if you are not satisfied with the last one.
* `/continue` make `ChatGPT` to append responses.
* `/edit` for editing your previous prompt.
* `/new` to start a new conversation.
* `/del` to delete current conversation and back to conversation choosing page.
* `/token` for printing current access token.
* `/copy` for copying the last response of  `ChatGPT` to pasteboard.
* `/copy_code`  for copying the code in the last response of  `ChatGPT` to pasteboard.
* `/clear` for cleaning the screen.
* `/version` for printing the version of Pandora.
* `/exit` to exit Pandora.

## Cloud mode

- setting up a service just like official `ChatGPT` website. it's so same as only jesus could tell it apart.

* you need to use `pandora-cloud` instead of `pandora` to start Pandora.
* enabling `PANDORA_CLOUD`  if you are using Docker to start Pandora.
* Other parameters are same as these guys in normal mode.

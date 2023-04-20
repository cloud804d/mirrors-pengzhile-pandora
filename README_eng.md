

# Pandora

Pandora, talking with ChatGPT in command lines, and with more surprises.

It implements almost everything as ChatGPT official website. Besides, it's unimaginably fast because of mysterious optimizations.

<!-- PROJECT SHIELDS -->

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/pengzhile/pandora)](https://github.com/pengzhile/pandora/issues)
[![Commits](https://img.shields.io/github/last-commit/pengzhile/pandora/master)](https://github.com/pengzhile/pandora/commits/master)
[![PyPi](https://img.shields.io/pypi/v/pandora-chatgpt.svg)](https://pypi.python.org/pypi/pandora-chatgpt)
[![Downloads](https://static.pepy.tech/badge/pandora-chatgpt)](https://pypi.python.org/pypi/pandora-chatgpt)
[![PyPi workflow](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml)
[![Docker workflow](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml)

<!-- PROJECT LOGO -->
<br />

<p align="center">

  <h3 align="center">Pandora</h3>
  <p align="center">
Pandora, talking with ChatGPT in command lines, and with more surprises.
    <br />
    <a href="https://github.com/pengzhile/pandora/README.md"><strong>README in 中文 »</strong></a>
    <br />
    <br />
    <a href="https://chat.zhile.io/login">Demo View</a>
    ·
    <a href="https://github.com/pengzhile/pandora/issues">Bug Report</a>
    ·
    <a href="https://github.com/pengzhile/pandora/issues">Feature Request</a>
  </p>

</p>

## Table of Contents

- [Why using Pandora](#why-using-pandora)
- [Screenshots](#screenshots)
- [Make it run](#make-it-run)
- [Start parameters](#start-parameters)
- [Docker](#docker)
- [Access Token things](#access-token-things)
- [HTTP RESTful API](#http-restful-api)
- [Commands](#commands)
- [Cloud mode](#cloud-mode)
- [Misc](#misc)

## Why using Pandora

1. bypassing some official rate limits during peak hours.
2. responsing as fast as PLUS, but it's free.
3. surviving in sometime while the official site is down.
4. running in web, command line or RESTful API mode, as you wish.
5. avoiding disconnecting or error messages while the official site suffers.

## Screenshots

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

## Misc

* The Pandora, it is by standing upon the shoulders of giants.
* If you submit an issue regarding errors or bugs, I will fix them.
* **Star**, pls, Dad.
* PHP is the best programming language in the world.

## Contributors

> Thx for these adorable people.

[![Star History Chart](https://contrib.rocks/image?repo=pengzhile/pandora)](https://github.com/pengzhile/pandora/graphs/contributors)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=pengzhile/pandora&type=Date)

# Pandora

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/pengzhile/pandora)](https://github.com/pengzhile/pandora/issues)
[![Commits](https://img.shields.io/github/last-commit/pengzhile/pandora/master)](https://github.com/pengzhile/pandora/commits/master)
[![PyPi](https://img.shields.io/pypi/v/pandora-chatgpt.svg)](https://pypi.python.org/pypi/pandora-chatgpt)
[![Downloads](https://static.pepy.tech/badge/pandora-chatgpt)](https://pypi.python.org/pypi/pandora-chatgpt)

[![PyPi workflow](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/python-publish.yml)
[![Docker workflow](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/pengzhile/pandora/actions/workflows/docker-publish.yml)

[中文版本](https://github.com/pengzhile/pandora/blob/master/README.md)

### `Pandora`, a command-line `ChatGPT`.

### Implements main operations of web version `ChatGPT`. Passes through `Cloudflare`, theoretically, it works fast.

## Screenshots

  <details>

  <summary>

  ![alt Screenshot5](https://github.com/pengzhile/pandora/raw/master/doc/images/s05.png)

  </summary>

  ![alt Screenshot1](https://github.com/pengzhile/pandora/raw/master/doc/images/s01.png)
  ![alt Screenshot2](https://github.com/pengzhile/pandora/raw/master/doc/images/s02.png)
  ![alt Screenshot3](https://github.com/pengzhile/pandora/raw/master/doc/images/s03.png)
  ![alt Screenshot4](https://github.com/pengzhile/pandora/raw/master/doc/images/s04.png)
  ![alt Screenshot6](https://github.com/pengzhile/pandora/raw/master/doc/images/s06.png)

  </details>

## How to Run:

* Python version must be at least `3.7`.

* Run with pip

  ```shell
  pip install Pandora-ChatGPT
  pandora
  ```

* Run with compilation

  ```shell
  pip install .
  pandora
  ```

* Run with Docker Hub

  ```shell
  docker pull pengzhile/pandora
  docker run -it --rm pengzhile/pandora
  ```

* Run with Docker compilation

  ```shell
  docker build -t pandora .
  docker run -it --rm pandora
  ```

* Simple, straightforward, and elegant.

## Program Arguments

* Use `pandora --help` to view the list of program arguments.
* `-p` or `--proxy` specify a proxy, in the format of `protocol://user:pass@ip:port`.
* `-t` or `--token_file` specify a file that stores the `Access Token`, and log in using the `Access Token`.
* `-s` or `--server` start as a `http` server, in the format of `ip:port`.
* `-v` or `--verbose` displays debugging information, and prints the exception stack trace when an error occurs, for debugging purposes.

## Docker Environment Variables

* `PANDORA_ACCESS_TOKEN` Specifies the `Access Token` string for.
* `PANDORA_PROXY` Specifies a proxy, in the format of `protocol://user:pass@ip:port`.
* `PANDORA_SERVER` Start as a `http` server, in the format of `ip:port`.
* `PANDORA_VERBOSE` displays debugging information, and prints the exception stack trace when an error occurs, for debugging purposes.
* When running the `Pandora` using Docker, set the corresponding environment variables, regardless of the `Program Arguments` mentioned above.

## About Access Token

* Log in with the `Access Token` allows you to bypass the proxy.
* It is usually used by those who log in to `ChatGPT` with their `Google` or `Microsoft` accounts.
* Firstly, log in to `ChatGPT` normally, whether it's with a username and password, or with `Google` or `Microsoft`.
* After successfully logging in, go to the chat page and open the URL `https://chat.openai.com/api/auth/session`.
* The long string of characters in the `accessToken` field is your `Access Token`.
* The `Access Token` can be copied and saved, and its validity period is currently `1 month`.
* Do not leak your `Access Token`, as it can manipulate your account.

## HTTP API Doc

* Visit [doc/HTTP-API.md](https://github.com/pengzhile/pandora/blob/master/doc/HTTP-API.md)

## Command Operations

* In the conversation interface, press `Enter` twice to send your input to `ChatGPT`.
* In the conversation interface, use `/?` to print the supported command operations.
* `/title` re-sets the title of the current conversation.
* `/select` returns to the conversation selection interface.
* `/reload` reloads all the contents of the current conversation, like pressing `F5`.
* `/regen` if you are not satisfied with `ChatGPT`'s current response, you can ask it to re-answer.
* `/edit` edit one of your previous prompt.
* `/new` opens a new conversation directly.
* `/del` deletes the current conversation and returns to the conversation selection interface.
* `/token` prints the current `Access Token`, which you may need, but do not leak it.
* `/clear` clears the screen.
* `/version` print the version of `Pandora`.
* `/exit` exits `Pandora`.

## macOS specific issues

* If you get an error: `certificate verify failed: unable to get local issuer certificate`。
* First: Press `Command`+`Space` buttons or open `Spotlight`.
* Second：type `Install Certificates.command` and execute it.
* Problem solved.

## Other Information

* `Pandora` is an open-source project that stands on the shoulders of other giants, thank you!
* Raise an issue for any errors or bugs you encounter, and the developer will fix them as soon as possible.
* The developer may not be able to keep up with the changes in the `ChatGPT` API in the future.
* If you like it, give the project a star, we are all old friends.
* This `README` is translated by `ChatGPT`.

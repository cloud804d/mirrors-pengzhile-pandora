# Pandora HTTP API

### 特殊说明：如果有多个`Access Token`，可以使用`X-Use-Token: token_name` 头指定使用哪个。

### `/api/models`

* **HTTP方法：** `GET`
* **URL参数：** `无`
* **接口描述：** 列出账号可用的模型。

### `/api/conversations`

* **HTTP方法：** `GET`
* **URL参数：**
    * `offset` 数字类型，默认为：`1`。
    * `limit` 数字类型，默认为：`20`。
* **接口描述：** 以分页方式列出会话列表。

### `/api/conversations`

* **HTTP方法：** `DELETE`
* **URL参数：** `无`
* **接口描述：** 删除所有会话。

### `/api/conversation/<conversation_id>`

* **HTTP方法：** `GET`
* **URL参数：** `无`
* **接口描述：** 通过会话ID获取指定会话详情。

### `/api/conversation/<conversation_id>`

* **HTTP方法：** `DELETE`
* **URL参数：** `无`
* **接口描述：** 通过会话ID删除指定会话。

### `/api/conversation/<conversation_id>`

* **HTTP方法：** `PATCH`
* **JSON字段：**
    * `title` 新标题。
* **接口描述：** 通过会话ID设置指定的会话标题。

### `/api/conversation/gen_title/<conversation_id>`

* **HTTP方法：** `POST`
* **JSON字段：**
    * `model` 对话所使用的模型。
    * `message_id` `ChatGPT`回复的那条消息的ID。
* **接口描述：** 自动生成指定新会话的标题，通常首次问答后调用。

### `/api/conversation/talk`

* **HTTP方法：** `POST`
* **JSON字段：**
    * `prompt` 提问的内容。
    * `model` 对话使用的模型，通常整个会话中保持不变。
    * `message_id` 消息ID，首次通常使用`str(uuid.uuid4())`来生成一个。
    * `parent_message_id` 父消息ID，首次同样需要生成。之后获取上一条回复的消息ID即可。
    * `conversation_id` 首次对话可不传。`ChatGPT`回复时可获取。
    * `stream` 是否使用流的方式输出内容，默认为：`True`
* **接口描述：** 向`ChatGPT`提问，等待其回复。

### `/api/conversation/regenerate`

* **HTTP方法：** `POST`
* **JSON字段：**
    * `prompt` 提问的内容。
    * `model` 对话使用的模型，通常整个会话中保持不变。
    * `message_id` 上一条用户发送消息的ID。
    * `parent_message_id` 上一条用户发送消息的父消息ID。
    * `conversation_id` 会话ID，在这个接口不可不传。
    * `stream` 是否使用流的方式输出内容，默认为：`True`
* **接口描述：** 让`ChatGPT`重新生成回复。

### `/api/conversation/goon`

* **HTTP方法：** `POST`
* **JSON字段：**
    * `model` 对话使用的模型，通常整个会话中保持不变。
    * `parent_message_id` 父消息ID，上一次`ChatGPT`应答的消息ID。
    * `conversation_id` 会话ID。
    * `stream` 是否使用流的方式输出内容，默认为：`True`
* **接口描述：** 让`ChatGPT`讲之前的恢复继续下去。
 
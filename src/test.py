import asyncio

from pandora.openai.api import ChatCompletion


# openai.api_key = api_key
#
#
# def main():
#     resp = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Who won the world series in 2020?"},
#             {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#             {"role": "user", "content": "Where was it played?"}
#         ]
#     )
#
#     print(resp)
#
#     print(json.dumps([
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]))


async def main():
    api_key = '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'
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: 2021-09 Current date: 2023-03-02"},
        {"role": "user", "content": "write quick sort use java"},
    ]

    chat = ChatCompletion(api_key, 'socks5://127.0.0.1:7980')
    async for line in chat.request(model, messages, raw=True):
        print(line)


if __name__ == '__main__':
    asyncio.run(main())

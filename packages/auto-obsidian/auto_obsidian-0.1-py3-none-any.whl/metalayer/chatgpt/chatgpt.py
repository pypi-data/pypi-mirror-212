import asyncio
import os
import time
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

from metalayer.chatgpt.logger import log_result, log_result_async

@log_result
def complete(messages, model='gpt-3.5-turbo', **completion_kwargs):
    response = openai.ChatCompletion.create(model=model, messages=messages, **completion_kwargs)
    text = response.choices[0].message.content
    return text.encode("ascii", errors="ignore").decode()

@log_result_async
async def complete_async(messages, model='gpt-3.5-turbo', **completion_kwargs):
    response = await openai.ChatCompletion.acreate(model=model, messages=messages, **completion_kwargs)
    text = response.choices[0].message.content
    return text.encode("ascii", errors="ignore").decode()


def example():
    messages = [
        {'role': 'system', 'content': "You're a chatbot that makes edgy jokes at the request of the user."},
        {'role': 'user', 'content': "Write me a poem by Alex Jones about frogs."},
    ]
    start = time.time()
    turbo_outout = complete(messages, 'gpt-3.5-turbo')
    print(f'GPT-3.5 Turbo completed in {time.time() - start} seconds')
    print(turbo_outout)

    start = time.time()
    gpt4_output = complete(messages, 'gpt-4')
    print(f'GPT-4 completed in {time.time() - start} seconds')
    print(gpt4_output)


def async_example():
    async def _async_example():
        messages = [
            {'role': 'system', 'content': "You're a chatbot that makes edgy jokes at the request of the user."},
            {'role': 'user', 'content': "Write me a poem by Alex Jones about frogs."},
        ]

        start = time.time()
        turbo_outout = complete_async(messages, 'gpt-3.5-turbo')
        gpt4_output = complete_async(messages, 'gpt-4')

        await turbo_outout
        print(f'GPT-3.5 Turbo completed in {time.time() - start} seconds')
        await gpt4_output
        print(f'GPT-4 completed in {time.time() - start} seconds')

    asyncio.run(_async_example())


if __name__ == '__main__':
    # example()
    async_example()


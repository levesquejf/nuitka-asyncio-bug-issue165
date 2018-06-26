import aiohttp
import asyncio
import traceback

from concurrent.futures import CancelledError


async def http_call():
    while True:
        url = 'http://httpbin.org/delay/10'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                pass

        await asyncio.sleep(0)


async def will_fail():
    await asyncio.sleep(5)
    raise Exception('Ok, time to crash!')


def main():
    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(http_call()),
        asyncio.ensure_future(will_fail()),
    ]

    loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

    for task in asyncio.Task.all_tasks():
        if not task.done():
            print(f'Cancelling {task}')
            task.cancel()
        try:
            loop.run_until_complete(task)
        except Exception as e:
            print(f'Exception catched: {e} \n {traceback.format_exc()}')


if __name__ == '__main__':
    main()

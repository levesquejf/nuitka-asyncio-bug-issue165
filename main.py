import aiohttp
import asyncio


async def http_call(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                print(f"Status code is {resp.status}")
        except Exception:
            print("Exception")


async def run():
    await http_call("https://www.google.com")
    await http_call("https://www.google.com")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()

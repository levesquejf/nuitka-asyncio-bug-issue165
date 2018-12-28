import asyncio

from concurrent.futures import CancelledError
from contextlib import asynccontextmanager


@asynccontextmanager
async def async_context():
    ctx = Obj()
    yield ctx


class Obj:
    async def fail_now(self, *args, **kwargs):
        raise RuntimeError('Ok, time to crash!')


class Obj2:
    async def run(self):
        for _ in range(0, 2):
            async with async_context() as ctx:
                reader_task = asyncio.ensure_future(self.reader(ctx))
                writer_task = asyncio.ensure_future(self.writer(ctx))
                done, pending = await asyncio.wait(
                    [reader_task, writer_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()
                    try:
                        await task
                    except CancelledError:
                        print('Cancelled')
                        pass
                for task in done:
                    try:
                        await task
                    except Exception as e:
                        print(f'Exception catched: {e}', flush=True)

    async def reader(self, my_obj):
        await asyncio.sleep(1)
        await my_obj.fail_now(self)

    async def writer(self, my_obj):
        await asyncio.sleep(2)
        await my_obj.fail_now(self)


def main():
    loop = asyncio.get_event_loop()
    my_obj = Obj2()
    loop.run_until_complete(my_obj.run())


if __name__ == '__main__':
    main()

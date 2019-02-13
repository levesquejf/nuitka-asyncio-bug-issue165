import asyncio

from concurrent.futures import CancelledError


class Obj:
    async def fail_now(self, *args, **kwargs):
        raise RuntimeError('Ok, time to crash! - If you see this, the Nuitka issue is not present.')


class Task:
    async def run(self):
        my_obj = Obj()
        reader_task = asyncio.ensure_future(self.reader(my_obj))
        writer_task = asyncio.ensure_future(self.writer(my_obj))
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
    my_task = Task()
    loop.run_until_complete(my_task.run())


if __name__ == '__main__':
    main()

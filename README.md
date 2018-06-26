This repo illustrates a potential bug when using Nuitka with asyncio coroutines.

When a coroutine is cancelled during execution, the Exception should be `CancelledError` (at least it is on native Python 3.6.5). However, when compiled with [Nuitka v0.5.30](http://nuitka.net/), the Exception is `RuntimeError: cannot reuse already awaited coroutine`.

It can be easily reproduced using Docker containers.

### Running with Python 3.6.5

```
# ./run-native.sh
( ... docker building the image ... )

Cancelling <Task pending coro=<http_call() running at main.py:12> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x7f493b125dc8>()]>>
Exception catched:
 Traceback (most recent call last):
  File "main.py", line 38, in main
    loop.run_until_complete(task)
  File "/usr/local/lib/python3.6/asyncio/base_events.py", line 468, in run_until_complete
    return future.result()
concurrent.futures._base.CancelledError

Exception catched: Ok, time to crash!
 Traceback (most recent call last):
  File "main.py", line 38, in main
    loop.run_until_complete(task)
  File "/usr/local/lib/python3.6/asyncio/base_events.py", line 468, in run_until_complete
    return future.result()
  File "main.py", line 20, in will_fail
    raise Exception('Ok, time to crash!')
Exception: Ok, time to crash!
```

### Running on Linux, compiled with Nuitka 0.5.30 on Python 3.6.5

```
# ./run-nuitka.sh
( ... docker building the image ... )

Exception catched: Ok, time to crash!
 Traceback (most recent call last):
  File "/opt/app/main.dist/main.py", line 38, in main
  File "/opt/app/main.dist/asyncio/base_events.py", line 468, in run_until_complete
  File "/opt/app/main.dist/main.py", line 20, in will_fail
Exception: Ok, time to crash!

Cancelling <Task pending coro=<http_call() running at /opt/app/main.dist/main.py:12> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x7ff94d98b858>()]>>
Exception catched: cannot reuse already awaited coroutine
 Traceback (most recent call last):
  File "/opt/app/main.dist/main.py", line 38, in main
  File "/opt/app/main.dist/asyncio/base_events.py", line 468, in run_until_complete
  File "/opt/app/main.dist/main.py", line 12, in http_call
RuntimeError: cannot reuse already awaited coroutine
```

Note that this issue is not only present with `aiohttp` but with other packages and coroutines. This package is only used as an example.

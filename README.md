Issue tracked at [Nuitka/#213](https://github.com/Nuitka/Nuitka/issues/213)

This repo illustrates a potential bug when using Nuitka with asyncio coroutines. In some cases, Exceptions are returned as `RuntimeError: cannot reuse already awaited coroutine` instead of the correct Exception. This is very similar to bug [Issue 404](http://bugs.nuitka.net/issue404) fixed in 0.5.32.

It can be easily reproduced using Docker containers.

This exact reproducer only works on Python 3.7. It works by changing the Dockerfile-nuitka base image to Python 3.6.8.

### Running with Python 3.7.3

```
# ./run-native.sh
( ... docker building the image ... )

Cancelled
Exception catched: Ok, time to crash! - If you see this, the Nuitka issue is not present.
```

### Running on Linux (Docker), compiled with Nuitka 0.6.3.1 on Python 3.7.3

```
# ./run-nuitka.sh
( ... docker building the image ... )

Traceback (most recent call last):
  File "/opt/app/main.dist/main.py", line 50, in <module>
  File "/opt/app/main.dist/main.py", line 46, in main
  File "/opt/app/main.dist/asyncio/base_events.py", line 584, in run_until_complete
  File "/opt/app/main.dist/main.py", line 24, in run
  File "/opt/app/main.dist/main.py", line 39, in writer
RuntimeError: cannot reuse already awaited coroutine
```

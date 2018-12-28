Issue tracked at [Nuitka/#213](https://github.com/Nuitka/Nuitka/issues/213)

This repo illustrates a potential bug when using Nuitka with asyncio coroutines. In some cases, Exceptions are returned as `RuntimeError: cannot reuse already awaited coroutine` instead of the correct Exception. This is very similar to bug [Issue 404](http://bugs.nuitka.net/issue404) fixed in 0.5.32.

It can be easily reproduced using Docker containers.

### Running with Python 3.7.2

```
# ./run-native.sh
( ... docker building the image ... )

Cancelled
Exception catched: Ok, time to crash!
Cancelled
Exception catched: Ok, time to crash!
```

### Running on Linux, compiled with Nuitka 0.6.0.6 on Python 3.7.2

```
# ./run-nuitka.sh
( ... docker building the image ... )

Traceback (most recent call last):
  File "/opt/app/main.dist/main.py", line 73, in <module>
  File "/opt/app/main.dist/main.py", line 58, in main
  File "/opt/app/main.dist/asyncio/base_events.py", line 584, in run_until_complete
  File "/opt/app/main.dist/main.py", line 35, in run
  File "/opt/app/main.dist/main.py", line 50, in writer
RuntimeError: cannot reuse already awaited coroutine
```


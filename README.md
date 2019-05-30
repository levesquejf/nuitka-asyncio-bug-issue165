Issue tracked at [Nuitka/#165](https://github.com/Nuitka/Nuitka/issues/165)

This repo illustrates a potential bug when using Nuitka with asyncio coroutines. In some cases, Exceptions are returned as `RuntimeError: cannot reuse already awaited coroutine` instead of the correct Exception. This is very similar to bug [Issue 404](http://bugs.nuitka.net/issue404) fixed in 0.5.32 and bug [Nuitka/#213](https://github.com/Nuitka/Nuitka/issues/213).

It can be easily reproduced using Docker containers.

This bug is present in Python 3.6.8 and 3.7.3 (both tested with Nuitka 0.6.3.1)

###How to trigger the bug

In this case, we trigger an SSL exception within aiohttp by changing the IP of the domain www.google.com to an IP used by Apple (take a look at the --add-host docker run option in run-\*.sh files). Then, we make a call to https://www.google.com. Since the hostname is not good in the SSL certificate received from the server, an exception is raised by aiohttp and it triggers the bug if the code is compiled with nuitka.

This is not a real use case but it's the only way I found to easily raise the exception with aiohttp and trigger the nuitka bug.

### Running on Linux (Docker) with native Python 3.6.8

```
# ./run-native.sh
( ... docker building the image ... )
( ... ssl.CerticateError that I am not able to catch ... )

Exception
Exception
```

### Running on Linux (Docker), compiled with Nuitka 0.6.3.1 on Python 3.6.8

```
# ./run-nuitka.sh
( ... docker building the image ... )
( ... ssl.CerticateError that I am not able to catch ... )

Traceback (most recent call last):
  File "/opt/app/main.dist/main.py", line 25, in <module>
  File "/opt/app/main.dist/main.py", line 21, in main
  File "/opt/app/main.dist/asyncio/base_events.py", line 484, in run_until_complete
  File "/opt/app/main.dist/main.py", line 15, in run
RuntimeError: cannot reuse already awaited compiled_coroutine
```

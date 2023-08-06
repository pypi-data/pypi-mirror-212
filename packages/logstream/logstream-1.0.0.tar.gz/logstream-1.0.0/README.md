# logstream #

logstream is basically "tail -f" of operating system syslog data.  

## Golang
```bash
go build
./logstream
```

## Python
[![Python Versions](https://img.shields.io/pypi/pyversions/pypistats.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/pypistats/)
[![Package Version](https://img.shields.io/pypi/v/logstream.svg)](https://pypi.python.org/pypi/logstream/)
 
logstream is a command line tool and python generator.  

### Run from source ###

```bash
./python/logstream/logstream.py
```

### Install via pip ###

```bash
pip3 install logstream
```

```text
Usage: logstream

    --help
    --version
    --format [type]

    os darwin:
        [default|compact|json|ndjson|syslog]

    os linux:
        [short|short-full|short-unix|verbose|export]
        [json|json-pretty|json-sse|json-seq]

    os windows:
        TODO

    --tail file
```

---

### logstream python shell ###

```python3
>>> import logstream
```

logstream is a generator
stream is a yeild of each line
```python3
>>> for line in logstream.stream():
...     print(line)
```

tail a file
```python3
>>> logstream.tail('/tmp/file')
<generator object tail at 0x7f806034b2e0>
>>> for line in logstream.tail('/tmp/file'):
...     print(line)
```


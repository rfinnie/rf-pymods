# rf-pymods

This is a collection of small pieces of Python code which are useful in other projects.
While you could technically import this package and use it directly, it's mostly encouraged to take the needed functionality and embed them directly in the needed project

## croniter_hash

An extension to the [croniter](https://pypi.org/project/croniter/) module, primarily adding support for Jenkins-style "H" hashing definitions, as well as "R" random definitions.

```python
epoch = datetime(2020, 1, 1, 0, 0)
hash_id = "hello"

# Hashed daily
croniter_hash("H H * * *", epoch, hash_id=hash_id).get_next(datetime)
"""datetime.datetime(2020, 1, 1, 11, 10)"""

# Each hashed definition is consistent to its specified hash_id
croniter_hash("H H * * *", epoch, hash_id="hello").get_next(datetime)
"""datetime.datetime(2020, 1, 1, 11, 10)"""
croniter_hash("H H * * *", epoch, hash_id="hello").get_next(datetime)
"""datetime.datetime(2020, 1, 1, 11, 10)"""
croniter_hash("H H * * *", epoch, hash_id="bonjour").get_next(datetime)
"""datetime.datetime(2020, 1, 1, 20, 52)"""

# The hash_id can be binary
croniter_hash("H H * * *", epoch, hash_id=b"\x01\x02\x03\x04").get_next(datetime)
"""datetime.datetime(2020, 1, 1, 14, 53)"""

# Epoch output
croniter_hash("H H * * *", epoch, hash_id=hash_id).get_next(float)
"""1577877000.0"""

# 6th-position second formation is supported
croniter_hash("H H * * * H", epoch, hash_id=hash_id).get_next(datetime)
"""datetime.datetime(2020, 1, 1, 11, 10, 32)"""

# Named "@" definitions work too, and assume hashing to the second
croniter_hash("@daily", epoch, hash_id=hash_id).get_next(datetime)
"""datetime.datetime(2020, 1, 1, 11, 10, 32)"""
```

## numfmt

Formats numbers into human-pleasing representation.
Supports string and F-string formatting, binary SI prefixes, and customizable rollover points.

```python
# Basic repr formatting
numfmt(12345)
"""12.35 k"""
numfmt(12345, fmt="{num.real:0.09f} {num.prefix}")
"""12.345000000 k"""

# Positional or named attributes
"{0.real:0.03f} {0.prefix}B".format(numfmt(12345))
"""12.345 kB"""
"{num.real:0.01f} {num.prefix}B/s".format(num=numfmt(12345))
"""12.3 kB/s"""

# F-strings
num = numfmt(12345); f"{num.real:0.04f} {num.prefix}B"
"""12.3450 kB"""

# Named attributes, binary SI prefixes
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(12345, binary=True))
"""12.06 KiB"""

# Rollover before 100% of a normal prefix change
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(897306, rollover=0.9))
"""897.31 kB"""
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(973829, rollover=0.9))
"""0.97 MB"""

# Rollover after 100% of a normal prefix change
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(1032456, rollover=1.1))
"""1032.46 kB"""
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(1122334, rollover=1.1))
"""1.12 MB"""

# Limit number of prefix changes
"{num.real:0.02f} {num.prefix}B".format(num=numfmt(123000000000, limit=2))
"""123000.00 MB"""
```

## readiter

A block-based iterable wrapper around filehandle read(), allowing for an interating loop without needing to check for the filehandle end sentinel.

```python
count = 0
with open("/bin/ls", "rb") as fh:
    for block in readiter(fh):
        count += 1

count
"""139"""

count = 0
with open("/etc/shells", "r") as fh:
    for block in readiter(fh, size=10):
        count += 1

count
"""22"""
```

## safe_write

(Try to) safely write files with minimum collision possibility, by writing to a temporary file and then moving into final place upon filehandle close.
The filehandle object otherwise performs identically to a real `open()` filehandle.

```python
with safe_write("foo") as f:
    print("Current filename open is: {}".format(f.name))
    print("Upon close, {} will be moved to {}".format(f.name, f.original_name))
    f.write("bar")

"""Current filename open is: foo.tmp726c0df7-276e-4d51-b99b-2632855d7bef~"""
"""Upon close, foo.tmp726c0df7-276e-4d51-b99b-2632855d7bef~ will be moved to foo"""
"""3"""

os.stat("foo")
"""os.stat_result(st_mode=33204, st_ino=48500857, st_dev=64768, st_nlink=1,
                  st_uid=1000, st_gid=1000, st_size=3, st_atime=1617931328,
                  st_mtime=1617931328, st_ctime=1617931328)"""
```

## License

Copyright (c) 2020-2021 Ryan Finnie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


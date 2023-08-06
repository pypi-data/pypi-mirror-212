# eTDD

Framework for Test-driven development (TDD) to support to isolate the unit code in C/C++.

# Example 1

You can create the file tdd.py and execute it with the follow code:

```
from etdd import TDD, full_main

tdd = TDD(main=full_main, envpath="envpath.ini")
tdd.download_from_git("https://github.com/neubertm/TDD_framework.git")

test = tdd.test("TDD_framework/TESTs/BitInverter_Tpkg/src/test.cpp", "BitInverter")
test.files = ["TDD_framework/project/BitInverter/BitInverter.*", "TDD_framework/TESTs/BitInverter_Tpkg/src/MemLeakDetection*.h"]
test.compile = ["BitInverter.c"]

tdd.menu()
```

# Windows

Before to execute the test, you need to execute the option "Install CppUTest on ./tmp" in the tdd.menu(). It will download and compile the cpputest code.

You need to install also:
 - cmake
 - cppcheck
 - git
 - mingw-gcc
 - doxygen and dot (optional)


# Linux

You must to install the library libcpputest-dev
```
sudo apt install cmake libcpputest-dev doxygen cppcheck
```
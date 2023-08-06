Opa



Example 1

from etdd import TDD, full_main

tdd = TDD(main=full_main, envpath="envpath.ini")
tdd.download_from_git("https://github.com/neubertm/TDD_framework.git")


test = tdd.test("TDD_framework/TESTs/BitInverter_Tpkg/src/test.cpp", "BitInverter")
test.files = ["TDD_framework/project/BitInverter/BitInverter.*", "TDD_framework/TESTs/BitInverter_Tpkg/src/MemLeakDetection*.h"]
test.compile = ["BitInverter.c"]

tdd.menu()

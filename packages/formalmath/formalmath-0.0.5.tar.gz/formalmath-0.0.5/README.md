# formalmath

A formal mathematics package.

## setmm

A port for [metamath](https://us.metamath.org) and `set.mm`. The language `metamath` is a math proof verifying language. And, `set.mm` is its main database of theorems, based on the classical ZFC axiom system.

`MObject` is the basic class. Any `MObject` have a label. Some of them have short_code or metamath_code. The label system is unique (if you create a new MObject with the same label with existing one, the program will raise ValueError). So does the short_code and metamath_code.

 `Constant` is the class of constants, corresponding to $c statements in metamath.

`Variable` is the class of variables, corresponding to $v statements in metamath.

The port of other concepts in metamath and set.mm is a work in process.

Example code:

```python
from formalmath import setmm
test1 = setmm.MObject("x1")
test2 = setmm.MObject("y1")
# test3 = setmm.MObject("x1")
print(test1) # output: MObject("x1")
test3 = setmm.MObject.find_MObject_by_label("y1")
print(test3) # output: MObject("y1")

lp = setmm.Constant("\\left(")
rp = setmm.Constant("\\right)")
# lp2 = setmm.Constant("\\left(")
print(lp) # output: Constant("\left(")
testConst = setmm.Constant.find_MObject_by_label("\\right)")
print(testConst) # output: Constant("\right)")
```


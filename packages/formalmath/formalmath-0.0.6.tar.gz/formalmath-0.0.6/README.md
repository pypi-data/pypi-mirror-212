# formalmath

A formal mathematics package.

## setmm

A port for [metamath](https://us.metamath.org) and `set.mm`. The language `metamath` is a math proof verifying language. And, `set.mm` is its main database of theorems, based on the classical ZFC axiom system.

`MObject` is the basic class. Any `MObject` have a label. Some of them have short_code or metamath_code. The label system is unique (if you create a new MObject with the same label with existing one, the program will raise ValueError). So does the short_code and metamath_code.

 `Constant` is the class of constants, corresponding to $c statements in metamath.

`Variable` is the class of variables, corresponding to $v statements in metamath.

`Formula` is the base class of formulas, corresponding to wff in metamath and set.mm.

`FormulaVariable` is the class of formula with only one symbol.

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

lp1 = setmm.Constant("\\left(")
rp1 = setmm.Constant("\\right)")
# lp2 = setmm.Constant("\\left(")
print(lp1) # output: Constant("\left(")
testConst = setmm.Constant.find_MObject_by_label("\\right)")
print(testConst) # output: Constant("\right)")

lp = setmm.Constant("(")
rp = setmm.Constant(")")
ra = setmm.Constant("->")
phi = setmm.FormulaVariable("phi")
psi = setmm.FormulaVariable("psi")
chi = setmm.FormulaVariable("chi")
phi_implies_psi = setmm.Formula("phips",list_of_symbols=[lp,phi,ra,psi,rp])
complex_imply = setmm.Formula("ccimply",list_of_symbols=[lp,phi_implies_psi,ra,chi,rp])
print(complex_imply) # Formula("(","(","phi","->","psi",")","->","chi",")")
```


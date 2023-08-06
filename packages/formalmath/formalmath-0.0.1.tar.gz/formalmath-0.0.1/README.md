# formalmath

A formal mathematics package.

## setmm

A port for [metamath](https://us.metamath.org) and set.mm.

Example code:

```python
from formalmath import setmm
lp = setmm.Constant('\\left(','(','(')
rp = setmm.Constant('\\right)',')',')')
ra = setmm.Constant('\\rightarrow','->','->')
phi = setmm.Variable('\\varphi','phi','ph')
psi = setmm.Variable('\\psi','psi','ps')
wph = setmm.Formula("\\varphi", [phi,], metamath_code='wph')
wps = setmm.Formula('\\psi',[psi,],metamath_code='wps')
wi = setmm.Formula("auto",[lp,phi,ra,psi,rp],metamath_code='wi')
print(wi.label) # result is '\\left(\\varphi\\rightarrow\\psi\\right)'
```


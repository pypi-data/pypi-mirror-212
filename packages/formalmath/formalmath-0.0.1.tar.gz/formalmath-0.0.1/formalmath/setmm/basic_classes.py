'''
Python port for a slightly extended version of the formal language metamath (us.metamath.org) and the theorem database set.mm written by metamath. This system includes over 40000 theorems in the classic ZFC axiom system.

The basic classes will be defined in this file. That includes:
1. Constant. That correspond to $c statement in metamath.
2. Variable. That correspond to $v statement in metamath.
3. Formula. That correspond to wff in metamath and set.mm. It is not a part of the basic metamath language. But it is defined in set.mm to denote well formed formula. There is always new ways to form a wff, when a new term is introduced. But all of them correspond to a conbination of old terms.
4. ClassVariable. That correspond to class in metamath and set.mm.
5. SetVariable. That correspond to setvar in metamath and set.mm.
6. Axiom. That correspond to $a statements that are axioms.
7. Definition. That correspond to $a statements that are definitions.

Some basic constants will be defined here too, such as left and right parenthesis, well-formed formula symbol and turnstile.
'''


class Constant:
    '''
    $c statements in metamath.
    '''
    def __init__(self, symbol, short_code=None, metamath_code=None):
        '''
        symbol: a string that represents the constant, such as '\left('
        short_code: a shorter string representing the same constant, such as '('
        metamath_code: the original code in set.mm, such as ')'
        '''
        self.label = symbol
        if short_code:
            self.short_code = short_code
        if metamath_code:
            self.metamath_code = metamath_code
    
class Variable:
    '''
    $v statements in metamath.
    '''
    def __init__(self, symbol, short_code=None, metamath_code=None):
        '''
        symbol: a string that represents the constant, such as '\left('
        short_code: a shorter string representing the same constant, such as '('
        metamath_code: the original code in set.mm, such as ')'
        '''
        self.label = symbol
        if short_code:
            self.short_code = short_code
        if metamath_code:
            self.metamath_code = metamath_code

class Formula:
    '''
    The class of well-formed formulas.
    '''
    def __init__(self, label, template, substitution=None, metamath_code=None):
        '''
        label: a string that represents the formula
        template: a template for Formula
        substitution: substitutions of the template that replaced the wffs, variables... to the right one.
        metamath_code: the original label in set.mm

        example: 
        template: [lp, ph, ra, ps, rp], where lp, ra, rp are constants, ph, ps are wffs.
        substitution: {1: varphi, 3: psi}, where varphi, psi are wffs.
        formula: [lp, varphi, ra, psi, rp] 
        '''

        if metamath_code:
            self.metamath_code = metamath_code
        if isinstance(template, Formula):
            self.formula = template.formula
        else:
            self.formula = template
        if substitution:
            for k in substitution.keys():
                assert not isinstance(substitution[k], Constant)
                assert isinstance(substitution[k], type(self.formula[k])) or isinstance(substitution[k], Variable)
                self.formula[k] = substitution[k]
        if label=='auto':
            self.label = ''.join([c.label for c in self.formula])
        else:
            self.label = label

if __name__=='__main__':
    lp = Constant('\\left(','(','(')
    rp = Constant('\\right)',')',')')
    ra = Constant('\\rightarrow','->','->')
    phi = Variable('\\varphi','phi','ph')
    psi = Variable('\\psi','psi','ps')
    wph = Formula("\\varphi", [phi,], metamath_code='wph')
    wps = Formula('\\psi',[psi,],metamath_code='wps')
    wi = Formula("auto",[lp,phi,ra,psi,rp],metamath_code='wi')
    print(wi.label)

    
    

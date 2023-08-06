'''
Python port for a slightly extended version of the formal language metamath (us.metamath.org) and the theorem database set.mm written by metamath. This system includes over 40000 theorems in the classic ZFC axiom system.

The basic classes will be defined in this file. That includes:
0. MObject. The base class for all classes.
1. Constant. That correspond to $c statement in metamath.
2. Variable. That correspond to $v statement in metamath.
3. FormulaTemplate. That correspond to $a statements starting with wff symbol. Basically, it generates new formula from old. But the template can also have Constant, ClassVariable, SetVariable, etc.
4. Formula. That correspond to wff in metamath and set.mm. It is not a part of the basic metamath language. But it is defined in set.mm to denote well formed formula. There is always new ways to form a wff, when a new term is introduced. But all of them correspond to a conbination of old terms.
5. ClassVariable. That correspond to class in metamath and set.mm.
6. SetVariable. That correspond to setvar in metamath and set.mm.
7. Axiom. That correspond to $a statements that are axioms.
8. Definition. That correspond to $a statements that are definitions.

Some basic constants will be defined here too, such as left and right parenthesis, well-formed formula symbol and turnstile.
'''

class MObject:
    '''
    Base class for all metamath classes.
    Use this to ensure the uniqueness of labels and codes.
    '''

    # global dictionaries that ensures the uniqueness of MObject labels, short_codes and metamath_codes.
    # these dicts can also be used to search MObjects by labels, short_codes and metamath_codes.
    MObject_labels = {}
    MObject_short_codes = {}
    MObject_metamath_codes = {}

    def __init__(self, label, short_code=None, metamath_code=None):
        '''
        construction function of MObject.
        label: label of the MObject. It is unique.
        short_code: a shorter code for the MObject. Also unique.
        metamath_code: the corresponding original code in set.mm.
        '''
        # ensure the uniqueness of label
        self._check_unique_label(label)
        # define the label of an MObject
        self.label = label
        
        if short_code:
            # ensure the uniqueness of short_code
            self._check_unique_short_code(short_code)
            # define the short_code of an MObject
            self.short_code = short_code

        if metamath_code:
            # ensure the uniqueness of metamath_code
            self._check_unique_metamath_code(metamath_code)
            # define the metamath_code of an MObject
            self.metamath_code = metamath_code

        # add the new MObject into dicts
        MObject.MObject_labels[label] = self
        if short_code:
            MObject.MObject_short_codes[short_code] = self
        if metamath_code:
            MObject.MObject_metamath_codes[metamath_code] = self
    
    def _check_unique_label(self, label):
        '''
        ensure label is not seen in MObject_labels
        '''
        # if label is used before, raise ValueError.
        if label in MObject.MObject_labels:
            raise ValueError("Duplicate label: {}".format(label))
        
    def _check_unique_short_code(self, short_code):
        '''
        ensure short_code is not seen in MObject_short_codes
        '''
        # if short_code is used before, raise ValueError.
        if short_code in MObject.MObject_short_codes:
            raise ValueError("Duplicate short_code: {}".format(short_code))

    def _check_unique_metamath_code(self, metamath_code):
        '''
        ensure metamath_code is not seen in MObject_metamath_codes
        '''
        # if metamath_code is used before, raise ValueError.
        if metamath_code in MObject.MObject_metamath_codes:
            raise ValueError("Duplicate metamath_code: {}".format(metamath_code))
    
    def __str__(self):
        '''
        print MObject
        '''
        return f"MObject(\"{self.label}\")"
    
    @classmethod
    def find_MObject_by_label(cls, label):
        '''
        Find MObject by label. Need exact match. 
        '''
        if label in MObject.MObject_labels:
            return MObject.MObject_labels[label]
        else:
            raise ValueError("MObject label not found: {}".format(label))

    @classmethod
    def find_MObject_by_short_code(cls, short_code):
        '''
        Find MObject by short_code. Need exact match. 
        '''
        if short_code in MObject.MObject_short_codes:
            return MObject.MObject_short_codes[short_code]
        else:
            raise ValueError("MObject short_code not found: {}".format(short_code))

    @classmethod
    def find_MObject_by_metamath_code(cls, metamath_code):
        '''
        Find MObject by metamath_code. Need exact match. 
        '''
        if metamath_code in MObject.MObject_metamath_codes:
            return MObject.MObject_metamath_codes[metamath_code]
        else:
            raise ValueError("MObject metamath_code not found: {}".format(metamath_code))

class Constant(MObject):
    '''
    $c statement in metamath, denote constant objects.
    Example: left and right parenthesis, wff symbol
    '''
    def __init__(self, label, short_code=None, metamath_code=None):
        '''
        construction function of Constant.
        just need to inherit from MObject.
        '''
        super().__init__(label, short_code, metamath_code)
    
    def __str__(self):
        '''
        print Constant. will override the __str__ method in MObject.
        '''
        return f"Constant(\"{self.label}\")"

class Variable(MObject):
    '''
    $v statement in metamath, denote variable objects.
    '''
    def __init__(self, label, short_code=None, metamath_code=None):
        '''
        construction function of Variable.
        just need to inherit from MObject.
        '''
        super().__init__(label, short_code, metamath_code)
    
    def __str__(self):
        '''
        print Variable. will override the __str__ method in MObject.
        '''
        return f"Variable(\"{self.label}\")"

class Formula(MObject):
    '''
    base class for well formed formulas.
    '''
    def __init__(self, label, short_code=None, metamath_code=None, list_of_symbols=None):
        '''
        construction function for Formula.
        list_of_symbols: a list of constants and formulas, making the symbols of the new formula 
        '''
        super().__init__(label, short_code, metamath_code)
        if list_of_symbols:
            self._check_symbol_type(list_of_symbols)
            my_list = []
            for symbol in list_of_symbols:
                if isinstance(symbol, Formula):
                    my_list = my_list + symbol.list_of_symbols
                else:
                    my_list.append(symbol)
            self.list_of_symbols = my_list
    
    def _check_symbol_type(self, list_of_symbols):
        '''
        Ensure that all symbols in the list_of_symbols are of type Constant or Formula.
        Otherwise, raise TypeError.
        '''
        for symbol in list_of_symbols:
            if not isinstance(symbol, (Constant, Formula)):
                raise TypeError(f"{symbol}: not in supported type. We support Constant and Formula for symbols in list_of_symbols.")
    
    def __str__(self):
        '''
        print Formula. will override the __str__ method in MObject.
        '''
        labelstr = ','.join([f"\"{s.label}\"" for s in self.list_of_symbols])
        return f"Formula({labelstr})"

class FormulaVariable(Variable, Formula):
    '''
    $f statement of form $f wff varname $. It means that varname represents a well formed formula.
    This class is the special kind of Formula consisting of only one variable.
    '''
    def __init__(self, label, short_code=None, metamath_code=None):
        super().__init__(label, short_code, metamath_code)
        self.list_of_symbols = [self]
    
    def __str__(self):
        return f"Formula(\"{self.label}\")"

class FormulaTemplate(MObject):
    '''
    $a statements that generates new Formula from old by substitution.
    '''


if __name__=='__main__':
    lp = Constant("(")
    rp = Constant(")")
    ra = Constant("->")
    phi = FormulaVariable("phi")
    psi = FormulaVariable("psi")
    chi = FormulaVariable("chi")
    phi_implies_psi = Formula("phips",list_of_symbols=[lp,phi,ra,psi,rp])
    complex_imply = Formula("ccimply",list_of_symbols=[lp,phi_implies_psi,ra,chi,rp])
    print(complex_imply) # Formula("(","(","phi","->","psi",")","->","chi",")")

    
    

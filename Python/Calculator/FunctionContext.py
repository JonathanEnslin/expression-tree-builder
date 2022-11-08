from re import split
from RealValuedExpression import *

class FunctionContext:
    class FunctionContextError(Exception):
        def __init__(self, message) -> None:
            super().__init__(message)

    def __init__(self) -> None:
        self.funcs = {}

    def breakDownIdentifier(self, id: str) -> tuple:
        splitList = split('\(|\)', id)
        print(splitList)
        return splitList[0], split(',|;' ,splitList[1])

    # Example: Client wants to store f(x,y) = x^2+y
    # client passes in identifier = f, vars = ['x', 'y;], expression = x^2+y, expressionTree is the real valued expression built from the passed expression
    def assign(self, identifier: str, vars: list, expression: str, expressionTree: RealValuedExpression) -> None:
        # id, vars = self.breakDownIdentifier(identifier)
        # expressionTree = RealValuedExpressionBuilder().build(expression)
        self.funcs[identifier] = (expression, vars, expressionTree)

    # returns (expression, vars, expressionTree)
    def lookup(self, identifier) -> tuple:
        if identifier in self.funcs.keys(): # ensure key exists
            # if it exists return corresponding value
            return self.funcs[identifier]
        else:
            # otherwise, raise an exception
            raise self.FunctionContextError(f'Function \'{identifier}\' not assigned')
    
    def lookupExpressionTree(self, identifier: str) -> RealValuedExpression:
        return self.lookup(identifier)[2]

    def lookupExpressionVars(self, identifier: str) -> RealValuedExpression:
        return self.lookup(identifier)[1]
    
    def lookupExpression(self, identifier: str) -> RealValuedExpression:
        return self.lookup(identifier)[0]

    def __str__(self) -> str:
        return self.funcs.__str__()
    
    def toString(self) -> str:
        retStr: str = ""
        retStr += "Functions:\n"
        for id in self.funcs:
            details = self.funcs[id]
            vars = ""
            for var in details[1][:-1]:
                vars += f"{var},"
            vars += details[1][-1]
            retStr += f"  {id}({vars})={details[0]}\n"
        return retStr
        
from FunctionContext import FunctionContext
from NumericalContext import NumericalContext
from RealValuedExpressionBuilder import RealValuedExpressionBuilder
import ExpressionHelperFunctions
from re import split

class Calculator:
    # custom exception class
    class CalculatorError(Exception):
        def __init__(self, message) -> None:
            super().__init__(message)

    def __init__(self) -> None:
        self.vars = NumericalContext()
        self.functions: FunctionContext = FunctionContext()

    def splitIdPars(self, function) -> tuple:
        functionId, functionVars, extra = split('\(|\)', function)  # split the function id and and the function arguments, extra is for the extra list cell 
        functionVars = ExpressionHelperFunctions.clearWhitespace(functionVars)
        functionVars = split(',|;', functionVars) # seperate the function variables, can be delimited using ',' or ';'
        return functionId, functionVars

    # this will convert strings containing numbers to numbers, or otherwise replace the variable with the corresponding value
    # using the calculator's numerical context
    def processPars(self, pars: list) -> list:
        functionVars = pars
        for i in range(len(functionVars)):
            cell = functionVars[i]
            tempCell = cell
            if tempCell[0] == '-': # incase cell is a negative number
                tempCell = tempCell[1:] # remove minus
            if ExpressionHelperFunctions.isNumber(tempCell) == False: # if cell is not a number
                try:
                    cell = str(self.vars.lookup(cell)) # search for the variable in the variables context
                except NumericalContext.NumericalContextError:
                    raise self.CalculatorError(f"Variable: '{cell}' is not recognized")
            cell = float(cell)
            if cell // 1 == cell:
                cell = int(cell)
            functionVars[i] = cell
        return functionVars

    # client passes in function in form f(x)=4x^2
    def addFunction(self, function: str) -> None:
        builder: RealValuedExpressionBuilder = RealValuedExpressionBuilder()    
        function, expression = split('=', function) # split the function id and arguments from the expression
        functionId, functionVars, extra = split('\(|\)', function)  # split the function id and and the function arguments, extra is for the extra list cell
        functionVars = ExpressionHelperFunctions.clearWhitespace(functionVars)
        functionVars = split(',|;', functionVars) # seperate the function variables, can be delimited using ',' or ';'
        expressionTree = builder.build(expression) # build the tree
        self.functions.assign(functionId, functionVars, expression, expressionTree) # store the function in the context

    def addVariable(self, name: str, value: int or float):
        self.vars.assign(name, value)

    def evaluateFunction(self, function: str) -> int or float:
        tempContext: NumericalContext = NumericalContext()
        id, pars = self.splitIdPars(function)
        self.processPars(pars)
        vars = self.functions.lookupExpressionVars(id)
        for var, value in zip(vars, pars):
            tempContext.assign(var, value)
        combinedContext = tempContext.combine(self.vars)
        return self.functions.lookupExpressionTree(id).evaluate(combinedContext)
        

    def __str__(self) -> str:
        newlinedVars = self.vars.toString().replace(',', ",\n")
        retStr = f"{self.functions.toString()}\n{newlinedVars}"
        return retStr
    


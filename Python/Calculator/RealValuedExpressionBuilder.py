from ExpressionHelperFunctions import *
from RealValuedExpression import *
from ExpressionPreparer import *

class RealValuedExpressionBuilder:
    def __init__(self) -> None:
        pass

    # Level 1 precedence operators: +-
    # Level 2 precedence opreators: */
    # Level 3 precedence operators: ^
    def opPrecedenceLevel(self, op: str) -> int:
        if op in '+-':
            return 1
        if op in '*/':
            return 2
        return 3

    # Creates an expression that is not an operator
    def getTerminalExpression(self, cell) -> RealValuedExpression:
        if isNumber(cell): # if a number is contained
            if cell.isdecimal(): # cell is a decimal number
                cell = int(cell)
            else: # cell is a floating point number
                cell = float(cell)
            terminal = ConstantExpression(cell)
        else: # if a variable is contained
            terminal = VariableExpression(cell)
        return terminal

    def getOpExpression(self, cell: str, rightOp: RealValuedExpression = None) -> BinaryExpression:
        if cell == '*':
            return MultiplicationExpression(None, rightOp)
        if cell == '/':
            return DivisionExpression(None, rightOp)
        if cell == '+':
            return AdditionExpression(None, rightOp)
        if cell == '-':
            return SubtractionExpression(None, rightOp)
        if cell == '^':
            return ExponentExpression(None, rightOp)
        return None

    def buildTree(self, clarifiedList: list) -> RealValuedExpression:
        prevTerminal: ConstantExpression or VariableExpression = None
        prevOperator: BinaryExpression = None
        prevOps: list[BinaryExpression] = [None, None, None]
        retOp: RealValuedExpression = None
        retOpPrecedence: int = None

        # process first cell
        cell = clarifiedList[-1]
        if type(cell) is not list:                          # if it is not a subtree
            prevTerminal = self.getTerminalExpression(cell) # if the first terminal is a constant or variable
        else:
            prevTerminal = self.buildTree(cell)             # if the first 'terminal' is a tree
        if len(clarifiedList) < 2:
            return prevTerminal                             # expression only consists of a constant or a variable
        # otherwise, add cell as right operand to first operator
        cell = clarifiedList[-2]
        retOp = prevOperator = prevOps[self.opPrecedenceLevel(cell) - 1] = self.getOpExpression(cell, prevTerminal) # create a new node, with the first const/var as the right operand
        retOpPrecedence = self.opPrecedenceLevel(cell) - 1
        for cell in reversed(clarifiedList[:-2]): # loop through each element but the last 2
            if type(cell) is not list:      # if it is not a subtree
                cell: str = cell            # tell vscode linter that it is a string
                if isOperator(cell):        # if an operator is contained
                    i = level = self.opPrecedenceLevel(cell) - 1 # get the index-level of the new operator
                    prevOperator = self.getOpExpression(cell) # create a new expression node
                    if level < retOpPrecedence:
                        retOpPrecedence = level
                        retOp = prevOperator
                    while i >= 0: # while index not below minimum 
                        if prevOps[i] is not None: # if a previous operator of a lower is found
                            # if i == level:         # if the level of the previous operator is the same as the level of the new operator
                            rightHand: RealValuedExpression = prevOps[i].getAndSetLeft(prevOperator) # get the left hand of the previous operator, and udpate it to point to the new expression
                            prevOperator.getAndSetRight(rightHand) # set the new operators right hand equal to the previous operators left hand
                            break
                        i -= 1
                    prevOps[level] = prevOperator # update the prevops list to contain the new node
                    if i == -1: # if a previous operator of lower precedence was not found, then new expression should be the root of the tree
                        # for each expression in the prevops list, as soon as an expression of 
                        # lower precedence is found, it should become the right operand of the new expression 
                        for expression in prevOps[level + 1:]:
                            if expression is not None: # if an operator of higher precedence is found
                                prevOperator.getAndSetRight(expression) # set that operator as the right operand of the new operator
                                break
                        for i in range(level + 1, 3): # clear list of higher precedence operators
                            prevOps[i] = None
                else:
                    prevTerminal = self.getTerminalExpression(cell) # otherwise, it is a constant or variable expression
                    prevOperator.getAndSetLeft(prevTerminal) # add it as the left operand as the previous operator
            else:
                prevTerminal = self.buildTree(cell) # if is a list, it means there is a sub tree
                prevOperator = prevOperator.getAndSetLeft(prevTerminal) # set sub tree as left operand of previous 
        return retOp
    
    def build(self, expression: str, verbose: bool = False) -> RealValuedExpression:
        prepper: ExpressionPreparer = ExpressionPreparer()
        preparedExpression = prepper.prepare(expression, verbose = verbose)
        expresionTree: RealValuedExpression = self.buildTree(preparedExpression)
        return expresionTree
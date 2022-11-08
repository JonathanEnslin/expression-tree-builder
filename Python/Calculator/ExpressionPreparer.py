from ExpressionHelperFunctions import *

class ExpressionPreparer:
    def __init__(self) -> None:
        pass

    # this function takes in an expression, adds operators to clarify the syntax of the expression
    # Example: X(6X)(5+5ALL)6 would become X*(6*X)*(5+5*ALL)*6
    def clarify(self, expression: str) -> str:
        newExpression = ""
        if len(expression) < 2:
            return expression
        for l,r in zip(expression, expression[1:]): # loop through chars in pairs, with the right char being advanced one position
            newExpression += l
            if isVar(l) and (isNumeric(r) or isOpeningBracket(r)):
                newExpression += '*'
            elif isNumeric(l) and (isVar(r) or isOpeningBracket(r)):
                newExpression += '*'
            elif isClosingBracket(l) and (isOpeningBracket(r) or isVar(r) or isNumeric(r)):
                newExpression += '*'
        newExpression += expression[-1]
        return newExpression

    # Takes in an iterator to the start of the expression being parsed
    # This slices an expression into atomic units
    #   Atomic units are segments of an expression that can stand alone, such as:
    #       variables, constants, operators
    # It will return a tree consisting of atomic units and branch into subtrees, that in turn also consist of atomic units as well as other branches
    # the tree structure comes from the fact that brackets will be see as an individual structure, and that tree will be stored inside the list as well
    def slice(self, it) -> list:
        expressionList: list = []
        curr = next(it, None)
        while curr is not None: # while end of string not reached
            if isOpeningBracket(curr):
                expressionList.append(self.slice(it)) # if a opening bracket is encountered, create a sub tree
            elif isClosingBracket(curr): # if closing bracket is reached, sub-tree is created, return the list
                return expressionList
            elif isNumeric(curr):
                expressionList.append(curr) # add in first digit of new number
                while (curr := next(it, None)) is not None and isNumeric(curr): # add remaining digits
                    expressionList[-1] += curr
                continue
            elif isOperator(curr):
                    expressionList.append(curr)
            elif isVar(curr):
                expressionList.append(curr) # add in first digit of new number
                while (curr := next(it, None)) is not None and isVar(curr): # add remaining digits
                    expressionList[-1] += curr
                continue
            curr = next(it, None) # next character
        if expressionList[0] == '-':
            expressionList.insert(0, '0') # to account for an expression startin with a zero, -x becomes 0-x
        return expressionList

    def prepare(self, expression: str, verbose: bool = False) -> list:
        if verbose:
            print(expression)
        clarified = clearWhitespace(expression)
        if verbose:
            print(clarified)
        clarified = self.clarify(clarified)
        if verbose:
            print(clarified)
        sliced = self.slice(iter(clarified))
        if verbose:
            print(sliced)
        return sliced
    
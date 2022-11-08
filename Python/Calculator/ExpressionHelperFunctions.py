# takes in an expression string and removes any whitespaces
def clearWhitespace(expression: str) -> str:
    return expression.replace(" ", "")

def isOperator(ch: str) -> bool:
    operators = ['*','/','+','-','^']
    return ch in operators

def isOpeningBracket(ch: str) -> bool:
    return ch == '(' or ch == '['

def isClosingBracket(ch: str) -> bool:
    return ch == ')' or ch == ']'

# a decimal point is also included as being numeric
def isNumeric(ch: str) -> bool:
    return ch.isdigit() or ch == '.'

# returns true if a character is not an operator, nor numeric, nor brackets, anything that can be a variable
def isVar(ch: str) -> bool:
    return not (isNumeric(ch) or isOperator(ch) or ch == "(" or ch == ")")

# determines if the string contains only a single number
def isNumber(s: str):
    isNum = True
    decimalPoints = 0
    for ch in s:
        isNum = isNum and isNumeric(ch)
        decimalPoints += (ch == '.')
    return isNum and (decimalPoints < 2)
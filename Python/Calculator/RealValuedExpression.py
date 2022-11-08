import NumericalContext
from abc import ABC, abstractmethod
# Base expression class
class RealValuedExpression(ABC):
    # abstract evaluate class
    @abstractmethod
    def evaluate(self, context: NumericalContext) -> int or float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
#======================================================================

# Expression class for a constant value
class ConstantExpression(RealValuedExpression):
    # constructor taking in a constant float or int
    def __init__(self, value: int or float) -> None:
        self.value = value
    
    # returns the value of the consant expression
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.value

    def __str__(self) -> str:
        return self.value.__str__()
#======================================================================

# Expression class for a variable value, needs a context
class VariableExpression(RealValuedExpression):
    # constructor taking in the name of the variable
    def __init__(self, name: str):
        self.name = name
    
    # returns the value of the variable using the passed CalculatorContext
    def evaluate(self, context: NumericalContext) -> int or float:
        return context.lookup(self.name)

    def __str__(self) -> str:
        return self.name.__str__()
#======================================================================

class BinaryExpression(RealValuedExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand
    
    def getAndSetLeft(self, leftOperand: RealValuedExpression) -> RealValuedExpression:
        oldLeft = self.leftOperand
        self.leftOperand = leftOperand
        return oldLeft

    def getAndSetRight(self, rightOperand: RealValuedExpression) -> RealValuedExpression:
        oldRight = self.rightOperand
        self.rightOperand = rightOperand
        return oldRight
#======================================================================

# expression class for the multiplication operation
class MultiplicationExpression(BinaryExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        super().__init__(leftOperand, rightOperand)

    # returns the mulitple of the left and right operand
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.leftOperand.evaluate(context) * self.rightOperand.evaluate(context)

    def __str__(self) -> str:
        return f"({self.leftOperand}*{self.rightOperand})"
#======================================================================

# expression class for the division operation
class DivisionExpression(BinaryExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        super().__init__(leftOperand, rightOperand)

    # returns the value of the left hand operand divided by the right hand operand
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.leftOperand.evaluate(context) / self.rightOperand.evaluate(context)
        
    def __str__(self) -> str:
        return f"({self.leftOperand}/{self.rightOperand})"
#======================================================================

# expression class for the addition operation
class AdditionExpression(BinaryExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        super().__init__(leftOperand, rightOperand)

    # returns the sum of the left and right operand
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.leftOperand.evaluate(context) + self.rightOperand.evaluate(context)

    def __str__(self) -> str:
        return f"({self.leftOperand}+{self.rightOperand})"
#======================================================================

# expression class for the subtraction operation
class SubtractionExpression(BinaryExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        super().__init__(leftOperand, rightOperand)

    # returns the value of the right hand operand subtracted from the left hand operand
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.leftOperand.evaluate(context) - self.rightOperand.evaluate(context)

    def __str__(self) -> str:
        return f"({self.leftOperand}-{self.rightOperand})"
#======================================================================

# expression class for the exponentiation operation
class ExponentExpression(BinaryExpression):
    def __init__(self, leftOperand: RealValuedExpression, rightOperand: RealValuedExpression) -> None:
        super().__init__(leftOperand, rightOperand)

    # returns the value of the left hand operation to the power of the right hand operation
    def evaluate(self, context: NumericalContext) -> int or float:
        return self.leftOperand.evaluate(context) ** self.rightOperand.evaluate(context)

    def __str__(self) -> str:
        return f"({self.leftOperand}^{self.rightOperand})"
#======================================================================

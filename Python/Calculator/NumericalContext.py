# Context will be stored as a map, mapping strings (chars) to numerical values
class NumericalContext:
    """Stores the context for the calculator, such as variables and their values"""
    
    # custom exception class
    class NumericalContextError(Exception):
        def __init__(self, message) -> None:
            super().__init__(message)

    
    # Default constructor
    def __init__(self) -> None:
        # Dictionary containing variable names and their values
        self.varDict = {}
    
    # assigns a variable and the value mapped to
    def assign(self, name: str, value: int or float) -> None:
        self.varDict[name] = value

    def lookup(self, name: str) -> int or float:
        if name in self.varDict.keys(): # ensure key exists
            # if it exists return corresponding value
            return self.varDict[name]
        else:
            # otherwise, raise an exception
            raise self.NumericalContextError(f'variable \'{name}\' not assigned')
    
    def __str__(self) -> str:
        return self.varDict.__str__()

    # makes a shallow copy
    def copy(self):
        newContext = NumericalContext()
        newContext.varDict = self.varDict.copy()
        return newContext

    # combines two contexts, if two contexts contain the same name for a variable, self will overwrite the other one
    def combine(self, other):
        combinedContext: NumericalContext = other.copy()
        for name in self.varDict:
            combinedContext.assign(name, self.varDict[name])
        return combinedContext

    def toString(self) -> str:
        return f"Variables:\n{self.__str__()}"
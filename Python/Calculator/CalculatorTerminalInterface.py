from Calculator import Calculator
from re import split
from ExpressionHelperFunctions import clearWhitespace

from NumericalContext import NumericalContext

class CalculatorTerminalInterface:

    def __init__(self) -> None:
        self.calc = Calculator()
        self.endLoop = False
        self.options: dict = {
            1: ("Add Function", self.addFunction),
            2: ("Add variable/constant", self.addVariable),
            3: ("Evaluate function", self.evaluateFunction),
            4: ("Display Calculator", self.displayCalculator),
            'z': ("Exit", self.terminateLoop)
        }

    # def immediateCalculation(self) -> None:

    def terminateLoop(self) -> None:
        self.endLoop = True

    def addFunction(self) -> None:
        print("Please provide a function:", end = " ")
        function = input()
        self.calc.addFunction(function)

    def evaluateFunction(self) -> None:
        print("Please provide the function to be evaluated:", end = " ")
        call = input()
        try:
            print(call, '=', self.calc.evaluateFunction(call))
        except NumericalContext.NumericalContextError as e:
            print(f"Error: {e}")
        print("Press ENTER to continue..")
        input()

    def addVariable(self) -> None:
        print("Please provide the variable you would like to add:", end = " ")
        var = input()
        var = clearWhitespace(var)
        varName, varValue = split('=', var)
        varValue = float(varValue)
        if varValue // 1 == varValue:
            varValue = int(varValue)
        self.calc.addVariable(varName, varValue)

    def displayCalculator(self) -> None:
        print(self.calc)
        print("Press ENTER to continue..")
        input()


    def displayOptions(self) -> None:
        print("------------------------")
        print("Please choose an option:")
        print("------------------------")
        for option in self.options:
            print(f"|({option}) {self.options[option][0]}")
        print("------------------------")
        print("Option:", end = " ")

    def getUserInput(self):
        inp = input()
        if inp.isdecimal():
            inp = int(inp)
            if inp < 1 or inp > 4:
                print("Invalid input, please try again:", end = " ")
                self.getUserInput()
            else:
                self.options[inp][1]()
        elif inp.lower() != 'z':
            print("Invalid input, please try again:", end = " ")
            self.getUserInput()
        else:
            self.options[inp][1]()

    def runInterface(self) -> None:
        while not self.endLoop:
            self.displayOptions()
            self.getUserInput()

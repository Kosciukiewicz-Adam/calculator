from globals import *
from decimal import *

class Calculations:
    def __init__(self):
        self.initialCalculationOperations = []
        self.calculationOperations = []

    def getResult(self, calculationString):
        self.splitCalculationToParts(calculationString)
        self.executeFirstOrderCalculations()
        result = self.getFinalResult()

        self.initialCalculationOperations = []
        self.calculationOperations = []

        return result

    def calculate(self, firstValue, secondValue, operator):
        if operator == "*":
            return Decimal(firstValue) * Decimal(secondValue)
        elif operator == "/":
            return Decimal(firstValue) / Decimal(secondValue)
        elif operator == "+":
            return Decimal(firstValue) + Decimal(secondValue)
        elif operator == "-":
            return Decimal(firstValue) - Decimal(secondValue)

    def splitCalculationToParts(self, calculationString):
        for index in range(0, len(calculationString)):
            isNegativeValue = calculationString[index] == "-"
            isOperator = calculationString[index] in operators

            if index > 0:
                isNegativeValue = isNegativeValue and self.initialCalculationOperations[-1]["type"] == "operator"

            if isOperator and not isNegativeValue:
                self.initialCalculationOperations.append({"type": "operator", "value": calculationString[index]})
            else:
                if len(self.initialCalculationOperations) == 0:
                    type = "operator" if isOperator else "number"
                    self.initialCalculationOperations.append({"type": type, "value": calculationString[index]})
                else:
                    if self.initialCalculationOperations[-1]["type"] == "operator":
                        self.initialCalculationOperations.append({"type": "number", "value":calculationString[index]})
                    else:
                        self.initialCalculationOperations[-1]["value"] += calculationString[index]
            
    def executeFirstOrderCalculations(self):
        iterationsToSkipCounter = 0

        for index in range(0, len(self.initialCalculationOperations)):
            operation = self.initialCalculationOperations[index]

            if iterationsToSkipCounter == 0:
                remainingOperations = len(self.initialCalculationOperations) - index - 1
                
                if iterationsToSkipCounter > 0:
                    iterationsToSkipCounter -= 1

                if remainingOperations >= 2:
                    nextOperation = self.initialCalculationOperations[index + 1]
                    afterNextOperation = self.initialCalculationOperations[index + 2]

                    if (
                        operation["type"] == "number" and
                        nextOperation["type"] == "operator" and
                        nextOperation["value"] in ["/", "*"] and
                        afterNextOperation["type"] == "number"
                    ):
                        self.calculationOperations.append({"type": "number", "value": self.calculate(
                            self.initialCalculationOperations[index]["value"],
                            afterNextOperation["value"],
                            nextOperation["value"]
                        )})

                        iterationsToSkipCounter = 3
                    else:
                        self.calculationOperations.append(operation)
                else:
                    self.calculationOperations.append(operation)
            
        
    def getFinalResult(self):
        sum = 0
        operatorToUse = ""

        for index in range(0, len(self.calculationOperations)):
            operation = self.calculationOperations[index]

            if operation["type"] == "operator":
                operatorToUse = operation["value"]
            else:
                if index > 0:
                    sum = self.calculate(sum, operation["value"], operatorToUse)
                else:
                    sum = operation["value"]

        if sum % 1 == 0:
            return str(int(sum))

        return str(sum)
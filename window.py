import tkinter as tk
from calculations import Calculations
from globals import *

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.resultValue = ""

        self.displayFrame = self.createDisplayFrame()
        self.buttonFrame = self.createButtonFrame()
        self.resultLabel = self.createResultLabel()

        self.buttonFrame.rowconfigure(0, weight=1)

        for i in range(1,5):
            self.buttonFrame.rowconfigure(i, weight=1)
            self.buttonFrame.columnconfigure(i, weight=1)

        self.createButtons()
        self.createOperatorButtons()
        self.createCustomButton("C", (0,1), LIGHT_BLUE, 3, self.clearValues)
        self.createCustomButton("=", (4,3), LIGHT_BLUE, 2, self.calculateResult)

    def updateLabelValue(self):
        self.resultLabel.config(text=self.resultValue)

    def canPlaceDot(self):
        if len(self.resultValue) == 0:
            return False

        lastValue = self.resultValue[-1]
        distanceToLastDot = None
        distanceToLastOperator = None
        lastValueDotOrOperator = lastValue in operators or lastValue == "."
        doesExpresionHaveOperator = set(operators).intersection(list(self.resultValue))
        doesExpresionHaveDot = "." in self.resultValue

        if lastValueDotOrOperator or not doesExpresionHaveOperator and doesExpresionHaveDot:
            return False

        if not doesExpresionHaveOperator and not doesExpresionHaveDot:
            return True
        
        distanceCounter = 0

        for index in reversed(range(0, len(self.resultValue))):
            distanceCounter +=1

            if self.resultValue[index] in operators and distanceToLastOperator == None:
                distanceToLastOperator = distanceCounter
            elif self.resultValue[index] == "." and distanceToLastDot == None:
                distanceToLastDot = distanceCounter

        return distanceToLastDot > distanceToLastOperator

    def defaultHandleButtonClick(self, value):
        if value == "." and not self.canPlaceDot():
            return

        self.resultValue += str(value)
        self.updateLabelValue()

    def clearValues(self):
        self.resultValue = ""
        self.updateLabelValue()

    def calculateResult(self):
        calculations = Calculations()
        result = calculations.getResult(calculationString=self.resultValue)
        self.resultValue = result
        self.updateLabelValue()

    def handleOperationButtonClick(self, value):
        isPrevValueOperator = len(self.resultValue) > 0 and self.resultValue[-1] in operators
        isNegativeSimbol = value == "-" and isPrevValueOperator

        if len(self.resultValue) > 2:
            isNegativeSimbol = isNegativeSimbol and self.resultValue[-1] not in operators

        if not isNegativeSimbol and isPrevValueOperator:
            return

        self.resultValue += str(value)
        self.updateLabelValue()

    def createButtons(self):
        for digit, gridValue in DIGITS.items():
            button = tk.Button(self.buttonFrame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT_STYLE, borderwidth=0,
                command=lambda value = digit: self.defaultHandleButtonClick(value)
            )
            button.grid(row=gridValue[0], column=gridValue[1], sticky=tk.NSEW)

    def createOperatorButtons(self):
        counter = 0
        for operation, symbol in OPERATIONS.items():
            button = tk.Button(self.buttonFrame,text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0,
                command=lambda value = operation: self.handleOperationButtonClick(value))
            button.grid(row=counter, column=4, sticky=tk.NSEW)
            counter += 1

    def createCustomButton(self, symbol, grid, bg, columnSpan, handleClick):
        button = tk.Button(self.buttonFrame,text=symbol, bg=bg, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda: handleClick())
        button.grid(row=grid[0], column=grid[1], sticky=tk.NSEW, columnspan=columnSpan)

    def createResultLabel(self):
        label = tk.Label(
            self.displayFrame,
            font=LARGE_FONT_STYLE,
            text=self.resultValue,
            fg=LABEL_COLOR,
            bg=LIGHT_GRAY,
            anchor=tk.E,
            padx=24,
        )

        label.pack(expand=True, fill="both")
        return label

    def createDisplayFrame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY) 
        frame.pack(expand=True, fill="both")
        return frame

    def createButtonFrame(self):
        button = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        button.pack(expand=True, fill="both")
        return button

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    Window().run()
# NOTE - Please make sure images are showing on the UI (UCL logo, images of money, image of boy, donut etc).

import math
import random
from random import randint

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Assmt3 import *

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_wholeWindow()
ui.setupUi(window)

#Creating/opening an appendable CSV file to which to write results from each trial, including headers
resultsCSV = open("Results CSV.csv", "a")
resultsCSV = open("Results CSV.csv", "r")
resultsRead = resultsCSV.read()
if "Age" not in resultsRead: # Making sure headers only print on the first trial
    resultsCSV = open("Results CSV.csv", "w")
    resultsCSV.write("Age" + "," + "Education Level" + "," + "Gender" + "," + "Condition (mc - money, cc - control)" + "," + "Time Squares" + "," + "Help offered (no of sheets)")
resultsCSV.close()

# A function to colour the buttons
def colourButton(buttonNames): #
    buttonNames.setStyleSheet("background-color: lightGrey")
    # FLEXIBILITY NOTE: For this programme it was more code-efficient to make this function specific to lighGrey. To make the function more flexible this, simply add "colour" to the arguments of the function and also as the argument of buttNames.setStyleSheet()
colourButton(ui.nextButtCons) # Is there a way to pass all these buttons into one execution of the function? I tried splitting the buttons with "and", " , " and + within the function, but couldn't get it to work.
colourButton(ui.nextButtDem)
colourButton(ui.clearButt)
colourButton(ui.nextButtScramb)
colourButton(ui.helpButt)
colourButton(ui.nextButtInstr)
colourButton(ui.submitButt)
colourButton(ui.submitButtHelp)
colourButton(ui.noThanksButt)
colourButton(ui.finishButt)


# *********CONSENT PAGE*********

# Starting programme from Consent Page (index O)
ui.expStack.setCurrentIndex(0)
ui.errorConsentPage.hide()

#If all yes boxes are ticked, navigate to next page (Demographics Page)
def showDemogPage(): # Note: I'm scripting all "yes" buttons here instead of putting them in a container and reading them as children, as containers are already being used to store the yes and no radios on each question line (to make sure only yes OR no can be clicked).
    if ui.yesRadio1.isChecked() and ui.yesRadio2.isChecked() and ui.yesRadio3.isChecked() and ui.yesRadio4.isChecked() and ui.yesRadio5.isChecked() and ui.yesRadio6.isChecked() and ui.yesRadio7.isChecked():
        ui.expStack.setCurrentIndex(1)
    else:
        ui.errorConsentPage.show()

ui.nextButtCons.clicked.connect(showDemogPage)


# *********DEMOGRAPHICS PAGE*********

#Hide error messages
ui.errorAge.hide()
ui.errorGender.hide()
ui.errorEducation.hide()

#Set values for educationCombo box
items = ("Please choose", "High School", "Bachelors", "Masters", "Professional Diploma", "PhD")
ui.educationCombo.addItems(items)

#Accessing lists of words for the scramble task (used un next function, showScrambPage())
wordsMoneyDoc = open("wordsMoneyDoc.txt", "r")
wordsNeutralDoc = open("wordsNeutralDoc.txt", "r")

# Making sure there is an equal number of trials in each condition type (It will obviously be unequal by 1 if number of participants isn't in a multuple of 2!)
condition = "mc" # Starting the distribution process with money condition
import re #REFERENCE: This block. I adapted this functionality from online as I thought it was an efficient function for searching a CSV: https://docs.python.org/2/library/collections.html#collections.Counter
import collections
words = re.findall(r'\w+', open("Results CSV.csv").read())
moneyCondCount = collections.Counter(words).get('mc')
controlCondCount = collections.Counter(words).get('cc')
if moneyCondCount > controlCondCount:
    condition = "cc"
else:
    condition = "mc"

# Setting up imagery in the rest of the experiment based on condition selected
if condition == "mc": # The "money prime" condition.
    wordsRead = wordsMoneyDoc # For descramble puzzle
    ui.donutPic.hide()

elif condition == "cc": # The control condition
    wordsRead = wordsNeutralDoc
    ui.moneyBag.hide() # Removing images of money for control group
    ui.moneyCoins.hide()
    ui.dollarPic.hide()

# The function executed when "Next button on demographics page is clicked. Make sure participant can't
# proceed unless all fields have been filled and age condition met
def showScrambPage():
    ui.correctMessage.hide()
    ui.incorrectMessage.hide()
    count = 0 # Counting number of fields that have been filled on this page
    if ui.ageSpin.value() >= 18:
        count = count + 1
        ui.errorAge.hide()
    else:
        ui.errorAge.show()
    if ui.educationCombo.currentText() != "Please choose":
        count = count + 1
        ui.errorEducation.hide()
    else:
        ui.errorEducation.show()
    if ui.male.isChecked() or ui.female.isChecked() or ui.other.isChecked():
        count = count + 1
        ui.errorGender.hide()
    else:
        ui.errorGender.show()
    if count == 3:
        global ageEducation
        ageEducation = "\n" + str(ui.ageSpin.value()) + "," + str(ui.educationCombo.currentText()) # Storing the age and eductaion information entered on this page into a variable for writing at the end
        for butt in ui.radioContnrGen.children(): # Storing gender
            if butt.isChecked():
                global gender
                gender = butt.objectName()
        ui.expStack.setCurrentIndex(2)
# Setting up scramble page with first row of words
    wordsReadLine = wordsRead.readline()
    wordsRow = wordsReadLine.split(" ")
    ui.word1.setText(wordsRow[0])
    ui.word2.setText(wordsRow[1])
    ui.word3.setText(wordsRow[2])
    ui.word4.setText(wordsRow[3])
    ui.word5.setText(wordsRow[4])

ui.nextButtDem.clicked.connect(showScrambPage)



# *********SCRAMBLE WORD PAGE**********

pageTimer = QTimer()

def showPuzzleInstr():
    ui.expStack.setCurrentIndex(4)


# MAKING THE SET OF SCRAMBLED WORDS CHANGE EVERY TIME NEXT IS CLICKED, THEN MOVE TO NEXT PAGE WHEN 5 RUNS COMPLETED
runs = 0   #Counting the number of sentences that have been executed
correctCount = 0   #Counting the number of words that have been entered in the correct place
correctCountSingle = 0  #Counting the number of words that have been entered in the correct place

def nextScrambClicked():
    global runs # Creating a way to count when the runs have finished so prog knows when to move to next page
    global correctCountSingle
    if runs < 4: # NOTE: If this were the actual experiment, I would have included 30 runs (as per the original) - I've reduced it as requested to make marking easier
        wordsReadLine = wordsRead.readline()  # Reading a new line of words in the excel sheet every time nextButtScramb is clicked
        wordsRow = wordsReadLine.split(" ")
        runs = runs + 1
        ui.word1.setText(wordsRow[0])
        ui.word2.setText(wordsRow[1])  # In about 1 in every 30-60 run-throughs, this line returns an error. There seems
        # to be no pattern and I can't get the error to replicate easily to find out what the problem is. If this happens
        # when marking, please just run it again and it will work - then so you can see the rest of the programme
        ui.word3.setText(wordsRow[2])
        ui.word4.setText(wordsRow[3])
        ui.word5.setText(wordsRow[4])
        if correctCountSingle == 5:
            ui.incorrectMessage.hide()
            ui.correctMessage.show()
            correctCountSingle = 0 #Re-setting correct count for next run
        elif correctCountSingle < 5:
            ui.correctMessage.hide()
            ui.incorrectMessage.show()
            correctCountSingle = 0 #Re-setting correct count for next run
        for slot in ui.slotContainer.children():
            slot.setText("-")
    else:
        ui.expStack.setCurrentIndex(3)
        pageTimer.start(3500)
        pageTimer.timeout.connect(showPuzzleInstr)
        pageTimer.setSingleShot(True)
        fallTimer.start(20) # This for an animation on the "Well done" page

def clearWords(): # Allowing words to be deleted if user makes an error and wants to reset
    for slot in ui.slotContainer.children():
        slot.setText("-")
ui.clearButt.clicked.connect(clearWords)


# Making CLICKED WORDS GO ONE BY ONE INTO THE SENTENCE and adding 1 to "correctCount" when entered in the right place

# Note: I spent a long, long time trying to do this as a single function. It seems like a really simple thing to do -
# but it wouldn't work for a reason I don't understand. I have copied this failed attempt below - if you can see where
# I went wrong, I would greatly appreciate pointers. (correctCount hadn't been added in this version yet).

# def wordDrop(wordLabel): #Function for word 1 in the jumbled row. Will drop word1 into the next avaiable slot (ie slot that doesn't contain "-")
#     if ui.slot1.text() == '-':
#         ui.slot1.setText(wordLabel.text())
#     elif ui.slot2.text() == '-':
#         ui.slot2.setText(wordLabel.text())
#     elif ui.slot3.text() == '-':
#         ui.slot3.setText(wordLabel.text())
#     elif ui.slot4.text() == '-':
#         ui.slot4.setText(wordLabel.text())
#     else:
#         ui.slot5.setText(wordLabel.text())
# wordDrop(ui.word1)
# wordDrop(ui.word2)
# wordDrop(ui.word3)
# wordDrop(ui.word4)
# wordDrop(ui.word4)


def wordDrop1(): #Function for word 1 in the jumbled row. Will drop word1 into the next avaiable slot (ie slot that doesn't contain "-")
    if ui.slot1.text() == '-':
        ui.slot1.setText(ui.word1.text())
    elif ui.slot2.text() == '-':
        ui.slot2.setText(ui.word1.text())
        global correctCount
        correctCount = correctCount + 1 # For all the jumbled sentences, the correct slot for word1 is slot2, so we add to correctCount
        global correctCountSingle
        correctCountSingle = correctCountSingle + 1
    elif ui.slot3.text() == '-':
        ui.slot3.setText(ui.word1.text())
    elif ui.slot4.text() == '-':
        ui.slot4.setText(ui.word1.text())
    else:
        ui.slot5.setText(ui.word1.text())

def wordDrop2(): # Same as above but for word2
    if ui.slot1.text() == '-':
        ui.slot1.setText(ui.word2.text())
        global correctCount
        correctCount = correctCount + 1
        global correctCountSingle
        correctCountSingle = correctCountSingle + 1
    elif ui.slot2.text() == '-':
        ui.slot2.setText(ui.word2.text())
    elif ui.slot3.text() == '-':
        ui.slot3.setText(ui.word2.text())
    elif ui.slot4.text() == '-':
        ui.slot4.setText(ui.word2.text())
    else:
        ui.slot5.setText(ui.word2.text())

def wordDrop3():
    if ui.slot1.text() == '-':
        ui.slot1.setText(ui.word3.text())
    elif ui.slot2.text() == '-':
        ui.slot2.setText(ui.word3.text())
    elif ui.slot3.text() == '-':
        ui.slot3.setText(ui.word3.text())
    elif ui.slot4.text() == '-':
        ui.slot4.setText(ui.word3.text())
        global correctCount
        correctCount = correctCount + 1
        global correctCountSingle
        correctCountSingle = correctCountSingle + 1
    else:
        ui.slot5.setText(ui.word3.text())

def wordDrop4():
    if ui.slot1.text() == '-':
        ui.slot1.setText(ui.word4.text())
    elif ui.slot2.text() == '-':
        ui.slot2.setText(ui.word4.text())
    elif ui.slot3.text() == '-':
        ui.slot3.setText(ui.word4.text())
    elif ui.slot4.text() == '-':
        ui.slot4.setText(ui.word4.text())
    else:
        ui.slot5.setText(ui.word4.text())
        global correctCount
        correctCount = correctCount + 1
        global correctCountSingle
        correctCountSingle = correctCountSingle + 1

def wordDrop5():
    if ui.slot1.text() == '-':
        ui.slot1.setText(ui.word5.text())
    elif ui.slot2.text() == '-':
        ui.slot2.setText(ui.word5.text())
    elif ui.slot3.text() == '-':
        ui.slot3.setText(ui.word5.text())
        global correctCount
        correctCount = correctCount + 1
        global correctCountSingle
        correctCountSingle = correctCountSingle + 1
    elif ui.slot4.text() == '-':
        ui.slot4.setText(ui.word5.text())
    else:
        ui.slot5.setText(ui.word5.text())

# Executing the above functions only when its corresponding word is clicked
#ui.word1.clicked.connect(wordDrop)

ui.word1.clicked.connect(wordDrop1)
ui.word2.clicked.connect(wordDrop2)
ui.word3.clicked.connect(wordDrop3)
ui.word4.clicked.connect(wordDrop4)
ui.word5.clicked.connect(wordDrop5)

ui.nextButtScramb.clicked.connect(nextScrambClicked)


# ********* WELL DONE (FALLING DONUTS/MONEY) PAGE *********

# ANIMATING FALLING DOUGHNUTS/MONEY
fallTimer = QTimer()

global yDrop # Creating a variable for the y axis coordinate of the image
yDrop = 270 # Starting point for y coordinate

def pictureFall():
    global yDrop
    if yDrop != 440: # 440 is the furthest down I want the image to go
        yDrop = yDrop + 1 # Moving image down 1 unit at a time
        if condition == "cc":
            ui.donutPic.setGeometry(290, yDrop, 91,101)
            ui.dollarPic.hide()
        elif condition == "mc":
            ui.dollarPic.setGeometry(270, yDrop, 141, 121)

fallTimer.timeout.connect(pictureFall)



# *********INSTRUCTIONS PAGE - SQUARES*********

def showPuzzlePage():
    ui.expStack.setCurrentIndex(5)

ui.nextButtInstr.clicked.connect(showPuzzlePage)



# *********SQUARES PAGE*********

ui.timeDisp.hide() #Simply hiding the widget where I'm storing the timer count
ui.errorMessagePuz.hide()

def startTimer():
    global timeDisp
    timeDisp = float(ui.timeDisp.text())
    timeDisp = timeDisp + 1
    ui.timeDisp.setText(str(timeDisp))
    puzzleTimer.start(100)

puzzleTimer = QTimer()
puzzleTimer.timeout.connect(startTimer)

ui.nextButtInstr.clicked.connect(puzzleTimer.start)

def stopTimer():
    global timeDisp
    timeDisp = float(ui.timeDisp.text())
    puzzleTimer.stop()

ui.helpButt.clicked.connect(stopTimer)

# CREATING DRAG CLASS
#REF: This class was adapted from the following page as, although it needed quite heavily simplified, seemed a good option for creating a drag and drop function. Various Qt Documentaion pages were also used to understand and edit this code accordingly: https://stackoverflow.com/questions/42604618/drag-and-drop-a-qlabel-in-pyqt
class dragableLabel(QLabel): # Creating a new class/widget which inherits from class QLabel - called dragableLabel (DL)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: # event.button is mouse press/click. If mouse click is "left" rather than "right" action the following:
            self.mousePressPos = event.globalPos()  # The global position of the mouse at time of the click becomes "mousePressPos"
            self.mouseMovePos = event.globalPos()   # And is also stored in mouseMovePos
        super(dragableLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos()) #Mapping movement of mouse on the widget to global.
            globalPos = event.globalPos() # The position of the mouse when clicked (ie when event happens)
            diff = globalPos - self.mouseMovePos # Global position of mouse less global position whe clicked = "diff"
            newPos = self.mapFromGlobal(currPos + diff) # The "moved to" position
            self.move(newPos) #Moving DL to the new position
            self.mouseMovePos = globalPos
        super(dragableLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            moved = event.globalPos() - self.mousePressPos
            if moved.manhattanLength() > 3: # If moved less than 3 units on "Manhattan Grid", ignore the event.
                event.ignore()
                return
        super(dragableLabel, self).mouseReleaseEvent(event) # ? Does this at end of every function


# CREATING THE COLOURED TILES (DRAGABLE LABELS)
# NOTE - The puzzle is designed to be impossible so the participant is forced to ask for help
greenTiles = ["gt1", "gt2", "gt3", "gt4"]
gt1 = 300
for i in greenTiles:
    gt = dragableLabel(ui.squaresPage)
    gt.setStyleSheet("background-color: green")
    gt.setGeometry(10, gt1, 71, 71)
    gt.show()
    gt1 = gt1 + 90

blueTiles = ["bt1", "bt2", "bt3", "bt4"]
bt1 = 300
for i in blueTiles:
    bt = dragableLabel(ui.squaresPage)
    bt.setStyleSheet("background-color: blue")
    bt.setGeometry(90, bt1, 71, 71)
    bt.show()
    bt1 = bt1 + 90

redTiles = ["rt1", "rt2", "rt3", "rt4"]
rt1 = 300
for i in redTiles:
    rt = dragableLabel(ui.squaresPage)
    rt.setStyleSheet("background-color: red")
    rt.setGeometry(490, rt1, 71, 71)
    rt.show()
    rt1 = rt1 + 90

yellowTiles = ["yt1", "yt2", "yt3", "yt4"]
yt1 = 300
for i in yellowTiles:
    yt = dragableLabel(ui.squaresPage)
    yt.setStyleSheet("background-color: yellow")
    yt.setGeometry(570, yt1, 71, 71)
    yt.show()
    yt1 = yt1 + 90

# Function to move to debrief page
def showHelpRequestPage():
    ui.expStack.setCurrentIndex(6)

def submitButtClicked():
    ui.errorMessagePuz.show()

ui.submitButt.clicked.connect(submitButtClicked)
ui.helpButt.clicked.connect(showHelpRequestPage)


# ********* HELP REQUEST PAGE *********

# Writing everything to CSV
def submitAndWrite():
    helpOffered = ui.sheetsSpin.value()
    resultsCSV = open("Results CSV.csv", "a")
    resultsCSV.write(str(ageEducation) + "," + str(gender) + "," + str(condition) + "," + str(timeDisp) + "," + str(helpOffered))
    resultsCSV.close()
    ui.expStack.setCurrentIndex(7)

ui.submitButtHelp.clicked.connect(submitAndWrite)
ui.noThanksButt.clicked.connect(submitAndWrite)


# *********DEBRIEF PAGE*********

def finishButtClicked():
    QProcess.startDetached("TCYL3/Assmt 3.py")  # REFERENCE: Stackoverflow: https://stackoverflow.com Used as it was the best way I could find to end and close the programme after a timer
    sys.exit(0)
    # I have designed this restart function as though the exercise is accessed by the participant through
    # a web link (found, for example, on Facebook). So the "run" button here acts as the questionnaire URL,
    # which would be clicked by the participant to open the exercise.

ui.finishButt.clicked.connect(finishButtClicked)

window.show()
sys.exit(app.exec_())

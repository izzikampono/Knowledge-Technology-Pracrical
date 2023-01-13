import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, \
    QLineEdit, QInputDialog, QFormLayout, QBoxLayout, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QDoubleValidator
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

# from PyQt5 import *

# global dictionary of dynamically changing widgets
widgets = {
    "button": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": []
}

# initiallize GUI application
app = QApplication(sys.argv)

# window and settings
window = QWidget()
window.setWindowTitle("What's that compound????")
window.setFixedWidth(1000)
# window.move(2700, 200)
window.setStyleSheet("background: #161219;")

# #initialliza grid layout
grid = QGridLayout()


def clear_widgets():
    ''' hide all existing widgets and erase
        them from the global dictionary'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def show_frame1():
    '''display frame 1'''
    clear_widgets()
    frame1()


def start():
    '''display frame 2'''
    clear_widgets()
    #frame2()
    next_question_frame()


def frame_button2():
    clear_widgets()
    # question widget
    question = QLabel("QUESTION2button")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )
    widgets["question"].append(question)
    create_buttons()
    button1 = create_buttons("answer1", 85, 5)
    button2 = create_buttons("answer2", 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)

    # place widget on the grid
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)

def frame_button4():
    clear_widgets()
    # question widget
    question = QLabel("QUESTION4button")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )
    widgets["question"].append(question)
    create_buttons()
    # answer button widgets
    button1 = create_buttons("answer1", 85, 5)
    button2 = create_buttons("answer2", 5, 85)
    button3 = create_buttons("answer3", 85, 5)
    button4 = create_buttons("answer4", 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    # place widget on the grid
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)

def frame_input_text():
    clear_widgets()
    # question widget
    question = QLabel("QUESTION4button")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )
    e2 = QLineEdit()
    e2.setValidator(QDoubleValidator(0.99, 99.99, 2))
    e2.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 12px;" +
        "color: 'white';" +
        "padding: 30px;"
    )

    button1 = create_buttons("Next", 5, 85)
    button1.clicked.connect(show_frame1)

    widgets["button"].append(button1)
    widgets["question"].append(question)
    widgets["text"].append(e2)

    grid.addWidget(widgets["button"][-1], 3, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["text"][-1], 2, 0)


def next_question_frame():
    # display frame for next question
    clear_widgets()
    dicty = utils.makeDictionaryBool(current_question)
    l = list(dicty.keys())  #question
    q = l[0]
    num_of_opt = len(dicty)-1

    if num_of_opt == 2:
        show_frame_button2(q, l)
    elif num_of_opt == 4:
        show_frame_button4(q, l)
    else:
        show_frame_input_text(q)

    # dict = utils.makeDictionaryBool(model.current_question)


def create_buttons(answer, l_margin, r_margin):
    '''create identical buttons with custom left & right margins'''
    button = QPushButton(answer)
    # button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        # setting variable margins
        "*{margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px}
        *:hover{
            background: '#BC006C'
        }
        '''
    )
    button.clicked.connect(show_frame1)
    return button


def frame1():
    # button widget
    button = QPushButton("START")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#BC006C';
            border-radius: 45px;
            font-size: 35px;
            color: 'white';
            padding: 25px 0;
            margin: 100px 200px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    # button callback
    button.clicked.connect(start)
    widgets["button"].append(button)

    # place global widgets on the grid
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


def frame2():
    # question widget
    question = QLabel("QUESTION")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )
    widgets["question"].append(question)

    # answer button widgets
    button1 = create_buttons("answer1", 85, 5)
    button2 = create_buttons("answer2", 5, 85)
    button3 = create_buttons("answer3", 85, 5)
    button4 = create_buttons("answer4", 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    # place widget on the grid
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)


# display frame 1
frame1()

window.setLayout(grid)

window.show()
sys.exit(app.exec())  # terminate the app

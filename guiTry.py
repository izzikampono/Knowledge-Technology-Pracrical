import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, \
    QLineEdit, QInputDialog, QFormLayout, QBoxLayout, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QDoubleValidator
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import xml.etree.ElementTree as et
import utils
import model_class

# global dictionary of dynamically changing widgets
widgets = {
    "button": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "text": []
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

# Tree = et.parse("rules.xml")
# root = Tree.getroot()
# current_question = root.find("question")

global dicty, l, q, num_of_opt, model, input_text, list_of_input, flag
list_of_input = []
flag = 0
model = model_class.Model()

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
    model.reset()
    next_question_frame()

def show_frame_button2(que, l):
    # question widget
    question = QLabel(que)
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"
    )
    widgets["question"].append(question)
    button1 = create_buttons(l[1], 85, 5)
    button2 = create_buttons(l[2], 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)

    # place widget on the grid
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)

def show_frame_button3(que, l):
    # question widget
    question = QLabel(que)
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"
    )
    widgets["question"].append(question)
    button1 = create_buttons(l[1], 85, 5)
    button2 = create_buttons(l[2], 5, 85)
    button3 = create_buttons(l[3], 85, 5)
    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)

    # place widget on the grid
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)


def show_frame_button4(que, l):
    # question widget
    question = QLabel(que)
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
    button1 = create_buttons(l[1], 85, 5)
    button2 = create_buttons(l[2], 5, 85)
    button3 = create_buttons(l[3], 85, 5)
    button4 = create_buttons(l[4], 5, 85)

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


def next_question():
    global flag,model
    list_of_input.append(float(input_text.text()))
    #print(input_text.text())
    # print(list_of_input)
    if(len(list_of_input) == 3):
        print("in if statement")
        model.calculateNumAtoms(list_of_input[0], list_of_input[1], list_of_input[2])
        flag = 1
        print(model.state)
        model.changeState2()

    next_question_frame()


def show_frame_input_text():
    # question widget
    label = ""
    if len(list_of_input) == 0:
        label = "Input molar mass:"
    elif len(list_of_input) == 1:
        label = "Input weight of compound:"
    elif len(list_of_input) == 2:
        label = "Input weight of precipitate:"

    question = QLabel(label)
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)

    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )

    global input_text
    input_text = QLineEdit()
    input_text.setValidator(QDoubleValidator(0.99, 99.99, 2))  # range of input, decimal points
    input_text.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 12px;" +
        "color: 'white';" +
        "padding: 30px;"
    )

    button1 = create_next_button("Next", 5, 85)
    button1.clicked.connect(next_question)
    
    widgets["button"].append(button1)
    widgets["question"].append(question)
    widgets["text"].append(input_text)

    grid.addWidget(widgets["button"][-1], 3, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["text"][-1], 2, 0)


def next_question_frame():
    # display frame for next question
    clear_widgets()
    global dicty, q, l, num_of_opt, flag
    dicty = utils.makeDictionaryBool(model.current_question)
    model.checkState()
    l = list(dicty.keys())
    q = l[0]
    num_of_opt = len(dicty)-1

    
    if model.mostRecent() == True and flag == 0:
        show_frame_input_text()
        flag = 1
    elif num_of_opt == 2:
        flag = 0
        show_frame_button2(q, l) 
    elif num_of_opt == 3:
        show_frame_button3(q, l)
    elif num_of_opt == 4:
        flag = 0
        show_frame_button4(q, l)

def create_next_button(answer, l_margin, r_margin):
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
    return button

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
    button.clicked.connect(lambda x: get_answer(answer))
    return button

def get_answer(answer):
    global dicty
    fact = dicty[answer]
    model.newFact(fact)
    # print(fact)
    
    model.changeState2()
    # model.updateFactbase()
    # rules = model.checkRules()
    # model.askRelatedQuestion(rules)

    next_question_frame()



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
    # button callbacks
    button.clicked.connect(start)
    widgets["button"].append(button)

    # place global widgets on the grid
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


# display frame 1
def show_ques():
    frame1()

show_ques()

window.setLayout(grid)

window.show()
sys.exit(app.exec())  # terminate the app

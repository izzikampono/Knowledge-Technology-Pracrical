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
    "text": [],
    "conclusion": [],
    "final_answer":[]
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
# model.reset()

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
    update_question_frame()

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
        print("in if, calculate num atoms")
        model.calculateNumAtoms(list_of_input[0], list_of_input[1], list_of_input[2])
        flag = 1
        print(model.state)
    
    model.changeState2()
    update_question_frame()

def next_no_input():
    global model
    factBase = model.root.find("factBase")
    newElement = et.SubElement(factBase,"fact")
    newElement.set("name","num_atoms")
    newElement.text =" test  "

    model.newFact(newElement)
    model.state = "agg_state"
    model.changeState2()
    update_question_frame()

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

    button1 = create_buttons("Next", 5, 85)
    button1.clicked.connect(next_question)
    
    widgets["button"].append(button1)
    widgets["question"].append(question)
    widgets["text"].append(input_text)

    grid.addWidget(widgets["button"][-1], 3, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["text"][-1], 2, 0)

def get_possible_answer():
    possible_answer = model.system_output()
    answer = "Possible compound(s): \n\n" + possible_answer[0] + "\n"

    for x in range(1, len(possible_answer)):
            answer = answer + "\n" + str(possible_answer[x]) + "\n"
    
    return answer

def show_frame_conclusion():
    show = 0
    possible_answer = get_possible_answer()
    model.updateFactbase()

    conclusion = model.checkConclusion()

    text = conclusion.text
    tag = conclusion.attrib['value']
    
    if tag == "unorganic" or tag == "not halogenic":
        show = 1
    
    if tag == "perform spectrometry" or tag == "weigh compound" or tag == "weigh precipitate":
        next = create_buttons("Next", 5, 85)
        next.clicked.connect(next_no_input)

        widgets["button"].append(next)
        grid.addWidget(widgets["button"][-1], 3, 1)
        
    con = QLabel(text)
    con.setAlignment(QtCore.Qt.AlignCenter)
    con.setWordWrap(True)

    answer = QLabel(possible_answer)
    answer.setAlignment(QtCore.Qt.AlignCenter)
    answer.setWordWrap(True)

    con.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"
    )

    answer.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 18px;" +
        "color: 'white';" +
        "padding: 75px;"
    )
    
    widgets["conclusion"].append(con)
    widgets["final_answer"].append(answer)
    grid.addWidget(widgets["conclusion"][-1], 1, 0, 1, 2)
    if(show == 0):
        grid.addWidget(widgets["final_answer"][-1], 2, 0, 1, 2)


def update_question_frame():
    # display frame for next question
    clear_widgets()
    global dicty, q, l, num_of_opt, flag, model
    dicty = utils.makeDictionaryBool(model.current_question)
    l = list(dicty.keys())
    q = l[0]
    num_of_opt = len(dicty)-1
    
    if model.state == "conclusion":
        show_frame_conclusion()
    elif model.mostRecent() == True and flag == 0:
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
    if(answer == "Next"):
        return button
    else:
        button.clicked.connect(lambda x: get_answer(answer))
    return button

def get_answer(answer):
    global dicty,model
    fact = dicty[answer]
    model.newFact(fact)
    if model.state!="conclusion":
        model.checkState()
    model.changeState2()
    model.updateFactbase()
    update_question_frame()  # after button clicked, frame updates

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

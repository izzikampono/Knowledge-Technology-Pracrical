
# def frame_button2():
#     clear_widgets()
#     # question widget
#     question = QLabel("QUESTION2button")
#     question.setAlignment(QtCore.Qt.AlignCenter)
#     question.setWordWrap(True)
#     question.setStyleSheet(
#         "font-family: Shanti;" +
#         "font-size: 25px;" +
#         "color: 'white';" +
#         "padding: 75px;"
#
#     )
#     widgets["question"].append(question)
#     create_buttons()
#     button1 = create_buttons("answer1", 85, 5)
#     button2 = create_buttons("answer2", 5, 85)
#
#     widgets["answer1"].append(button1)
#     widgets["answer2"].append(button2)
#
#     # place widget on the grid
#     grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
#     grid.addWidget(widgets["answer1"][-1], 2, 0)
#     grid.addWidget(widgets["answer2"][-1], 2, 1)
#
# def frame_button4():
#     clear_widgets()
#     # question widget
#     question = QLabel("QUESTION4button")
#     question.setAlignment(QtCore.Qt.AlignCenter)
#     question.setWordWrap(True)
#     question.setStyleSheet(
#         "font-family: Shanti;" +
#         "font-size: 25px;" +
#         "color: 'white';" +
#         "padding: 75px;"
#
#     )
#     widgets["question"].append(question)
#     create_buttons()
#     # answer button widgets
#     button1 = create_buttons("answer1", 85, 5)
#     button2 = create_buttons("answer2", 5, 85)
#     button3 = create_buttons("answer3", 85, 5)
#     button4 = create_buttons("answer4", 5, 85)
#
#     widgets["answer1"].append(button1)
#     widgets["answer2"].append(button2)
#     widgets["answer3"].append(button3)
#     widgets["answer4"].append(button4)
#
#     # place widget on the grid
#     grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
#     grid.addWidget(widgets["answer1"][-1], 2, 0)
#     grid.addWidget(widgets["answer2"][-1], 2, 1)
#     grid.addWidget(widgets["answer3"][-1], 3, 0)
#     grid.addWidget(widgets["answer4"][-1], 3, 1)
#
# def frame_input_text():
#     clear_widgets()
#     # question widget
#     question = QLabel("QUESTION4button")
#     question.setAlignment(QtCore.Qt.AlignCenter)
#     question.setWordWrap(True)
#     question.setStyleSheet(
#         "font-family: Shanti;" +
#         "font-size: 25px;" +
#         "color: 'white';" +
#         "padding: 75px;"
#
#     )
#     widgets["question"].append(question)
#
#     textbox = QLineEdit()
#     textbox.setStyleSheet(
#         '''
#         *{
#             border: 4px solid '#BC006C';
#             border-radius: 45px;
#             font-size: 35px;
#             color: 'white';
#             padding: 25px 0;
#             margin: 100px 200px;
#         }
#         *:hover{
#             background: '#BC006C';
#         }
#         '''
#     )
#     textbox.move(20, 20)
#     textbox.resize(280, 40)
#
# def next_question_frame():
#     # display frame for next question
#     clear_widgets()
#
#     #dict = utils.makeDictionaryBool(model.current_question)
#

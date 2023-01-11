import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from utils import *

dpg.create_context()
dpg.create_viewport(title='Determining chemical compounds', width=600, height=300)


def input_callback(sender, data):
    # dpg.get_value("Regular##inputtext")
    input_value = dpg.get_value("Input")
    print(input_value)


with dpg.window(label="Question 1"):
    dpg.add_text("Question 1 text")
    dpg.add_button(label="Answer 1")
    dpg.add_button(label="Answer 2")
    dpg.add_input_text(label="Input text", default_value=" ")
    # prints smth to terminal
    dpg.add_button(label="Input text", callback=input_callback)

# demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

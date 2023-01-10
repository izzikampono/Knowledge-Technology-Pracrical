import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Determining chemical compounds', width=600, height=300)

with dpg.window(label="Main Window"):
    dpg.add_text("Question 1")
    dpg.add_button(label="Answer 1")
    dpg.add_button(label="Answer 2")
    dpg.add_input_text(label="string", default_value=" ")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()


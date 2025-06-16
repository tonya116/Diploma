import dearpygui.dearpygui as dpg

dpg.create_context()

# big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
# big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
# small_let_end = 0x00FF  # small "я" in cyrillic alphabet
# remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
# alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
# alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped
with dpg.font_registry():
    with dpg.font("assets/arial_rus.ttf", 18) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        # biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
        # for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
        #     dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
        #     dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
        #     biglet += 1  # choose next letter
        dpg.bind_font(default_font)

dpg.create_viewport(title='Основное окно программы', width=800, height=600)
dpg.setup_dearpygui()

with dpg.window(label="Еще одно окно"):
    dpg.add_text("Просто текст")
    dpg.add_button(label="Сохранить")
    dpg.add_input_text(label="строка")
    dpg.add_slider_float(label="число с плавающей точкой")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
from dearpygui import dearpygui as dpg


def on_tab_changed(s, a, u):
    print(a)
    active_tab = dpg.get_value('tab_bar')
    print('Active tab:', active_tab)
    for tab in dpg.get_item_children('tab_bar')[1]:
        if not dpg.is_item_visible(tab):
            print('This tab was closed:', tab)
            dpg.delete_item(tab)

dpg.create_context()
dpg.create_viewport()
with dpg.window():
    with dpg.tab_bar(callback=on_tab_changed, tag='tab_bar'):
        dpg.add_tab(label='Tab 1', closable=True)
        dpg.add_tab(label='Tab 2', closable=True)
        dpg.add_tab(label='Tab 3', closable=True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(width=600, height=600)
dpg.setup_dearpygui()

W = H = 550

with dpg.window(label="Test", width=W, height=H):
    # Somehow drawlist ignores pos=(x, y), so we're using a group to place the
    # draw list into the desired position.  The larger the offset from (0, 0),
    # the more distorted image_quad will be.
    x = 100
    y = 0
    with dpg.group(pos=(x, y)):
        with dpg.drawlist(width=W, height=H):
            with dpg.draw_layer(tag="main pass", depth_clipping=True, perspective_divide=True, cull_mode=dpg.mvCullMode_None):
                dpg.set_clip_space(dpg.last_item(), 0, 0, W, H, -10.0, 10.0)

                with dpg.draw_node(tag="cube"):
                    N = 40
                    a = -N
                    b = N
                    c = -N
                    d = N
                    e = -N*5
                    f = N*5
                    proj = dpg.create_orthographic_matrix(a, b, c, d, e, f)
                    dpg.apply_transform(dpg.last_item(), proj)

                    s = 2
                    # Triangles seem to be transformed properly, so we're using
                    # two triangles to simulate a square.
                    dpg.draw_triangle((-s, -s, -s), (s, s, -s), (s, -s, -s), color=(255, 0, 255, 0),  fill=(255, 255, 255, 255), thickness=30)
                    dpg.draw_triangle((-s, -s, -s), (-s, s, -s), (s, s, s), color=(255, 0, 255, 0),  fill=(255, 255, 255, 255), thickness=30)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
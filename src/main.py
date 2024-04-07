import pyray as pr

screen_width:int = 800
screen_height:int = 600

pr.set_config_flags(pr.ConfigFlags.FLAG_WINDOW_UNDECORATED)
pr.init_window(screen_width, screen_height, "raygui - portable window")

# general variables
mouse_position: pr.Vector2 = pr.Vector2(0, 0)
window_position: pr.Vector2 = pr.Vector2(500, 200)
pan_offset: pr.Vector2 = mouse_position
drag_window: bool = False

pr.set_window_position(int(window_position.x), int(window_position.y))

exit_window: bool = False

pr.set_target_fps(60)

# main game loop
while not pr.window_should_close() and not exit_window:
    #update
    mouse_position: pr.Vector2 = pr.get_mouse_position()

    if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT) and not drag_window:
        if pr.check_collision_point_rec(mouse_position, pr.Rectangle(0, 0,screen_width, 20)):
            drag_window = True
            pan_offset = mouse_position

    if drag_window:
        window_position.x += (mouse_position.x - pan_offset.x)
        window_position.y += (mouse_position.y - pan_offset.y)

        pr.set_window_position(int(window_position.x), int(window_position.y))

        if pr.is_mouse_button_released(pr.MouseButton.MOUSE_BUTTON_LEFT):
            drag_window = False

    # draw
    pr.begin_drawing()

    pr.clear_background(pr.RAYWHITE)

    exit_window = pr.gui_window_box(pr.Rectangle(0, 0, screen_width, screen_height), "#198 PORTABLE WINDOW")

    pr.draw_text(f"Mouse Position: [{mouse_position.x}, {mouse_position.y}]", 10, 40, 10, pr.DARKGRAY)
    pr.draw_text(f"Pan offset: [{pan_offset.x}, {pan_offset.y}]", 10, 60, 10, pr.DARKGRAY)
    pr.draw_text(f"Window Position: [{window_position.x}, {window_position.y}]", 10, 80, 10, pr.DARKGRAY)

    pr.end_drawing()

# de-initialization
pr.close_window()




#pr.init_window(800, 450, "PY Typing Trainer")
#pr.set_target_fps(60)

#camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)

#while not pr.window_should_close():
#    pr.update_camera(camera, pr.CAMERA_ORBITAL)
#    pr.clear_background(pr.RAYWHITE)
#    pr.begin_mode_3d(camera)
#    pr.draw_grid(20, 1.0)
#    pr.end_mode_3d()
#    pr.draw_text("Hello world", 190, 200, 20, pr.VIOLET)
#    pr.end_drawing()
#pr.close_window()
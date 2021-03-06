"""
"""
import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.vec2d import Vec2d


mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


class GameWindow(pyglet.window.Window):
    """
    """

    def __init__(
            self,
            warpmap,
            dt_for_physicx,
            space,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        # set window location
        position = Vec2d(300, 50)
        self.set_location(position.x, position.y)
        self.warpmap = warpmap
        self.dt_for_physicx = dt_for_physicx
        self.remain_time_for_updating_physicx = dt_for_physicx
        self.space = space
        # framerate display
        self.fps = FPSDisplay(self)

        ########################################################################
        # self.record_filename = f"/tmp/warp#{4}hz#{self.warpmap.w}#{self.warpmap.h}#{self.warpmap.size}.pkl"
        ########################################################################

    def on_draw(self):
        self.clear()

        ########################################################################
        # Record (dump pickle in file) Warp grid (animation)
        # # 4 Hz
        # if not self.fps.count:
        #     with open(self.record_filename, "ab") as tmp_warp_file:
        #         pickle.dump(self.warpmap.get_web_crossings(), tmp_warp_file)
        ########################################################################

        self.warpmap.draw_debug(draw_flag=True, draw_web_constraints=True)

        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.quit_game()

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        mouse_body.position = x, y
        hit = self.space.point_query_nearest((x, y), 10, pymunk.ShapeFilter())
        if hit is not None:
            global selected
            body = hit.shape.body
            rest_length = mouse_body.position.get_distance(body.position)
            stiffness = 1000
            damping = 10
            selected = pymunk.DampedSpring(mouse_body, body, (0, 0), (0, 0),
                                           rest_length, stiffness, damping)
            self.space.add(selected)

    def on_mouse_release(self, x, y, button, modifiers):
        global selected
        if selected is not None:
            self.space.remove(selected)
            selected = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse_body.position = x, y

    def update(self, dt):
        """

        :param dt:
        :return:

        """
        # dt: deltatime from display
        self.remain_time_for_updating_physicx -= dt

        while self.remain_time_for_updating_physicx < 0.0:
            self.warpmap.relax(self.dt_for_physicx)
            self.remain_time_for_updating_physicx += self.dt_for_physicx

    def quit_game(self):
        # http://nullege.com/codes/search/pyglet.app.exit
        pyglet.app.exit()

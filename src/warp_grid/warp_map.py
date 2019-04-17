"""
"""
from dataclasses import dataclass, field
import itertools
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glPointSize
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_POINTS, GL_LINES
from OpenGL.raw.GL.VERSION.GL_2_0 import (
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    glUseProgram
)
import pathlib
import pyglet
import pymunk
from pymunk import Vec2d, Space

from warp_grid.flag import Flag3D


@dataclass
class WarpMapPyMunk(object):
    space: Space

    h: int = 13
    w: int = 11

    size: int = 32

    bs: list = field(default_factory=list)
    static_bs: list = field(default_factory=list)

    def __post_init__(self):
        web_group = 1

        for y in range(self.h):
            for x in range(self.w):
                b = pymunk.Body(1, 1)
                b.position = Vec2d(x, y) * self.size
                b.velocity_func = self.constant_velocity

                s = pymunk.Circle(b, 15)
                s.filter = pymunk.ShapeFilter(group=web_group)
                s.ignore_draw = True

                self.space.add(b, s)
                self.bs.append(b)

        stiffness = 5000. * 0.1
        damping = 100 * 0.1

        def add_joint(a, b):
            rl = a.position.get_distance(b.position) * 0.9
            j = pymunk.DampedSpring(a, b, (0, 0), (0, 0),
                                    rl, stiffness, damping)
            j.max_bias = 1000
            self.space.add(j)

        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                bs_xy = self.bs[x + y * self.w]
                for yi in range(y - 1, y + 2):
                    for xi in range(x - 1, x + 2):
                        if (xi, yi) != (x, y) and ((x - xi) * (y - yi) == 0):
                            add_joint(bs_xy, self.bs[xi + yi * self.w])

        print("len(self.space.constraints): {}".format(
            len(self.space.constraints)))

        # ATTACH POINTS
        def _static_point(b):
            static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            static_body.position = b.position
            self.static_bs.append(static_body)

            j = pymunk.PivotJoint(static_body, b, static_body.position)
            j.damping = 100
            j.stiffness = 20000
            self.space.add(j)

        self.static_bs = []
        # fisrt and last rows
        for x in range(self.w):
            _static_point(self.bs[x])
            _static_point(self.bs[x + (self.h - 1) * self.w])
        # first and last cols
        for y in range(self.h):
            _static_point(self.bs[y * self.w])
            _static_point(self.bs[(self.w - 1) + y * self.w])

        cooling_map_img = pyglet.image.load(
            pathlib.Path('datas/cooling_map.png'))
        # self.cooling_map_sprite = pyglet.sprite.Sprite(img=cooling_map_img)
        self.cooling_map_tex = cooling_map_img.get_texture()

        x = (self.w * 4) * 2.0
        y = (self.h * 4) * 2.0
        vlist_arr = [
            0, 0, 1.0, 1.0, 1.0, 0, 0,
            x, 0, 1.0, 1.0, 1.0, 1, 0,
            0, y, 1.0, 1.0, 1.0, 0, 1,
            x, y, 1.0, 1.0, 1.0, 1, 1,
        ]
        self.vlist = pyglet.graphics.vertex_list(
            4,
            ('v2f',
             list(itertools.chain(*zip(vlist_arr[::7], vlist_arr[1::7])))),
            ('t2f',
             list(itertools.chain(*zip(vlist_arr[5::7], vlist_arr[6::7]))))
        )

        # http://io7m.com/documents/fso-tta/
        self.vertex_shader_source = """
                #version 130
 
                out vec2 vTexCoord;
                 
                void
                main() {
                  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                  vTexCoord = vec2(gl_MultiTexCoord0);
                }
                """

        self.fragment_shader_source = """                
                #version 130
                
                uniform sampler2D tex0;
                
                in vec2 vTexCoord;
                out vec4 fragColor;
                
                void main() {
                    fragColor = texture(tex0, vTexCoord) * 8;
                }
                """

        self.shader = compileProgram(
            compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
            compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER),
        )

        self.flag = Flag3D()

    @staticmethod
    def constant_velocity(body: pymunk.Body, _gravity, _damping, _dt):
        body_velocity_normalized = body.velocity.normalized()
        #
        body.velocity = body_velocity_normalized * 75

    def get_web_crossings(self):
        return [
            [b.position.x, b.position.y]
            for b in self.bs
        ]

    def draw_debug(self,
                   draw_flag=False,
                   draw_static_attach_points=False,
                   draw_web_crossings=True,
                   draw_web_constraints=False, ):
        if draw_flag:
            # self.vao._draw_frame()
            self.flag.update(self.bs)
            glUseProgram(self.shader)
            self.flag.draw()
            glUseProgram(0)

        # static attach points
        if draw_static_attach_points:
            glColor3f(1, 0, 1)
            glPointSize(6)

            a = []
            for b in self.static_bs:
                a += [b.position.x, b.position.y]
                pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web crossings / bodies
        if draw_web_crossings:
            glColor3f(.1, .8, .05)
            a = []
            for b in self.bs:
                a += [b.position.x, b.position.y]
            glPointSize(4)
            pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web net / constraints
        if draw_web_constraints:
            a = []
            for j in self.space.constraints:
                a += [j.a.position.x, j.a.position.y, j.b.position.x,
                      j.b.position.y]
            pyglet.graphics.draw(len(a) // 2, GL_LINES, ('v2f', a))

    def relax(self, dt):
        self.space.step(dt)

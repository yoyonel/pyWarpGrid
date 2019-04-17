"""
"""
from dataclasses import dataclass

import pyglet
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glPointSize
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_POINTS, GL_LINES
from OpenGL.raw.GL.VERSION.GL_2_0 import (
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    glUseProgram
)

from warp_grid.flag import Flag3D
from warp_grid.warp_map_simulation import WarpMapSimulation


@dataclass
class WarpMapRenderer(WarpMapSimulation):
    flag: Flag3D = Flag3D()

    def __post_init__(self):
        super().__post_init__()

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

    def draw_debug(self,
                   draw_flag=False,
                   draw_static_attach_points=False,
                   draw_web_crossings=True,
                   draw_web_constraints=False, ):
        if draw_flag:
            self.flag.update(self.bs)
            glUseProgram(self.shader)
            self.flag.draw()
            glUseProgram(0)

        # static attach points
        if draw_static_attach_points:
            a = self.extract_positions_from_bodys(self.static_bs)
            glColor3f(1, 0, 1)
            glPointSize(6)
            pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web crossings / bodies
        if draw_web_crossings:
            a = self.extract_positions_from_bodys(self.bs)
            glColor3f(.1, .8, .05)
            glPointSize(4)
            pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web net / constraints
        if draw_web_constraints:
            a = self.extract_positions_from_bodys(
                self.space.constraints,
                func_extractor=lambda c: [c.a.position.x, c.a.position.y,
                                          c.b.position.x, c.b.position.y])
            pyglet.graphics.draw(len(a) // 2, GL_LINES, ('v2f', a))

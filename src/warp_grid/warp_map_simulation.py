"""
"""
from dataclasses import dataclass, field
import itertools
from typing import List, Iterable, Callable

import pymunk
from pymunk import Vec2d, Space, Body


@dataclass
class WarpMapSimulation(object):
    space: Space

    h: int = 13
    w: int = 11

    size: int = 32

    bs: List[Body] = field(default_factory=list)
    static_bs: List[Body] = field(default_factory=list)

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

        def add_joint(body_a: Body, body_b: Body):
            rl = body_a.position.get_distance(body_b.position) * 0.9
            j = pymunk.DampedSpring(body_a, body_b, (0, 0), (0, 0),
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
        def _static_point(body: Body):
            static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            static_body.position = body.position
            self.static_bs.append(static_body)

            j = pymunk.PivotJoint(static_body, body, static_body.position)
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

    @staticmethod
    def constant_velocity(body: pymunk.Body, _gravity, _damping, _dt):
        body_velocity_normalized = body.velocity.normalized()
        #
        body.velocity = body_velocity_normalized * 75

    @staticmethod
    def extract_positions_from_bodys(
            bodys: Iterable[Body],
            func_extractor: Callable[[Body], List] = lambda body: (
                    body.position.x, body.position.y)
    ) -> List[int]:
        return list(itertools.chain(*map(func_extractor, bodys)))

    def get_web_crossings(self) -> List[int]:
        return self.extract_positions_from_bodys(self.bs)

    def relax(self, dt):
        self.space.step(dt)

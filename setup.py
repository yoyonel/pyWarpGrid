# -*- encoding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='pyWarpGrid',
    version='0.1.0',
    license='MIT',
    description='',
    author='Lionel ATTY',
    author_email='yoyonel@hotmail.com',
    url='https://github.com/yoyonel/pyWarpGrid',
    packages=['pyWarpGrid.{}'.format(x) for x in find_packages('src/pyglet_pymunk')],
    package_dir={'': 'src'},
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Pyglet',
        'Programming Language :: Python :: Implementation :: Pymunk',
        'Topic :: Utilities',
    ],
    keywords=[],
    install_requires=[
        "cocos2d",
        "euclid",
        "numpy",
        "pillow",
        "PyOpenGL",         # http://pyopengl.sourceforge.net/ctypes/using.html
        "pyglet==1.3.2",
        "pymunk==5.3.2",    # https://stackoverflow.com/questions/45120438/pymunk-drawing-utils-not-working
                            # https://github.com/viblo/pymunk/issues/122
    ],
    entry_points={
        'console_scripts': [
            'WarpGrid = pyWarpGrid.warp_grid.app:main',
        ]
    },
    python_requires='>=3.7'
)

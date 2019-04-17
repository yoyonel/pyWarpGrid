PROJECT_NAME?=pyglet-pymunk-breakout-game
#
PACKAGE_NAME=$(shell python setup.py --name)
PACKAGE_FULLNAME=$(shell python setup.py --fullname)
PACKAGE_VERSION:=$(shell python setup.py --version)
#
PYTEST_OPTIONS?=-v
TOX_DIR?=${HOME}/.tox/hmx/$(PROJECT_NAME)
#
SDIST_PACKAGE=dist/${shell python setup.py --fullname}.tar.gz
SOURCES=$(shell find src/ -type f -name '*.py') setup.py MANIFEST.in

all: ${SDIST_PACKAGE}

${SDIST_PACKAGE}: ${SOURCES}
	@echo "Building python project..."
	@python setup.py sdist

pip: requirements_dev.txt
	@pip install -r requirements_dev.txt --upgrade

re: fclean all

fclean:
	@find . -name "*.pyc" -exec git rm --cached {} \;

"""
Usage IN TERMINAL .. :
	python build.py py2app
"""

from setuptools import setup

APP = ['AshCode.py']
DATA_FILES = [("", ["images"]), ("", ["Audio"])]
OPTIONS = {
	"iconfile": "images/icon.icns"
}

setup(
	name = "Ash Code",
	version = "1.0.0",
	app = APP,
	data_files = DATA_FILES,
	options = {"py2app": OPTIONS},
	  setup_requires = ["py2app"]
)
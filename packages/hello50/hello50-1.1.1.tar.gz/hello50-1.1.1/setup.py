from setuptools import setup, find_packages
import codecs
import os, glob

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.1'
DESCRIPTION = 'Hello world shit!!!!'
LONG_DESCRIPTION = 'Hello world 3~~~~~'

# Setting up
setup(
    name="hello50",
    version=VERSION,
    author="Malik",
    author_email="myemail46926213@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'hello'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    data_files=glob.glob('db/**')
)


"""
python setup.py sdist
twine upload dist/*

"""
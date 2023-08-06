from setuptools import setup, find_packages


VERSION = '1.0.3'
DESCRIPTION = 'A python lib to extend classes'
LONG_DESCRIPTION = 'A python lib to extend classes. Inject methods in a class without inheritance. It access protected methods and attributes.'

# Setting up
setup(
    name="ExtendClass",
    version=VERSION,
    author="Rodrigo Santos de Carvalho",
    author_email="<rodrigosc2401@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'extend', 'class', 'extend class', 'extendclass', 'extend-class', 'extend_class', 'extendclass'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

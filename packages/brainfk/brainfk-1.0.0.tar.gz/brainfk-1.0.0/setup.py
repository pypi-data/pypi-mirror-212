from setuptools import setup

setup(
    name="brainfk",
    version="1.0.0",
    packages=["brainfk"],
    entry_points={"console_scripts": ["brainfk = brainfk.interpreter:main"]},
    install_requires=["argparse"],
    author="Estifanose Sahilu",
    description="A Brainfuck interpreter package",
    url="https://github.com/estif0/brainfk",
)

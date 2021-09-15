from setuptools import setup

setup(
    name='sm',
    version='0.1',
    py_modules=['sm'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sm=sm:cli
    ''',
)
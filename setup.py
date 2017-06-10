from distutils.core import setup

setup(
    name='ir_distance',
    version='0.1',
    packages=[''],
    url='https://github.com/wasperen/ir_distance',
    license='MIT',
    author='wasperen',
    author_email='willem@van.asperen.org',
    install_requires=[
        'pigpio',
    ],
    description='Module to read distance from Sharp GP2D02 components on a Raspberry PI'
)

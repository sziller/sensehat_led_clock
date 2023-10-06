#!/usr/bin/python3.10

from setuptools import setup

'''
setup function to be run when creating packages for Organica
command to be typed in:
python setup.py sdist
'''
# ATTENTION! Wheel file might be needed, depending on environment

setup(
    name='sensehat_led_clock',  # package name, used at pip or tar.
    version='0.0.0',  # version Nr.... whatever
    packages=["SenseHatLedClock"],  # string list of packages to be translated
    url='',  # if url is used at all
    license='',  # ...
    author='sziller',  # well obvious
    author_email='sziller@gmail.com',  # well obvious
    description='SenseHat mounted 8x8 sized LED-clock',  # well obvious
    install_requires=[
        "sense_emu",
        "sense_hat"],
    dependency_links=[],  # if dependent on external projects
)

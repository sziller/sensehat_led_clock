#!/usr/bin/python3.10

import os
from setuptools import setup

'''
setup function to be run when creating packages for Organica
command to be typed in:
python setup.py sdist
python setup.py bdist_wheel
python setup.py sdist bdist_wheel
'''
# ATTENTION! Wheel file might be needed, depending on environment
NAME = 'sensehat_led_clock'
DOMAIN_NAME = "sziller.eu/"
PROJECT_PATH = "Projects/"
GEN_PACKAGES_PATH = PROJECT_PATH + "001_GeneralAssistance/GeneralCoding/Python/general_package_development/"
RPI_PACKAGES_PATH = PROJECT_PATH + "900_Raspberry/"
HAT_PACKAGES_PATH = RPI_PACKAGES_PATH + "SenseHat/"

INSTALL_REQUIRES = [
        "sense_emu",
        "sense_hat",
        "sensehat_assist @ http://{}{}sensehat_assist/dist/sensehat_assist-0.0.0-py3-none-any.whl"
        .format(DOMAIN_NAME, HAT_PACKAGES_PATH),
        "assist @ http://{}{}assist/dist/assist-0.0.0-py3-none-any.whl"
        .format(DOMAIN_NAME, GEN_PACKAGES_PATH)
    ]

print("--" + "-"*30 + "--",)
print("- {:^30} -".format(NAME))
print("--" + "-"*30 + "--",)
print("- {:^30} -".format("INSTALL_REQUIRES"))
print("--" + "-"*30 + "--")
for _ in INSTALL_REQUIRES:
    print(_)
print("--" + "-"*30 + "--")

setup(
    name=NAME,  # package name, used at pip or tar.
    version='0.0.0',  # version Nr.... whatever
    packages=["SenseHatLedClock"],  # string list of packages to be translated
    url='',  # if url is used at all
    license='',  # ...
    author='sziller',  # well obvious
    author_email='sziller@gmail.com',  # well obvious
    description='SenseHat mounted 8x8 sized LED-clock',  # well obvious
    install_requires=INSTALL_REQUIRES,
    dependency_links=[],  # if dependent on external projects
)

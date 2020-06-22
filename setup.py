#!/usr/bin/env python3

from setuptools import setup


setup(
    name="rf-pymods",
    description="A collection of small Python modules",
    author="Ryan Finnie",
    author_email="ryan@finnie.org",
    packages=["rf_pymods"],
    install_requires=["croniter"],
)

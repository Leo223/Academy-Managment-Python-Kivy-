#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(name='Excel de Asistencias',
	  version='1.1',
	  description= 'Crea un Excel de asistencias del mes correspondiente (INPUT: archivo JSON)',
	  author='JCP',
	  scripts=['Excel_Converter.py'],
	  console=['Excel_Converter.py'],
	  options={'py2exe': {'bundle_files': 1}},
	  zipfile=None
)

# import os
# os.system('python setup.py py2exe')
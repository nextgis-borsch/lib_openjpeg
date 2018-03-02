#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
##
## Copyright (c) 2017 NextGIS <info@nextgis.com>
## License: GPL v.2
##
## Purpose: Post processing script
################################################################################

import fileinput
import os
import sys
import shutil

cmake_src_path = os.path.join(sys.argv[1], 'CMakeLists.txt')

if not os.path.exists(cmake_src_path):
    exit('Parse path not exists')

utilfile = os.path.join(os.getcwd(), os.pardir, 'cmake', 'util.cmake')

# Get values
ver_major = "0"
ver_minor = "0"
ver_patch = "0"

ver_major_get = False
ver_minor_get = False
ver_patch_get = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKGRAY = '\033[0;37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DGRAY='\033[1;30m'
    LRED='\033[1;31m'
    LGREEN='\033[1;32m'
    LYELLOW='\033[1;33m'
    LBLUE='\033[1;34m'
    LMAGENTA='\033[1;35m'
    LCYAN='\033[1;36m'
    WHITE='\033[1;37m'

def extract_value(text):
    val_text = text.split(" ")
    val_text = val_text[1].split(")")
    return val_text[0]

def color_print(text, bold, color):
    if sys.platform == 'win32':
        print text
    else:
        out_text = ''
        if bold:
            out_text += bcolors.BOLD
        if color == 'GREEN':
            out_text += bcolors.OKGREEN
        elif color == 'LGREEN':
            out_text += bcolors.LGREEN
        elif color == 'LYELLOW':
            out_text += bcolors.LYELLOW
        elif color == 'LMAGENTA':
            out_text += bcolors.LMAGENTA
        elif color == 'LCYAN':
            out_text += bcolors.LCYAN
        elif color == 'LRED':
            out_text += bcolors.LRED
        elif color == 'LBLUE':
            out_text += bcolors.LBLUE
        elif color == 'DGRAY':
            out_text += bcolors.DGRAY
        elif color == 'OKGRAY':
            out_text += bcolors.OKGRAY
        else:
            out_text += bcolors.OKGRAY
        out_text += text + bcolors.ENDC
        print out_text

with open(cmake_src_path) as f:
    for line in f:
        if "set(OPENJPEG_VERSION_MAJOR" in line:
            ver_major = extract_value(line)
            ver_major_get = True
        elif "set(OPENJPEG_VERSION_MINOR" in line:
            ver_minor = extract_value(line)
            ver_minor_get = True
        elif "set(OPENJPEG_VERSION_BUILD" in line:
            ver_patch = extract_value(line)
            ver_patch_get = True

        if ver_major_get and ver_minor_get and ver_patch_get:
            break

for line in fileinput.input(utilfile, inplace = 1):
    if "set(MAJOR_VERSION " in line:
        print "    set(MAJOR_VERSION " + ver_major + ")"
    elif "set(MINOR_VERSION " in line:
            print "    set(MINOR_VERSION " + ver_minor + ")"
    elif "set(REV_VERSION " in line:
            print "    set(REV_VERSION " + ver_patch + ")"
    else:
        print line,

#!/usr/bin/env python

import getopt
import sys
import os
import configparser

globle_ini=os.environ.get('WPM_HOME',"~/wpm.ini");

conf=configparser.ConfigParser();


conf.read("./wpm.ini",encoding="utf-8")


print(conf.get("default","version"));


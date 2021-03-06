#!/usr/bin/env python2

# AL-hotcorners:
# A script for adding hot corners to Openbox.
# Written for CrunchBang Linux <http://crunchbang.org/>
# by Philip Newborough <corenominal@corenominal.org>
# ----------------------------------------------------------------------
# License:
#            DO WHAT THE YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE YOU WANT TO.
#
# Mildly modified to fit ARCHLabs naming scheme and to abide by Philip's rules
# ----------------------------------------------------------------------

from Xlib import display
from Xlib.ext.xtest import fake_input
from Xlib import X
from subprocess import Popen, PIPE, STDOUT
import sys, time, os, ConfigParser, re

check_intervall = 0.08

p = Popen(['xdotool','getdisplaygeometry'], stdout=PIPE, stderr=STDOUT)
Dimensions = p.communicate()
Dimensions = Dimensions[0].replace('\n', '')
Dimensions = Dimensions.split(' ')
width = int(Dimensions[0])
height = int(Dimensions[1])
hw = width / 2
rt = width - 1
bt = height - 1

def print_usage():
   print "AL-hotcorners: usage:"
   print "  --help          show this message and exit"
   print "  --kill          attempt to kill any running instances"
   print "  --daemon        run daemon and listen for cursor triggers"
   print ""
   exit()

if len(sys.argv) < 2 or sys.argv[1] == "--help":
   print_usage()

elif sys.argv[1] == "--kill":
   print "Attempting to kill any running instances..."
   os.system('pkill -9 -f AL-hotcorners')
   exit()

elif sys.argv[1] == "--daemon":
   Config = ConfigParser.ConfigParser()
   cfgdir = os.getenv("HOME")+"/.config/AL-hotcorners"
   rcfile = cfgdir+"/AL-hotcornersrc"
   bounce = 2
   disp = display.Display()
   root=display.Display().screen().root

   def mousepos():
      data = root.query_pointer()._data
      return data["root_x"], data["root_y"], data["mask"]

   def mousemove(x, y):
      fake_input(disp, X.MotionNotify, x=x, y=y)
      disp.sync()

   try:
      cfgfile = open(rcfile)
   except IOError as e:
      if not os.path.exists(cfgdir):
         os.makedirs(cfgdir)
      cfgfile = open(rcfile,'w')
      Config.add_section('Hot Corners')
      Config.set('Hot Corners','top_left_corner_command', 'skippy-xd-toggle')
      Config.set('Hot Corners','top_right_corner_command', 'gmrun')
      Config.set('Hot Corners','bottom_left_corner_command', '')
      Config.set('Hot Corners','bottom_right_corner_command', '')
      Config.write(cfgfile)
      cfgfile.close()

   while True:
      Config.read(rcfile)
      time.sleep(check_intervall)
      pos = mousepos()
      
      if pos[0] == 0 and pos[1] == 0:   
         if Config.get('Hot Corners','top_left_corner_command') != '':
            time.sleep(0.2)
            pos = mousepos()
            if pos[0] == 0 and pos[1] == 0:
               mousemove(pos[0] + bounce, pos[1] + bounce)
               os.system('(' + Config.get('Hot Corners','top_left_corner_command') + ') &')
               mousemove(pos[0] + bounce, pos[1] + bounce)
               time.sleep(0.1)
      
      elif pos[0] == rt and pos[1] == 0:
         if Config.get('Hot Corners','top_right_corner_command') != '':
            time.sleep(0.2)
            pos = mousepos()
            if pos[0] == rt and pos[1] == 0 :
               mousemove(pos[0] - bounce, pos[1] + bounce)
               os.system('(' + Config.get('Hot Corners','top_right_corner_command') + ') &')
               mousemove(pos[0] - bounce, pos[1] + bounce)
               time.sleep(0.1)

      elif pos[0] == 0 and pos[1] == bt:
         if Config.get('Hot Corners','bottom_left_corner_command') != '':
            time.sleep(0.2)
            pos = mousepos()
            if pos[0] == 0 and pos[1] == bt:
               mousemove(pos[0] + bounce, pos[1] - bounce)
               os.system('(' + Config.get('Hot Corners','bottom_left_corner_command') + ') &')
               mousemove(pos[0] + bounce, pos[1] - bounce)
               time.sleep(0.1)

      elif pos[0] == rt and pos[1] == bt:
         if Config.get('Hot Corners','bottom_right_corner_command') != '':
            time.sleep(0.2)
            pos = mousepos()
            if pos[0] == rt and pos[1] == bt:
               mousemove(pos[0] - bounce, pos[1] - bounce)
               os.system('(' + Config.get('Hot Corners','bottom_right_corner_command') + ') &')
               mousemove(pos[0] - bounce, pos[1] - bounce)
               time.sleep(0.1)

else:
   print_usage()
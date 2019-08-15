#!/usr/bin/env python3

import sys
from signal import signal, SIGPIPE, SIG_DFL

# http://newbebweb.blogspot.com/2012/02/python-head-ioerror-errno-32-broken.html
signal(SIGPIPE,SIG_DFL)

# Taken from: https://mail.python.org/pipermail/tutor/2003-November/026645.html
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


# Remove buffering, processing large datasets eats memory otherwise
sys.stdout = Unbuffered(sys.stdout)

#! /usr/bin/env python

import os
import sys
from pymarkovchain import MarkovChain

def stringify_file(fp):
	try:
		f = open(fp)
	except:
		print("CRITICAL: unable to open file " + fp)
		sys.exit(1);
	s = "";
	for l in f.readlines():
		s += l 
	return s

try:
	fp = sys.argv[1]
except:
	print "CRITICAL: no input files!"
	sys.exit(0)

try:
	msl = int(sys.argv[2])
except:
	msl = 0
	print "WARNING: no minimum sentence length specified, defaulting to zero"

def countString(s):
	words = ''.join(c if c.isalnum() else ' ' for c in s).split()
	return len(words)

print ("initializing markov engine...")
mc = MarkovChain("./markov")
print ("reading input file " + fp)
f = stringify_file(fp)
print ("generating markov database")
mc.generateDatabase(f)
print ("ready to generate strings.")
sd = False
s = ""
while True:
	if not sd:
		ts = mc.generateString()
	else:
		ts = mc.generateStringWithSeed(s)
	if countString(ts) >= msl:
		os.system("clear")
		print ("\n" + ts + "\n")
		sd = False
		s = raw_input("\npress enter to generate string. : ")
		if (len(s) > 0):
			sd = True

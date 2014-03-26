#! /usr/bin/env python

import os
import sys
from pymarkovchain import MarkovChain
import string

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
	msl = int(sys.argv[1])
except:
	msl = 0
	print "WARNING: no minimum sentence length specified, defaulting to zero"

def countString(s):
	words = ''.join(c if c.isalnum() else ' ' for c in s).split()
	return len(words)

print ("initializing markov engine...")
mc = MarkovChain("./markov")
f = ""
infile = open("texts.txt",'r')
for fp in infile:
	fp = fp[:-1]
	print ("reading input file " + fp)
	f += stringify_file(fp)

if raw_input("regen database: ").lower() == 'y':
	print ("generating markov database")
	mc.generateDatabase(f)
print ("ready to generate strings.")

def pgraph():
	while True:
		os.system("clear")
		iterations = int(raw_input("Iterations: "))
		seed = raw_input("Seed: ")
		if seed == '!q':
			return
		if (len(seed) == 0):
			sd = False
		else:
			if f.find(seed) != -1:
				sd = True
			else:
				raw_input('could not find "' + seed + '" in database\npress enter to continue')
				sd = False		
		c = 0
		final = ""
		while c < iterations:
			if sd:
				ts = mc.generateStringWithSeed(seed)
			else:
				ts = mc.generateString()
			if c == 0:
				final += ts.split(' ',1)[1]

			final += ts
			sd = True
			seed = ts.split()[-1]
			seed = seed.translate(string.maketrans("",""), string.punctuation)
			c += 1
		print ("\n" + final + "\n")
		raw_input("press enter to continue...")
if raw_input("press enter to begin.") == "beta":
	pgraph()

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
		if s == '!pg':
			pgraph()
		if (len(s) > 0):
			if f.find(s) != -1:
				sd = True
			else:
				raw_input('could not find "' + s + '" in database\npress enter to continue')
				sd = False

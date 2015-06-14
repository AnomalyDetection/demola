#! /usr/bin/python
'''
Randomly generate test data
'''
import random

file_good = '../data/good_log.txt'
file_ugly = '../data/ugly_log.txt'
good_set = []
ugly_set = []

fd_good = file( file_good, 'r' )
while True:
	line = fd_good.readline().strip()
	if len(line) == 0:
		break
	good_set.append( line )
fd_good.close()

fd_ugly = file( file_ugly, 'r' )
while True:
	line = fd_ugly.readline().strip()
	if len(line) == 0:
		break
	ugly_set.append( line )
fd_ugly.close()


random.shuffle( good_set )
random.shuffle( ugly_set )

for i in range( 0,30):
	print ugly_set[i]
for i in range( 0,30):
	print good_set[i]

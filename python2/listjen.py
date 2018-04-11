#!/usr/bin/python

import string
import sys

if len(sys.argv) != 2:
	sys.exit('Usage: ./%s <full_list_name>' % sys.argv[0])

alph = list(string.ascii_lowercase)
digs = list(string.digits)
symb = ['-', '_']
both = alph + digs
alls = alph + digs + symb
output = open(str(sys.argv[1]), 'w')

selected = alls

n = 0
for a in range(len(selected)):
	for b in range(len(selected)):
		for c in range(len(selected)):
			output.write(selected[a])
			output.write(selected[b])
			output.write(selected[c])
			output.write('\n')
			n += 1

sys.exit('[*] List Generated, ' + str(n) + ' Words Written.')

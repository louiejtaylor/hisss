#!/usr/bin/python

# Script to list (paired) samples in a target directory
# matching a particular pattern.

import os, sys

# TODO: grab using argparse

try:
	patt=sys.argv[2]
except IndexError:
	patt = "{sample}_pass_{rp}.fastq"

extension = patt.split('.')[-1]

fastqs = [f for f in os.listdir(sys.argv[1]) if f.endswith(extension)]

ids = set([i.split('_')[0] for i in fastqs])

for i in ids:
	print "  "+ i + ": ['"+patt.replace("{sample}", i).replace("{rp}", '1')+"', '" +patt.replace("{sample}", i).replace("{rp}", '2')+"']"


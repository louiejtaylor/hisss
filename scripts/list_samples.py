#!/usr/bin/python2

# Script to list (paired) samples in a target directory
# matching a particular pattern.

import os, argparse, re

# Set up parser
parser = argparse.ArgumentParser(description='List samples to be added to viruSnake config file.')
parser.add_argument('dir', type=str, help='data directory')
parser.add_argument('-pattern', dest="pattern", default="DEFAULT", type=str, help='pattern for constant parts of sample names, like {sample}_{rp}.fastq for paired or {sample}.fastq for unpaired')
parser.add_argument('--unpaired', dest="paired", default=True, const=False, action="store_const", help="unpaired reads")

#parser.add_argument('format', metavar='f', default="fastq.gz", type=str, help="file format") # can I assume this from the pattern?

args = parser.parse_args()

# Set default patterns, error check user-input
if args.pattern == "DEFAULT":
	if args.paired:
		pattern = "{sample}_{rp}.fastq"
	else:
		pattern = "{sample}.fastq.gz"
else:
	pattern = args.pattern
	if args.paired:
		if (not "{sample}" in pattern) | (not "{rp}" in pattern):
			raise Exception("Paired read pattern must contain both '{sample}' and '{rp}'")
	else:
		if "{rp}" in pattern:
			raise Exception("Unpaired read pattern must not contain '{rp}'")
		if not "{sample}" in pattern:
			raise Exception("Unpaired read pattern must contain '{sample}'")

extension = pattern.split('.')[-1]
re_pattern = pattern.replace("{sample}", "(.+)").replace("{rp}","[12]")

# Find samples and build sample list
files = [f for f in os.listdir(args.dir) if f.endswith(extension)]
ids = list(set([g.group(1) for g in [re.search(re_pattern, f) for f in files] if g]))

if len(ids)==0:
	raise Exception("No samples detected with pattern: "+pattern)

for i in ids:
	if args.paired:
		print "  "+ i + ": ['"+pattern.replace("{sample}", i).replace("{rp}", '1')+"', '" +pattern.replace("{sample}", i).replace("{rp}", '2')+"']"
	else:
		print "  "+ i + ": '"+pattern.replace("{sample}", i)+"'"

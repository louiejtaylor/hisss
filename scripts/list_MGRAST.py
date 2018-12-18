#!/bin/python

# Script to generate sample and metadata sections of config file
# given an SRA project ID.

from __future__ import print_function
import requests, argparse, sys, subprocess, io

# Set up parser
parser = argparse.ArgumentParser(description='Add samples and metadata to hisss config file from SRA project ID.')
parser.add_argument('ids', type=str, nargs='+', help='MG-RAST project or sample IDs')
#TODO: add ability for user to specify other metadata columns from SRA .csv they want
args = parser.parse_args()

# List samples
cmd_args = ["grabseqs", "mgrast", "-l"] + args.ids
result = subprocess.run(cmd_args, stdout=subprocess.PIPE, check=True)
f = io.StringIO(result.stdout.decode("ASCII"))
info = {'Run':[], 'LibraryLayout':[]}

for j in f.read().split('\n'):
	if len(j.strip()) > 0:
		i = j.split(',')
		if len(i) == 2:
			info['LibraryLayout'].append("paired")
			info['Run'].append(i[0].split('_1.fastq.gz')[0])
		elif len(i) == 1:
			info['LibraryLayout'].append("unpaired")
			info['Run'].append(i[0].split('.fastq.gz')[0])


# Output in config format
p_chunk,up_chunk=["study_metadata:\n  repo: 'mgrast'\n"]*2

for k in info.keys():
	if k != "Run":
		if k != "LibraryLayout":
			p_chunk += "  "+str(k)+": "+str(list(set(info[k]))) + '\n'
			up_chunk += "  "+str(k)+": "+str(list(set(info[k]))) + '\n'
		else:
			p_chunk += "  paired: True\n"
			up_chunk += "  paired: False\n"

			if len(list(set(info[k]))) == 2:
				sys.stderr.write("WARNING: Dataset contains both paired and unpaired, outputting both in separate config chunks\n\n")

p_chunk += "\nsamples:\n"
up_chunk += "\nsamples:\n"

for i in range(len(info["Run"])):
	sample = info["Run"][i]
	if info["LibraryLayout"][i] == "PAIRED":
		p_chunk += "  "+sample+": ['"+sample+"_1','"+sample+"_2']\n"
	else:
		up_chunk += "  "+sample+": '"+sample+"'\n"

if not p_chunk.strip().endswith(":"):
	print(p_chunk)
if not up_chunk.strip().endswith(":"):
	print(up_chunk)

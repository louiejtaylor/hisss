#!/bin/python

# Script to generate sample and metadata sections of config file
# given an SRA project ID.

from __future__ import print_function
import requests, argparse, sys

# Set up parser
parser = argparse.ArgumentParser(description='Add samples and metadata to hisss config file from SRA project ID.')
parser.add_argument('id', type=str, help='SRA project ID')
#TODO: add ability for user to specify other metadata columns from SRA .csv they want
args = parser.parse_args()

# Grab sample summary
csv = requests.get("http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term="+args.id)
f = open(args.id+".csv","w")
f.write(csv.text)
f.close()

# Grab sample info
lines = [l.split(',') for l in csv.text.split("\n")]# if "AMPLICON" not in l]
info = {"Run":[],"LibraryLayout":[], "ScientificName":[], "Study_Pubmed_id":[], "SampleType":[], "Body_Site":[]}
info_locs = {"Run":lines[0].index("Run"), "LibraryLayout":lines[0].index("LibraryLayout"), "ScientificName":lines[0].index("ScientificName"), "Study_Pubmed_id":lines[0].index("Study_Pubmed_id"), "SampleType":lines[0].index("SampleType"), "Body_Site":lines[0].index("Body_Site")}
# TODO: can simplify above

# Parse sample summary
for line in lines[1:]:
	if len(line) > 1:
		for k in info_locs.keys():
			info[k].append(line[info_locs[k]])

# Output in config format
p_chunk,up_chunk=["study_metadata:\n  repo: 'sra'\n"]*2

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

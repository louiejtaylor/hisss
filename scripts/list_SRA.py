#!/bin/python3

# Script to generate sample and metadata sections of config file
# given an SRA project ID.

from __future__ import print_function
import requests, argparse

# Set up parser
parser = argparse.ArgumentParser(description='Add samples and metadata to hisss config file from SRA project ID.')
parser.add_argument('id', type=str, help='SRA project ID')
#TODO: add ability for user to specify other metadata columns from SRA .csv they want
args = parser.parse_args()

# Grab sample summary
csv = requests.get("http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term="+args.id)
lines = [l.split(',') for l in csv.text.split("\n")]
info = {"Run":[], "ScientificName":[], "Study_Pubmed_id":[], "SampleType":[], "Body_Site":[]}
info_locs = {"Run":lines[0].index("Run"), "ScientificName":lines[0].index("ScientificName"), "Study_Pubmed_id":lines[0].index("Study_Pubmed_id"), "SampleType":lines[0].index("SampleType"), "Body_Site":lines[0].index("Body_Site")}
# TODO: can simplify above

# Parse sample summary
for line in lines[1:]:
	if len(line) > 1:
		for k in info_locs.keys():
			info[k].append(line[info_locs[k]])

# Output in config format
print("study_metadata:")
for k in info.keys():
	if k != "Run":
		print("  "+str(k)+": "+str(list(set(info[k]))))

print("\nsamples:")
for sample in info["Run"]:
	print("  "+sample+": ['"+sample+"_1','"+sample+"_2']")
#TODO: parse unpaired or paired from metadata

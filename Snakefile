# Snakemake workflow ot align reads to one or more 
# genomic sequences and produce useful outputs including 
# coverage maps and summary tables.
#
# See the README.md for more information.
#
# Authors: Louis Taylor and Arwa Abbas

#from collections import OrderedDict

#def get_sample_urls():
#	return OrderedDict({"testA-1":"https://github.com/louiejtaylor/viruSnake/blob/master/test_data/fastq/gz/testA_1.fastq.gz?raw=true", "testA-2":"https://github.com/louiejtaylor/viruSnake/blob/master/test_data/fastq/gz/testA_2.fastq.gz?raw=true"})

# Setup
OUTPUT_DIR = str(config["io"]["output"])
LOCAL_DATA_DIR = str(config["io"]["data"])
TARGETS = str(config["align"]["targets"])
DATA_DIR = str(config["io"]["output"]+"/download")

if config["io"]["download"] == False:
	include: "rules/local_data.rules"


#print(type(config["samples"]))
#print(config["samples"])

# Rules

include: "rules/download.rules"

if config["io"]["paired"] == True:
	include: "rules/align_paired.rules"
else:
	include: "rules/align_single.rules"

include: "rules/summary.rules"

include: "rules/plot.rules"

rule all:
	input:
		rules.all_summary.output,
		rules.all_plot.output


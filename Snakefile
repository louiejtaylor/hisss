# Snakemake workflow to align reads to one or more 
# genomic sequences and produce useful outputs including 
# coverage maps and summary tables.
#
# See the README.md for more information.
#
# Authors: Louis Taylor and Arwa Abbas

# Setup
OUTPUT_DIR = str(config["io"]["output"])
LOCAL_DATA_DIR = str(config["io"]["data"])
TARGETS = str(config["align"]["targets"])
DATA_DIR = str(config["io"]["output"]+"/download")

# Rules
if config["io"]["download"] == False:
	include: "rules/local_data.rules"
else:
	include: "rules/download.rules"

if config["io"]["paired"] == True:
	include: "rules/align_paired.rules"
else:
	include: "rules/align_single.rules"

include: "rules/summary.rules"

include: "rules/plot.rules"

rule all:
	input:
		rules.all_sample_summary.output,
		rules.all_summary.output,
		rules.all_plot.output


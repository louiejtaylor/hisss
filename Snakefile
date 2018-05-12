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

un = not config["io"]["paired"]

if config["io"]["download"] == False:
	include: "rules/local_data_"+ un*"un"+"paired.rules"
else:
	include: "rules/download.rules"

include: "rules/align_"+un*"un"+"paired.rules"

include: "rules/process_alignment.rules"

include: "rules/summary.rules"

include: "rules/plot.rules"

rule all:
	input:
		rules.all_sample_summary.output,
		rules.all_summary.output,
		rules.all_plot.output


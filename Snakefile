# Snakemake workflow ot align reads to one or more 
# genomic sequences and produce useful outputs including 
# coverage maps and summary tables.
#
# See the README.md for more information.
#
# Authors: Louis Taylor and Arwa Abbas


# Setup
OUTPUT_DIR = str(config["dirs"]["output"])
DATA_DIR = str(config["dirs"]["data"])
TARGETS = str(config["dirs"]["targets"])

# Rules

#include: "rules/download.rules"

include: "rules/align.rules"

include: "rules/summary.rules"

rule all:
	input:
		rules.all_summary.output


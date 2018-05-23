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

un = "un"*int(not config["io"]["paired"]) # use paired or unpaired rule versions

try:
	if config["study_metadata"]["sra"] == True:
		# trust SRA metadata over user
		un = "un"*int(not config["study_metadata"]["paired"])
		include: "rules/sra_" + un + "paired.rules"
		print("using " + un + "paired data from SRA")
except KeyError:
	DATA_DIR = LOCAL_DATA_DIR
	print("using local " + un + "paired data")

include: "rules/align_" + un + "paired.rules"

include: "rules/process_alignment.rules"

include: "rules/summary.rules"

include: "rules/plot.rules"

rule all:
	input:
		rules.all_summary.output,
		rules.all_plot.output


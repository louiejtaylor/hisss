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

un = "un"*int(not config["io"]["paired"])

if config["io"]["download"] == False:
	include: "rules/local_data_"+ un +"paired.rules"
else:
	try:
		if config["study_metadata"]["sra"] == True:
			include: "rules/sra.rules"
	except KeyError:
		include: "rules/download_"+ un +"paired.rules"

include: "rules/align_"+ un +"paired.rules"

include: "rules/process_alignment.rules"

include: "rules/summary.rules"

include: "rules/plot.rules"

rule all:
	input:
		rules.all_sample_summary.output,
		rules.all_summary.output,
		rules.all_plot.output


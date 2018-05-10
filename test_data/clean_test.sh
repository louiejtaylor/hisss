#!/bin/bash

# script to clean up test output
# for safety, will only run when called from a dir named "test_data"

wd=`pwd`
cur_dir=${wd##/*/}

if [ "$cur_dir" != "test_data" ]; then
	echo "current dir is '${cur_dir}' not 'test_data', exiting"
	exit 1
fi
echo "in '${cur_dir}', attempting to remove indices and output directory"

rm -r output
rm genomes/pcv.fasta.*

echo "done"

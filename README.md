# viruSnake
A snakemake workflow to download/align reads to targets and produce useful outputs. 

Getting it up and running is hopefully simple (maybe there'll be an install script to handle this later):

    git clone https://github.com/louiejtaylor/viruSnake
    cd viruSnake
    
We use conda to handle dependencies, you can install miniconda from [here](https://conda.io/miniconda.html). Make a new conda enviroment, then install dependencies from `requirements.txt` like so:
    
    conda create -n viruSnake
    source activate viruSnake
    conda install -c bioconda -c conda-forge --file requirements.txt 
    
To run, all you need is a config file to point Snakemake to your data and targets (see `test_data/test_config.yml for an example`), then run in the viruSnake root dir:

    snakemake -p --configfile [your_config.yml] all

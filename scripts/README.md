# Using hisss to download reads from SRA

Thesea are streamlined instructions to use hisss just for downloading sequences from the SRA. This assumes you've already completed the [installation steps](https://github.com/louiejtaylor/hisss/blob/master/README.md) for hisss and have a config file (although setting the alignment target in the config isn't necessary).

First, if you aren't already, make sure you're in the hisss conda environment with `source activate hisss`. Then, use `list_SRA.py` to add the study's samples to your config file:

    python hisss/scripts/list_SRA.py SRP####### >> my_config.yml

Here, `SRP######` is the SRA project ID, but you can pass a lot of different things here, including BioProject (`PRJ######`), datasets mirrored from the ENA (usually look something like `ERA######`), and a bunch of other random accession number types that I've seen listed in papers that all seem to work (to my extreme surprise).

After this command, you should see a bit of metadata as well as properly formatted samples appended to `my_config.yml`. `list_SRA.py` will automatically determine the paired or unpairedness of the samples from the SRA metadata. In the case that there are both paired and unpaired samples in the project, you should see a warning that multiple formats were output--here it's usually easiest to make two config files (i.e. `my_config_paired.yml` and `my_config_single.yml`) and do two separate hisss runs.

Finally, the downloading should be super easy, just run this in the hisss directory: 

    snakemake -p --restart-times 5 --notemp --configfile [path/to/my_config.yml] download_only

The `restart-times` option is absoulutely crucial, since SRA downloads seem to fail every so often but will succeed if you try again. The `notemp` option keeps reads around, since hisss usually removes all read and alignment files to stay lightweight. Finally, specifying `download_only` as the target rule ensures that hisss goes only as far as downloading the reads.

There are many more useful options that you could pass to snakemake that are beyond the scope of this tutorial. Read more about them [here](http://snakemake.readthedocs.io/en/stable/executable.html)! Feel free to [open an issue](https://github.com/louiejtaylor/hisss/issues) or tweet [@Louviridae](https://twitter.com/Louviridae) or [@A2_Insanity](https://twitter.com/A2_Insanity). Good luck!


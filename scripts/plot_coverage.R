#!/usr/bin/Rscript

#This script visualizes output from samtools depth
#It requires input in csv format and a filename for the PDF.


#Import libraries
library(methods)
library(ggplot2)
library(magrittr)
library(reshape2)

#Set up argument parser and QC-------------------------------------------------
args <- commandArgs()

#print(args)
cov <- args[6]
output <-args[7]

if(!file_test("-f", cov)) 
{
  stop("Coverage file not defined.")
}

if(is.na(output)) 
{
  stop("Output file not defined.")
}

#Convert to a dataframe if a positive hit--------------------------------------
cov_df <- if(!file.size(cov) == 0){
      read.table(cov, sep = "\t")
}

colnames(cov_df) <- c("AlignTarget", "Position", "Count")

#Exit quietly if dataframe doesn't exit?


#Coverage Maps-----------------------------------------------------------------

##Function for creating plots.
plot_nuc_cov <- function(cov_df) {
  p.list <- lapply(sort(unique(cov_df$AlignTarget)), function(i) {
    ggplot(cov_df[cov_df$AlignTarget==i,], 
           aes(x = Position, 
               y = Count), fill = "grey") +
    geom_col() +
    facet_wrap(~AlignTarget, scales = "free", ncol = 1) +
    ggtitle(NULL) +
    xlab("Position") + 
    ylab("Coverage") +
    theme_bw(base_size = 14) + 
    theme(panel.grid.major = element_blank(),
          panel.grid.minor.x = element_blank(),
          panel.spacing = unit(1.2, "lines"),
          strip.background = element_rect(colour="black", fill="white"),
          legend.position="right",
          axis.text.x = element_text(size = rel(0.7)))
  })
  
  return(p.list)
}


#Plot alignments---------------------------------------------------------------
plots <- plot_nuc_cov(cov_df)
pdf(output, onefile = TRUE)
invisible(lapply(plots, print))
dev.off()


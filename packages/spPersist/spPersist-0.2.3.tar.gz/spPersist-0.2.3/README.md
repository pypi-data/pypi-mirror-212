# Spatial Transcriptomics with Persistent Homology

This is a package for classifying Spatial Transcriptomics data according to its 
spatial topology. The specific mathematical foundation for the classification is
the theory of Persistent Homology and its homology barcodes. The package so far
contains a data processing module, called dp, allowing users to load either the
standard datasets from Visium and MERFISH, or published datasets into desired
annotated data format for the analysis performed in this package. The format is
compatible with the package Squidpy.

It is intended that the package will also include a pre-processing module, a 
persistent homology module and a homological classification module, respectively
named pp, ph and hc.
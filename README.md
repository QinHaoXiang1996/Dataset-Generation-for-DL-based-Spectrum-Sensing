# Dataset Generation for DL based Spectrum Sensing
*Source code for dataset generation of paper "Spectrum Sensing in Cognitive Radio: A Deep Learning Based Model"

*Our dataset generation source code is based on the method in Paper "T. O’Shea and N. West, Radio machine learning dataset generation with gnu radio, in Proc. GNU Radio Conference (GRCon16), vol. 1, 2016." (https://github.com/radioML/dataset).

*dataset_generation.py is the main program for dataset generation

*source_material, analyze_stats.py, source_alphabet.py, timeseries_slicer.py and transmitters.py are provided by T. O’Shea and N. West.

*For source_material, T. O’Shea and N. West gave the following description in their paper above: for digital modulations, we use the entire Gutenberg works of Shakespeare in ASCII, with whitening randomizers applied to ensure equiprobable symbols and bits. All of our modems then use these two data sources with the corresponding digital or analog data source.

*analyze_stats.py, source_alphabet.py, timeseries_slicer.py and transmitters.py are used for signal simulation, which are described in detail in "T. O’Shea and N. West, Radio machine learning dataset generation with gnu radio, in Proc. GNU Radio Conference (GRCon16), vol. 1, 2016."
## How to generate Figure 9

1. Make sure the Python packages `pandas` and `matplotlib` are installed

2. Download and unzip the dataset *(see Artifact Appendix for download links)* into `./data/applet` and `./data/service` directories respectively

3. Run the Python scripts:

```
$ python3 trigger_level_analyze.py [type]
$ python3 trigger_level_plot.py
```
The second script will generate a `fig_9.pdf` file to reproduce Figure 9 in the paper. 
Set `type` to `all` to generate the left subplot, or set `type` to `filter` to generate the right subplot.
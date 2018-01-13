#
# Script to create a clustered heatmap of viral coverage of metagenomes.
#
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def draw_heatmap(fpath):
	
	# Read data text file into dataframe
	df = pd.read_csv(fpath, sep="\t", header=0, index_col=0)
	dims = df.shape
	df.drop(df.columns[(dims[1]-1)],axis=1,inplace=True)
	
	# Create a clustered heatmap showing viral composition of the metagenomes
	clustmap = sns.clustermap(df, cmap="mako", robust=True, col_cluster=False, )
	clustmap.savefig('clustered_heatmap.png')

	return



if __name__ == "__main__":

	ap = argparse.ArgumentParser(description = 'Clustered Heatmap Visualization')
	ap.add_argument("file", help="Filepath to combined results file")
	args = ap.parse_args()

	draw_heatmap(args.file)





from os import listdir
import argparse


def combine_virusfriends_results(dirpath):
	read_mapping_hash = {}
	all_org_ids = []
	all_sra_ids = []
	for file in listdir(dirpath):
		sra_id = file[:-4]
		all_sra_ids.append(sra_id)
		read_mapping_hash[sra_id] = {}
		with open(dirpath + "/" + file, 'r') as fin:
			for i, line in enumerate(fin):
				if i == 0:
					continue
				org_id = line.strip().split("\t")[0]
				mapped_reads = line.strip().split("\t")[2]
				if org_id not in all_org_ids:
					all_org_ids.append(org_id)
				read_mapping_hash[sra_id][org_id] = mapped_reads

	with open("combined_results.txt", "w") as fout:
		fout.write("SRA_ID\t")
		for org in all_org_ids:
			fout.write(org + "\t")
		fout.write("\n")
		for sra_id in all_sra_ids:
			fout.write(sra_id + "\t")
			for org_id in all_org_ids:
				if org_id in read_mapping_hash[sra_id].keys():
					fout.write(read_mapping_hash[sra_id][org_id] + "\t")
				else:
					fout.write("0\t")
			fout.write("\n")

	return





if __name__ == "__main__":

	ap = argparse.ArgumentParser(description = "Combining output files from samstats.py")
	ap.add_argument("dirpath", help="Filepath to the directory of output files from samstats.py")
	args = ap.parse_args()

	combine_virusfriends_results(args.dirpath)



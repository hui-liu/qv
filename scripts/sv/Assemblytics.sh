# $1: delta file
# $2: sample
#Assemblytics delta output_prefix unique_length_required min_size max_size
# https://www.nature.com/articles/s41586-022-04822-x#Sec8
source ~/.bash_conda
conda activate py27

Assemblytics $1 $2 10000 50 10000000


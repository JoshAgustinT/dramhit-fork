
# nohup ./collect.sh large single-local 32 &


python parse.py output.txt

python plot.py thesis_data_with_mlc.csv


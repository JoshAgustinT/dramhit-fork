
# nohup ./runner.sh &

./collect.sh large single-local 32

python parse.py output-all.txt

python plot.py thesis_data_with_mlc.csv
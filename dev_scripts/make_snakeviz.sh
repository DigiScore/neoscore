# Requires snakeviz https://jiffyclub.github.io/snakeviz/

set -o xtrace
mkdir tmp
python3 -m cProfile -o tmp/out.prof examples/kitchen_sink.py --image
python3 -m snakeviz --server tmp/out.prof
rm -r tmp

# Requires snakeviz https://jiffyclub.github.io/snakeviz/

set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.prof examples/kitchen_sink.py --image
snakeviz --server tmp/out.prof
rm -r tmp

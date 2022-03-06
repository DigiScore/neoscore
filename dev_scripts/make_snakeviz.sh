# Requires snakeviz https://jiffyclub.github.io/snakeviz/

set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.prof vtests/vtest.py --image
snakeviz --server tmp/out.prof
rm -r tmp

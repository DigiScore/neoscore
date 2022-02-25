# Requires snakeviz https://jiffyclub.github.io/snakeviz/

set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.prof vtests/goldberg.py --image
snakeviz tmp/out.prof
rm -r tmp

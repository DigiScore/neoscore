set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.pstats vtests/vtest.py
gprof2dot -f pstats tmp/out.pstats | dot -Tpng -o tmp/graph.png
eog tmp/graph.png
rm -r tmp

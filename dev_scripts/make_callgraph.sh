# Requires gprof2dot https://github.com/jrfonseca/gprof2dot
# Also uses Eye of Gnome (eog) as an image viewer

set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.pstats vtests/vtest.py --image
gprof2dot -f pstats tmp/out.pstats | dot -Tpng -o tmp/graph.png
eog tmp/graph.png
rm -r tmp

# Requires gprof2dot https://github.com/jrfonseca/gprof2dot
# Also uses Eye of Gnome (eog) as an image viewer

Help() {
    echo "Generate and display a vtest.py callgraph"
    echo
    echo "Usage: sh dev_scripts/make_callgraph.sh [root_func]"
    echo
    echo "If [root_func] is passed, the graph will be pruned to that root"
    echo "e.g. sh dev_scripts/make_callgraph.sh modulename:123:funcname"
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done

set -o xtrace
mkdir tmp
python -m cProfile -o tmp/out.pstats vtests/vtest.py --image
gprof2dot -f pstats --root="$1" tmp/out.pstats | dot -Tpng -o tmp/graph.png
eog tmp/graph.png
rm -r tmp

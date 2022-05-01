set +x
export PYTHONPROFILEIMPORTTIME=1
python examples/kitchen_sink.py --image 2>&1 | less

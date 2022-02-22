set +x
export PYTHONPROFILEIMPORTTIME=1
python vtests/vtest.py --image 2>&1 | less

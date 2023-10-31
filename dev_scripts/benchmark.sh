# Benchmark the example with https://github.com/sharkdp/hyperfine

hyperfine --show-output --export-csv benchmark_results.csv 'python3 examples/kitchen_sink.py --image'

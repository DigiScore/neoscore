# Benchmark the example with https://github.com/sharkdp/hyperfine

hyperfine --show-output --export-csv benchmark_results_sink.csv 'python3 examples/kitchen_sink.py --image'
hyperfine --show-output --export-csv benchmark_results_circle.csv 'python3 examples/circle.py --image'

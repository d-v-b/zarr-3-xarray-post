zarr_version := '3'
log_path := "results/results.csv"
concurrency := '10' 
bench_script := 'bench/era_5_bench_zarr' + zarr_version + '.py'

setup_log:
    echo 'time,zarr_version,concurrency_limit' > {{log_path}}

run-bench:
    for i in {0..8}; do uv run {{bench_script}} --concurrency-limit {{concurrency}} >> {{log_path}}; done
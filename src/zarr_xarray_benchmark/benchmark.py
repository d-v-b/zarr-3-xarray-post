import subprocess
import click
from pathlib import Path

era5_url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'

@click.command()
@click.option('--data-url', default=era5_url)
@click.option('--output-csv', required=True)
@click.option('--reps', default='8')
def run_benchmark_cli(data_url: str, output_csv: str, reps: str):
    reps_parsed = int(reps)
    csv_header = 'time,zarr_version,concurrency_limit\n'
    results = []
    # v2 benchmark
    for rep in range(reps_parsed):
        res = run_benchmark_v2(data_url)
        results.append({'time': res, 'zarr_version': '2.0.0', 'concurrency_limit': None})
    # v3 benchmark
    for concurrency_limit in [1, 10, 100, 200]:
        for rep in range(reps_parsed):
            res = run_benchmark_v3(data_url, concurrency_limit)
            results.append({'time': res, 'zarr_version': '3.0.1', 'concurrency_limit': concurrency_limit})

    
    Path(output_csv).write_text(csv_header + '\n'.join([f'{r["time"]},{r["zarr_version"]},{r["concurrency_limit"]}' for r in results]))

def run_benchmark_v3(data_url: str, concurrency_limit: int) -> float:
    proc = subprocess.Popen([
        'uv', 
        'run', 
        'bench/open_dataset_zarr3.py', 
        '--url', 
        data_url, 
        '--concurrency-limit', 
        str(concurrency_limit)],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True)
    duration, _ = proc.communicate()
    return float(duration)

def run_benchmark_v2(data_url: str) -> float:
    proc = subprocess.Popen([
        'uv', 
        'run', 
        'bench/open_dataset_zarr2.py', 
        '--url', 
        data_url],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True)
    duration, _ = proc.communicate()
    return float(duration)

if __name__ == '__main__':
    run_benchmark_cli()
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
    csv_header = 'time,zarr_version,xarray_version,concurrency_limit\n'
    results = []
    # v2 benchmark
    for _ in range(reps_parsed):
        dur, zv, xv = run_benchmark_v2(data_url)
        results.append({
            'time': dur, 
            'zarr_version': zv, 
            'xarray_version': xv, 
            'concurrency_limit': None
            })
        # v3 benchmark with old xarray
        dur, zv, xv = run_benchmark_v3(
            'bench/open_dataset_zarr3_old_xarray.py', 
            data_url, 
            100)
        results.append(
            {
                'time': dur, 
                'zarr_version': zv, 
                'xarray_version': xv,
                'concurrency_limit': 100
            })
    # v3 benchmark with latest xarray
    for concurrency_limit in [1, 10, 100, 200]:
        for _ in range(reps_parsed):
            dur, zv, xv = run_benchmark_v3(
                'bench/open_dataset_zarr3.py', 
                data_url, 
                concurrency_limit)
            results.append(
                {
                    'time': dur, 
                    'zarr_version': zv, 
                    'xarray_version': xv,
                    'concurrency_limit': concurrency_limit
                })

    Path(output_csv).write_text(csv_header + '\n'.join([f'{r["time"]},{r["zarr_version"]},{r["xarray_version"]},{r["concurrency_limit"]}' for r in results]))

def run_benchmark_v3(script_path: str, data_url: str, concurrency_limit: int) -> tuple[float,str,str]:
    proc = subprocess.Popen([
        'uv', 
        'run', 
        script_path, 
        '--url', 
        data_url, 
        '--concurrency-limit', 
        str(concurrency_limit)],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True)
    results, _ = proc.communicate()
    dur_str, zarr_version, xarray_version = results.rstrip('\n').split(',')
    return float(dur_str), zarr_version, xarray_version

def run_benchmark_v2(data_url: str) -> tuple[float,str,str]:
    proc = subprocess.Popen([
        'uv', 
        'run', 
        'bench/open_dataset_zarr2.py', 
        '--url', 
        data_url],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True)
    results, _ = proc.communicate()
    dur_str, zarr_version, xarray_version = results.rstrip('\n').split(',')
    return float(dur_str), zarr_version, xarray_version
if __name__ == '__main__':
    run_benchmark_cli()
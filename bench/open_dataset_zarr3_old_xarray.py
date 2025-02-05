# /// script
# dependencies = [
#     "fsspec",
#     "gcsfs@git+https://github.com/fsspec/gcsfs.git#egg=gcsfs",
#     "zarr==3.0.1",
#     "xarray==2024.11.0",
#     "click"
# ]
# ///

import click
import xarray
import time
import zarr

def benchmark(url: str, concurrency_limit: int):
	start = time.time()
	with zarr.config.set({'async.concurrency': concurrency_limit}):
		xarray.open_dataset(
			url,     
			engine='zarr',     
			consolidated=False,     
			storage_options = {'token': 'anon'})
	return time.time() - start

@click.command()
@click.option('--url', required=True)
@click.option('--concurrency-limit', default=None)
def run_cli(url: str, concurrency_limit: int | None):
	if concurrency_limit is None:
		concurrency_limit_parsed = zarr.config.get('async.concurrency')
	else:
		concurrency_limit_parsed = int(concurrency_limit)
	result = benchmark(url, concurrency_limit=concurrency_limit_parsed)
	zarr_version = zarr.__version__
	xarray_version = xarray.__version__
	click.echo(f'{result:0.2f},{zarr_version},{xarray_version}')

if __name__ == '__main__':
	run_cli()
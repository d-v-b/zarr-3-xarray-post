# /// script
# dependencies = [
#     "fsspec",
#     "gcsfs@git+https://github.com/fsspec/gcsfs.git#egg=gcsfs",
#     "zarr==2.18",
#     "xarray==2025.01.1",
#     "click"
# ]
# ///
import click
import xarray
import time

import click
import xarray
import time
import zarr

def benchmark(url: str):
	start = time.time()
	xarray.open_dataset(
		url,     
		engine='zarr',     
		consolidated=False,     
		storage_options = {'token': 'anon'})
	return time.time() - start

@click.command()
@click.option('--url', required=True)
def run_cli(url: str):
	result = benchmark(url)
	zarr_version = zarr.__version__
	xarray_version = xarray.__version__
	click.echo(f'{result:0.2f},{zarr_version},{xarray_version}')

if __name__ == '__main__':
	run_cli()
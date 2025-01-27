# /// script
# dependencies = [
#   "fsspec[gcs]",
#   "zarr==2.18",
#   "click",
# ]
# ///
import zarr
from zarr import open_group
from time import time
import json
n_reps = 8
import click
import timeit
url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'
@click.command()
@click.option('--concurrency-limit', default=None)
def test_list_members_cli(concurrency_limit: int | None):
    concurrency_limit = 0
    result = timeit.timeit("test_list_members(url)", setup="from __main__ import test_list_members", globals={'url': url}, number=1)
    click.echo(f'{result},{zarr.__version__},{concurrency_limit}'),

def test_list_members(url: str) -> None:
    z = open_group(
        url, 
        mode='r',
        storage_options = {'token': 'anon', 'use_listings_cache': False})
    t = time()
    members = tuple(z.items())
    return time() - t

if __name__ == '__main__':
    test_list_members_cli()
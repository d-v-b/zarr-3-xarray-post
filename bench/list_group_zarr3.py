# /// script
# dependencies = [
#   "fsspec[gcs]",
#   "zarr==3.0.0",
#   "click"
# ]
# ///

import zarr
from zarr import open_group
from time import time
import click
import timeit

url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'
@click.command()
@click.option('--concurrency-limit', default=None)
def test_list_members_cli(concurrency_limit: int | None):
    if concurrency_limit is None:
        _concurrency_limit = zarr.config.get('async.concurrency')
    else:
        _concurrency_limit = int(concurrency_limit)
    result = timeit.timeit(f"test_list_members(url, _concurrency_limit)", setup="from __main__ import test_list_members", globals={'url': url, '_concurrency_limit': _concurrency_limit}, number=1)
    click.echo(f'{result},{zarr.__version__},{_concurrency_limit}')

def test_list_members(url: str, concurrency_limit: int) -> None:
    z = open_group(
        url, 
        mode='r',
        storage_options = {'token': 'anon'},
        use_consolidated = False)
    t = time()
    with zarr.config.set({'async.concurrency': concurrency_limit}):
        members = tuple(z.members())
    return time() - t

if __name__ == '__main__':
    test_list_members_cli()
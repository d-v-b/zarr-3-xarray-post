# /// script
# dependencies = [
#   "fsspec[gcs]",
#   "click",
#   "rich"
# ]
# ///
import timeit
import click
from gcsfs import GCSFileSystem
import rich
url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'

@click.command()
def test_list_prefix_time_cli():
    result = timeit.timeit("test_list_prefix_time(url)", setup="from __main__ import test_list_prefix_time", globals={'url': url}, number=1)
    click.echo(f'{result}')

def test_list_prefix_time(url):    
    fs = GCSFileSystem(token='anon')
    _ = fs.ls(url)

if __name__ == '__main__':
    test_list_prefix_time_cli()
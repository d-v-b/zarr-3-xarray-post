# /// script
# dependencies = [
#     "fsspec",
#     "gcsfs@git+https://github.com/fsspec/gcsfs.git#egg=gcsfs",
#     "zarr==2.18",
#     "xarray==2025.01.1",
# ]
# ///
import xarray
import time

url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'
start = time.time()
xarray.open_dataset(
	url,     
	engine='zarr',     
	consolidated=False,     
	storage_options = {'token': 'anon'})

print(f'elapsed:  {time.time() - start:0.2f} seconds')
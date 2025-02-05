# About
This is a collection of python scripts for benchmarking the `Xarray.open_dataset` function with different versions of `zarr-python`.

# Usage

## Installation

`git clone https://github.com/d-v-b/zarr-3-xarray-post.git`

## Dependencies

- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

## Generating benchmark results
```bash
uv run src/zarr_xarray_benchmark/benchmark.py --output-csv results/results.csv --reps 8
```
This will run the main benchmarking script. Each condition will be tested `reps` times (e.g., 8 in the above example)

## Visualizing benchmark results
```bash
uv run src/zarr_xarray_benchmark/plot.py --data results/results.csv --output plot.png
```

This will generate a plot of the results, and save it to the file called `plot.png`.
from matplotlib import pyplot as plt
import click
import polars as pl
import numpy as np 

@click.command()
@click.option('--data', required=True)
@click.option('--output', required=True)
def plot_cli(data: str, output: str):
    df = pl.read_csv(data)
    fig = plot(df)
    fig.savefig(output)


url = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'

def plot(df: pl.DataFrame):
    fig, axs = plt.subplots(dpi=200, figsize=(8, 6))
    axs.set_title("Time required to open the ARCO ERA5 dataset in Xarray")
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.yaxis.set_label_text('Time (s)')
    gb = df.group_by(
        pl.col('zarr_version'), 
        pl.col('concurrency_limit'))
    num_plots = len(df.unique(['zarr_version', 'concurrency_limit']))
    order = gb.agg(
        pl.min('time')
        ).with_columns(
            pl.col('concurrency_limit').replace('None', 0)
            ).sort(by='concurrency_limit')
    spread = (-0.05, 0.05)
    xticks = list(range(num_plots))
    xlabels = []
    for row in order.iter_rows(named=True):
        if row['zarr_version'].startswith('2'):
            label = (f'Zarr Python = {row["zarr_version"]}')
        else:
            label = (f'Zarr Python = {row["zarr_version"]}\nconcurrency limit = {row["concurrency_limit"]}')
        xlabels.append(label)
    axs.set_xticks(xticks, labels=xlabels)

    for _, data in gb:
        vals = data['time'].to_numpy()
        idx = order['time'].to_list().index(vals.min())
        axs.plot(
            [idx + 1.5 * spread[0], idx + 1.5 * spread[-1]], 
            [vals.mean()] * 2, 
            color=(.4,.4,.4), 
            linestyle='dotted')
        axs.plot(
            np.random.uniform(idx + spread[0], idx + spread[1], len(vals)), 
            vals, 
            markersize=6, 
            linestyle='None', 
            color='salmon', 
            marker='o', 
            markerfacecolor='none')
        axs.text(
            idx + 2.5 * spread[1], 
            vals.mean(), 
            f'Mean: {vals.mean():0.2f} s', 
            verticalalignment='center', 
            horizontalalignment='left')
    plt.xticks(rotation=15)
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    plot_cli()
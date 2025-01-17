from matplotlib import pyplot as plt
import click
import polars as pl
import numpy as np 

@click.command()
@click.option('--data', required=True)
def plot_cli(data: str):
    df = pl.read_csv(data)
    plot(df)

uri = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'

def plot(df: pl.DataFrame):
    fig, axs = plt.subplots(dpi=100)
    axs.set_title(f'Time required to list the groups contained in ARCO ERA5')
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.grid(True, alpha=.5)
    axs.yaxis.set_label_text('Time (s)')
    gb = df.group_by(pl.col('zarr_version'), pl.col('concurrency_limit'))
    num_plots = len(df.unique(['zarr_version', 'concurrency_limit']))
    order = gb.agg(pl.min('time')).sort(by='time', descending=True)
    markers = ['o', 'v', 'x']
    colors = ['c', 'r', 'gray']
    spread = (-0.05, 0.05)
    xticks = list(range(num_plots))
    xlabels = []
    for row in order.iter_rows(named=True):
        if row['zarr_version'].startswith('2'):
            label = (f'zarr_version: {row["zarr_version"]}')
        else:
            label = (f'zarr_version: {row["zarr_version"]}\nconcurrency limit: {row["concurrency_limit"]}')
        xlabels.append(label)
    axs.set_xticks(xticks, labels=xlabels)
    # order by descending mean time
    for cols, data in gb:
        vals = data['time'].to_numpy()
        idx = order['time'].to_list().index(vals.min())
        axs.plot([idx + 2 * spread[0], idx + 2 * spread[-1]], [vals.mean()] * 2, color='k')
        axs.plot(np.random.uniform(idx + spread[0], idx + spread[1], len(vals)), vals,marker=markers[idx], markersize=8, fillstyle='none', linestyle='None', color=colors[idx])
        axs.text(idx + 2.2 * spread[1], vals.mean(), f'Mean: {vals.mean():0.2f} s', verticalalignment='center', horizontalalignment='left')
    plt.show()

if __name__ == '__main__':
    plot_cli()
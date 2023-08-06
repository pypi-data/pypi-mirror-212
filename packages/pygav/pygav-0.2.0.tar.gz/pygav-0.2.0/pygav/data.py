from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def lineplot(data: pd.DataFrame,
             x: str,
             y: str,
             hue: Optional[str] = None,
             style: Optional[str] = None,
             figsize: Optional[tuple[int, int]] = None,
             filename: Optional[str] = None,
             logx: bool = False,
             logy: bool = False,
             rotatex: bool = False,
             xlim: Optional[tuple[int, int]] = None,
             ylim: Optional[tuple[int, int]] = None,
             title: Optional[str] = None,
             xlabel: Optional[str] = None,
             ylabel: Optional[str] = None,
             vline: Optional[tuple[float, str, str]] = None,  # (xpos, linestyle e.g. ':', color e.g. 'orange')
             show: bool = False):

    _, ax = plt.subplots(figsize=figsize)

    plot = sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, ax=ax)

    if title:
        plot.set_title(title)
    if xlabel:
        plot.set_xlabel(xlabel)
    if ylabel:
        plot.set_ylabel(ylabel)

    if xlim is not None:
        plot.set(xlim=xlim)
    if ylim is not None:
        plot.set(ylim=ylim)

    if logx:
        plot.set(xscale='log')
    if logy:
        plot.set(yscale='log')

    if rotatex:
        plot.set_xticklabels(plot.get_xticklabels(), rotation=30)

    if vline is not None:
        plt.axvline(vline[0], 0, 1, linestyle=vline[1], color=vline[2])

    plt.tight_layout()

    fig = plot.get_figure()
    if filename:
        fig.savefig(filename)

    if show:
        plt.show()


def barplot(data: pd.DataFrame,
            x: str,
            y: str,
            hue: Optional[str] = None,
            figsize: Optional[tuple[int, int]] = None,
            filename: Optional[str] = None,
            logx: bool = False,
            logy: bool = False,
            rotatex: bool = False,
            xlim: Optional[tuple[int, int]] = None,
            ylim: Optional[tuple[int, int]] = None,
            title: Optional[str] = None,
            xlabel: Optional[str] = None,
            ylabel: Optional[str] = None,
            vline: Optional[tuple[float, str, str]] = None,  # (xpos, linestyle e.g. ':', color e.g. 'orange')
            show: bool = False):

    _, ax = plt.subplots(figsize=figsize)

    plot = sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax)

    if title:
        plot.set_title(title)
    if xlabel:
        plot.set_xlabel(xlabel)
    if ylabel:
        plot.set_ylabel(ylabel)

    if xlim is not None:
        plot.set(xlim=xlim)
    if ylim is not None:
        plot.set(ylim=ylim)

    if logx:
        plot.set(xscale='log')
    if logy:
        plot.set(yscale='log')

    if rotatex:
        plot.set_xticklabels(plot.get_xticklabels(), rotation=30)

    if vline is not None:
        plt.axvline(vline[0], 0, 1, linestyle=vline[1], color=vline[2])

    plt.tight_layout()

    fig = plot.get_figure()
    if filename:
        fig.savefig(filename)

    if show:
        plt.show()


def relplot(data: pd.DataFrame,
            x: str,
            y: str,
            col: Optional[str] = None,
            hue: Optional[str] = None,
            style: Optional[str] = None,
            kind: str = 'line',
            figsize: Optional[tuple[int, int]] = None,
            filename: Optional[str] = None,
            logx: bool = False,
            logy: bool = False,
            rotatex: bool = False,
            xlim: Optional[tuple[int, int]] = None,
            ylim: Optional[tuple[int, int]] = None,
            title: Optional[str] = None,
            xlabel: Optional[str] = None,
            ylabel: Optional[str] = None,
            vline: Optional[tuple[float, str, str]] = None,  # (xpos, linestyle e.g. ':', color e.g. 'orange')
            show: bool = False):

    _, ax = plt.subplots(figsize=figsize)

    plot = sns.relplot(data=data, x=x, y=y, col=col, hue=hue, style=style, kind=kind, ax=ax)

    if title:
        plot.fig.subplots_adjust(top=0.9)
        plot.fig.suptitle(title)
    if xlabel:
        plot.set_xlabel(xlabel)
    if ylabel:
        plot.set_ylabel(ylabel)

    if xlim is not None:
        plot.set(xlim=xlim)
    if ylim is not None:
        plot.set(ylim=ylim)

    if logx:
        plot.set(xscale='log')
    if logy:
        plot.set(yscale='log')

    if rotatex:
        plot.set_xticklabels(plot.get_xticklabels(), rotation=30)

    if vline is not None:
        plt.axvline(vline[0], 0, 1, linestyle=vline[1], color=vline[2])

    plt.tight_layout()

    fig = plot.get_figure()
    if filename:
        fig.savefig(filename)

    if show:
        plt.show()

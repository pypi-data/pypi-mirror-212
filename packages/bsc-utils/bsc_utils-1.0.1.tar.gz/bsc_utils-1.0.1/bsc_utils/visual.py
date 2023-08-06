import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from bsc_utils.helpers import row_ratio


def plotly(subplots: dict, **layout_kwargs) -> go.Figure:

    no_subplots = len(subplots)

    fig = make_subplots(
        rows=no_subplots,
        cols=1,
        shared_xaxes=True,
        row_heights=row_ratio(no_subplots),
        vertical_spacing=0.25 / no_subplots,
        subplot_titles=list(subplots.keys()),
        specs=[[{
            'secondary_y': True
        }] for _ in subplots]
    )

    for row_id, subplot in enumerate(subplots.values()):
        for trace in subplot:
            fig.add_trace(
                {
                    k: v
                    for k, v in trace.items()
                    if k not in ['secondary_y', 'range', 'showticklabels']
                },
                secondary_y=trace.get('secondary_y', False),
                row=(row_id + 1),
                col=1,
            )
            if trace.get('range'):
                if not trace.get('secondary_y'):
                    fig['layout'][f'yaxis{row_id * 2 + 1}'].update(
                        range=trace.get('range'), side='right'
                    )
                else:
                    fig['layout'][f'yaxis{row_id * 2 + 2}'].update(
                        range=trace.get('range'),
                        showticklabels=trace.get('showticklabels'),
                        side='right'
                    )

    fig.update_traces(
        xaxis=f'x{no_subplots}',
        xhoverformat='%a %d %b %Y',
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        automargin=True,
        showspikes=True,
        spikemode='across+toaxis',
        spikesnap='cursor',
        spikethickness=1,
        spikedash='solid',
    )
    fig.update_yaxes(
        showgrid=False,
        showline=False,
        automargin=True,
    )
    fig.update_layout(
        showlegend=True,
        autosize=True,
        font_family='Rockwell',
        hovermode='x unified',
        **layout_kwargs
    )
    return fig
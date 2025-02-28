import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import numpy as np
def plot_array(arr, x, l):
    df = pd.DataFrame({'H':x, 'time':arr})
    fig = px.line(df, x='H', y='time', log_y=l, width=800, height=400, markers='.')
    fig.update_traces(showlegend=True)
    fig.update_layout(
        plot_bgcolor='white'
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.data[0].name = "Restricted language"
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
        )
    )
    if l==True:
        fig.update_layout(yaxis_range=[-4, 3], xaxis_title="Corridor length", yaxis_title="Time (secs)",
                          xaxis={"dtick": 2})
    else:
        fig.update_layout(yaxis_range=[0, max(arr)+0.01], xaxis_title="Corridor length", yaxis_title="Time (secs)",
                      xaxis={"dtick": 2})

    fig.show()
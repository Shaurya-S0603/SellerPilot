import plotly.graph_objects as go

GREEN = "#2E7D32"
GREEN_LIGHT = "#66BB6A"

def style_figure(fig):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="white",

        font=dict(
            family="Inter",
            color="#1E293B",
        ),

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20,
        ),

        legend=dict(
            orientation="h",
            y=1.05,
            x=1,
            xanchor="right",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E5E7EB",
    )

    fig.update_yaxes(
        gridcolor="#E5E7EB",
        zeroline=False,
    )

    return fig
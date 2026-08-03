import plotly.graph_objects as go


class ChartService:

    def create_price_chart(self, history):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        return fig
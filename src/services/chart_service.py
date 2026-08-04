import plotly.graph_objects as go
from src.utils.logger import logger

class ChartService:

    def create_price_chart(self, history):

        logger.info(f"Creating Price Chart")

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
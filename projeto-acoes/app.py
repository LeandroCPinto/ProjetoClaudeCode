from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
from data import get_stock_data

app = Flask(__name__)

COLORS = {
    "PETR4": "#1f77b4",
    "ITUB4": "#ff7f0e",
    "VALE3": "#2ca02c",
}

def build_charts(df):
    tickers = df["Ticker"].unique()

    # Gráfico 1: Cotação histórica
    fig1 = go.Figure()
    for ticker in tickers:
        d = df[df["Ticker"] == ticker]
        fig1.add_trace(go.Scatter(
            x=d["Date"], y=d["Close"],
            name=ticker, line=dict(color=COLORS[ticker], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + ticker + "</extra>"
        ))
    fig1.update_layout(
        title="Cotação Histórica (Fechamento)",
        xaxis_title="Data", yaxis_title="Preço (R$)",
        template="plotly_dark", hovermode="x unified"
    )

    # Gráfico 2: Retorno acumulado %
    fig2 = go.Figure()
    for ticker in tickers:
        d = df[df["Ticker"] == ticker]
        fig2.add_trace(go.Scatter(
            x=d["Date"], y=d["Retorno_%"],
            name=ticker, line=dict(color=COLORS[ticker], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra>" + ticker + "</extra>"
        ))
    fig2.add_hline(y=0, line_dash="dot", line_color="gray")
    fig2.update_layout(
        title="Retorno Acumulado no Ano (%)",
        xaxis_title="Data", yaxis_title="Retorno (%)",
        template="plotly_dark", hovermode="x unified"
    )

    # Gráfico 3: Volume negociado
    fig3 = go.Figure()
    for ticker in tickers:
        d = df[df["Ticker"] == ticker]
        fig3.add_trace(go.Bar(
            x=d["Date"], y=d["Volume"],
            name=ticker, marker_color=COLORS[ticker], opacity=0.8,
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f}<extra>" + ticker + "</extra>"
        ))
    fig3.update_layout(
        title="Volume Negociado Diário",
        xaxis_title="Data", yaxis_title="Volume",
        template="plotly_dark", barmode="group", hovermode="x unified"
    )

    return (
        pio.to_html(fig1, full_html=False, include_plotlyjs="cdn"),
        pio.to_html(fig2, full_html=False, include_plotlyjs=False),
        pio.to_html(fig3, full_html=False, include_plotlyjs=False),
    )


@app.route("/")
def index():
    df = get_stock_data()
    chart1, chart2, chart3 = build_charts(df)
    return render_template("index.html", chart1=chart1, chart2=chart2, chart3=chart3)


if __name__ == "__main__":
    app.run(debug=True)

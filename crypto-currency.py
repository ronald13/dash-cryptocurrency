import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests

app = Dash(__name__, external_stylesheets=[])

coins = ["bitcoin", "ethereum", "solana", "cosmos", ]
interval = 6000 # update frequency - adjust to keep within free tier
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"


def get_data():
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)


def make_card(coin):
    change = coin["price_change_percentage_24h"]
    price = coin["current_price"]
    color = "danger" if change < 0 else "success"
    icon = "↑" if change < 0 else "↓"
    return html.Div([
        html.Div(
            [
                html.Div(
                    [html.Img(src=coin["image"], height=35, className="currency_img"),
                     html.Div(coin["name"], className="currency_name")], className='app_row'
                ),
               html.Div([
                   html.H4(f"${price:,}", className='currency_price'),
                   html.Div(coin["symbol"], className="currency_symbol")], className='app_row'
               ),
               html.Div(
                    [f"{round(change, 2)}%",
                     html.I(className='currency_icon')],
                     className=f"text-{color} arrow-style"
               ),
            ],
            className="app_box",
        ),
    ])


mention = html.A(
     html.Img(src="assets/img/logo.png", height=35, className="currency_img"), href="https://www.coingecko.com/en/api", style={'padding-left':'20px'}
)
interval = dcc.Interval(interval=interval)
cards = html.Div()
app.layout = dbc.Container([interval, mention,  cards, ], className="my-5")


@app.callback(
    Output(cards, "children"),
    Input(interval, "n_intervals")
)
def update_cards(_):
    coin_data = get_data()
    if coin_data is None or type(coin_data) is dict:
        return dash.no_update
    coin_cards = []
    updated = None
    for coin in coin_data:
        if coin["id"] in coins:
            updated = coin.get("last_updated")
            coin_cards.append(make_card(coin))

    card_layout = html.Div([
        html.Div([
            html.H3('Wallets'),
            html.P('Start investing, earn crypto and stack tokens'),
            html.Div('View all wallets')
        ], className='app_static-box'),
        html.Div([html.Div(card) for card in coin_cards],className="app_items"),
        # html.Div(html.Div(f"Last Updated {updated}")),
    ], style={'display':'flex'})
    return card_layout


if __name__ == "__main__":
    app.run_server(debug=True)
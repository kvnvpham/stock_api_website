from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SearchForm
import requests
from datetime import date
import pandas
import plotly.express as px
import os

STOCK_ENDPOINT = "http://api.marketstack.com/v1"
API_KEY = os.environ.get("API_KEY")
data = None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
    global data

    form = SearchForm()

    if form.validate_on_submit():
        params = {
            "access_key": API_KEY,
            "symbols": form.search.data,
            "date_from": form.date_from.data,
            "date_to": form.date_to.data
        }

        response = requests.get(url=f"{STOCK_ENDPOINT}/eod", params=params)
        data = response.json()["data"]

        return redirect(url_for("search", data=data))

    return render_template("search.html", form=form, data=data)


@app.route("/graph")
def show_graph():
    df = pandas.DataFrame(data)
    df["date"] = df["date"].str.split("T", expand=True)[0]
    df["date"] = pandas.to_datetime(df["date"])
    sorted_dataframe = df.sort_values("date")[["date", "symbol", "close"]]

    figure = px.line(sorted_dataframe,
                     x="date",
                     y="close",
                     color="symbol",
                     title="Close Price Over Time")
    figure.update_layout(yaxis_title="Price",
                         xaxis_title="Date",
                         xaxis_tickangle=45)

    return render_template("data_graph.html", data=data, graph=figure.to_html(full_html=False))


@app.context_processor
def inj_copyright():
    return {"year": date.today().year}


if __name__ == "__main__":
    app.run(debug=True)

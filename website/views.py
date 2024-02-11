from flask import Blueprint, render_template, request, redirect, url_for, send_file, Response
from .models import Salesfigures
from . import db
import pandas as pd
import openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os

id_to_day = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    message = request.args.get("message", None)
    salesfigures_list = Salesfigures.query.all()
    if len(salesfigures_list)>0:
        df = pd.DataFrame([(r.id, r.money_made, r.biggest_spend, r.bestseller, r.worstseller, r.mvp ) for r in salesfigures_list], columns=['id', 'Profit', "Biggest Spend", "Bestseller", "Worstseller", "MVP"])
        print(df)
        mvp_name = df["MVP"].mode()[0]
        max_spend = df["Profit"].max()
        biggest_spend = df["Biggest Spend"].max()
        biggest_spend_day = df.loc[df["Biggest Spend"].idxmax()]
        biggest_spend_day = biggest_spend_day["id"]
        biggest_spend_day = id_to_day.get(biggest_spend_day)
        bestseller = df["Bestseller"].mode()[0]
        worstseller = df["Worstseller"].mode()[0]

        days = [id_to_day.get(r.id) for r in salesfigures_list]
        profit = df["Profit"].values
        plt.style.use('ggplot')
        plt.scatter(days,profit)
        plt.title("Weekly Takings")
        plt.xlabel("Day")
        plt.ylabel("Income")
        plt.savefig('website/static/images/main_plot.png')

        return render_template("index.html", salesfigures_list=salesfigures_list, mvp_name=mvp_name, max_spend = max_spend, bestseller = bestseller, worstseller = worstseller, biggest_spend=biggest_spend, biggest_spend_day=biggest_spend_day, message=message)
    else:
        return render_template("index.html", salesfigures_list = salesfigures_list, message=message)


@my_view.route("/add", methods=["POST"])
def add():
    try:
        money_made = request.form.get("money_made", type = float)
        biggest_spend = request.form.get("biggest_spend", type = float)
        bestseller = request.form.get("bestseller")
        worstseller = request.form.get("worstseller")
        mvp = request.form.get("mvp")
        new_salesfigures = Salesfigures(money_made = money_made, biggest_spend=biggest_spend, bestseller=bestseller, worstseller=worstseller, mvp=mvp)
        db.session.add(new_salesfigures)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    except:
        message = "There was an error adding your record. Ensure all values are entered"
        return redirect(url_for("my_view.home", message=message))

@my_view.route("/monday")
def monday():
    figures = Salesfigures.query.filter_by(id=1).first()
    return render_template("days.html", figures = figures)

@my_view.route("/tuesday")
def tuesday():
    figures = Salesfigures.query.filter_by(id=2).first()
    return render_template("days.html", figures = figures)

@my_view.route("/wednesday")
def wednesday():
    figures = Salesfigures.query.filter_by(id=3).first()
    return render_template("days.html", figures = figures)

@my_view.route("/thursday")
def thursday():
    figures = Salesfigures.query.filter_by(id=4).first()
    return render_template("days.html", figures = figures)

@my_view.route("/friday")
def friday():
    figures = Salesfigures.query.filter_by(id=5).first()
    return render_template("days.html", figures = figures)

@my_view.route("/saturday")
def saturday():
    figures = Salesfigures.query.filter_by(id=6).first()
    return render_template("days.html", figures = figures)

@my_view.route("/sunday")
def sunday():
    figures = Salesfigures.query.filter_by(id=7).first()
    return render_template("days.html", figures = figures)
# @my_view.route("/generate")
# def generate():
#     results = Salesfigures.query.all()
#     df = pd.DataFrame([(r.id, r.drinks_sold, r.money_made, r.mean) for r in results], columns=['id', 'Sold', 'Profit', "Mean"])
#     print(df)
#     df.to_excel("sales_figures.xlsx", sheet_name = 'Sales Figures', index = False)
    
#     return send_file('../sales_figures.xlsx')

# def graph_generate():
#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     means = Salesfigures.query.filter(Salesfigures.mean).limit(7).all()
#     means = [(mean.mean) for mean in means]
#     print(means)

#     plt.scatter(days, means)
#     plt.xlabel("Day of the Week")
#     plt.ylabel("Mean Price of Drink")

#     return plt

# @my_view.get("/see_graph")
# def see_graph():
#     plot = graph_generate()

#     plot.savefig('website/static/images/plot.png')

#     return render_template("plot1.html")



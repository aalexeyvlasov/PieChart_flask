#!/usr/bin/env python3
# vim: set ai et ts=4 sw=4:

import sqlite3
import json
import sys

from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json

from datetime import time






app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chart.html")

def create_prices_db():
    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Prices(date_start INTEGER, '
                                    'product TEXT, '
                                    'price REAL)')
    c.execute('INSERT INTO Prices VALUES("1970-01-01","A", 20)')
    c.execute('INSERT INTO Prices VALUES("2019-02-04","B", 45)')
    c.execute('INSERT INTO Prices VALUES("2018-05-11","A", 27)')

    conn.commit()




def sel_row(data_base, table, price, date):
    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()
    c.execute("SELECT product, MAX(date_start) FROM Prices GROUP BY product")

    data = c.fetchall()

    q_col = 'pragma table_info('+table+')'
    c.execute(q_col)
    data1 = c.fetchall()


    conn.commit()
    c.close()
    conn.close()

def name_product(q):

    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()

    c.execute(
        "SELECT * FROM Prices WHERE product LIKE '%{q}%' COLLATE NOCASE ORDER BY date_start"
        "".format(q=q))

    prod =  c.fetchall()

    print (prod)

    Data = []
    prod_price = []

    for x in prod:
        Data.append(x[0])

    for x in prod:
        prod_price.append(x[2])

    name_p = (Data, prod_price)


    print(name_p)

    conn.commit()
    c.close()
    conn.close()



def create_sales_db():
    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS Sales(product TEXT, '
                                                'date INTEGER, '
                                                'amount INTEGER, '
                                                'country TEXT)')

    c.execute('INSERT INTO Sales VALUES("A", "2019-02-15", 92, "RU")')
    c.execute('INSERT INTO Sales VALUES("B", "2019-05-06", 113, "GB")')
    c.execute('INSERT INTO Sales VALUES("B", "2019-06-20", 12, "NA")')

    conn.commit()





def create_revenue_db():
    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Revenue AS SELECT * FROM Prices JOIN Sales ON Prices.product=Sales.product")
    c.execute("UPDATE Revenue SET price = 20 WHERE product = 'A' AND date < '2018-05-11'")
    c.execute("UPDATE Revenue SET price = 27 WHERE product = 'A' AND date >= '2018-05-11'")
    #c.execute("ALTER TABLE Revenue ADD revenue REAL")
    c.execute("UPDATE Revenue SET revenue = price*amount")
    c.execute("SELECT product, price, date, amount, country, revenue FROM Revenue GROUP BY date")

    rev = c.fetchall()
    print("\nВыручка:\n", rev)

    conn.commit()
    c.close()
    conn.close()

    #return render_template("Revenue.html", print("\nВыручка:\n", rev) )


@app.route("/datareceiver", methods=["POST"])
def create_pie_db():
    conn = sqlite3.connect('Prices.db')
    c = conn.cursor()

    data_rec = request.get_json(force=True)  # раскрывает строку в объект (for item in data)

    for item in data_rec:
        for key in item:
            if key == "Item 1":
                plist = item[key]
            if key == "Item 2":
                plist2 = item[key]



        c.execute("SELECT {plist}, {plist2} FROM Revenue GROUP BY date".format(plist=plist, plist2=plist2))

    rev = c.fetchall()

    print(rev)


    dt_name = []
    for x in rev:
        dt_name.append(x[-2])

    dt_value = []
    for x in rev:
        dt_value.append(x[-1])


    print(dt_name)
    print(dt_value)

    filename = "static/js/dt_name.json"
    myfile1 = open(filename, mode='w')
    json.dump(dt_name, myfile1)

    myfile1.close()

    fileval = "static/js/dt_value.json"
    myfile2 = open(fileval, mode='w')
    json.dump(dt_value, myfile2)

    myfile2.close()




    conn.commit()
    c.close()
    conn.close()

    return ""



@app.route("/datareceiver2", methods=["POST"])
def get_pie():

    dt_name = open("static/js/dt_name.json", mode='r').read()
    dt_value = open("static/js/dt_value.json", mode='r').read()

    print(dt_name)
    print(dt_value)


    return jsonify({"numb": dt_value, "dname": dt_name})

















if __name__ == '__main__':
    data_base = 'Prices.db'
    table = 'Prices'
    price = 'price'
    date = 'date_start'
    q = input("Enter the product name:\n", )


    create_prices_db()
    sel_row(data_base, table, price, date)
    name_product(q)
    create_sales_db()
    create_revenue_db()



app.run(0)





import os
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config.from_object('config')

base = automap_base()
engine = create_engine('postgres://score:Rysherat2@shopscore.devman.org:5432/shop')
base.prepare(engine, reflect=True)
order = base.classes.orders
session = Session(engine)


@app.route('/')
def score():
    return render_template('score.html')


@app.route('/get_score')
def get_score():
    first_unprocessed_order = session.query(order).filter(order.confirmed.is_(None))\
            .order_by(order.created.asc()).first()
    backlog_waiting = round((datetime.utcnow() - first_unprocessed_order.created)\
            .total_seconds()/60)
    backlog_count = session.query(order).filter(order.confirmed.is_(None)).count()
    date_utcnow = datetime.utcnow().date()
    orders_processed = session.query(order)\
            .filter(order.confirmed > (date_utcnow - timedelta(days=1)),
                    order.confirmed < (date_utcnow + timedelta(days=1))).count()

    return jsonify(backlogWaitingTime=backlog_waiting,
            backlogCount=backlog_count,
            ordersProcessed=orders_processed)


if __name__ == "__main__":
    app.run()

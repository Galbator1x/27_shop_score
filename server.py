import os
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

Base = automap_base()
engine = create_engine('postgres://score:Rysherat2@shopscore.devman.org:5432/shop')
Base.prepare(engine, reflect=True)
Order = Base.classes.orders
session = Session(engine)


@app.route('/')
def score():
    return render_template('score.html')


@app.route('/get_score')
def get_score():
    first_unprocessed_order = session.query(Order).filter(Order.confirmed.is_(None))\
            .order_by(Order.created.asc()).first()
    backlog_waiting = round((datetime.utcnow() - first_unprocessed_order.created)\
            .total_seconds()/60)
    if backlog_waiting < 8:
        backlog_color = '#2ECC40' # green
    elif backlog_waiting <= 30:
        backlog_color = '#FFDC00' # yellow
    else:
        backlog_color = '#FF4136' # red
    backlog_count = session.query(Order).filter(Order.confirmed.is_(None)).count()
    date_utcnow = datetime.utcnow().date()
    orders_processed = session.query(Order)\
            .filter(Order.confirmed > (date_utcnow - timedelta(days=1)),
                    Order.confirmed < (date_utcnow + timedelta(days=1))).count()

    return jsonify(backlogWaitingTime=backlog_waiting,
            backlogWaitingColor=backlog_color,
            backlogCount=backlog_count,
            ordersProcessed=orders_processed)


if __name__ == "__main__":
    app.run()

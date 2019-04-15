from flask import Flask, url_for, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, MenuItem, Restaurant

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def restaurants_all():
    restaurants = session.query(Restaurant).all()
    items = session.query(MenuItem).all()
    template = render_template('restaurant.html', restaurants=restaurants, items=items)
    return template


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

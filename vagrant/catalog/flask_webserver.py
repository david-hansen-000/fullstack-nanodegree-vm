from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, MenuItem, Restaurant

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def hello_restaurants():
    output = "<html><body>"
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        output += "<h1>{}</h1>".format(restaurant.name)
        output += "<h3>Menu Items</h3>"
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        for item in items:
            output += "<br>Item Name: {}".format(item.name)
            output += "<br>Descriptioin: {}".format(item.description)
            output += "<br>Price: {}".format(item.price)
        output += "<br><br>"
    output += "</body></html>"
                                                


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

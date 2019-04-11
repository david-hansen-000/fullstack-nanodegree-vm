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
@app.route('/restaurants')
def restaurants_all():
    output = "<html><body>"
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        output += "<h1>{}</h1><br>".format(restaurant.name)
        output += "<h3>Menu Items</h3><br>"
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
        for item in items:
            output += "Item Name: {}".format(item.name)
            output += "<br>Descriptioin: {}".format(item.description)
            output += "<br>Price: {}<br><br>".format(item.price)
        output += "<br>"
    output += "</body></html>"
    return output

@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    output = "<html><body>"
    output += "<h1>{}</h1><br>".format(restaurant.name)
    for item in items:
        output += "Item Name: {}".format(item.name)
        output += "<br>Descriptioin: {}".format(item.description)
        output += "<br>Price: {}<br><br>".format(item.price)
    output += "<br>"
    output += "</body></html>"
    return output

@app.route('/restaurants/new/<int:restaurant_id>')
def newMenuItem(restaurant_id):
    return "page to create a new menu item {}. Task 1 complete!".format(restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/edit/<int:restaurant_id>&<int:menu_id>')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit menu item #{} from restaurant {}. Task 2 complete!".format(menu_id, restaurant_id)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/delete/<int:restaurant_id>&<int:menu_id>')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete menu item #{} from restaurant {}. Task 3 complete!".format(menu_id, restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

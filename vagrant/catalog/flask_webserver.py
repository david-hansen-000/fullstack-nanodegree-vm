from flask import Flask, render_template, url_for, request, redirect
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
    output = render_template('restaurants.html', restaurants=restaurants)
    return output


@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    output = render_template('restaurant_menu.html', restaurant=restaurant, items=items)
    return output


@app.route('/restaurants/new/<int:restaurant_id>', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], description=request.form['description'],
                            price=request.form['price'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('restaurant_new_item.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/edit/<int:restaurant_id>&<int:menu_id>')
def edit_menu_item(restaurant_id, menu_id):
    return "page to edit menu item #{} from restaurant {}. Task 2 complete!".format(menu_id, restaurant_id)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/delete/<int:restaurant_id>&<int:menu_id>')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete menu item #{} from restaurant {}. Task 3 complete!".format(menu_id, restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

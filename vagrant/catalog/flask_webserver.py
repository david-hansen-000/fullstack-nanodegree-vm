from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, MenuItem, Restaurant

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_item_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


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


@app.route('/restaurants/new/<int:restaurant_id>/<int:menu_id>', methods=['GET', 'POST'])
def new_menu_item(restaurant_id, menu_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], description=request.form['description'],
                            price=request.form['price'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        item = MenuItem(name="New Value", description="New Value", price="$0", id=0, restaurant_id=restaurant_id)
        return render_template('restaurant_item.html', item=item)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/edit/<int:restaurant_id>/<int:menu_id>', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        session.add(item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        output = render_template('restaurant_item.html', item=item)
        return output


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/delete/<int:restaurant_id>/<int:menu_id>', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("menu item deleted")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

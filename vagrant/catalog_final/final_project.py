from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

app = Flask(__name__)

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name': 'Blue Burgers', 'id': '2'},
               {'name': 'Taco Hut', 'id': '3'}]

# Fake Menu Items
items = [
    {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
    {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
     'id': '2'},
    {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
     'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
    {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
     'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}


@app.route('/')
@app.route('/restaurants')
def restaurants_all():
    return render_template('all_restaurants.html', restaurants=restaurants)


@app.route('/restaurants/view/menu/<int:restaurant_id>')
def view_menu_items(restaurant_id):
    return render_template('view_menu.html', menu_items=items)


@app.route('/restaurants/delete/restaurant/<int:restaurant_id>')
def delete_restaurant(restaurant_id):
    return render_template('delete_entry.html', item='Restaurant')


@app.route('/restaurants/delete/menuitem/<int:menu_id>')
def delete_menuitem(menuitem_id):
    return render_template('delete_entry.html', item='MenuItem')


@app.route('/restaurants/edit/restaurant/<int:restaurant_id>')
def edit_restaurant(restaurant_id):
    return render_template('edit_entry.html', item='Restaurant', type='Edit')


@app.route('/restaurants/edit/menuitem/<int:menu_id>')
def edit_menuitem(menuitem_id):
    return render_template('edit_entry.html', item='MenuItem', type='Edit')


@app.route('/restaurants/new/restaurant')
def new_restaurant():
    return render_template('edit_entry.html', item='Restaurant', type='New')


@app.route('/restaurants/new/menuitem')
def new_menuitem():
    return render_template('edit_entry.html', item='MenuItem', type='New')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

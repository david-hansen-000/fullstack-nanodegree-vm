from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def restaurants_all():
    return render_template('all_restaurants.html')


@app.route('/restaurants/delete/restaurant/<int:restaurant_id')
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
    return render_templat('edit_entry.html', item='Restaurant', type='New')

@app.route('/restaurants/new/menuitem')
def new_menuitem():
    return render_templat('edit_entry.html', item='MenuItem', type='New')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
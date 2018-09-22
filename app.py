''' flask app with mongodb '''
#start mongod server daemon asap
#first we import the Flask class.
from flask import Flask, render_template, redirect
from flask_pymongo import MongoClient
import pymongo
from scrape_mars import scrape
import os

# create the flask object i.e. initialize flask instance
app = Flask(__name__)

client= pymongo.MongoClient('mongodb://localhost:27017/')
#get a Database instance from a MongoClient
db = client['mars']
'''
Rendering Templates

Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the HTML escaping
 on your own to keep the application secure. 
Because of that Flask configures the Jinja2 template engine for us automatically.

To render a template you can use the render_template() method. 
All you have to do is provide the name of the template and the variables you want to 
pass to the template engine as keyword arguments (mars=mars).


Flask will look for templates in the templates folder
'''
#default route
#route() decorator to bind a function to a URL.
#---------------------------------------------------------
@app.route('/')
def index():
    mars = db.mars.find_one()
#serve (provide) template to index.html
    return render_template('index.html', mars=mars)

#start scrape route; inserts results into  mars MongoDB
#---------------------------------------------------------
@app.route('/scrape')
def get():
    mars = db.mars
    data = scrape()
    mars.update({}, data, upsert=True)

    return redirect('http://localhost:5000/', code=302)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

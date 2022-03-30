from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

#Create an instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home(): 
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html",mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scraper():
    mars_mdb = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    print(mars_data)    
    mars_mdb.update_one({},{"$set":mars_data},upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    
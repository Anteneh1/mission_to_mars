from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape

app = Flask(__name__)


# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)


db = client.about_mars
collection = db.about_mars_info

@app.route("/")
def index():
   

    mars_info= list(db.collection.find())
    return  render_template('index.html', mars_info=mars_info)
#
@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_info = scrape.scrape()
    db.collection.insert_one(mars_info)
    return  redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)    


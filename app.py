import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'all_golf'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')

@app.route('/get_index')
def get_index():
    return render_template("index.html")

@app.route('/add_review')
def add_review():   
    return render_template("write.html", category=mongo.db.category.find(), brands=mongo.db.brands.find(), models=mongo.db.models.find(), score=mongo.db.score.find())

@app.route('/get_reviews')
def get_reviews():
    return render_template("reviews.html", reviews=mongo.db.reviews.find())

@app.route('/insert_review', methods=['POST'])
def insert_review():
    reviews = mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('get_reviews'))

@app.route('/insert_brand', methods=['POST'])
def insert_brand():
    brands = mongo.db.brands
    brand_doc = {'brand_name': request.form.get('brand_name')}
    brands.insert_one(brand_doc)
    return redirect(url_for('add_review'))

@app.route('/insert_model', methods=['POST'])
def insert_model():
    models = mongo.db.models
    model_doc = {'model_name': request.form.get('model_name')}
    models.insert_one(model_doc)
    return redirect(url_for('add_review'))

@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    all_reviews = mongo.db.reviews.find()
    return render_template('editreview.html', review=the_review, reviews=all_reviews)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

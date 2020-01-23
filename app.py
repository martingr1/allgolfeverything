import os
from flask import Flask, render_template, redirect, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'all_golf'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')
app.secret_key = os.urandom(24)

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in'
    return render_template("login.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form.get('username')})

    if login_user:
        if check_password_hash(request.form.get['password'], login_user['password']) == login_user['password']:
            session['username'] = request.form.get('username')
            return redirect(url_for('get_index'))
    print(login_user)
    
    return 'Invalid username/password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form.get('username')})

        if existing_user is None:
            securepass = generate_password_hash(request.form.get('password'))
            users.insert_one({'username': request.form.get('username'), 'password': securepass})
            session['username'] = request.form.get('username')
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/get_login')
def get_login():
    return render_template("login.html")

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
    all_categories = mongo.db.category.find()
    all_brands = mongo.db.brands.find()
    all_models = mongo.db.models.find()
    all_scores = mongo.db.score.find()
    return render_template('editreview.html', review=the_review, category =all_categories, brands =all_brands,
    models =all_models, score=all_scores)

@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    reviews = mongo.db.reviews
    reviews.update({'_id': ObjectId(review_id)},
    {
        'category_name':request.form.get('category_name'),
        'brand_name': request.form.get('brand_name'),
        'model_name': request.form.get('model_name'),
        'review_text':request.form.get('review_text'),
        'score':request.form.get('score')
    })
    return redirect(url_for('get_reviews'))

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    return redirect(url_for('get_reviews'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
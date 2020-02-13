import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'all_golf'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')
app.secret_key = os.urandom(24)

mongo = PyMongo(app)


@app.route('/')

@app.route("/get_index")
def get_index():
    return render_template("index.html")

@app.route('/get_login')
def get_login():
    return render_template("login.html")


@app.route('/login', methods=['GET'])
def login():
    if 'user' in session:
        existing_user = mongo.db.users.find_one({"username": session['user']})
        if existing_user:
            flash("You are logged in already!")
            return redirect(url_for('get_index'))
    else:
        return render_template("login.html")


@app.route('/user_auth', methods=['POST'])
def user_auth():
    form = request.form.to_dict()
    existing_user = mongo.db.users.find_one({"username": form['username']})
    if existing_user:
        if check_password_hash(existing_user['password'], form['password']):
            session['user'] = form['username']
            flash("You were logged in successfully!")
            return redirect(url_for('get_reviews'))
        else:
            flash("Invalid credentials supplied, please check your username or password")
            return redirect(url_for('get_login'))
    else:
        flash("You must be registered to access the platform!")
        return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if 'user' in session:
        flash('You are already signed in!')
        return redirect(url_for('get_index'))

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one(
            {'username': request.form.get('username')})

        if existing_user is None:
            securepass = generate_password_hash(request.form.get('password'))
            users.insert_one({'username': request.form.get(
                'username'), 'password': securepass})
            session['username'] = request.form.get('username')
            flash('Thank you for registering with All Golf Everything, please login')
            return redirect(url_for('login'))
        else:
            flash("That username already exists!")
            return redirect(url_for('register'))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out")
    return render_template("login.html")

@app.route('/add_review')
def add_review():
    return render_template("write.html", category=mongo.db.category.find(), brands=mongo.db.brands.find(), models=mongo.db.models.find(), score=mongo.db.score.find())

@app.route('/insert_review', methods=['POST'])
def insert_review():

    if 'user' in session:
        reviews = mongo.db.reviews
        reviews.insert_one({
            'review_title': request.form.get('review_title'),
            'category_name': request.form.get('category_name'),
            'brand_name': request.form.get('brand_name'),
            'model_name': request.form.get('model_name'),
            'score': request.form.get('score'),
            'review_text': request.form.get('review_text'),
            'image_url': request.form.get('image_url'),
            'author': session['user'],
            'upvote': int(request.form.get('upvote'))
        })
        flash("Review submitted, thank you.")
        return redirect(url_for('get_reviews'))

    else:
        flash("You must be logged in to do this!")
        return render_template("login.html")

@app.route('/edit_review/<review_id>', methods=['GET'])
def edit_review(review_id):

    if 'user' in session:
        user = session['user']
        the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        the_author = the_review["author"]
        
        if user == the_author:
       
            all_categories = mongo.db.category.find()
            all_brands = mongo.db.brands.find()
            all_models = mongo.db.models.find()
            all_text = mongo.db.reviews.review_text.find()
        
            all_images = mongo.db.reviews.image_url.find()
            all_scores = mongo.db.score.find()
            all_upvote = mongo.db.reviews.upvote.find()
            return render_template('editreview.html', review=the_review, text=all_text, category=all_categories, brands=all_brands,
                           models=all_models, score=all_scores, image=all_images, upvote=all_upvote)
        
        else:
            flash("You can only edit your own posts!")
        return redirect(url_for('get_reviews'))
    
    else:
        flash("You must be logged in to do this!")
        return render_template("login.html")

@app.route('/get_reviews')
def get_reviews():
    
    if 'user' in session:
        reviews = mongo.db.reviews.find().sort("_id", -1).limit(5)
        return render_template("reviews.html", reviews=reviews, category=mongo.db.category.find().sort("_id", -1), brands=mongo.db.brands.find())
    else:
        flash("You must be logged in to do this!")
        return render_template("login.html")

@app.route('/filter_reviews', methods=['POST'])
def filter_reviews():

    query = {}
    all_categories = mongo.db.category.find()
    all_brands = mongo.db.brands.find()
    brands = request.form.get("brand_name")
    categories = request.form.get("category_name")
    
    if 'brand_name' in request.form:
        
        if 'category_name' in request.form:
            
            query.update({"category_name": categories, "brand_name": brands})
            reviews = mongo.db.reviews.find(query)
            return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
        
        else:
            query.update({"brand_name": brands})
            reviews = mongo.db.reviews.find(query)
            return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
   
    elif 'category_name' in request.form:
        query.update({"category_name": categories})
        reviews = mongo.db.reviews.find(query)
        return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
    
    else:
        all_reviews = mongo.db.reviews.find()
        return render_template("reviews.html", reviews=all_reviews, brands=all_brands, category=all_categories)

@app.route('/insert_brand', methods=['POST'])
def insert_brand():
    
    if 'user' in session:
        
        if request.method == 'POST':
            brands = mongo.db.brands
            existing_brand = brands.find_one(
            {'brand_name': request.form.get('brand_name')})
                
            if existing_brand is None:
                brand_doc = {'brand_name': request.form.get('brand_name')}
                brands.insert_one(brand_doc)
                flash("Brand successfully added, please continue with your review.")
                return redirect(url_for('add_review'))          

            else: 
                flash("Brand already exists in database, please select from dropdown.")
                return redirect(url_for('add_review'))    
    else:
        flash("You must be logged in to do this!")
        return render_template("login.html")

@app.route('/insert_model', methods=['POST'])
def insert_model():

    if 'user' in session:
        
        if request.method == 'POST':
            models = mongo.db.models
            existing_model = models.find_one(
            {'model_name': request.form.get('model_name')})
                
            if existing_model is None:
                model_doc = {'model_name': request.form.get('model_name')}
                models.insert_one(model_doc)
                flash("Model successfully added, please continue with your review.")
                return redirect(url_for('add_review'))          

            else: 
                flash("Model already exists in database, please select from dropdown.")
                return redirect(url_for('add_review'))    
    else:
        flash("You must be logged in to do this!")
        return render_template("login.html")




@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):

    reviews = mongo.db.reviews
    reviews.update({'_id': ObjectId(review_id)},
                   {
        'category_name': request.form.get('category_name'),
        'image_url': request.form.get('image_url'),
        'brand_name': request.form.get('brand_name'),
        'model_name': request.form.get('model_name'),
        'review_text': request.form.get('review_text'),
        'score': request.form.get('score'),
        'upvote': int(request.form.get('upvote'))
    })
    flash("Review successfully edited.")
    return redirect(url_for('get_reviews'))


@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    the_review = mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    return redirect(url_for('get_reviews'))


@app.route('/search_reviews',  methods=["POST", "GET"])
def search_reviews():

    if 'user' in session:
        if request.method == 'POST':
            query = request.form.get("search_query")
            results = mongo.db.reviews.find({"$text": {"$search": query}})
        return render_template("search.html", results=results, review=mongo.db.reviews.find())
    else:
        flash("You must be logged in to do this!")
        return render_template("login.html") 

@app.route('/upvoted/<review_id>')
def upvoted(review_id):

    mongo.db.reviews.find_one_and_update(
        {'_id': ObjectId(review_id)},
        {'$inc': {"upvote": 1}},
        {"upsert": True}
    )
    return redirect(url_for('get_reviews'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

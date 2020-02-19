import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'all_golf'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')
app.secret_key = os.urandom(24)

mongo = PyMongo(app)


@app.route('/')

@app.route("/get_index")
def get_index():
    return render_template("index.html")

###### Login, Authentication, Registration ######

@app.route('/get_login')
def get_login():
    return render_template("login.html")

@app.route('/login', methods=['GET'])
def login():
    if 'user' in session: #Check if user is logged in.
        existing_user = mongo.db.users.find_one({"username": session['user']}) #Check if user exists in db already.
        if existing_user: #If it does, display message on index.
            flash("You are logged in already!")
            return redirect(url_for('get_index'))
    else:
        return render_template("login.html") #If not, redirect to login.


@app.route('/user_auth', methods=['POST'])
def user_auth():
    form = request.form.to_dict() 
    existing_user = mongo.db.users.find_one({"username": form['username']}) #Initial check to see if user exists already.
    if existing_user: #If username matches db, check password.
        if check_password_hash(existing_user['password'], form['password']):
            session['user'] = form['username']
            flash("You were logged in successfully!")#If they match, log the user in and show reviews page.
            return redirect(url_for('get_reviews'))
        else: #If either username or password don't match, display message and show login page.
            flash("Invalid credentials supplied, please check your username or password")
            return redirect(url_for('get_login'))
    else: #If username doesn't exist in users, the user must register. Display message and redirect to registration.
        flash("You must be registered to access the platform!")
        return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if 'user' in session: #Check if user is logged in 
        flash('You are already signed in!')
        return redirect(url_for('get_index'))

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one(
            {'username': request.form.get('username')}) #Create variable for existing user and check against db
                                                        #for existing username
        if existing_user is None: #if user doesn't exist, get the password from the form
            username = request.form.get('username')
            password = request.form.get('password')
            if username: #check for an entry in username field
                if password: #if there is an entry in the password field, encrypt it and submit to db
                    securepass = generate_password_hash(password)
                    users.insert_one({'username': request.form.get(
                        'username'), 'password': securepass})
                    flash('Thank you for registering with All Golf Everything, please login')
                    return redirect(url_for('login'))
                else:
                    flash('You cannot have a blank password') #if password is blank, display message and redirect to
                    return redirect(url_for('register'))        #register template
            else:
                flash('You cannot have a blank username') #if blank in username field, display message
                return redirect(url_for('register')) #anmd redirect to register template
        else:
            flash("That username already exists!")#if username already in users, display message and
            return redirect(url_for('register'))# redirect to register template

    return render_template("register.html")


@app.route("/logout")
def logout():
    if 'user' in session: #Check if user is logged in
        session.pop("user", None) #logout user
        flash("You have been logged out")
        return render_template("login.html")
    else:
        flash("You are not logged in.")#If user is not logged in, display message and redirect to login template
        return render_template("login.html")


###### Reviews ######

@app.route('/add_review')
def add_review():

    if 'user' in session:
        return render_template("write.html", category=mongo.db.category.find().sort("category_name", 1), brands=mongo.db.brands.find().sort("brand_name", 1), models=mongo.db.models.find().sort("model_name", 1), score=mongo.db.score.find())
    else:
        flash("You must be logged in to do this!") #If they aren't, send them to the login page.
        return render_template("login.html")

@app.route('/get_reviews')
def get_reviews():

    if 'user' in session: # Check if the user is logged in.
        reviews = mongo.db.reviews.find().sort("_id", -1).limit(10) # If they are, display the top 5 newest reviews.
        return render_template("reviews.html", reviews=reviews, category=mongo.db.category.find().sort("category_name", 1), brands=mongo.db.brands.find().sort("brand_name", 1))
          
    else:
        flash("You must be logged in to do this!") #If they aren't, send them to the login page.
        return render_template("login.html")

@app.route('/insert_review', methods=['POST'])
def insert_review():

    if 'user' in session: # Check if the user is logged in.
        reviews = mongo.db.reviews #If they are, take form values from template and create a new document
                                    #in the collection.
        reviews.insert_one({
            'review_title': request.form.get('review_title'),
            'category_name': request.form.get('category_name'),
            'brand_name': request.form.get('brand_name'),
            'model_name': request.form.get('model_name'),
            'score': request.form.get('score'),
            'review_text': request.form.get('review_text'),
            'image_url': request.form.get('image_url'),
            'author': session['user'], #add session user as a new string field, 'author' to be user for validation.
            'upvote': int(request.form.get('upvote')) #Add upvote as a new integer key with value 0 to work correctly with upvote function.
        })
        flash("Review submitted, thank you.") 
        return redirect(url_for('get_reviews'))

    else:
        flash("You must be logged in to do this!")#If there is no valid session, redirect to login page.
        return render_template("login.html")

@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):

    reviews = mongo.db.reviews
    reviews.update({'_id': ObjectId(review_id)},
                   {
            'review_title': request.form.get('review_title'),
            'category_name': request.form.get('category_name'),
            'brand_name': request.form.get('brand_name'),
            'model_name': request.form.get('model_name'),
            'score': request.form.get('score'),
            'review_text': request.form.get('review_text'),
            'image_url': request.form.get('image_url'),
            'author': session['user'], #add session user as a new string field, 'author' to be user for validation.
            'upvote': int(request.form.get('upvote')) #Add upvote as a new integer key with value 0 to work correctly with upvote function.
    })
    flash("Review successfully edited.")
    return redirect(url_for('get_reviews'))
        
@app.route('/edit_review/<review_id>', methods=['GET'])
def edit_review(review_id):

    if 'user' in session: # Check if the user is logged in.
        user = session['user']
        the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        the_author = the_review["author"]
        
        if user == the_author: #If they are, check if their user session name matches the author name of the document they
                                #are trying to edit. If it does, render the editreview template.
       
            all_categories = mongo.db.category.find().sort("category_name", 1) 
            all_brands = mongo.db.brands.find().sort("brand_name", 1)
            all_models = mongo.db.models.find().sort("model_name", 1)
            all_text = mongo.db.reviews.review_text.find()
        
            all_images = mongo.db.reviews.image_url.find()
            all_scores = mongo.db.score.find()
            all_upvote = mongo.db.reviews.upvote.find()
            return render_template('editreview.html', review=the_review, text=all_text, category=all_categories, brands=all_brands,
                           models=all_models, score=all_scores, image=all_images, upvote=all_upvote)
        
        else:
            flash("You can only edit your own posts!") #If there is no match, display message on the reviews page.
        return redirect(url_for('get_reviews'))
    
    else:
        flash("You must be logged in to do this!") #If there is no valid session, redirect to login page.
        return render_template("login.html")

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    
    if 'user' in session: # Check if the user is logged in.
        user = session['user']
        the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        the_author = the_review['author'] #If they are, check if their user session name matches the author name of the document they
                                #are trying to delete.
        if user == the_author:
            
            mongo.db.reviews.delete_one({"_id": ObjectId(review_id)}) #If it does, delete the document and show message.
            flash("Review deleted")
            return redirect(url_for('get_reviews'))#Redirect to reviews.

        else:
            flash("You can only edit your own posts!")#If there is no match, display message on the reviews page.
        return redirect(url_for('get_reviews'))
    
    else:
        flash("You must be logged in to do this!")#If there is no valid session, redirect to login page.
        return render_template("login.html")

###### Insert ######

@app.route('/insert_brand', methods=['POST'])
def insert_brand():
    
    if 'user' in session: #Check if user is logged in.
        
        if request.method == 'POST': #if request is made, get the brand name from the form.
            brands = mongo.db.brands
            existing_brand = brands.find_one(
            {'brand_name': request.form.get('brand_name')})
                
            if existing_brand is None:#check if the brand exists already in db. If not, add to brands.
                brand_doc = {'brand_name': request.form.get('brand_name')}
                brands.insert_one(brand_doc)
                flash("Brand successfully added, please continue with your review.")
                return redirect(url_for('add_review'))          

            else: #If it exists, flash message and redirect to write reviews page.
                flash("Brand already exists in database, please select from dropdown.")
                return redirect(url_for('add_review'))    
    else: #If no valid session, flash message and redirect to login.
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

###### Searching and Filtering ######

@app.route('/filter_reviews', methods=['POST'])
def filter_reviews():

    query = {} #create a query variable to pass to mongo and search the db
    all_categories = mongo.db.category.find().sort("category_name", 1) 
    all_brands = mongo.db.brands.find().sort("brand_name", 1) 
    brands = request.form.get("brand_name")#get the value from brand input
    categories = request.form.get("category_name")#get the value from category input
    
    if 'brand_name' in request.form: #if brand selector has a value
        
        if 'category_name' in request.form: #check if category selector also has a value
            
            query.update({"category_name": categories, "brand_name": brands}) #if both are true, create query and filter results
            reviews = mongo.db.reviews.find(query)
            return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
        
        else: #if category has no value, use only the brand filter and return results in reviews template.
            query.update({"brand_name": brands})
            reviews = mongo.db.reviews.find(query)
            return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
   
    elif 'category_name' in request.form: #if brand has no value, check if category has a value
        query.update({"category_name": categories})#if it does, filter by category.
        reviews = mongo.db.reviews.find(query)
        return render_template("reviews.html", reviews=reviews, brands=all_brands, category=all_categories)
    
    else:
        all_reviews = mongo.db.reviews.find() #if neither has a value, reload the default template for reviews.
        return render_template("reviews.html", reviews=all_reviews, brands=all_brands, category=all_categories)

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

###### Upvoting ######

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

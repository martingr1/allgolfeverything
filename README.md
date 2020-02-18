All Golf Everything
====== 

This application (app) has been designed and coded for the 'Data Centric Development' milestone project in the Full Stack Developer 
course at the Code Institute.

The app is designed to be a resource for club golfers to use in order to make informed buying decisions on new purchases, 
share information on golf related gear and generally keep informed of new developments on and off the golf course.

Rather than relying solely on reviews from editors or journalists, All Golf is aimed at providing an open sharing platform
for amateur golfers to share their honest opinions on experiences they've had with particular products.

Project Criteria
=====

The below criteria were set out by Code Institute as an example project outline to follow. As an avid golfer I wanted to put my own twist on these
and create something for which I believe there is a genuine need for in the market. 

##Project Example Idea
Build a book review and recommendation site.

##External user’s goal:
Find books they would like to read.

##Site owner's goal:
Earn money on each book purchased via a link from the site.

##Potential features to include:
Create a web application that allows users to upload details of books, including book name, author name, link to cover image and any other relevant fields. 
Allow users to write comments about any book and upvote it.

##Create the backend code and frontend form(s) to allow users to add new books and reviews to the site, edit them and delete them.

##Advanced potential feature (nice-to-have):
Add a link such as the following to each book page, such that you could conceivably earn money from people looking to buy the book: https://www.amazon.com/s?tag=faketag&k=alice+in+wonderland 
Note that we do not actually encourage you to create an affiliate link, but rather want to demonstrate how this could work. 
Instead, for this project, we encourage you to just keep the tag value as something fake. 
Also, note that in general it's better to link directly to the book's page in the store, but that's a bit more difficult.

Project Design
=====

##Database and Data Model

The project criteria specified that MongoDB be used as the database for the project, principally through MongoDB Atlas.

![alt text][db]

[db]: https://github.com/martingr1/allgolfeverything/static/images/database_model.pdf "Databse Model"

After consideration and some testing, the above databse model was decided upon. This gave a suitably flexible structure to be able to allow users to Create, Read, 
Update and Delete review documents in their own collection; whilst also being able to select and (in some cases) amend other key value pairs without affecting the review itself.

All values were set as strings apart from 'upvote' in the reviews collection. This allowed for incremental python code ('$inc') to be 
used to create a like function.

##Indexing

There is one text index on the databse that allows users to search across title, category, brand or model.

##Back end

In accordance with CI criteria, the main language used to create the app was Python (version 3.7). 

In order to achieve desired functionality extensive use was made of the Flask framework specifically:

1. render_template
2. redirect
3. request
4. url_for
5. session (for login function)
6. flash (for user messaging)
7. Werkzeug Security (for password encryption)
8. bson

##Front end and UX 

The front end was coded using HTML5, CSS and Jinja. Bootstrap 4 was used for styling and layout and responsiveness.

My main design philosophies were:

1. Display information as simply and clearly as possible.
2. Display only relevant information to users.
3. Mobile first.
4. Green, Grey, Yellow colour scheme to fit with golfing theme.
5. Help users get to what they want in as few clicks as possible.

![alt text][ux]

[ux]: https://github.com/martingr1/allgolfeverything/static/images/login_review.pdf "UX Design"

##User stories 

There were three main user stories to consider when creating the app.

##Golfer 1

As a golfer I want to be able to read reviews from golfers with similar interests as me. I want to be able to
consume information regarding products I may be interested in purchasing to help my buying decsion.

##Golfer 2

As a golfer I want to be able to review purchases I've made in order to help others make buying decisions. I want to be able
to revisit my reviews and update or delete them in future.

##Site owner

As the owner of the site, I want to be give people a link to gear reviewed by users, so that they can buy the products they
like quickly and easily. Moreover, I can monetise these links via a channel partnership to help fund the site.


Project Features
=====

##Login, Authentication, Registration

In order to access the site, users must first register and then login. 

This is done via the index.html page, where the user has the option to do either.

If the user tries to login with invalid credentials, they will be sent a message and redirected to the login page.

If the user tries to register with an existing or blank username, they will be sent a message and redirected to the
registration page.

If the user tries to register a blank password, they will be sent a message and redirected to the
registration page.

##Read

Upon logging in successfully, users will be redirected to reviews.html and recieve a confirmation message at the top of the page
telling them that they have been successfully logged in.

From here, they can automatically view the top 10 newest reviews left on the page.

##Search and Filter results

Users can filter results while on reviews.html by either category name or brand name to find what they are looking for quickly.

They can cancel all filters by hitting the refresh filters button.

In addition, there is a search bar at the top right of the page that will allow them to perform a quick search. Upon clicking
the search button, users will be redirected to search.html. This is a read-only results view.

##Create

Users can leave reviews by clicking the 'Contribute' link at the top of the page. This will take them to write.html where
they can use the form provided to create their own review.

The selectors are linked to the relevant collections in the databse so the user can select these from a dropdown. If a 
particular brand or model isn't present in the list, the user can insert them using the 'add' buttons and continue
with their review.

If the user attempts to add a brand or modal already in the database, they will be informed that it already exists and
redirected to write.html again.

Once submitted, the user will be redirected to reviews.html where they can see their review. If no image url was provided,
the image will be a default image set by allgolfeverything.

##Update & Delete

Users can update/edit/delete their own reviews by clicking the edit or delete button at the bottom of any review. 
If they try to edit someone else's review, they will recieve a message stating that they can't do that and redirected 
to reviews.html.

If they try to edit their own review, they will be redirected to editreview.html where they can make any changes, hit submit
and be redirected back to reviews.html where they can see their updated review.

If they delete their own review, they will recieve a confirmation of the action and be redirected back to review.html.

##Likes

Users can like any post by hitting the like button. This increments the upvote key for that review and refreshes the page.

The user can see that the like(s) total will have incremented by one.

##Affiliate links

Users can click on the 'american golf' logo to be sent to their page for that particular brand. 

This is not intended to be a fully realised affiliate link, rather it is an academic proof of concept as to how 
it may work in a real world commercial environment.


Project Testing
=====

The project was tested manually across 3 categories:

1. Login, Authentication and Registration
2. CRUD
3. Defensive

Please see the results of testing [here]https://github.com/martingr1/allgolfeverything/static/images/testing.pdf  .

Bugs and Acknowledgements 
=====
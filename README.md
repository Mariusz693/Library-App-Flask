# Library-App-Flask

Web application for the library with user authorization and admin panel.


### Main functionalities for Visitors:
- See all books, authors, book categories, book details, author
- Search for a book, author or find books from a given category

|![Library_FlaskApp](../main/screenshots/visitor_1.png)|![Library_FlaskApp](../main/screenshots/visitor_2.png)|
|------------------------------------------------------|------------------------------------------------------|
|![Library_FlaskApp](../main/screenshots/visitor_3.png)|![Library_FlaskApp](../main/screenshots/visitor_4.png)|
|![Library_FlaskApp](../main/screenshots/visitor_5.png)|![Library_FlaskApp](../main/screenshots/visitor_6.png)|


### Main functionalities for Users:
- Create a profile, update, change password, delete account
- Check currently borrowed and returned books

|![Library_FlaskApp](../main/screenshots/user_1.png)|![Library_FlaskApp](../main/screenshots/user_2.png)|
|---------------------------------------------------|---------------------------------------------------|
|![Library_FlaskApp](../main/screenshots/user_3.png)|![Library_FlaskApp](../main/screenshots/user_4.png)|
|![Library_FlaskApp](../main/screenshots/user_5.png)|![Library_FlaskApp](../main/screenshots/user_6.png)|


### Main functionalities for Admin:
- Create a book profile, update or delete
- Create a author profile, update or delete
- Create or dalete category
- Create a book borrow, return
- List of book volumes borrowed by the user
- Change user status for admin or vice versa

|![Library_FlaskApp](../main/screenshots/admin_1.png) |![Library_FlaskApp](../main/screenshots/admin_2.png) |
|-----------------------------------------------------|-----------------------------------------------------|
|![Library_FlaskApp](../main/screenshots/admin_3.png) |![Library_FlaskApp](../main/screenshots/admin_4.png) |
|![Library_FlaskApp](../main/screenshots/admin_5.png) |![Library_FlaskApp](../main/screenshots/admin_6.png) |
|![Library_FlaskApp](../main/screenshots/admin_7.png) |![Library_FlaskApp](../main/screenshots/admin_8.png) |
|![Library_FlaskApp](../main/screenshots/admin_9.png) |![Library_FlaskApp](../main/screenshots/admin_10.png)|
|![Library_FlaskApp](../main/screenshots/admin_11.png)|![Library_FlaskApp](../main/screenshots/admin_12.png)|
|![Library_FlaskApp](../main/screenshots/admin_13.png)|![Library_FlaskApp](../main/screenshots/admin_14.png)|
|![Library_FlaskApp](../main/screenshots/admin_15.png)|![Library_FlaskApp](../main/screenshots/admin_16.png)|


### Technologies:
* Flask (Python's framework)
* SQLAlchemy
* Bootstrap
* Blueprint
* WTForms
* JavaScript

### Installation:
* Creating a virtual environment `virtualenv -p python3 env`
* Activation of the virtual environment `source env/bin/activate`
* Installation of necessary libraries `pip3 install -r requirements.txt`
* Creating a file .env wich environment variables `DATABASE_URL` and `SECRET_KEY`
* Database initialization `python3 manage.py db init`
* Creating migration `python3 manage.py db migrate`
* Migration upgrade `python3 manage.py db upgrade`
* Launching the application `flask run`

### Contact
* [LinkedIn](https://www.linkedin.com/in/mariusz-kuleta/)
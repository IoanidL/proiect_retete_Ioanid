INSTALLATION STEPS

Get the app from the GitHub repo: https://github.com/IoanidL/proiect_retete_Ioanid

Create the virtual environment: python -m venv venv

Activate the venv: venv\Scripts\activate

To install this project's packages, run: pip install -r requirements.txt in your pycharm local terminal. 

To generate db migrations, run: python manage.py makemigrations

To migrate, run in your local terminal: python manage.py migrate

To run the server, run in your local terminal: python manage.py runserver

URL's available

'' Papa Bun Home page showing all recipes
'recipe/add/' add form for recipes for logged users
'recipe/<int:id>/edit/' edit form for a specific recipe by its owner
'recipe/<int:id>/delete/' delete confirmation for a recipe by its owner
'recipe/<int:id>/' detailed view of a specific recipe
'my-recipes/' all recipes of a logged user

'accounts/register/' register form for new users
'accounts/login/' user login page
'accounts/logout/' user logout page
'login/error/' failed login page
### Setup ###
Navigate into folder
```
cd challenge2
```
Create  your Virtual Environment depending on your Os
Pip install requirements.
Update your environment variables.

```
create a .env file
add following info
DB_USER=
DB_PASSWORD=
DB_NAME = 
STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=

```
Run migration.

```
python manage.py migrate

```


## Workflow 

User's sign up and proceed to login
upon login if user has not yet subscribed to premium, take to a page asking the to subscribe.
after subscription roture users to the home page of the app.

A user can cancel their subscription.

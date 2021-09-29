![IrishInteriors logo](ca298/ca298app/static/img/logo.png)


##

E-commerce app built using Django, SQLite, and ExpressJS academic project I created with a partner.

The final version of this app we focused on providing an API from Django to our 
ExpressJS front-end app and implemented a single-page app using EJS and jQuery. 
In earlier versions, ExpressJS was not involved, we created a multi-page app 
using Django's template engine to render data in our HTML.

There is access to both implementations of the app where the multi-page app and single-page app
can be accessed at port 8000 and 3000 respectively. This was for an academic purpose, 
I learned how to deal with APIs and got introduced to making full-stack applications.

## Setup

### Installation

Firstly, install the requirements from [requirements.txt](ca298/requirements.txt).

If you are at the root of the repository you can install it like so.
```
pip install -r ca298/requirements.txt
```

Once you are done, you will now need to install the node modules, which if you are in the node directory, you can do it as follows.
```
npm install
```

### Running the app

#### Django
In order to run the Django server, go into the ca298 directory from root, you will need to run the following command.
```
python manage.py runserver
```

#### ExpressJS
In order to run the ExpressJS, you ***must*** have the Django server running, this is because we get our data stored in the database through the API in Django.
Go into the node directory from the root and run the following command to start the server.
```
npm start
```

##
### Disclaimer

I do not own any of the images except for the logo.
This app is intended as a demo only.

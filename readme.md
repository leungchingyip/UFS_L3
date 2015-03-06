This is Udacity Full Stack Nano Degree project 3. 
It is a web app for displaying items. It base on Flask and Bootstrap.
----------------

**What's included?**
.
├── catalog.py  
├── model.py  
├── readme.md  
├── static  
│   └── dist  
│       ├── css  
│       │   ├── blog.css  
│       │   ├── bootstrap-theme.css  
│       │   ├── bootstrap-theme.css.map  
│       │   ├── bootstrap-theme.min.css  
│       │   ├── bootstrap.css  
│       │   ├── bootstrap.css.map  
│       │   └── bootstrap.min.css  
│       ├── fonts  
│       │   ├── glyphicons-halflings-regular.eot  
│       │   ├── glyphicons-halflings-regular.svg  
│       │   ├── glyphicons-halflings-regular.ttf  
│       │   └── glyphicons-halflings-regular.woff  
│       └── js  
│           ├── bootstrap.js  
│           ├── bootstrap.min.js  
│           └── npm.js  
└── templates  
├── add.html  
├── base.html  
├── csrf.html  
├── delete.html  
├── edit.html  
├── home.html  
├── item.html  
└── newcategory.html  

**How to use?**

1. Install [Flask](http://flask.pocoo.org/docs/0.10/installation/):

2. Install [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/install.html). It provides the csrf protection function in this app.

3. Set your 'username', 'password' and 'secret_key' in Catalog.py.

4. Database structure is changable by modify model.py before the first time running of the APP. Schemas modify after running, please refer to [Altering Schemas through Migrations](http://docs.sqlalchemy.org/en/latest/core/metadata.html#altering-schemas-through-migrations)

5. Add {% include "csrf.html" %} for csrf protection in form tag in html template if add any new.

6. Deploy it on your server. More infomation:[Deployment Options](http://flask.pocoo.org/docs/0.10/deploying/)



from flask import Flask,render_template, jsonify,request, session, flash, url_for, redirect,json
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.app_context().push()

api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tech2link.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = "a_secure_and_hard_secret_key"

class Identity(db.Model):
    '''Representation of Identity'''
    __tablename__ = 'identity'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    phone_number = db.Column(db.Integer , nullable=False)
    skill = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
   


def __init__(self, first_name, last_name, email, phone_number, skill, location):
        '''initializes identity '''
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.skill = skill
        self.location = location


@app.route("/identity", methods = ['POST'])
def identity():
    '''creates an identity object from form input received and 
      stores in the database '''
    if request.method == 'POST':    
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        skill =  request.form['skill']
        location =  request.form['location']
       
    
        nw_identity = Identity(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, skill = skill , location = location)
        db.session.add(nw_identity)
        db.session.commit()
     
        return redirect('/success')
       
@app.route("/tutors", methods=[ 'POST' , 'GET'])
def tutors():
    '''displays the content of the queried database on tutors page from form input 
     received,else renders fail page if queried result does not match input '''
    id_lists = []

    location = request.form['location'] 
    skill = request.form['skill']
                  
    identities = Identity.query.filter_by(location = location, skill = skill).all()

    if identities:    
        for identity in identities:
            id_lists.append({
                'first_name' : identity.first_name,
                'last_name':  identity.last_name,
                'email': identity.email,
                'phone_number': identity.phone_number,
                'skill': identity.skill,
                'location': identity.location
            })
            
        return render_template('tutors.html', id_lists=id_lists) 
    return render_template('fail.html')
    

@app.route('/', strict_slashes=False)
def home():
    '''returns the homepage'''
    return render_template('homepage.html') 

@app.route('/home', strict_slashes=False)
def homepage():
    '''displays the homepage'''
    return render_template('homepage.html')


@app.route('/success', strict_slashes=False)
def success():
    '''displays a success message'''    
    return render_template('success.html')

@app.route('/fail', strict_slashes=False)
def fail():
    '''display entries not found'''
    return render_template('fail.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

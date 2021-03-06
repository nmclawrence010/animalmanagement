from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from SAMapp import db, login_manager
from flask_login import UserMixin 


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


#Database model for User accounts
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	feedings_completed = db.relationship('Feedings', backref='user_completed', lazy=True)
	cleanings_completed = db.relationship('Cleanings', backref='user2_completed', lazy=True)
	monitoring_completed = db.relationship('Monitoring', backref='user3_completed', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#Database model for forum posts
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


#Model for the animals
class Animal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	species = db.Column(db.String(75), unique=True, nullable=False)
	feeding_information = db.Column(db.String(200), nullable=False)
	residency_status = db.Column(db.String(200), nullable=False)
	extra_information = db.Column(db.String(200))
	animal_image = db.Column(db.String(20), default='defaultanimal.jpg')
	animal_qr = db.Column(db.String(20))
	species_feedings = db.relationship('Feedings', backref='animal_feedings', lazy=True)
	species_cleanings = db.relationship('Cleanings', backref='animal_cleaning', lazy=True)
	species_monitoring = db.relationship('Monitoring', backref='animal_monitoring', lazy=True)

	def __repr__(self):
		return f"Animal('{self.species}', '{self.feeding_information}', '{self.residency_status}', '{self.animal_image}', '{self.extra_information}')"


#Model for classifications (Mammals, reptiles etc)
class Classification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	classification_type = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Classification('{self.classificationType}')"


#Storing feedings
class Feedings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))
	user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

	def __repr__(self):
		return f"Feedings('{self.date_completed}', '{self.extra_info}')"


#Storing Cleanings
class Cleanings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))
	user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

	def __repr__(self):
		return f"Cleanings('{self.date_completed}', '{self.extra_info}')"


#Monitoring Information
class Monitoring(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))
	user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

	def __repr__(self):
		return f"Monitoring('{self.date_completed}', '{self.extra_info}')"
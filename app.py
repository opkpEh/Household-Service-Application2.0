import datetime
from sqlite3 import IntegrityError

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'notasecret'
db = SQLAlchemy(app)

project_name= "Household Service"

#db modles
class User(db.Model):
    __tablename__= "user"

    id= db.Column(db.Integer, primary_key=True)
    full_name= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    professional = db.relationship('Professional', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Professional(db.Model):
    __tablename__= "professional"
    id= db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.String(50), unique=True, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Professional {self.professional_id}>'

def init_db():
    with app.app_context():
        db.create_all()

def drop_all_tables():
    with app.app_context():
        db.drop_all()

def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

@app.route("/")
def home():
    return render_template("home.html", project_name=project_name)

@app.route('/about')
def about():
    return render_template("aboutus.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('user_email')
        password = request.form.get('user_password')

        print(username, password)

        return redirect(url_for('home'))

    return render_template("login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        try:
            # Explicitly get all form fields and print for debugging
            user_type = request.form.get('user_type')
            full_name = request.form.get('full_name')
            email = request.form.get('user_email')
            password = request.form.get('user_password')

            # Debug print to see what values are actually being received
            print(f"Received form data: {request.form}")

            # Additional validation
            if not all([user_type, full_name, email, password]):
                flash('Please fill all required fields', 'error')
                return render_template("signup.html")

            # Hash the password
            hashed_password = generate_password_hash(password)

            new_user = User(
                full_name=full_name,
                email=email,
                password=hashed_password,
                user_type=user_type
            )

            if user_type == 'professional':
                professional_id = request.form.get('professional_id')
                service_type = request.form.get('service_type')
                experience = request.form.get('experience')
                description = request.form.get('description')

                # More detailed validation for professional fields
                if not all([professional_id, service_type, experience, description]):
                    print("Missing professional fields:", {
                        'professional_id': professional_id,
                        'service_type': service_type,
                        'experience': experience,
                        'description': description
                    })
                    flash('Please fill all professional fields', 'error')
                    return render_template("signup.html")

                try:
                    professional = Professional(
                        professional_id=professional_id,
                        service_type=service_type,
                        experience=int(experience),
                        description=description,
                        user=new_user
                    )
                    db.session.add(professional)
                except ValueError as ve:
                    flash(f'Invalid experience value: {ve}', 'error')
                    return render_template("signup.html")

            db.session.add(new_user)

            try:
                db.session.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('Email or Professional ID already exists', 'error')
                return render_template("signup.html")
            except Exception as e:
                db.session.rollback()
                flash(f'Database error: {str(e)}', 'error')
                return render_template("signup.html")

        except Exception as e:
            # More detailed error logging
            print(f"Unexpected error in signup: {e}")
            flash(f'An unexpected error occurred: {str(e)}', 'error')
            return render_template("signup.html")

    return render_template("signup.html")

@app.route('/forgot_password')
def forgot_password():
    return render_template("forgot_password.html")

if __name__ == "__main__":
    init_db()
    app.run(port= 5000, host='0.0.0.0')

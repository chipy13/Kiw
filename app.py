from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from expert_rules import SkinDiagnosisEngine
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skincare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    consultations = db.relationship('Consultation', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    skin_type = db.Column(db.String(50), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)

# Create database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    consultations = Consultation.query.filter_by(user_id=current_user.id).order_by(Consultation.date.desc()).all()
    return render_template('dashboard.html', consultations=consultations)

@app.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def diagnosis():
    if request.method == 'POST':
        # Collect all symptoms from the form
        symptoms = {
            'oiliness': request.form.get('oiliness'),
            'acne': request.form.get('acne'),
            'pores': request.form.get('pores'),
            'shine': request.form.get('shine'),
            'sensitivity': request.form.get('sensitivity'),
            'flaking': request.form.get('flaking'),
            'tightness': request.form.get('tightness'),
            'redness': request.form.get('redness'),
            't_zone': request.form.get('t_zone'),
            'cheeks': request.form.get('cheeks'),
            'irritation': request.form.get('irritation')
        }
        
        # Run the expert system
        engine = SkinDiagnosisEngine()
        engine.reset()
        
        # Declare facts based on user input
        for symptom, value in symptoms.items():
            if value:
                engine.declare(SkinFact(**{symptom: value}))
        
        engine.run()
        
        # Get results
        skin_type = None
        recommendations = []
        
        for fact in engine.facts:
            if fact.get('skin_type'):
                skin_type = fact['skin_type']
            if fact.get('recommendations'):
                recommendations = fact['recommendations']
        
        if not skin_type:
            skin_type = "Undetermined"
            recommendations = ["Please consult with a dermatologist for accurate diagnosis"]
        
        # Save consultation
        consultation = Consultation(
            user_id=current_user.id,
            skin_type=skin_type,
            symptoms=str(symptoms),
            recommendations="\n".join(recommendations)
        )
        db.session.add(consultation)
        db.session.commit()
        
        return redirect(url_for('results', consultation_id=consultation.id))
    
    return render_template('diagnosis.html')

@app.route('/results/<int:consultation_id>')
@login_required
def results(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    if consultation.user_id != current_user.id:
        abort(403)
    
    return render_template('results.html', consultation=consultation)

@app.route('/report/<int:consultation_id>')
@login_required
def report(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    if consultation.user_id != current_user.id:
        abort(403)
    
    return render_template('report.html', consultation=consultation)

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/consultation')
@login_required
def consultation():
    return render_template('consultation.html')

if __name__ == '__main__':
    app.run(debug=True)

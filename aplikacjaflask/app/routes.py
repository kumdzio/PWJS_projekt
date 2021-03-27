from app import app
from flask import Flask,render_template,Response,redirect,url_for,request,session,abort
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    DEBUG = True,
    SECRET_KEY='sekretny_klucz'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Category %r>' % self.name

print(User.query.all())

@app.route("/")
def main():
    tytul="Witam"
    tresc="na stronie glownej"
    return render_template('index.html', tytul=tytul, tresc=tresc )

@app.route('/omnie')
def omnie():
    tytul="O mnie"
    tresc="Nazywam sie Konrad Krusinski"
    return render_template('omnie.html', tytul=tytul,tresc=tresc)

@app.route('/informacje')
@login_required
def informacje():
    tytul="Informacje"
    tresc="Wszystkie posty:"
    posty=[
        {
            'author':{'username':'Janek'},
            'body':'Słonecznie w Elblągu!'
        },
        {
           'author':{'username':'Kasia'},
            'body':'Film Kroll ma ciekawa fabule.'
        },
        ]
    return render_template('informacje.html', tytul=tytul, tresc=tresc, posty=posty )

@app.route("/login", methods=["GET", "POST"])
def login():
    tytul = 'Zaloguj się'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for("main"))
        else:
            return abort(401)
    else:
        return render_template('formularz_logowania.html', tytul=tytul)


@app.errorhandler(401)
def page_not_found(e):
    tytul="Coś poszło nie tak..."
    blad = "401"
    return render_template('blad.html', tytul=tytul, blad=blad)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    tytul="Wylogowanie"
    return render_template('logout.html', tytul=tytul)

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/rejestracja', methods=["GET", "POST"])
def rejestracja():
    tytul="Dodawanie nowego konta"
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        password_confirmation=request.form['password_confirmation']
        if password!=password_confirmation:
            result="hasła się nie zgadzają"
        else:
            newUser=User(username=username,password=password)
            try:
                db.session.add(newUser)
                db.session.commit()
                result="Dodano pomyślnie. Teraz możesz się zalogować"
                print(">>>>>>>>>>dodano uzytkownika: "+newUser.__repr__())
            except:
                result="Błąd przy dodawaniu. Spróbuj ponownie. Prawdopodobnie podany login jest zajęty."
            
        return render_template('rejestracja.html',tytul=tytul, result=result)
    else:
        return render_template('rejestracja.html',tytul=tytul)

if __name__ == "__main__":
    app.run()

from app import app,db,login_manager
from flask import render_template,redirect,url_for,request,abort
from flask_login import UserMixin,login_required,login_user,logout_user,current_user
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    
    def get(lookingForId):
        user_found=User.query.filter(User.id==lookingForId).first()
        if user_found:
            return user_found
        else:
            return None

    def __repr__(self):
        return '<User %r,%d>' % (self.username,self.id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship ('User', backref=db.backref('posts',lazy=True))

    
    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Category %r>' % self.name

# db.create_all()
# db.session.commit()
# admin=User(username="admin",password='1234')
# db.session.add(admin)

# py = Category(name='Python')
# Post(title='Hello Python!', body='Python is pretty cool', category=py, user=admin)

# pogoda = Category(name='Pogoda')
# Post(title="Siemka!",body='Słonecznie w Elblągu!',category=pogoda,user=admin)
# Post(title="Hejka!",body="Film Kroll ma ciekawa pogode.",category=pogoda,user=admin)

# db.session.add(py)
# # db.session.delete(Post.query.first())
# db.session.commit()
# print(Post.query.all())
# print(User.query.all())

@app.route("/")
def main():
    tytul="Witam"
    tresc="na stronie glownej"
    return render_template('index.html', tytul=tytul, tresc=tresc )

@app.route('/omnie')
def omnie():
    tytul="O mnie"
    tresc="Nazywam sie Konrad"
    return render_template('omnie.html', tytul=tytul,tresc=tresc)

@app.route('/informacje', methods=["GET","POST"])
@login_required
def informacje():
    tytul="Informacje"
    tresc="Wszystkie posty:"
    msg=""
    
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        category=Category.query.first()
        user=current_user
        post=Post(title=title,body=body,category=category,user=user)
        try:
            db.session.add(post)
            db.session.commit()
            msg="Post dodany pomyślnie!"
        except:
            msg="Błąd dodawania posta, spróbuj ponownie"
    
    posty=Post.query.order_by(Post.pub_date).all();
    return render_template('informacje.html', tytul=tytul, tresc=tresc, posty=posty, msg=msg )

@app.route("/login", methods=["GET", "POST"])
def login():
    tytul = 'Zaloguj się'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_found=User.query.filter(User.username==username).first()
        if user_found:
            if(password==user_found.password):
                login_user(user_found)
                return redirect(url_for("main"))
            else:
                return abort(401)
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
    return User.get(userid)

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
            except:
                result="Błąd przy dodawaniu. Spróbuj ponownie. Prawdopodobnie podany login jest zajęty."
            
        return render_template('rejestracja.html',tytul=tytul, result=result)
    else:
        return render_template('rejestracja.html',tytul=tytul)

if __name__ == "__main__":
    app.run()

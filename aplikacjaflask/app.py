from flask import Flask,render_template,Response,redirect,url_for,request,session,abort
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY='sekretny_klucz'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name,self.password)


users=[User(id) for id in range(1,10)]


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

if __name__ == "__main__":
    app.run()

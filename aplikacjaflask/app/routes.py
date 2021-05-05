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

#db.create_all()
#db.session.commit()
#admin=User(username="admin",password='1234')
#db.session.add(admin)

#py = Category(name='Python')
# Post(title='Hello Python!', body='Python is pretty cool', category=py, user=admin)

#pogoda = Category(name='Pogoda')
# Post(title="Siemka!",body='Słonecznie w Elblągu!',category=pogoda,user=admin)
# Post(title="Hejka!",body="Film Kroll ma ciekawa pogode.",category=pogoda,user=admin)

#db.session.add(py)
# # db.session.delete(Post.query.first())
#db.session.commit()
# print(Post.query.all())
# print(User.query.all())

@app.route("/")
def main():
    tytul="Zainteresowania Konrada Krusińskiego"
    tresc="Jako młody student infomatyki w trybie zaocznym pracuję jako obsługa techniczna sklepów internetowych oraz zajmuję się księgowaniem transakcji handlowych. "
    tresc+="W czasie wolnym staram się rozwijać swoje zaintereoswania i pasje. Jako człowiek młody i dynamicznie rozwijający się postanowiłem, że nie ma sensu "
    tresc+="ograniczanie się do jednego obszaru zainteresowań. Do swoich głównych zajęć w czasie wolnym zaliczyłbym: tworzenie stron internetowych, majsterkowanie przy "
    tresc+="elektronice, majsterkowanie przy mechanice (głównie swój samochód oraz motocykl), tworzenie gry - w liczbie pojedyńczej ponieważ aktualnie uczestniczę w "
    tresc+="swoim pierwszym większym projekcie"
    informacja="Więcej dokładnych informacji znajduje się w postach"
    return render_template('index.html', tytul=tytul, tresc=tresc, informacja = informacja )

@app.route('/omnie')
def omnie():
    tytul="O mnie"
    tresc="Nazywam sie Konrad i stworzyłem tę stronę by podzielić się swoimi pasjami."
    return render_template('omnie.html', tytul=tytul,tresc=tresc)

@app.route('/informacje', methods=["GET","POST"])
@login_required
def informacje():
    tytul="Zainteresowania"
    tresc="Wszystkie komentarze:"
    msg=""
    podtytul1="Elektronika"
    tresc_zainteresowania1="Lubię naprawiać wszelką elektronikę. Nigdy nic nie daje mi tagiego uczucia zafrasowania jak pierwsze otwarcie nienzanego mi dotąd sprzętu czy "
    tresc_zainteresowania1+="nieznanej mi dotąd konstrukcji. Elektronika jest obszarem tak obszernym i skomplikowanym, że uważam, że zawsze będę miał wyzwanie z naprawą "
    tresc_zainteresowania1+="kolejnego telewizora czy kolejnego laptpa i nigdy nie przestaną mnie zaskawiać coraz to nowsze i bardziej skomplikowane konstrukcje. "
    tresc_zainteresowania1+="Jednym z moich największych marzeń w tej dziedzinie jest skonstruowanie od podstaw inteligentnego systemu, który będzie miał kilka właściwości "
    tresc_zainteresowania1+="o których opowiem innym razem"
    podtytul2="Tworzenie gierki"
    tresc_zainteresowania2="Strasznie frapuje mnie tworzenie światów. Dlatego tworzenie gier jest tematem który jest dla mnie tak pociągający. Będąc twórcą gier można "
    tresc_zainteresowania2+="być swojego rodzaju bogiem w wykreowanym świecie. Będąc autorem jest się odpowiedzialnym za wszystko i wszystko można stworzyć tak jak się "
    tresc_zainteresowania2+="chce. Dzięki czemu można wykreować największe okropieństwa lub najpięknięjsze cudy. To jest piękne."
    link_obrazka1="https://krusinski.com.pl/zdj_el.jpg"
    link_obrazka2="https://krusinski.com.pl/gierka.png"
    
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
    return render_template('informacje.html', tytul=tytul, tresc=tresc, podtytul1=podtytul1, podtytul2=podtytul2, posty=posty, msg=msg, tresc_zainteresowania1=tresc_zainteresowania1, tresc_zainteresowania2=tresc_zainteresowania2, link_obrazka1=link_obrazka1, link_obrazka2=link_obrazka2 )

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

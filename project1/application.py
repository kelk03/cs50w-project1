import os


from flask import Flask, redirect, render_template, request, session, redirect,url_for, flash, render_template_string
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv("./env")
FLASK_APP=os.getenv("FLASK_APP")
DATABASE_URL=os.getenv("DATABASE_URL")

# Check for environment variable
if not ("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def registro():
    """Register user"""
    

    if request.method == "POST":
    
        # asegura se haya elegido un usuario
        if not request.form.get("username"):
            flash("Usuario requerido")
            print("falla users")
            return render_template("register.html")

        if not request.form.get("Lastname"):
            flash("Usuario requerido")
            print("falla users")
            return render_template("register.html")  

        if not request.form.get("Email"):
            flash("Correo Requerido")
            print("falla correo")
            return render_template("register.html")

        # asegura que haya una contraseña
        elif not request.form.get("Password"):
            flash("Contraseña requerida")
            print("falla password")
            return render_template("register.html")

        # Asegura que las contraseñas coincidan
        elif request.form.get("Password") != request.form.get("confirmation"):
            flash("Contraseñas no coinciden")
            print("falla confirm")
            return render_template("register.html")

        

        username = request.form.get("username")
        Lastname = request.form.get("Lastname")
        Email = request.form.get("Email")
        password = request.form.get("Password")


        nicks = db.execute("""
            INSERT INTO users(name,email,password)
            VALUES(:name, :email, :password) RETURNING id, name
        """,{
            "name": username,
            "email" : Email,
            "password": generate_password_hash(password)
        }
        ).fetchone()

        db.commit()
        session["user_id"] = nicks[0]
        session["username"] = nicks[1]

        flash("Registrado con exito")

        # redirecciona a la home page
        return render_template("index.html")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            print("1")
            return render_template_string("must provide username"), 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            print("2")
            return render_template_string("must provide password"),403


        # Query database for username
        username=request.form.get("username")
        password= request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE name=:username ",{"username":username}).fetchone()                  

        # Ensure username exists and password is correct
        if not rows:
               print("valimos")
               return render_template("login.html")
 
        else:
            if check_password_hash(rows[2], password):
                print("iniciando sesión...")
            
                session["user_id"] = rows[0]
                session["username"] = rows[1]
            else:
                print("contraseña incorrecta")
                return render_template("login.html")
        
        return render_template("search.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/search", methods=["POST"])
def search():
 
    if not request.form.get("book"):
        flash(" Escribí el libro ")
        return render_template("search.html")

    A= request.form.get("book")
    query = "%" + A + "%"

  
    query = query.title()
    
    rows = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query LIMIT 15",
                        {"query": query}).fetchall()
    

    if len(rows) ==0:
        flash("no hemos encontrado un libro con esos datos.")
        
        return render_template("search.html")
        
    else:
        
        return render_template("index.html", libros= rows)

@app.route("/book", methods=["POST"])
def book():
    if request.method == "POST":
        return render_template("index.html")
    
    else:
        return render_template("search.html")
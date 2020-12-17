from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mollyliebeskind@localhost:5432/example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

# instance of the database that we can interact with usuing sqlalchemy
db = SQLAlchemy(app)

# db.model = create and manipulate models (tables)
# db.session = create and manipulation transactions in the context of a session

# Person is inheriting from db.model
# table name = lowercase of class ('person') or explicit
# don't need the init becaues sqlalchemy already does it
class Person(db.Model):
    __tablename__ = 'persons'

    # include column constrainst to ensure data integrity
    # another option = set custom contraint:
        # db.CheckConstraint('price>0') ensures no item goes into column if price is not positive
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=False)

    def __repr__(self):
        return f"<Person ID: {self.id}, Name: {self.name}>"


# db.create_all() detects models and creates tables if they don't exist. If they do exist, does nothing.
db.create_all()

# decerator for connecting to flask app
@app.route('/')

# handles the user when they connect to the root (route handler)
def index():
    person = Person.query.first()
    return f"hello {person.name}"

if __name__ == "__main__":
    app.run(debug=True)
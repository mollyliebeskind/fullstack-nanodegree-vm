from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mollyliebeskind@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class ToDo(db.Model):
    # Define a todo class to create the to do table with columns id and description
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    # completed = db.Column(db.Boolean, nullable=False, default=False)

    # For debugging
    def __repr__(self):
        return f"<ID: {self.id}, Description: {self.description}"

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # get the information the user has input
    description = request.get_json()['description']
    error=False
    # commit that info to our database - set up error handling
    body = {}
    try:
        todo = ToDo(description=description)
        db.session.add(todo)
        body['description'] = todo.description
        db.session.commit()
    except:
        db.session.rollback()
        # prints system execution information 
        error=True
        print(sys.exc_info())
    finally:
        db.session.close() #happens regardless of commit or rollback 
    if error:
        abort(400)
    else:
        return jsonify(body)

# Call the html template with parameter data to pass info from database to html
# index method is the controller that is telling the views to use html and the models to select all
@app.route("/")
def index():
    return render_template("index.html", data=ToDo.query.all())

# comment this out if using migrate
# db.create_all()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

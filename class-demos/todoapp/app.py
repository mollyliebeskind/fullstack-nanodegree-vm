from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mollyliebeskind@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"
db = SQLAlchemy(app)

class ToDo(db.Model):
    # Define a todo class to create the to do table with columns id and description
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

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

db.create_all()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

# MVC = model (database), views (what the client sees), controle (communication between views and models)
# Get data from user through url addition, form, or json

# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mollyliebeskind@localhost:5432/todoapp'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#   __tablename__ = 'todos'
#   id = db.Column(db.Integer, primary_key=True)
#   description = db.Column(db.String(), nullable=False)

#   def __repr__(self):
#     return f'<Todo {self.id} {self.description}>'

# db.create_all()

# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#   description = request.form.get('description', '')
#   todo = Todo(description=description)
#   db.session.add(todo)
#   db.session.commit()
#   return redirect(url_for('index'))

# @app.route('/')
# def index():
#   return render_template('index.html', data=Todo.query.all())


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo_item = Todo(title=title, complete=False)
    db.session.add(new_todo_item)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_item_id>")
def update(todo_item_id):
    todo_item = Todo.query.filter_by(id=todo_item_id).first()
    todo_item.complete = not todo_item.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_item_id>")
def delete(todo_item_id):
    todo_item = Todo.query.filter_by(id=todo_item_id).first()
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for("home"))

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)

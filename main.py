from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


app = Flask(__name__)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    finish: Mapped[int] = mapped_column(Integer, nullable=False)


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(Todo).order_by(Todo.finish)).scalars()
    todo_list = result.all()
    return render_template("index.html", todo_list=todo_list)


@app.route('/update_checkbox', methods=['POST'])
def update_checkbox():
    data = request.get_json()
    checkbox_id = data['id']
    is_checked = data['checked']
    with app.app_context():
        requested_post = db.get_or_404(Todo, checkbox_id)
        if is_checked:
            requested_post.finish = 1
        else:
            requested_post.finish = 0
        db.session.commit()

    return redirect('/')


@app.route('/add_task', methods=['POST'])
def add_task():
    text = request.form.get("text").strip()
    if text != "":
        task = Todo(
            text=text,
            finish=0,
        )
        with app.app_context():
            db.session.add(task)
            db.session.commit()

    return redirect('/')


@app.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task = db.get_or_404(Todo, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=5003)

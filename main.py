from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


# Create database model
class Base(DeclarativeBase):
    pass


class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    finish: Mapped[int] = mapped_column(Integer, nullable=False)


# Routes
@app.route('/')
def get_all_posts():
    todo_list = Todo.query.order_by(Todo.finish).all()
    return render_template("index.html", todo_list=todo_list)


@app.route('/update_checkbox', methods=['POST'])
def update_checkbox():
    data = request.get_json()
    checkbox_id = data.get('id')
    is_checked = data.get('checked')
    if checkbox_id is None or is_checked is None:
        return jsonify({"error": "Invalid input"}), 400

    requested_post = Todo.query.get_or_404(checkbox_id)
    requested_post.finish = 1 if is_checked else 0
    db.session.commit()
    return jsonify({"message": "Checkbox updated successfully"}), 200


@app.route('/add_task', methods=['POST'])
def add_task():
    text = request.form.get("text").strip()
    if text:
        task = Todo(
            text=text,
            finish=0,
        )
        db.session.add(task)
        db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)

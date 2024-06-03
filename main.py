from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_step.db"
app.config['SECRET_KEY'] = 'YOUR SECRET KEY'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# format='%Y-%m-%d'
class add_task(FlaskForm):
    to_do_task = StringField(label='Type in the task you would like to add', validators=[DataRequired()])
    due_date = StringField(label='Date or time item is due by')
    submit = SubmitField('Add new task')


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    due_date: Mapped[str] = mapped_column(String(500), unique=True, nullable=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    tasks = []
    result = db.session.execute(db.select(Task).order_by(Task.id))
    all_task = result.scalars()
    return render_template('home.html', task=all_task)


@app.route('/new-task', methods=['GET', 'POST'])
def new_task():
    form = add_task()
    if form.validate_on_submit():
        new_task = Task(
            task=request.form['to_do_task'],
            due_date=request.form['due_date']
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete/<int:post_id>", methods=['GET', 'POST', 'DELETE'])
def delete(post_id):
    post = db.get_or_404(Task, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

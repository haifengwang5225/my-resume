import os
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    department = db.Column(db.Text)
    courses = db.relationship('Course', backref='professor', cascade="delete")


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    courseNumber= db.Column(db.Text)
    title = db.Column(db.Integer)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/professors')
def show_all_professors():
    professors = Professor.query.all()
    return render_template('professor-all.html', professors=professors)

@app.route('/professor/add', methods=['GET', 'POST'])
def add_professors():
    if request.method == 'GET':
        return render_template('professor-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        department = request.form['department']

        # insert the data into the database
        professor = Professor(name=name, department=department)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/professor/edit/<int:id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-edit.html', professor=professor)
    if request.method == 'POST':
        # update data based on the form data
        professor.name = request.form['name']
        professor.department = request.form['department']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_professors'))

@app.route('/professor/delete/<int:id>', methods=['GET', 'POST'])
def delete_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-delete.html', professor=professor)
    if request.method == 'POST':
        # delete the artist by id
        # all related songs are deleted as well
        db.session.delete(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))

@app.route('/courses')
def show_all_courses():
    courses = Course.query.all()
    return render_template('course-all.html', courses=courses)


@app.route('/course/add', methods=['GET', 'POST'])
def add_courses():
    if request.method == 'GET':
        professors = Professor.query.all()
        return render_template('course-add.html', professors=professors)
    if request.method == 'POST':
        # get data from the form
        courseNumber = request.form['courseNumber']
        title = request.form['title']
        description = request.form['description']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course = Course(courseNumber=courseNumber, title=title, description=description, professor=professor)

        # insert the data into the database
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/course/edit/<int:id>', methods=['GET', 'POST'])
def edit_song(id):
    course = Course.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('course-edit.html', course=course, professors=professors)
    if request.method == 'POST':
        # update data based on the form data
        course.courseNumber = request.form['courseNumber']
        course.title = request.form['title']
        course.description = request.form['description']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course.professor = professor
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_courses'))

@app.route('/course/delete/<int:id>', methods=['GET', 'POST'])
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('course-delete.html', course=course, professors=professors)
    if request.method == 'POST':
        # delete the artist by id
        # all related songs are deleted as well
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


if __name__ == '__main__':
    app.run()

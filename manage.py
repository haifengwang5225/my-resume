from flask_script import Manager
from resume import app, db, Professor, Course

manager = Manager(app)

@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    professor1= Professor(name='Julianna Butler', department='Economics')
    professor2= Professor(name='Jiannan Wang', department='Accounting')
    course1= Course(courseNumber="MISY350", title="Business Application Development II ", description="Covers concepts related to client side development, including cascading style sheets and JavaScript.", professor=professor2)
    course2= Course(courseNumber="MISY330", title="Database Design and Implementation ", description="Covers the design and implementation of enterprise databases in the business environment. A networked setting and its effect on database management will be emphasized.")
    course3= Course(courseNumber="ECON360", title="Government Regulation of Business  ", description="Normative, economic and legal foundations of government intervention in business, particularly antitrust and regulation; and the process and the effects of government policies.", professor=professor1)
    course4= Course(courseNumber="ECON103", title="Introduction to Macroeconomics ", description="Analyzes the determinants of unemployment, inflation, national income and policy issues relating to how the government alters unemployment and inflation through government spending, taxes and the money supply.")
    db.session.add(professor1)
    db.session.add(professor2)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

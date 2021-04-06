from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}" 

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
    #return 'Hello, World! Siddharth people'
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        todo = Todo.query.filter_by(sno=sno).first()
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=6969,debug=True)
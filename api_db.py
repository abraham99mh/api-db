from flask import Flask, request, abort
from flask import jsonify
import json, time
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import false
from sqlalchemy.sql import expression

app = Flask(__name__)

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    check = db.Column(db.Boolean, default=False)

    def __init__(self, name, check):
        self.name = name
        self.check = check

    def __repr__(self):
        return '<Task %s>' % self.name

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','name','check')


tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()

#db.create_all()


@app.route("/")
def page():
    return "Hola mundo"

@app.route("/api/tasks", methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks)

@app.route("/api/tasks/<int:id>", methods=["GET"])
def id(id):
    task = Task.query.get_or_404(id)
    print(task.name)
    return task_schema.jsonify(task)


@app.route("/api/tasks", methods=['POST'])
def create():
    if not request.json:
        abort(400)
    new_task = Task(name=request.json['name'],check=False)
    db.session.add(new_task)
    db.session.commit()

    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    task = Task.query.get_or_404(task_id)
    if 'name' in request.json:
        task.name = request.json['name']
    if 'check' in request.json:
        task.check = request.json['check']

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    del_task = Task.query.get_or_404(task_id)
    db.session.delete(del_task)
    db.session.commit()
    return task_schema.jsonify(del_task)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

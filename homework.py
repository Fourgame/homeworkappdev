from flask import request, Flask, jsonify
from flask_basicauth import BasicAuth
from pymongo import MongoClient

uri = "mongodb+srv://mongoo:xLnL2hyfI9uWwfIo@cluster0.hqpxerp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["student2"] 
students_collection = db["student_account"]

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = True

auth = BasicAuth(app)

@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
@auth.required
def get_all_students():
    students = list(students_collection.find({}, {"_id": 0}))  
    return jsonify({"Students": students})

@app.route("/students/<int:std_id>", methods=["GET"])
@auth.required
def get_student_by_id(std_id):
    student = students_collection.find_one({"std_id": std_id}, {"_id": 0})  
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students", methods={"POST"})
@auth.required
def create_student():
    data = request.get_json()
    student_id = data.get("std_id")
    existing_student = students_collection.find_one({"std_id": student_id})
    if existing_student:
        return jsonify({"error": "Cannot create new student"}), 500

    new_student = {
        "std_id": student_id,
        "name": data["name"]
    }

    students_collection.insert_one(new_student) 
    student = students_collection.find_one({"std_id": student_id}, {"_id": 0})  
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:std_id>", methods=["DELETE"])
@auth.required
def delete_student(std_id):
    result = students_collection.delete_one({"std_id": std_id})  
    if result.deleted_count > 0:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:std_id>", methods=["PUT"])
@auth.required
def update_student(std_id):
    student = students_collection.find_one({"std_id": std_id})
    if student:
        data = request.get_json()
        students_collection.update_one({"std_id": std_id}, {"$set": data})  
        updated_student = students_collection.find_one({"std_id": std_id}, {"_id": 0})
        return jsonify(updated_student), 200
    else:
        return jsonify({"message": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

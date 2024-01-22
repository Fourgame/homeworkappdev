from flask import request, Flask, jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = True  

auth = BasicAuth(app)

students = [
    {"std_id": 1, "name": "somcha"},
    {"std_id": 2, "name": "somsbangsan"},
    {"std_id": 3, "name": "somsiracha"}
]

@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
@auth.required
def get_all_students():
    return jsonify({"Students": students})

@app.route("/students/<int:std_id>", methods=["GET"])
@auth.required
def get_student_by_id(std_id):
    student = next((b for b in students if b["std_id"] == std_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students", methods={"POST"})
@auth.required
def create_student():
    data = request.get_json()
    student_id = data.get("std_id")
    if any(student["std_id"] == student_id for student in students):
        return jsonify({"error": "Cannot create new student"}), 500
    new_student = {
        "std_id": student_id,
        "name": data["name"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route("/students/<int:std_id>", methods=["DELETE"])
@auth.required
def delete_student(std_id):
    global students
    students = [s for s in students if s["std_id"] != std_id]
    if len(students) > len(students) - 1:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:std_id>", methods=["PUT"])
@auth.required
def update_student(std_id):
    student = next((s for s in students if s["std_id"] == std_id), None)
    if student:
        data = request.get_json()
        student.update(data)
        return jsonify(student), 200
    else:
        return jsonify({"message": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

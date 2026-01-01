from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# absolute DB path (IMPORTANT on Windows)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "Student API running"

@app.route("/create-table")
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    return "Table created successfully"

@app.route("/add-student/<name>/<int:marks>")
def add_student(name, marks):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO students (name, marks) VALUES (?, ?)",
        (name, marks)
    )
    conn.commit()
    conn.close()
    return f"Student {name} added"

@app.route("/students")
def get_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    result = []
    for student in students:
        result.append({
            "id": student["id"],
            "name": student["name"],
            "marks": student["marks"]
        })

    return jsonify(result)



@app.route("/students/<int:id>")
def get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))

@app.route("/add-student", methods=["POST"])
def add_student_post():
    data = request.get_json()
    name = data["name"]
    marks = data["marks"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO students (name, marks) VALUES (?, ?)",
        (name, marks)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student added successfully"})

@app.route("/update-student/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    marks = data["marks"]

    conn = get_db_connection()
    conn.execute(
        "UPDATE students SET marks=? WHERE id=?",
        (marks, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated"})

@app.route("/delete-student/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)

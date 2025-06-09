from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://nishantmi452:cm1sKpSzZUKNhyIF@test.ummkmki.mongodb.net/")
db = client["password_manager"]
collection = db["credentials"]

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save_password():
    website = request.form.get("website")
    email = request.form.get("email")
    password = request.form.get("password")

    if not website or not password:
        return render_template("index.html", error="Website and password are required.")

    existing = collection.find_one({"website": website})
    if existing:
        collection.update_one({"website": website}, {"$set": {"email": email, "password": password}})
    else:
        collection.insert_one({"website": website, "email": email, "password": password})

    return render_template("index.html", message="Password saved successfully.")

@app.route("/find", methods=["GET"])
def find_password():
    website = request.args.get("website")
    result = collection.find_one({"website": website})

    if result:
        return render_template("index.html", result=result)
    else:
        return render_template("index.html", error=f"No details found for {website}.")

@app.route("/update", methods=["PATCH"])
def update_password():
    data = request.get_json()
    website = data.get("website")
    email = data.get("email")
    password = data.get("password")

    result = collection.update_one({"website": website}, {"$set": {"email": email, "password": password}})
    if result.modified_count:
        return "Details updated successfully."
    else:
        return "Website not found.", 404

@app.route("/delete", methods=["DELETE"])
def delete_password():
    data = request.get_json()
    website = data.get("website")
    password = data.get("password")

    existing = collection.find_one({"website": website})
    if existing and existing.get("password") == password:
        collection.delete_one({"website": website})
        return "Details deleted successfully."
    else:
        return "Incorrect website or password.", 400

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, jsonify, request


from pymongo import MongoClient

client = MongoClient("your url")
db = client.dbsparta
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/studentdata", methods=["GET"])
def show_list():
    buckets_list = list(db.school01.find({}, {"_id": False}))
    return jsonify({"buckets": buckets_list})


@app.route("/data", methods=["POST"])
def test_btn():
    name = request.form["studentName"]
    student_class = request.form["studentClass"]
    score = request.form["studentScore"]
    count = db.school01.count_documents({})
    num = count + 1
    mydata = {
        "num": num,
        "done": 0,
        "name": name,
        "class": student_class,
        "score": score,
    }
    db.school01.insert_one(mydata)
    return jsonify({"msg": "data saved"})


@app.route("/update", methods=["POST"])
def update_student():
    num_receive = request.form["num_give"]
    db.school01.update_one({"num": int(num_receive)}, {"$set": {"done": 1}})
    # buckets_list = list(db.school01.find({}, {"_id": False}))
    return jsonify({"msg": "update done!"})


@app.route("/delete", methods=["POST"])
def remove_student():
    num_receive = request.form["num_give"]
    db.school01.delete_one({"num": int(num_receive)})
    return jsonify({"msg": "delete done!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request
import math
import pickle

app = Flask(__name__)

# Load the model
with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        Pclass = request.form.get("Pclass")
        Sex = request.form.get("Sex")
        Age = float(request.form.get("Age"))
        SibSp = int(request.form.get("SibSp"))
        Parch = int(request.form.get("Parch"))
        Fare = float(request.form.get("Fare"))
        Embarked = request.form.get("Embarked")

        # Encode the inputs
        pclass = 1 if Pclass == "Premiere" else (2 if Pclass == "Executive" else 3)
        gender = 0 if Sex == "Male" else 1
        age = math.ceil(Age)
        sibsp = math.ceil(SibSp)
        parch = math.ceil(Parch)
        fare = math.ceil(Fare)
        embarked = 0 if Embarked == "Southampton" else (1 if Embarked == "Cherbourg" else 2)

        # Make the prediction
        result = model.predict([[pclass, gender, age, sibsp, parch, fare, embarked]])
        output_labels = {1: "The passenger will Survive", 
                         0: "The passenger will not survive"}
        prediction = output_labels[result[0]]

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

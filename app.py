from flask import Flask, request, render_template
import os
import pandas as pd

app = Flask(__name__)

df_global = None

@app.route("/")
def home():
    return render_template("home.html")

UPLOAD_FOLDER = "uploads"

@app.route("/upload", methods=["POST"])
def upload():
    global df_global
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    df_global = pd.read_excel(filepath, engine="openpyxl")
    columns = df_global.columns.tolist()

    return render_template("select_column.html", columns=columns)

app.run(debug=True)


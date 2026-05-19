from flask import Flask, request
import os
import pandas as pd

app = Flask(__name__)

df_global = None

@app.route("/")
def home():
    return """
    <h1>Upload Spreadsheet</h1>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    """

UPLOAD_FOLDER = "uploads"

@app.route("/upload", methods=["POST"])
def upload():
    global df_global
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    df_global = pd.read_excel(filepath, engine="openpyxl")
    columns = df_global.columns.tolist()

    options = ''

    for col in columns:
        options += f'<option value = "{col}">{col}</option>'

    return f"""
    <h1>Select Column</h1>

    <form action="/analyze" method = "post">

        <select name = "column">
            {options}
        </select>

        <button type = "submit">Analyze</button>

    </form>
    """

app.run(debug=True)


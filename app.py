from flask import Flask, request, render_template
import os
import pandas as pd
import matplotlib.pyplot as plt

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

@app.route("/analyze", methods=["POST"])
def analyze():
    column = request.form["column"]
    col_data = df_global[column]
    col_data = col_data.dropna()
    plot_path = None

    plt.figure()
    col_data.hist()

    if pd.api.types.is_numeric_dtype(col_data):
        stats = {
            "type": "numeric",
            "mean": col_data.mean(),
            "median": col_data.median(),
            "std": col_data.std(),
            "missing": col_data.isnull().sum()
        }
        plot_filename = f"{column}_hist.png"
        plot_path = os.path.join("static", "plots", plot_filename)

        plt.title(f"{column} Distribtion")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.savefig(plot_path)

        plt.close()
    else:
        stats = {
            "type": "categorial",
            "unique": col_data.nunique(),
            "most_common": col_data.mode().iloc[0] if not col_data.mode().empty else None,
            "missing": df_global[column].isnull().sum()
        }
    return render_template("analysis.html", column=column, stats=stats, plot_path=plot_path)

app.run(debug=True)


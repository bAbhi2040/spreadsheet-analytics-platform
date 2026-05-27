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
PLOT_FOLDER = os.path.join("static", "plots")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    global df_global
    file = request.files['file']

    if file.filename == "":
        return "No file selected"
    
    if not file.filename.endswith(".xlsx"):
        return "Please upload an Excel document or file"
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        file.save(filepath)
        df_global = pd.read_excel(filepath, engine="openpyxl")
    except Exception:
        return "Data file invalid or corrupted"

    return render_template(
        "overview.html",
        columns=df_global.columns.tolist(),
        shape=df_global.shape,
        dtypes=df_global.dtypes,
        preview=df_global.head().to_html() 
    )

@app.route("/analyze", methods=["POST"])
def analyze():
    global df_global

    if df_global is None:
        return "No valid dataset uploaded"
    
    plot_type = request.form["plot_type"]
    column = request.form["column"]
    column2 = request.form["column2"]

    if column not in df_global.columns:
        return "Selected column is not a valid option"
    
    col_data = df_global[column]
    col_data = col_data.dropna()
    plot_path = None
    stats = {}

    if plot_type == "hist":
        if not pd.api.types.is_numeric_dtype(col_data):
            return "Histogram requires a numeric column"

        stats = {
            "type": "histogram",
            "mean": col_data.mean(),
            "median": col_data.median(),
            "std": col_data.std(),
            "missing": col_data.isnull().sum()
        }

        plot_filename = f"{column}_hist.png"
        plot_path = os.path.join(PLOT_FOLDER, plot_filename)

        plt.figure(figsize=(8,5))
        plt.hist(
            col_data,
            bins=20,
            edgecolor="black"
        )
        plt.grid(alpha=0.3)
        plt.title(f"{column} Distribtion")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        
        plt.savefig(plot_path)
        plt.close()

    elif plot_type == "scatter":

        if not column2 or column2 not in df_global.columns:
            return "Scatter plots require a second column"
        
        if not pd.api.types.is_numeric_dtype(df_global[column]) or not pd.api.types.is_numeric_dtype(df_global[column2]):
            return "Scatter plots require both columns to be numeric"
        
        scatter_data = df_global[[column, column2]].dropna()
    
        stats = {
            "type": "scatter",
            }
    
        plot_filename = f"{column}_vs_{column2}.png"
        plot_path = os.path.join("static", "plots", plot_filename)

        plt.figure()
        plt.scatter(scatter_data[column], 
                    scatter_data[column2],
                    alpha=0.7
        )
        plt.grid(alpha=0.3)
        plt.xlabel(column)
        plt.ylabel(column2)
        plt.title(f"{column} vs {column2}")
        plt.tight_layout()

        plt.savefig(plot_path)
        plt.close()
    
    else:
        return "Invalid plot type selected"


    return render_template("analysis.html",
                           column=column,
                           stats=stats,
                           plot_path=plot_path
                        )

app.run(debug=True)


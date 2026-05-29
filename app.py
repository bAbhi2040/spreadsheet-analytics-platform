from flask import Flask, request, render_template, session
import os
import pandas as pd
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key"

def render_overview(df, error=None):

    return render_template(
        "overview.html",
        columns=df.columns.tolist(),
        shape=df.shape,
        dtypes=df.dtypes,
        preview=df.head().to_html(),
        error=error
    )

@app.route("/")
def home():
    return render_template("home.html")

UPLOAD_FOLDER = "uploads"
PLOT_FOLDER = os.path.join("static", "plots")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']

    if file.filename == "":
        return render_template(
            "error.html",
            message = "No file selected"
        )
    
    if not file.filename.endswith(".xlsx"):
        return render_template(
            "error.html",
            message = "Please upload an Excel document or file"
        )
    
    unique_filename = f"{uuid.uuid4()}.xlsx"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        file.save(filepath)
        df = pd.read_excel(filepath, engine="openpyxl")
        session["filepath"] = filepath

    except Exception:
        return render_template(
            "error.html",
            message = "Data file invalid or corrupted"
        )

    return render_template(
        "overview.html",
        columns=df.columns.tolist(),
        shape=df.shape,
        dtypes=df.dtypes,
        preview=df.head().to_html() 
    )

@app.route("/analyze", methods=["POST"])
def analyze():
    filepath = session.get("filepath")

    if not filepath:
        return render_template(
            "error.html",
            message = "No valid dataset uploaded"
        )
    
    try:
        df = pd.read_excel(filepath, engine="openpyxl")
    
    except Exception:
        return render_template(
            "error.html",
            message = "Could not load dataset"
        )
    
    plot_type = request.form["plot_type"]
    column = request.form["column"]
    column2 = request.form["column2"]

    if column not in df.columns:
        return render_overview(
            df,
            error = "Selected column is not a valid option"
        )
    
    col_data = df[column].dropna()
    plot_path = None
    stats = {}

    if plot_type == "hist":
        if not pd.api.types.is_numeric_dtype(col_data):
            return render_overview(
                df,
                error = "Histogram requires a numeric column"
            )

        stats = {
            "type": "histogram",
            "mean": round(col_data.mean(), 4),
            "median": round(col_data.median(), 4),
            "std": round(col_data.std(), 4),
            "missing": col_data.isnull().sum()
        }

        plot_filename = f"{uuid.uuid4()}_hist.png"
        plot_full_path = os.path.join(PLOT_FOLDER, plot_filename)
        plot_path = os.path.join("static", "plots", plot_filename)
        

        plt.figure(figsize=(8,5))
        plt.hist(
            col_data,
            bins=20,
            edgecolor="black"
        )
        plt.grid(alpha=0.3)
        plt.title(f"{column} Distribution")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        
        plt.savefig(plot_full_path)
        plt.close()

    elif plot_type == "scatter":

        if not column2 or column2 not in df.columns:
            return render_overview(
                df,
                error = "Scatter plots require a second column"
            )
        
        if not pd.api.types.is_numeric_dtype(df[column]) or not pd.api.types.is_numeric_dtype(df[column2]):
            return render_overview(
                df,
                error = "Scatter plots require both columns to be numeric"
            )
        
        scatter_data = df[[column, column2]].dropna()
        correlation = scatter_data[column].corr(scatter_data[column2])
        if abs(correlation) > 0.8:
            relationship = "Strong correlation"
        elif abs(correlation) > 0.5:
            relationship = "Medium correlation"
        elif abs(correlation) > 0.3:
            relationship = "Weak correlation"
        else:
            relationship = "Very weak or no correlation"
    
        stats = {
            "type": "scatter",
            "correlation": round(correlation, 4),
            "relationship": relationship
            }
    
        plot_filename = f"{uuid.uuid4()}.png"
        plot_full_path = os.path.join(PLOT_FOLDER, plot_filename)
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

        plt.savefig(plot_full_path)
        plt.close()
    
    else:
        return render_overview(
                df,
                error = "Invalid plot type selected"
        )


    return render_template("analysis.html",
                           column=column,
                           column2=column2,
                           stats=stats,
                           plot_path=plot_path
                           )
    
if __name__ == "__main__":
    app.run(debug=True)


import json
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from services.bert import answer_question
from services.summarize import summarize
from services.helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/more_info")
def about():
    return render_template("more_info.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    params = json.loads(request.get_data().decode("utf-8"))
    input_text = params["input_text"]
    question = params["question"]

    if not input_text:
        return "Please provide some input text"
    
    if not question:
        return "Please enter your question"
    
    response = answer_question(question, input_text)
    return response


@app.route("/get_summary", methods=["POST"])
def get_summary():
    params = json.loads(request.get_data().decode("utf-8"))
    print("params")
    print(params)
    input_text = params["input_text"]
    sentences_qty = int(params["sentences_qty"])

    if not input_text:
        return "Please provide some input text"

    if not sentences_qty or sentences_qty <= 0:
        return "Number of sentences in summary must be a positive integer"
    
    summary = summarize(input_text, sentences_qty)
    return summary

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



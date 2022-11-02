from flask import Flask, render_template

from Controller import RetrainController, TextSummaryController

app = Flask(__name__)

@app.route('/admin/retrain', methods=['GET', 'POST'])
def editData():
    return RetrainController.retrainController()

@app.route('/', methods=['GET', 'POST'])
def textSummary():
    return TextSummaryController.index()

@app.route('/', methods=['GET', 'POST'])
def index():
    return TextSummaryController.index()

@app.route('/textSummary', methods=['POST'])
def indexURL():
    return TextSummaryController.textSummaryURL()

if __name__ == "__main__":
    app.run(debug=True)
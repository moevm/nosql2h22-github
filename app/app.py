from flask import Flask, render_template, url_for
import pymongo
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html', value=12)


if __name__ == "__main__":
    app.run(debug=True)
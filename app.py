from flask import Flask, jsonify
from scraper import scrape_priceoye_by_category

app = Flask(__name__)

@app.route("/mobiles", methods=["GET"])
def get_mobiles():
    data = scrape_priceoye_by_category()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # Mock search implementation
    return jsonify({
        "query": query,
        "results": [
            {"id": 1, "title": f"Result 1 for {query}"},
            {"id": 2, "title": f"Result 2 for {query}"}
        ]
    })

@app.route('/search/index', methods=['POST'])
def index_item():
    item = request.json
    # Mock indexing implementation
    return jsonify({"msg": "Item indexed successfully"}), 201

if __name__ == '__main__':
    app.run(port=5008)

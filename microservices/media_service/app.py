from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/media/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"msg": "File uploaded successfully"}), 201

@app.route('/media/<file_id>')
def get_file(file_id):
    # Mock file retrieval
    return jsonify({"file_url": f"/static/{file_id}"})

if __name__ == '__main__':
    app.run(port=5006)

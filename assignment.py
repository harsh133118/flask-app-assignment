from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=True)

# Initialize database
with app.app_context():
    db.create_all()

# Endpoint: Add an app (POST)
@app.route('/add-app', methods=['POST'])
def add_app():
    data = request.get_json()
    new_app = App(
        app_name=data['app_name'],
        version=data['version'],
        description=data['description']
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "App added successfully", "id": new_app.id})

# Endpoint: Get an app by ID (GET)
@app.route('/get-app/<int:id>', methods=['GET'])
def get_app(id):
    app_data = App.query.get(id)
    if not app_data:
        return jsonify({"error": "App not found"}), 404
    return jsonify({
        "id": app_data.id,
        "app_name": app_data.app_name,
        "version": app_data.version,
        "description": app_data.description
    })

# Endpoint: Update an app by ID (PUT)
@app.route('/update-app/<int:id>', methods=['PUT'])
def update_app(id):
    app_data = App.query.get(id)
    if not app_data:
        return jsonify({"error": "App not found"}), 404

    data = request.get_json()
    if 'app_name' in data:
        app_data.app_name = data['app_name']
    if 'version' in data:
        app_data.version = data['version']
    if 'description' in data:
        app_data.description = data['description']

    db.session.commit()
    return jsonify({"message": "App updated successfully", "app": {
        "id": app_data.id,
        "app_name": app_data.app_name,
        "version": app_data.version,
        "description": app_data.description
    }})

# Endpoint: Delete an app by ID (DELETE)
@app.route('/delete-app/<int:id>', methods=['DELETE'])
def delete_app(id):
    app_data = App.query.get(id)
    if not app_data:
        return jsonify({"error": "App not found"}), 404

    db.session.delete(app_data)
    db.session.commit()
    return jsonify({"message": "App deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

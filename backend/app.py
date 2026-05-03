import os
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "portfolio")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    fs = gridfs.GridFS(db)
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/api/resume/download', methods=['GET'])
def download_resume():
    try:
        # Find the most recently uploaded resume
        resume_file = db.fs.files.find_one({"filename": "Agin_CS_Resume.pdf"}, sort=[("uploadDate", -1)])
        
        if not resume_file:
            return jsonify({"error": "Resume not found in database. Please run upload_resume.py first."}), 404
            
        grid_out = fs.get(resume_file["_id"])
        
        return send_file(
            BytesIO(grid_out.read()),
            mimetype=grid_out.content_type or 'application/pdf',
            as_attachment=True,
            download_name="Agin_CS_Resume.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

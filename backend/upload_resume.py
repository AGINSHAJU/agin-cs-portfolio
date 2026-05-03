
import os
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "portfolio")

def upload_resume(file_path):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    fs = gridfs.GridFS(db)
    
    filename = "Agin_CS_Resume.pdf"
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find '{file_path}'")
        return
        
    with open(file_path, 'rb') as f:
        # Save to GridFS
        file_id = fs.put(f, filename=filename, content_type="application/pdf")
        
    print(f"Successfully uploaded {filename} to MongoDB!")
    print(f"File ID: {file_id}")

if __name__ == "__main__":
    # Look for a resume file in the parent directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resume_path = os.path.join(parent_dir, "Agin_CS_Resume.pdf")
    
    # Check if we should create a dummy resume for testing if it doesn't exist
    if not os.path.exists(resume_path):
        print(f"Resume not found at {resume_path}.")
        print("Creating a dummy PDF for testing purposes...")
        with open(resume_path, "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Agin CS Resume) Tj ET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000213 00000 n \n0000000299 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n393\n%%EOF\n")
            
    upload_resume(resume_path)

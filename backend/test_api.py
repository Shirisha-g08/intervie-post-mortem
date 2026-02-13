import requests

url = "http://localhost:8000/analyze"

try:
    with open("sample_resume.pdf", "rb") as pdf_file:
        files = {"resume": ("sample_resume.pdf", pdf_file, "application/pdf")}
        data = {
            "job_description": "We need a Python Developer with Flask and SQL experience.",
            "interview_experience": "I built a web app using Flask. Ideally, I think I did well."
        }
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            print("Success!")
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
except FileNotFoundError:
    print("sample_resume.pdf not found. Run create_pdf.py first.")
except Exception as e:
    print(f"Request failed: {e}")

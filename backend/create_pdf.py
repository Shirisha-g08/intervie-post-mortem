from reportlab.pdfgen import canvas

def create_resume():
    c = canvas.Canvas("sample_resume.pdf")
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "Python Developer")
    c.drawString(100, 700, "Skills: Python, FastAPI, Django, React, SQL")
    c.drawString(100, 680, "Experience: Built web apps using Flask.")
    c.save()

if __name__ == "__main__":
    create_resume()

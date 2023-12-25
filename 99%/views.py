from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import fitz
from pdfminer.high_level import extract_text
import os
from io import BytesIO
from docx import Document
from flask_mail import Message
from flask import current_app
from flask_mail import Mail
from PIL import Image
import pytesseract
# Import OpenAI library
import openai

# Set your OpenAI API key
openai.api_key = "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"

views = Blueprint("views", __name__)

mail = Mail()

@views.route("/upload_and_process", methods=["POST"])
def upload_and_process():
    if "file" not in request.files:
        return "No file part"

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No selected file"

    # Check if the file is a PDF, DOCX, or image
    if uploaded_file.filename.endswith((".pdf", ".docx")):
        text_content = extract_text_from_file(uploaded_file)

        # Send the text to OpenAI for summarization
        summary = generate_summary(text_content)

        # Store the original text and summary in session variables
        session["pdf_text"] = text_content
        session["summary"] = summary

        # Redirect to a new route to display the result with the BOTBOT
        return redirect(url_for("views.display_result"))

    elif uploaded_file.filename.endswith((".jpg", ".jpeg", ".png")):
        # Perform OCR on the image
        extracted_text = perform_ocr_on_image(uploaded_file)

        summary = generate_summary(extracted_text)

        # Store the original text and summary in session variables
        session["pdf_text"] = extracted_text
        session["summary"] = summary

        # Redirect to a new route to display the result with the BOTBOT
        return redirect(url_for("views.display_result"))

    return "Unsupported file format. Please upload a PDF, DOCX, or image file."

def perform_ocr_on_image(image_file):
    # Convert the image to grayscale for better OCR results
    image = Image.open(image_file).convert("L")

    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(image)

    return extracted_text

@views.route("/display_result")
def display_result():
    # Retrieve the stored summary from the session
    summary = session.get("summary", "")

    return render_template("result.html", summary=summary)


def generate_summary(text_content, max_tokens=500):
    # Ask OpenAI to summarize the content
    prompt = f"Please summarize the following content:\n{text_content}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens
    )

    # Extract the generated summary from the OpenAI response
    summary = response.choices[0].text.strip()

    # Remove leading "." if present
    if summary.startswith("."):
        summary = summary[1:]

    return summary




@views.route("/get_openai_response", methods=["POST"])
def get_openai_response():
    user_input = request.form.get("user_input")
    
    # Retrieve the stored PDF text from the session
    pdf_text = session.get("pdf_text", "")

    # Concatenate user input with the PDF text for OpenAI prompt
    prompt = f"{user_input} in a PDF document:\n{pdf_text}"

    # Call the OpenAI API for generating a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )

    return jsonify({"response": response.choices[0].text.strip()})

def extract_text_from_file_storage(file_storage):
    content_bytes = file_storage.read()
    content_stream = BytesIO(content_bytes)
    return extract_text(content_stream)

def save_to_text_file(text_content):
    with open("converted_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text_content)

def extract_text_from_file(uploaded_file):
    text_content = ""

    if uploaded_file.filename.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text_content += page.get_text()
        doc.close()
    elif uploaded_file.filename.endswith(".docx"):
        doc = Document(uploaded_file)
        for paragraph in doc.paragraphs:
            text_content += paragraph.text

    return text_content

@views.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    email_sent = False

    if request.method == "POST":
        # Process the form data and send email (you need to implement this)
        # Retrieve form data
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        feedback = request.form.get("feedback")

        # Send email (you need to implement this)
        send_email(name, email, phone, feedback)

        # Set the flag to True if the email is sent successfully
        email_sent = True

    return render_template("contact_us.html", email_sent=email_sent)   

def send_email(name, email, phone, feedback):
    # Create a Message object
    subject = 'New Feedback'
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nFeedback: {feedback}"
    recipients = ['ykpang-wp21@student.tarc.edu.my']

    message = Message(subject=subject, body=body, recipients=recipients)

    try:
        # Send the message using the 'mail' object
        mail.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory
)

from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from services.data_processor import process_file
from services.report_generator import generate_pdf_report
from services.email_sender import send_email


# ==========================================
# Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# Create Flask application
# ==========================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "automated-report-secret-key-2026"
)


# ==========================================
# Folder paths
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = "/tmp/uploads"
REPORT_FOLDER = "/tmp/reports"


# Create folders if they don't exist

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ==========================================
# Allowed file types
# ==========================================

ALLOWED_EXTENSIONS = {
    "csv",
    "xlsx"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================
# UPLOAD → PROCESS → PDF → EMAIL
# ==========================================

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    # --------------------------------------
    # 1. Check whether file was uploaded
    # --------------------------------------

    if "file" not in request.files:

        flash(
            "Please select an Excel or CSV file."
        )

        return redirect(
            url_for("index")
        )

    file = request.files["file"]


    # --------------------------------------
    # 2. Check filename
    # --------------------------------------

    if file.filename == "":

        flash(
            "No file selected."
        )

        return redirect(
            url_for("index")
        )


    # --------------------------------------
    # 3. Check file type
    # --------------------------------------

    if not allowed_file(file.filename):

        flash(
            "Only CSV (.csv) and Excel (.xlsx) "
            "files are supported."
        )

        return redirect(
            url_for("index")
        )


    try:

        # ==================================
        # STEP 1 — Save uploaded Excel file
        # ==================================

        original_filename = secure_filename(
            file.filename
        )

        unique_filename = (
            str(uuid.uuid4())
            + "_"
            + original_filename
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        file.save(filepath)


        # ==================================
        # STEP 2 — Read and process Excel
        # ==================================

        result = process_file(
            filepath,
            REPORT_FOLDER
        )


        # ==================================
        # STEP 3 — Generate PDF report
        # ==================================

        pdf_filename = generate_pdf_report(
            result,
            REPORT_FOLDER
        )

        pdf_path = os.path.join(
            REPORT_FOLDER,
            pdf_filename
        )


        # ==================================
        # STEP 4 — Get email from Excel
        # ==================================

        recipient_email = result[
            "recipient_email"
        ]


        # ==================================
        # STEP 5 — AUTOMATICALLY SEND EMAIL
        # ==================================

        send_email(
            recipient_email,
            pdf_path
        )


        # ==================================
        # STEP 6 — Save information
        # for dashboard
        # ==================================

        session["result"] = result

        session["pdf_filename"] = (
            pdf_filename
        )

        session["email_sent"] = True

        session["recipient_email"] = (
            recipient_email
        )


        # ==================================
        # STEP 7 — Success message
        # ==================================

        flash(
            "Report generated and automatically "
            f"sent to {recipient_email}."
        )


        return redirect(
            url_for("dashboard")
        )


    # ======================================
    # ERROR HANDLING
    # ======================================

    except Exception as error:

        print(
            "ERROR:",
            error
        )

        flash(
            f"Error: {error}"
        )

        return redirect(
            url_for("index")
        )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    result = session.get(
        "result"
    )

    pdf_filename = session.get(
        "pdf_filename"
    )

    email_sent = session.get(
        "email_sent",
        False
    )

    recipient_email = session.get(
        "recipient_email"
    )


    # If no report exists
    if not result:

        flash(
            "Please upload an Excel or CSV file first."
        )

        return redirect(
            url_for("index")
        )


    return render_template(
        "dashboard.html",
        result=result,
        pdf_filename=pdf_filename,
        email_sent=email_sent,
        recipient_email=recipient_email
    )


# ==========================================
# DOWNLOAD PDF
# ==========================================

@app.route(
    "/download/<filename>"
)
def download(filename):

    return send_from_directory(
        REPORT_FOLDER,
        filename,
        as_attachment=True
    )


# ==========================================
# DISPLAY CHART IMAGES
# ==========================================

@app.route(
    "/reports/<filename>"
)
def reports(filename):

    return send_from_directory(
        REPORT_FOLDER,
        filename
    )


# ==========================================
# START FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
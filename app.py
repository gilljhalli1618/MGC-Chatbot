from flask import Flask, render_template, request, jsonify
import os
import re

from dotenv import load_dotenv
from google import genai


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# You can change the model from .env if needed:
# GEMINI_MODEL=your-working-model-name
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

gemini_client = None

if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        print("==========================================")
        print("✅ Gemini API key loaded")
        print("🤖 Gemini model:", GEMINI_MODEL)
        print("==========================================")

    except Exception as e:

        print("❌ Gemini setup error:")
        print(e)

else:

    print("⚠️ GEMINI_API_KEY not found in .env")


# ============================================================
# VERIFIED MATA GUJRI COLLEGE INFORMATION
# ============================================================

college_info = {

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    "about": """
    <strong>🏫 Mata Gujri College, Fatehgarh Sahib</strong><br><br>

    Mata Gujri College was established in 1957 in honour of
    Mata Gujri Ji.<br><br>

    In 1964, the college came under the auspices of the
    Shiromani Gurdwara Parbandhak Committee (SGPC).<br><br>

    The college provides undergraduate, postgraduate,
    diploma and vocational programmes.
    """,

    # --------------------------------------------------------
    # PRINCIPAL
    # --------------------------------------------------------

    "principal": """
    <strong>👨‍🏫 Principal</strong><br><br>

    The Principal of Mata Gujri College, Fatehgarh Sahib is
    <strong>Dr. Biramjit Singh</strong>.
    """,

    # --------------------------------------------------------
    # MISSION
    # --------------------------------------------------------

    "mission": """
    <strong>🎯 Mission</strong><br><br>

    Mata Gujri College focuses on providing quality education,
    developing knowledge and skills, encouraging overall
    development and helping students adapt to social and
    technological changes.
    """,

    # --------------------------------------------------------
    # UG COURSES
    # --------------------------------------------------------

    "ug_courses": """
    <strong>🎓 UNDERGRADUATE (UG) COURSES</strong><br><br>

    • BBA<br>
    • BCA<br>
    • B.Sc. Honours Agriculture<br>
    • B.Sc. Honours Biotechnology<br>
    • B.Sc. Honours Chemistry<br>
    • B.Sc. Honours Mathematics<br>
    • B.Sc. Honours Life Sciences<br>
    • B.Sc. Honours Physical Sciences<br>
    • B.Com. Honours<br>
    • B.Sc. Honours Artificial Intelligence & Data Science<br>
    • B.A. Honours (Multi-disciplinary)<br>
    • B.A. Honours Economics<br>
    • B.A. Honours English<br>
    • B.A. Honours Journalism & Mass Communication<br>
    • B.A. Honours Political Science
    """,

    # --------------------------------------------------------
    # PG COURSES
    # --------------------------------------------------------

    "pg_courses": """
    <strong>🎓 POSTGRADUATE (PG) COURSES</strong><br><br>

    • MBA<br>
    • MCA<br>
    • M.Sc. Agriculture<br>
    • M.Sc. Honours Biotechnology<br>
    • M.Sc. Honours Food Technology<br>
    • M.Sc. Honours Microbiology<br>
    • M.Sc. Botany<br>
    • M.Sc. Chemistry<br>
    • M.Sc. Mathematics<br>
    • M.Sc. Physics<br>
    • M.Sc. Zoology<br>
    • M.Com<br>
    • M.Sc. IT & Lateral Entry<br>
    • M.A. Economics<br>
    • M.A. English<br>
    • M.A. Fine Arts<br>
    • M.A. Journalism & Mass Communication<br>
    • M.A. Music (Vocal)<br>
    • M.A. Political Science<br>
    • M.A. Psychology<br>
    • M.A. Punjabi
    """,

    # --------------------------------------------------------
    # DIPLOMA
    # --------------------------------------------------------

    "diploma": """
    <strong>📚 DIPLOMA / PG DIPLOMA COURSES</strong><br><br>

    • PGDCA<br>
    • PG Diploma in Counselling Psychology<br>
    • PG Diploma in Analytical Instrumentation<br>
    • Diploma in Sweets, Snacks & Savoury<br>
    • Diploma in Dairy Science
    """,

    # --------------------------------------------------------
    # VOCATIONAL
    # --------------------------------------------------------

    "vocational": """
    <strong>🛠️ VOCATIONAL COURSES</strong><br><br>

    • B.Vocational Retail Management<br>
    • B.Vocational Software Development<br>
    • Diploma in Dairy Science
    """,

    # --------------------------------------------------------
    # AI & DATA SCIENCE
    # --------------------------------------------------------

    "ai_ds": """
    <strong>🤖 B.Sc. Honours Artificial Intelligence & Data Science</strong><br><br>

    Mata Gujri College offers B.Sc. Honours Artificial
    Intelligence & Data Science as an undergraduate programme.<br><br>

    The programme is related to Artificial Intelligence,
    Data Science, programming, data analysis and related
    computing technologies.
    """,

    # --------------------------------------------------------
    # ADMISSION
    # --------------------------------------------------------

    "admission": """
    <strong>📝 ADMISSION INFORMATION</strong><br><br>

    Admission requirements depend on the programme and the
    applicable college/university rules.<br><br>

    Documents generally required may include:<br><br>

    • Passport-size photographs<br>
    • Aadhaar Card<br>
    • Detailed Marks Card of qualifying examination<br>
    • Character Certificate<br>
    • Migration Certificate, wherever applicable<br>
    • Residence Certificate, wherever applicable<br>
    • Other documents required for the particular programme
      or category<br><br>

    Eligibility, reservation, admission dates and vacancies
    can change.<br><br>

    Students should check the latest official college admission
    notice before applying.
    """,

    # --------------------------------------------------------
    # FEES
    # --------------------------------------------------------

    "fee": """
    <strong>💰 FEE INFORMATION – SESSION 2026-27</strong><br><br>

    <strong>B.Sc. Honours Artificial Intelligence & Data Science</strong><br>
    • 1st Semester: ₹25,000<br>
    • 2nd Semester: ₹23,200<br><br>

    <strong>B.Com. Honours</strong><br>
    • 1st Semester: ₹25,000<br>
    • 2nd Semester: ₹19,000<br><br>

    <strong>B.A. Honours Economics</strong><br>
    • 1st Semester with Registration: ₹21,000<br>
    • 2nd Semester: ₹16,000<br><br>

    <strong>B.A. Honours English</strong><br>
    • 1st Semester: ₹21,000<br>
    • 2nd Semester: ₹16,000<br><br>

    <strong>B.A. Honours Journalism & Mass Communication</strong><br>
    • 1st Semester: ₹21,000<br>
    • 2nd Semester: ₹17,000<br><br>

    <strong>B.A. Honours Political Science</strong><br>
    • 1st Semester with Registration: ₹20,000<br>
    • 2nd Semester: ₹15,000<br><br>

    <strong>B.Vocational Retail Management</strong><br>
    • 1st Semester: ₹25,000<br>
    • 2nd Semester: ₹23,200<br><br>

    <strong>B.Vocational Software Development</strong><br>
    • 1st Semester: ₹25,000<br>
    • 2nd Semester: ₹23,200<br><br>

    <strong>PGDCA</strong><br>
    • 1st Semester with Registration: ₹21,800<br>
    • 1st Semester without Registration: ₹20,350<br>
    • 2nd Semester: ₹19,500<br><br>

    <strong>PG Diploma in Counselling Psychology</strong><br>
    • 1st Semester with Registration: ₹16,610<br>
    • 1st Semester without Registration: ₹15,080<br>
    • 2nd Semester: ₹17,000<br><br>

    <strong>PG Diploma in Analytical Instrumentation</strong><br>
    • 1st Semester: ₹15,000<br>
    • 2nd Semester: ₹15,000<br><br>

    <strong>Diploma in Dairy Science</strong><br>
    • 1st Semester: ₹18,000<br>
    • 2nd Semester: ₹18,000
    """,

    # --------------------------------------------------------
    # SCHOLARSHIPS
    # --------------------------------------------------------

    "scholarship": """
    <strong>🎓 SCHOLARSHIPS & FEE CONCESSIONS</strong><br><br>

    • Post Matric Scholarship Scheme for Minorities<br>
    • Merit Cum Means Scholarship<br>
    • Post-Matric Scholarship for Students with Disabilities<br>
    • Central Sector Scheme of Scholarships for College and
      University Students<br>
    • National Scholarship for Postgraduate Studies<br>
    • AICTE Pragati Scholarship Scheme for Girl Students<br>
    • Dr. B.R. Ambedkar Post Matric Scholarship Scheme<br>
    • PM YASASVI Top Class Education Scheme<br><br>

    Eligibility, amount and application procedure depend on
    the individual scholarship scheme.
    """,

    # --------------------------------------------------------
    # FACILITIES
    # --------------------------------------------------------

    "facilities": """
    <strong>🏫 COLLEGE FACILITIES</strong><br><br>

    • Approximately 25-acre campus<br>
    • Experimental farm<br>
    • Medical Centre with ambulance facility<br>
    • Conference Hall<br>
    • Seminar Hall<br>
    • Bhal Nand Lal Auditorium<br>
    • Computer Labs including Apple Mac Lab<br>
    • CCTV surveillance<br>
    • Centrally air-conditioned library<br>
    • Approximately 71,000 books<br>
    • ICT-enabled classrooms<br>
    • Gymnasium<br>
    • Sports facilities<br>
    • Stadium and athletic track<br>
    • Football, Hockey and Cricket facilities<br>
    • Basketball, Lawn Tennis and Badminton courts<br>
    • Indoor games facilities<br>
    • Subsidized transport<br>
    • Daycare centre<br>
    • Boys' and Girls' hostels<br>
    • 24-hour power supply<br>
    • Student Centre<br>
    • Cafeteria and canteen<br>
    • ATM facility<br>
    • Digital Language Lab
    """,

    # --------------------------------------------------------
    # SPORTS / GROUND
    # --------------------------------------------------------

    "ground": """
    <strong>🏟️ SPORTS & GROUND</strong><br><br>

    The college has a stadium and athletic track along with
    various sports facilities.<br><br>

    Sports include:<br><br>

    • Football<br>
    • Hockey<br>
    • Cricket<br>
    • Basketball<br>
    • Lawn Tennis<br>
    • Badminton<br>
    • Indoor Games
    """,

    # --------------------------------------------------------
    # PARKING
    # --------------------------------------------------------

    "parking": """
    <strong>🚗 PARKING</strong><br><br>

    Detailed verified information about exact parking areas
    and parking capacity is not available in the current
    college information database.<br><br>

    Please contact the college for current parking details.
    """,

    # --------------------------------------------------------
    # PLACEMENT
    # --------------------------------------------------------

    "placement": """
    <strong>💼 TRAINING & PLACEMENT</strong><br><br>

    The Training and Placement Cell works as a link between
    students, academia and the corporate world.<br><br>

    It provides support through:<br><br>

    • Recruitment drives<br>
    • Placement sessions<br>
    • Career counselling<br>
    • Career guidance<br>
    • Industry-related information<br>
    • Employment opportunities<br><br>

    <strong>Training & Placement Cell:</strong><br>
    98761-73019 / 98148-97939
    """,

    # --------------------------------------------------------
    # CLUBS
    # --------------------------------------------------------

    "clubs": """
    <strong>👥 SOCIETIES & CLUBS</strong><br><br>

    • Big Bang Association<br>
    • Botany and Environment Association<br>
    • Chemical Association<br>
    • Commerce Association<br>
    • Computer Science Students Welfare Association<br>
    • English Literary Society<br>
    • Geography Association<br>
    • Management Association<br>
    • Planning Forum<br>
    • Political Science Association<br>
    • Punjabi Sahit Sabha<br>
    • Zoological Society
    """,

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    "departments": """
    <strong>🏢 DEPARTMENTS</strong><br><br>

    Academic areas include:<br><br>

    • Computer Science<br>
    • Commerce<br>
    • Agriculture<br>
    • Sciences<br>
    • Arts<br>
    • Management<br><br>

    Exact building-by-building department locations are not
    currently available in the information database.
    """,

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    "contact": """
    <strong>📞 CONTACT / OFFICIAL WEBSITE</strong><br><br>

    🌐 Official Website:<br>

    <a href="https://matagujricollege.org/" target="_blank">
    matagujricollege.org
    </a><br><br>

    📧 Email:<br>
    info@matagujricollege.org
    """
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# COMPLETE-WORD / PHRASE MATCH
# ============================================================

def contains_any(text, words):

    text = " " + normalize(text) + " "

    for word in words:

        word = " " + normalize(word) + " "

        if word in text:
            return True

    return False


# ============================================================
# DETECT COLLEGE QUESTION
# ============================================================

def is_college_context(message):

    college_words = [

        # College identity
        "mata gujri",
        "mata gujri college",
        "mgc",
        "college",
        "fatehgarh sahib",
        "fatehgarh",
        "sgpc",

        # Admission
        "admission",
        "admissions",

        # Courses
        "course",
        "courses",
        "program",
        "programme",
        "programmes",
        "ug",
        "undergraduate",
        "pg",
        "postgraduate",
        "diploma",
        "vocational",

        # Fees
        "fee",
        "fees",
        "fee structure",

        # Scholarships
        "scholarship",
        "scholarships",

        # People
        "principal",

        # Departments
        "department",
        "departments",

        # Facilities
        "facility",
        "facilities",
        "hostel",
        "hostels",
        "campus",
        "library",

        # Sports
        "ground",
        "sports",
        "stadium",
        "football",
        "hockey",
        "cricket",
        "basketball",
        "badminton",
        "tennis",

        # Parking
        "parking",

        # Placement
        "placement",
        "placements",

        # Clubs
        "club",
        "clubs",
        "society",
        "societies",

        # Specific courses
        "bca",
        "bba",
        "mca",
        "mba",
        "pgdca",
        "b voc",
        "bvoc",
        "retail management",
        "software development",

        # AI / DS
        "artificial intelligence",
        "data science",
        "ai ds",

        # Contact
        "contact",
        "website",

        # Mission
        "mission"
    ]

    return contains_any(
        message,
        college_words
    )


# ============================================================
# COLLEGE ANSWER
# ============================================================

def get_college_answer(message):

    text = normalize(message)


    # --------------------------------------------------------
    # ADMISSION
    # IMPORTANT: Check admission before mission.
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "admission",
            "admissions",
            "admission process",
            "how to apply",
            "apply for admission",
            "documents required",
            "required documents",
            "admission documents"
        ]
    ):

        return college_info["admission"]


    # --------------------------------------------------------
    # MISSION
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "mission",
            "college mission",
            "mgc mission"
        ]
    ):

        return college_info["mission"]


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "about college",
            "about mgc",
            "about mata gujri",
            "what is mgc",
            "what is mata gujri college",
            "tell me about college",
            "college information",
            "college history",
            "history of college",
            "when was college established"
        ]
    ):

        return college_info["about"]


    # --------------------------------------------------------
    # PRINCIPAL
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "principal",
            "college principal",
            "mgc principal",
            "who is principal"
        ]
    ):

        return college_info["principal"]


    # --------------------------------------------------------
    # UG COURSES
    # --------------------------------------------------------

    if contains_any(
        text,
        [   
            "course",
            "courses",
            "all courses",
            "list of courses",
            "available courses",
            "what courses",
            "program",
            "programs",
            "programme",
            "programmes"
        ]
    ):

        return(

        college_info["ug_courses"]
    + "<br><br>"
    + college_info["pg_courses"]
    + "<br><br>"
    + college_info["diploma"]
    + "<br><br>"
    + college_info["vocational"]
        )



    # --------------------------------------------------------
    # PG COURSES
    # --------------------------------------------------------

    


    # --------------------------------------------------------
    # AI & DATA SCIENCE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "ai ds",
            "ai and ds",
            "artificial intelligence and data science",
            "artificial intelligence data science",
            "bsc ai",
            "bsc ai ds",
            "bsc artificial intelligence"
        ]
    ):

        return college_info["ai_ds"]


    # --------------------------------------------------------
    # DIPLOMA
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "diploma",
            "diplomas",
            "pgdca",
            "pg diploma",
            "post graduate diploma"
        ]
    ):

        return college_info["diploma"]


    # --------------------------------------------------------
    # VOCATIONAL
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "vocational",
            "b voc",
            "bvoc",
            "b vocational",
            "retail management",
            "software development"
        ]
    ):

        return college_info["vocational"]


    # --------------------------------------------------------
    # FEES
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "fee",
            "fees",
            "fee structure",
            "fees structure",
            "course fee",
            "college fee",
            "semester fee"
        ]
    ):

        return college_info["fee"]


    # --------------------------------------------------------
    # SCHOLARSHIP
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "scholarship",
            "scholarships",
            "scholarship scheme",
            "fee concession",
            "financial aid"
        ]
    ):

        return college_info["scholarship"]


    # --------------------------------------------------------
    # FACILITIES
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "facility",
            "facilities",
            "college facilities",
            "campus facilities",
            "what facilities"
        ]
    ):

        return college_info["facilities"]


    # --------------------------------------------------------
    # SPORTS / GROUND
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "ground",
            "sports",
            "stadium",
            "athletic track",
            "football",
            "hockey",
            "cricket",
            "basketball",
            "badminton",
            "lawn tennis",
            "indoor games"
        ]
    ):

        return college_info["ground"]


    # --------------------------------------------------------
    # PARKING
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "parking",
            "car parking",
            "bike parking",
            "vehicle parking"
        ]
    ):

        return college_info["parking"]


    # --------------------------------------------------------
    # PLACEMENT
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "placement",
            "placements",
            "placement cell",
            "training placement",
            "job placement"
        ]
    ):

        return college_info["placement"]


    # --------------------------------------------------------
    # CLUBS / SOCIETIES
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "club",
            "clubs",
            "society",
            "societies",
            "student clubs",
            "associations"
        ]
    ):

        return college_info["clubs"]


    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "department",
            "departments",
            "academic departments"
        ]
    ):

        return college_info["departments"]


    # --------------------------------------------------------
    # CONTACT / WEBSITE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "contact",
            "contact number",
            "phone number",
            "email",
            "email id",
            "website",
            "official website",
            "college website"
        ]
    ):

        return college_info["contact"]


    # --------------------------------------------------------
    # UNKNOWN COLLEGE QUESTION
    # NEVER SEND TO GEMINI
    # --------------------------------------------------------

    return """
    <strong>🏫 Mata Gujri College Information</strong><br><br>

    Sorry, I don't have verified information about this
    college-related question in my current database.<br><br>

    I don't want to give you incorrect information.<br><br>

    Please check the official Mata Gujri College website:<br><br>

    <a href="https://matagujricollege.org/" target="_blank">
    🌐 Official College Website
    </a>
    """


# ============================================================
# GREETING DETECTION
# ============================================================

def is_greeting(message):

    return contains_any(
        message,
        [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "good night"
        ]
    )


# ============================================================
# GREETING RESPONSE
# ============================================================

def greeting_response():

    return """
    👋 Hello! Welcome to
    <strong>Mata Gujri College, Fatehgarh Sahib.</strong>
    <br><br>

    I am your
    <strong>MGC College Information Assistant.</strong>
    <br><br>

    You can ask me about:
    <br><br>

    🎓 Courses<br>
    📝 Admission<br>
    💰 Fees<br>
    🎓 Scholarships<br>
    🏫 Facilities<br>
    👨‍🏫 Principal<br>
    💼 Placement<br>
    🏟️ Sports<br>
    👥 Clubs & Societies<br><br>

    You can also ask general questions and Gemini will
    answer them. 😊
    """


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(message):

    # Gemini is not configured
    if gemini_client is None:

        return """
        <strong>🤖 Gemini is not configured.</strong><br><br>

        Please check the <strong>GEMINI_API_KEY</strong>
        in your <strong>.env</strong> file.
        """


    try:

        prompt = f"""
You are a helpful general-purpose AI assistant.

Answer the user's question in simple, clear and
student-friendly language.

IMPORTANT:

- This request has already been checked and is NOT a
  Mata Gujri College information request.
- Do not invent or provide specific information about
  Mata Gujri College.
- If the user asks about Mata Gujri College, do not guess.
- Give a useful answer to general questions.
- Use examples when helpful.
- Keep the answer reasonably concise.

User question:

{message}
"""


        print("🤖 Calling Gemini...")


        response = gemini_client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt

        )


        if response and response.text:

            return response.text.replace(
                "\n",
                "<br>"
            )


        return """
        Sorry, I could not generate an answer right now.
        """


    except Exception as e:

        print("❌ GEMINI ERROR:")
        print(e)

        return """
        <strong>⚠️ Gemini is temporarily unavailable.</strong><br><br>

        Please try the general question again in a moment.
        """


# ============================================================
# CHAT ROUTE
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "reply": "Please enter a question."
            })


        message = data.get(
            "message",
            ""
        ).strip()


        if not message:

            return jsonify({
                "reply": "Please enter a question."
            })


        print("")
        print("==========================================")
        print("USER:", message)
        print("==========================================")


        # ====================================================
        # 1. GREETING
        # ====================================================

        if is_greeting(message):

            print("👋 GREETING")
            print("➡️ Gemini NOT used")

            return jsonify({
                "reply": greeting_response()
            })


        # ====================================================
        # 2. COLLEGE QUESTION
        #
        # THIS IS THE MOST IMPORTANT PART.
        #
        # If this is a college question:
        #
        #     Gemini will NOT be called.
        #
        # ====================================================

        if is_college_context(message):

            print("🏫 COLLEGE QUESTION DETECTED")
            print("➡️ Using verified college_info")
            print("➡️ Gemini NOT used")

            reply = get_college_answer(
                message
            )

            return jsonify({
                "reply": reply
            })


        # ====================================================
        # 3. GENERAL QUESTION
        #
        # Gemini is used ONLY here.
        # ====================================================

        print("🤖 GENERAL QUESTION DETECTED")
        print("➡️ Gemini will be used")

        reply = ask_gemini(
            message
        )

        return jsonify({
            "reply": reply
        })


    except Exception as e:

        print("")
        print("❌ CHAT ROUTE ERROR:")
        print(e)
        print("")

        return jsonify({
            "reply":
            "❌ Sorry! Something went wrong. Please try again."
        }), 500


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    print("")
    print("==========================================")
    print("     MATA GUJRI COLLEGE CHATBOT")
    print("==========================================")
    print("")

    if GEMINI_API_KEY:
        print("🔑 Gemini API key: FOUND")
        print("🤖 Gemini model:", GEMINI_MODEL)
    else:
        print("⚠️ Gemini API key: NOT FOUND")

    print("")
    print("🌐 Open:")
    print("http://127.0.0.1:5000")
    print("")
    print("==========================================")
    print("")

    app.run(
        debug=True
    )

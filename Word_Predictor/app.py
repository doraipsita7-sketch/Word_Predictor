from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

CORS(app)

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")

# =========================================================
# YOUR DATA
# =========================================================

TEXT = """
astravimaan technologies is an earlystage deeptech startup focused on developing an aienabled defensegrade unmanned aerial system uas for tactical surveillance secure signal intelligence and autonomous mission execution the platform integrates artificial intelligence encrypted communication rf monitoring and precision navigation to operate effectively in hostile and electronically contested environments the startup has been provisionally selected for incubation at emtek centre of entrepreneurship
"""

# =========================================================
# TOKENIZE DATA
# =========================================================

words = re.findall(
    r"\b[\w'-]+\b",
    TEXT.lower()
)

# =========================================================
# PREDICTION API
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input received."
        }), 400


    start_word = str(
        data.get("start_word", "")
    ).strip().lower()


    try:
        token_count = int(
            data.get("tokens", 20)
        )

    except (ValueError, TypeError):

        return jsonify({
            "error": "Invalid token number."
        }), 400


    if start_word == "":

        return jsonify({
            "error": "Starting word is required."
        }), 400


    if token_count < 1:

        return jsonify({
            "error": "Token number must be at least 1."
        }), 400


    # =====================================================
    # FIND STARTING WORD
    # =====================================================

    if start_word not in words:

        return jsonify({
            "error":
            f"'{start_word}' was not found in the dataset."
        }), 404


    start_index = words.index(
        start_word
    )


    # =====================================================
    # GET REQUIRED TOKENS
    # =====================================================

    result_words = words[
        start_index:
        start_index + token_count
    ]


    result_text = " ".join(
        result_words
    )


    # =====================================================
    # SEND RESULT TO UI
    # =====================================================

    return jsonify({

        "text": result_text,

        "tokens": len(result_words)

    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("   AI WORD PREDICTOR")
    print("==========================================")
    print()
    print("Open this in your browser:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
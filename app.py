import os

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from QuizParse import QuizParser, QuizType

# -----------------------------
# Flask Configuration
# -----------------------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}

app = Flask(__name__)
app.secret_key = 'una_chiave_super_segreta'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

parser = None
questions = []


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from flask import abort

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error_message="Pagina non trovata (404)."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", error_message="Errore interno del server (500)."), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    # Qui puoi anche loggare l'errore se vuoi
    return render_template("error.html", error_message=f"Errore inaspettato: {str(e)}"), 500

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", error=None)


@app.route("/upload", methods=["POST"])
def upload_file():
    global parser, questions

    if "quiz_file" not in request.files:
        return render_template("index.html", error="Nessun file selezionato.")

    file = request.files["quiz_file"]
    if file.filename == "":
        return render_template("index.html", error="Nome file vuoto.")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        parser = QuizParser(filepath)
        parser.parse_file()
        questions = sorted(parser.questions, key=lambda q: q.number)

        if not questions:
            return render_template("index.html", error="Il file non contiene domande valide.")

        session.clear()
        session['answers'] = {}
        session['score'] = 0
        session['current_index'] = 0
        return redirect(url_for("quiz"))

    return render_template("index.html", error="Formato file non valido. Usa solo file .txt.")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    global questions

    current_index = session.get("current_index", 0)
    if current_index >= len(questions):
        return redirect(url_for("results"))

    question = questions[current_index]
    user_answer = session.get("last_answer")

    if request.method == "POST":
        if "continue" in request.form:
            # Passa alla domanda successiva
            session.pop("last_answer", None)
            session["current_index"] = current_index + 1
            return redirect(url_for("quiz"))
        else:
            # Salva la risposta utente e aggiorna punteggio
            user_answer = request.form.get("answer")
            session["last_answer"] = user_answer

            answers = session.get("answers", {})
            # Controlla se la risposta è corretta solo se non è già stata data
            if str(question.number) not in answers:
                if user_answer == question.correct_answer:
                    session["score"] = session.get("score", 0) + 1

            answers[str(question.number)] = user_answer
            session["answers"] = answers

    return render_template("quiz.html",
                           question=question,
                           current_index=current_index + 1,
                           total=len(questions),
                           user_answer=user_answer)


@app.route("/results")
def results():
    global questions

    score = session.get("score", 0)
    total = len(questions)
    percentage = (score / total * 100) if total > 0 else 0

    return render_template("results.html",
                           score=score,
                           total=total,
                           percentage=percentage,
                           answers=session.get("answers", {}),
                           questions=questions)



if __name__ == "__main__":
    app.run(debug=True)

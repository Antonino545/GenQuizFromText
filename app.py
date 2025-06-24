import re
import os
from enum import Enum
from typing import List, Dict, Tuple, Optional

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

# -----------------------------
# Enums and Classes
# -----------------------------
class QuizType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"


class Question:
    def __init__(self, number: int, text: str, options: List[Tuple[str, str]], correct_answer: str,
                 quiz_type: QuizType):
        self.number = number
        self.text = text
        self.options = options  # Lista di tuple (lettera, testo_opzione)
        self.correct_answer = correct_answer
        self.quiz_type = quiz_type


class QuizParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.questions: List[Question] = []
        self.answers: Dict[int, str] = {}
        self.quiz_type: Optional[QuizType] = None

    def detect_quiz_type(self, content: str) -> QuizType:
        true_false_pattern = r'\*\s*\(a\)\s*Vero\s*\*\s*\(b\)\s*Falso'
        if re.search(true_false_pattern, content, re.IGNORECASE):
            return QuizType.TRUE_FALSE

        multiple_choice_pattern = r'\*\s*\([a-d]\)'
        matches = re.findall(multiple_choice_pattern, content)
        if len(set(matches)) > 2:
            return QuizType.MULTIPLE_CHOICE

        return QuizType.MULTIPLE_CHOICE

    def parse_answers(self, content: str) -> None:
        if self.quiz_type == QuizType.TRUE_FALSE:
            match = re.search(r'Risposte:\s*(.+)', content)
            if match:
                answer_pairs = re.findall(r'(\d+)\.\(([a-b])\)', match.group(1))
                self.answers = {int(num): letter for num, letter in answer_pairs}
        else:
            match = re.search(r'Risposte:\s*((?:\d+\.\s*\([a-d]\)\s*)+)', content)
            if match:
                answer_pairs = re.findall(r'(\d+)\.\s*\(([a-d])\)', match.group(1))
                self.answers = {int(num): letter for num, letter in answer_pairs}

    def parse_multiple_choice_questions(self, content: str) -> None:
        question_blocks = re.findall(r'(\d+)\.\s+([^*]+)(?:\s*\*\s*([^1-9]+))+', content)
        for block in question_blocks:
            question_num = int(block[0])
            question_text = block[1].strip().split('\n')[0]

            question_start = content.find(question_text)
            if question_start == -1:
                continue

            next_question_match = re.search(r'\n\d+\.\s+', content[question_start + len(question_text):])
            if next_question_match:
                question_section = content[
                    question_start:question_start + len(question_text) + next_question_match.start()]
            else:
                answers_match = re.search(r'\nRisposte:', content[question_start:])
                question_section = content[question_start:] if not answers_match else content[
                    question_start:question_start + answers_match.start()]

            options_pattern = r'\*\s*\(([a-d])\)\s*([^\*]+?)(?=\*\s*\([a-d]\)|\nRisposte:|\n\d+\.|$)'
            options_matches = re.findall(options_pattern, question_section, re.DOTALL)

            options = [(letter, text.strip().split('\n')[0].strip()) for letter, text in options_matches[:4] if text.strip()]
            if question_text and options and question_num in self.answers:
                self.questions.append(Question(question_num, question_text, options, self.answers[question_num], QuizType.MULTIPLE_CHOICE))

    def parse_true_false_questions(self, content: str) -> None:
        question_blocks = re.findall(r'(\d+)\.\s+([^*]+?)\s*\*\s*\(a\)\s*Vero\s*\*\s*\(b\)\s*Falso', content, re.DOTALL)
        for block in question_blocks:
            question_num = int(block[0])
            question_text = block[1].strip()
            options = [("a", "Vero"), ("b", "Falso")]

            if question_num in self.answers:
                self.questions.append(Question(question_num, question_text, options, self.answers[question_num], QuizType.TRUE_FALSE))

    def parse_file(self) -> None:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.quiz_type = self.detect_quiz_type(content)
            self.parse_answers(content)

            if self.quiz_type == QuizType.TRUE_FALSE:
                self.parse_true_false_questions(content)
            else:
                self.parse_multiple_choice_questions(content)


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


@app.route("/quiz_info")
def quiz_info():
    global parser, questions
    quiz_type_display = "Vero/Falso" if parser and parser.quiz_type == QuizType.TRUE_FALSE else "Scelta Multipla"
    return render_template("quiz_info.html",
                           quiz_type=quiz_type_display,
                           total_questions=len(questions),
                           questions=questions)


if __name__ == "__main__":
    app.run(debug=True)

import re
import os
from typing import List, Dict, Tuple
from flask import Flask, render_template, request, redirect, url_for, session


# -----------------------------
# Definizione delle classi
# -----------------------------
class Question:
    def __init__(self, number: int, text: str, options: List[Tuple[str, str]], correct_answer: str):
        self.number = number
        self.text = text
        self.options = options  # Lista di tuple (lettera, testo_opzione)
        self.correct_answer = correct_answer


class QuizParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.questions: List[Question] = []
        self.answers: Dict[int, str] = {}

    def parse_file(self) -> None:
        """Parses the quiz file and extracts questions and answers."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Parse answers first (they're at the bottom of the file)
            answers_match = re.search(r'Risposte:\s*(.+)', content)
            if answers_match:

                answers_str = answers_match.group(1)
                # Parse answers into a dictionary
                answer_pairs = re.findall(r'(\d+)\.\(([a-d])\)', answers_str)
                self.answers = {int(num): letter for num, letter in answer_pairs}

            # Parse questions
            question_blocks = re.findall(r'(\d+)\.\s+([^*]+)(?:\s*\*\s*([^1-9]+))+', content)

            for block in question_blocks:
                question_num = int(block[0])
                question_text = block[1].strip()

                # Find all options for this question
                options_pattern = r'\*\s*\(([a-d])\)\s*([^\*]+?)(?=\*\s*\([a-d]\)|$)'
                options_matches = re.findall(options_pattern, content[content.find(question_text):].split('/n')[0])

                # Extract only the first 4 options
                options = [(letter, text.split('\n')[0].strip()) for letter, text in options_matches[:4]]

                # Create Question object
                if question_num in self.answers:
                    self.questions.append(Question(
                        question_num,
                        question_text,
                        options,
                        self.answers[question_num]
                    ))



# -----------------------------
# Configurazione Flask
# -----------------------------
app = Flask(__name__)
app.secret_key = 'una_chiave_super_segreta'  # Sostituisci con una chiave sicura

# Carica le domande dal file quiz.txt
parser = QuizParser("quiz.txt")
parser.parse_file()
# Ordina le domande per numero
questions = sorted(parser.questions, key=lambda q: q.number)


# -----------------------------
# Routes dell'applicazione
# -----------------------------
@app.route("/")
def index():
    session.clear()
    session['answers'] = {}   # Salveremo le risposte fornite
    session['score'] = 0
    session['current_index'] = 0  # indice della domanda corrente
    session.pop("last_answer", None)
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    current_index = session.get("current_index", 0)
    if current_index >= len(questions):
        return redirect(url_for("results"))

    question = questions[current_index]
    user_answer = session.get("last_answer")

    if request.method == "POST":
        if "continue" in request.form:
            # Pulisce la risposta precedente e passa alla domanda successiva
            session.pop("last_answer", None)
            session["current_index"] = current_index + 1
            return redirect(url_for("quiz"))
        else:
            # Salva la risposta dell'utente
            user_answer = request.form.get("answer")
            session["last_answer"] = user_answer
            # Aggiorna il punteggio se la risposta è corretta
            if user_answer == question.correct_answer:
                session["score"] = session.get("score", 0) + 1
            # Salva anche la risposta dell'utente nel dizionario generale (opzionale)
            answers = session.get("answers", {})
            answers[str(question.number)] = user_answer
            session["answers"] = answers

    return render_template("quiz.html",
                           question=question,
                           current_index=current_index + 1,
                           total=len(questions),
                           user_answer=user_answer)

@app.route("/results")
def results():
    return render_template("results.html",
                           score=session.get("score", 0),
                           total=len(questions),
                           answers=session.get("answers", {}),
                           questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
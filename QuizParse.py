from enum import Enum
from typing import List, Dict, Tuple, Optional
import re


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


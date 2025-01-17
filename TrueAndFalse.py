import re
from typing import List, Dict, Tuple
import os


class Question:
    def __init__(self, number: int, text: str, options: List[str], correct_answer: str):
        self.number = number
        self.text = text
        self.options = options
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

            # Parse answers (at the end of the file)
            answers_match = re.search(r'Risposte:\s*(.+)', content)
            if answers_match:
                answers_str = answers_match.group(1)
                # Parse answers into a dictionary
                answer_pairs = re.findall(r'(\d+)\.\(([a-b])\)', answers_str)
                self.answers = {int(num): letter for num, letter in answer_pairs}

            # Parse questions
            question_blocks = re.findall(r'(\d+)\.\s+([^*]+?)\s*\*\s*\(a\)\s*Vero\s*\*\s*\(b\)\s*Falso', content, re.DOTALL)

            for block in question_blocks:
                question_num = int(block[0])
                question_text = block[1].strip()

                # Options (always "Vero" and "Falso")
                options = [
                    ("a", "Vero"),
                    ("b", "Falso")
                ]

                # Create Question object if the answer exists
                if question_num in self.answers:
                    self.questions.append(Question(
                        question_num,
                        question_text,
                        options,
                        self.answers[question_num]
                    ))


class QuizRunner:
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.score = 0
        self.answers = {}

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        """Runs the interactive quiz."""
        self.clear_screen()
        print("=== Quiz Interattivo ===\n")

        for question in self.questions:
            print(f"\nDomanda {question.number}:")
            print(question.text)
            print("\nOpzioni:")

            for letter, text in question.options:

                text=text.split('\n')[0]
                print(f"{letter}) {text}\n")

            while True:
                answer = input("\nLa tua risposta (a/b/c/d) o 'q' per uscire: ").lower()

                if answer == 'q':
                    return

                if answer in ['a', 'b', 'c', 'd']:
                    self.answers[question.number] = answer
                    if answer == question.correct_answer:
                        self.score += 1
                        print("\n✅ Corretto!")
                    else:
                        print(f"\n❌ Sbagliato. La risposta corretta era: ({question.correct_answer})")

                    input("\nPremi Enter per continuare...")
                    self.clear_screen()
                    break
                else:
                    print("Risposta non valida. Inserisci a, b, c, o d.")

        self.show_results()

    def show_results(self):
        """Shows the final results of the quiz."""
        print("\n=== Risultati del Quiz ===")
        print(f"\nPunteggio finale: {self.score}/{len(self.questions)}")
        percentage = (self.score / len(self.questions)) * 100
        print(f"Percentuale corretta: {percentage:.1f}%")

        print("\nRiepilogo risposte:")
        for question in self.questions:
            user_answer = self.answers.get(question.number, '-')
            print(f"Domanda {question.number}: Tua risposta: ({user_answer}), "
                  f"Risposta corretta: ({question.correct_answer})")


def main():
    # Esempio di utilizzo
    try:
        parser = QuizParser("quiz.txt")
        parser.parse_file()

        if not parser.questions:
            print("Nessuna domanda trovata nel file!")
            return

        quiz = QuizRunner(parser.questions)
        quiz.run()

    except FileNotFoundError:
        print("File quiz.txt non trovato!")
    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")


if __name__ == "__main__":
    main()
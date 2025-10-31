import tkinter as tk
from tkinter import messagebox
import random

class MathsQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("400x300")
        
        self.difficulty = None
        self.score = 0
        self.question_num = 0
        self.attempts = 0
        self.current_answer = 0
        self.current_operation = ''
        self.num1 = 0
        self.num2 = 0
        
        self.displayMenu()
    
    def displayMenu(self):
        self.clearWindow()
        
        title = tk.Label(self.root, text="MATHS QUIZ", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="DIFFICULTY LEVEL")
        subtitle.pack(pady=10)
        
        easy_btn = tk.Button(self.root, text="1. Easy", width=20,
                            command=lambda: self.startQuiz(1))
        easy_btn.pack(pady=5)
        
        moderate_btn = tk.Button(self.root, text="2. Moderate", width=20,
                                command=lambda: self.startQuiz(2))
        moderate_btn.pack(pady=5)
        
        advanced_btn = tk.Button(self.root, text="3. Advanced", width=20,
                                command=lambda: self.startQuiz(3))
        advanced_btn.pack(pady=5)
    
    def randomInt(self, difficulty):
        if difficulty == 1:
            return random.randint(1, 9)
        elif difficulty == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)
    
    def decideOperation(self):
        return random.choice(['+', '-'])
    
    def startQuiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_num = 0
        self.nextQuestion()
    
    def nextQuestion(self):
        if self.question_num >= 10:
            self.displayResults()
            return
        
        self.question_num += 1
        self.attempts = 0
        self.num1 = self.randomInt(self.difficulty)
        self.num2 = self.randomInt(self.difficulty)
        self.current_operation = self.decideOperation()
        
        if self.current_operation == '+':
            self.current_answer = self.num1 + self.num2
        else:
            self.current_answer = self.num1 - self.num2
        
        self.displayProblem()
    
    def displayProblem(self):
        self.clearWindow()
        
        progress = tk.Label(self.root, text=f"Question {self.question_num}/10    Score: {self.score}/100")
        progress.pack(pady=20)
        
        problem_text = f"{self.num1} {self.current_operation} {self.num2} ="
        problem_label = tk.Label(self.root, text=problem_text, font=("Arial", 18))
        problem_label.pack(pady=20)
        
        if self.attempts > 0:
            hint = tk.Label(self.root, text="(Second attempt - 5 points)")
            hint.pack()
        
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14), width=10)
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        submit_btn = tk.Button(self.root, text="Submit", width=15,
                             command=self.checkAnswer)
        submit_btn.pack(pady=10)
    
    def checkAnswer(self):
        try:
            user_answer = int(self.answer_entry.get())
            self.isCorrect(user_answer)
        except ValueError:
            messagebox.showerror("Error", "Please enter a number!")
            self.answer_entry.delete(0, tk.END)
    
    def isCorrect(self, user_answer):
        if user_answer == self.current_answer:
            if self.attempts == 0:
                self.score += 10
                messagebox.showinfo("Correct!", "Well done! +10 points")
            else:
                self.score += 5
                messagebox.showinfo("Correct!", "Good! +5 points")
            self.nextQuestion()
        else:
            self.attempts += 1
            if self.attempts < 2:
                messagebox.showwarning("Wrong", "Try again!")
                self.displayProblem()
            else:
                messagebox.showinfo("Wrong", f"The answer was {self.current_answer}")
                self.nextQuestion()
    
    def displayResults(self):
        self.clearWindow()
        
        title = tk.Label(self.root, text="Quiz Finished!", font=("Arial", 16, "bold"))
        title.pack(pady=30)
        
        score_label = tk.Label(self.root, text=f"Your Score: {self.score}/100", font=("Arial", 14))
        score_label.pack(pady=10)
        
        grade, color = self.getGrade()
        grade_label = tk.Label(self.root, text=f"Grade: {grade}", font=("Arial", 20, "bold"))
        grade_label.pack(pady=10)
        
        play_again_btn = tk.Button(self.root, text="Play Again", width=15,
                                   command=self.displayMenu)
        play_again_btn.pack(pady=10)
        
        quit_btn = tk.Button(self.root, text="Quit", width=15,
                           command=self.root.quit)
        quit_btn.pack(pady=5)
    
    def getGrade(self):
        if self.score >= 90:
            return "A+", "#27ae60"
        elif self.score >= 80:
            return "A", "#2ecc71"
        elif self.score >= 70:
            return "B", "#3498db"
        elif self.score >= 60:
            return "C", "#f39c12"
        elif self.score >= 50:
            return "D", "#e67e22"
        else:
            return "F", "#e74c3c"
    
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizGUI(root)
    root.mainloop()
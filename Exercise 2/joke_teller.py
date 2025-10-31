import tkinter as tk
from tkinter import messagebox
import random
import os

class JokeTeller:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        #### Get the directory where this script is located ####
        script_dir = os.path.dirname(os.path.abspath(__file__))
        jokes_file = os.path.join(script_dir, 'randomJokes.txt')
        
        self.jokes = self.load_jokes(jokes_file)
        self.current_joke = None
        self.showing_punchline = False
        
        # Title Label #
        self.title_label = tk.Label(root, text="Alexa Joke Teller", 
                                    font=("Arial", 20, "bold"),
                                    bg="#2312a5", fg='white')
        self.title_label.pack(pady=20)
        
        # Joke Display #
        self.joke_text = tk.Text(root, height=8, width=50, 
                                font=("Arial", 12),
                                wrap=tk.WORD, bg='#ecf0f1',
                                state=tk.DISABLED)
        self.joke_text.pack(pady=20, padx=20)
        
        # Command Entry #
        self.entry = tk.Entry(root, font=("Arial", 12), width=40)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda e: self.process_command())
        
        # Button #
        self.button = tk.Button(root, text="Tell Me a Joke", 
                               font=("Arial", 12, "bold"),
                               bg='#3498db', fg='white',
                               command=self.process_command,
                               width=20, height=2)
        self.button.pack(pady=10)
        
        self.show_instructions()
    
    def load_jokes(self, filename):
        jokes = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and '?' in line:
                        parts = line.split('?', 1)
                        setup = parts[0].strip() + '?'
                        punchline = parts[1].strip()
                        jokes.append((setup, punchline))
        except FileNotFoundError:
            messagebox.showerror("Error", f"{filename} not found!")
        return jokes
    
    def show_instructions(self):
        self.update_display('Type "Alexa tell me a Joke" and press Enter\nor click the button!')
    
    def update_display(self, text):
        self.joke_text.config(state=tk.NORMAL)
        self.joke_text.delete(1.0, tk.END)
        self.joke_text.insert(1.0, text)
        self.joke_text.config(state=tk.DISABLED)
    
    def process_command(self):
        command = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        
        if command == "alexa tell me a joke" or command == "":
            if not self.showing_punchline:
                self.tell_joke()
            else:
                self.show_punchline()
        else:
            self.update_display('Please type "Alexa tell me a Joke"')
    
    def tell_joke(self):
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available!")
            return
        
        self.current_joke = random.choice(self.jokes)
        self.update_display(self.current_joke[0])
        self.showing_punchline = True
        self.button.config(text="Show Punchline")
    
    def show_punchline(self):
        if self.current_joke:
            self.update_display(f"{self.current_joke[0]}\n\n{self.current_joke[1]}")
            self.showing_punchline = False
            self.button.config(text="Tell Me a Joke")

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTeller(root)
    root.mainloop()
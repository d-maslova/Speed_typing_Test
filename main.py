import tkinter as tk
from tkinter import ttk, messagebox
import difflib
import os


class SpeedTypeTest:
    def __init__(self, main):
        # create the window
        self.main = main
        self.main.title("Speed Typing Test")
        self.main.config(width=100, height=40,
                         padx=20, pady=20)
        self.canvas = tk.Canvas(width=200, height=224, highlightthickness=0)

        # set vars for typing test
        self.get_text = tk.StringVar()
        self.get_text.set("Consequently, the clubrooms became deserted, the servants dozed in the antechambers,"
                          " the newspapers grew mouldy on the tables, sounds of snoring came from dark corners,"
                          " and the members of the Gun Club, erstwhile so noisy in their seances,"
                          " were reduced to silence by this disastrous peace and gave themselves"
                          " up wholly to dreams of a Platonic kind of artillery.")
        self.minute = 1
        self.type_test = self.get_text.get()

        # ## GUI ## #
        # Labels
        self.top_label = tk.Label(text="TEST YOUR SKILLS", font=("Century Gothic", 24))
        self.top_label.grid(row=0, column=0, columnspan=3, pady=20)
        self.timer_label = self.canvas.create_text(100, 130, text=60, font=("Century Gothic", 24))
        self.canvas.grid(row=1, column=2, ipady=5)
        # Text
        self.text = tk.Text(width=50, height=8, wrap="word", font=("Century Gothic", 15))
        self.text.insert(tk.INSERT, self.type_test)
        self.first_letter = self.type_test[0][0]
        self.text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="W")

        self.user_input = tk.Text(width=60, height=4, wrap="word", font=("Century Gothic", 12))
        self.user_input.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipady=5, ipadx=5, sticky="E")
        self.user_input.focus()
        self.user_input.bind(self.first_letter, func=self.start_time)

        # Scroll
        self.scroll = ttk.Scrollbar(orient="vertical", command=self.user_input.yview)
        self.scroll.grid(row=2, column=1, sticky=tk.E)
        self.user_input["yscrollcommand"] = self.scroll.set

        # Button
        self.restart_btn = tk.Button(text="Try Again", height=6, width=10, command=self.retry)
        self.restart_btn.grid(row=2, column=2, sticky="N", pady=7)

    def start_time(self, event):
        self.user_input.unbind(self.first_letter)
        self.timer(count=60)

    def timer(self, count):
        if count > -1:
            self.canvas.itemconfig(self.timer_label, text=count)
            self.main.after(1000, self.timer, count-1)
        if count == 0:
            self.check_mistakes()

    def check_mistakes(self):
        # set a counter for uncorrected errors
        self.mistakes = 0
        # count all characters the user has typed
        self.result = self.user_input.get("1.0", tk.END).rstrip()
        self.all_chars = len(self.result)

        # Makes test and users typings into list of words
        user = self.result.split(" ")
        test = self.type_test.split(" ")

        for user_word, test_word in zip(user, test[:self.all_chars]):
            if len(user_word) != len(test_word):
                seq = difflib.SequenceMatcher(None, user_word, test_word)
                d = round(seq.ratio())
                self.mistakes += d
            else:
                for char in range(len(test_word)):
                    if user_word[char] != test_word[char]:
                        self.mistakes += 1

        return self.calculate_wpm(self.mistakes, self.all_chars)

    def calculate_wpm(self, mistakes, num_chars):
        num_words = num_chars // 5
        gross_wpm = num_words / self.minute  # Number of words divided by time
        net_wpm = int(gross_wpm - (mistakes / self.minute))  # gross wpm minus (number of mistakes/time)
        return tk.messagebox.showinfo(title="TIME'S UP!",
                                            message=f"Your WPM score is: {net_wpm}.\n"
                                                    f"You made {self.mistakes} mistakes.")

    def retry(self):
        self.main.destroy()
        os.startfile("main.py")


root = tk.Tk()
type_test = SpeedTypeTest(root)
root.mainloop()

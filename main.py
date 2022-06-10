import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SpeedTypeTest:
    def __init__(self, main):
        # create the window
        self.main = main
        self.main.title("Speed Typing Test")
        self.main.config(width=100, height=40,
                         padx=20, pady=20)
        # self.canvas = tk.Canvas(width=200, height=224, highlightthickness=0)
        # self.circle_img = tk.PhotoImage("orange.png")
        # self.canvas.create_image(100, 100, image=self.circle_img)
        # self.canvas.grid(row=1, column=2)

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
        self.timer_label = tk.Label(text=60, font=("Century Gothic", 33), padx=30)
        self.timer_label.grid(row=1, column=2, ipady=5)

        # Text
        self.text = tk.Text(width=50, height=10, wrap="word", font=("Century Gothic", 18))
        self.text.insert(tk.INSERT, self.type_test)
        self.text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="W")

        self.user_input = tk.Text(width=59, height=4, wrap="word", font=("Century Gothic", 15))
        self.user_input.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipady=5, ipadx=5, sticky="E")
        self.user_input.focus()

        # Scroll
        self.scroll = ttk.Scrollbar(orient="vertical", command=self.user_input.yview)
        self.scroll.grid(row=2, column=1, sticky=tk.E)
        self.user_input["yscrollcommand"] = self.scroll.set

        # Button
        self.restart_btn = tk.Button(text="Check", height=6, width=10, command=self.check_mistakes)
        self.restart_btn.grid(row=2, column=2, sticky="N", pady=7)

    def check_mistakes(self):
        # set a counter for uncorrected errors
        self.mistakes = 0
        # count all characters the user has typed
        self.result = self.user_input.get("1.0", tk.END).rstrip()
        self.all_chars = len(self.result)
        # Makes test and users typings into list of words
        self.user = self.result.split(" ")
        self.test = self.type_test[:self.all_chars].split(" ")
        for user, test in zip(self.user, self.test):
            if user != test:
                for char in range(len(user)):
                    if user[char] != test[char]:
                        self.mistakes += 1
        return self.calculate_wpm(self.mistakes, self.all_chars), print(f"mistakes: {self.mistakes}")

    def calculate_wpm(self, mistakes, num_chars):
        num_words = num_chars//5
        gross_wpm = num_words/self.minute  # Number of words divided by time
        net_wpm = int(gross_wpm - (mistakes/self.minute))  # gross wpm minus (number of mistakes/time)
        return print(f"Net WPM: {net_wpm}")


root = tk.Tk()
type_test = SpeedTypeTest(root)
root.mainloop()

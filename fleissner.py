import tkinter as tk
from tkinter import filedialog, messagebox
import random

class Fleissner:
    def __init__(self):
        self.__size = 0
        self.__box_size = 50
        self.__square_colors = {}
        self.__x0 = 0
        self.__y0 = 0
        self.__x1 = 0
        self.__y1 = 0
        self.__square_white = []
        self.__square_grey_2 = []
        self.__square_grey_3 = []
        self.__square_grey_4 = []

        self.root = tk.Tk()
        self.root.title("Fleissner")

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        # Grille
        self.canvas = tk.Canvas(self.grid_frame)
        self.canvas.pack(side=tk.LEFT)

        # Boutons de droite
        self.button_frame = tk.Frame(self.grid_frame)
        self.button_frame.pack(side=tk.RIGHT, padx=10)

        self.button_random = tk.Button(self.button_frame, text="Random", command=self.drawColors)
        self.button_random.pack()

        self.load_button_pressed = tk.BooleanVar()
        self.load_button_pressed.set(False)

        self.button_load = tk.Button(self.button_frame, text="Load", command=self.load)
        self.button_load.pack()

        self.button_save = tk.Button(self.button_frame, text="Save", command=self.save)
        self.button_save.pack()

        self.create_var = tk.BooleanVar()
        self.create_checkbox = tk.Checkbutton(self.button_frame, text="Create", variable=self.create_var)
        self.create_checkbox.pack()

        self.clock_var = tk.BooleanVar()
        self.clock_checkbox = tk.Checkbutton(self.button_frame, text="Clock", variable=self.clock_var)
        self.clock_checkbox.pack()

        # Boutons du bas
        self.label = tk.Label(self.root, text="Grid size :")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.button_draw = tk.Button(self.root, text="Draw", command=self.drawSquares)
        self.button_draw.pack()

        self.label_message = tk.Label(self.root, text="Clear :")
        self.label_message.pack()

        self.entry_message = tk.Entry(self.root)
        self.entry_message.pack()
        self.__text = self.entry_message.get()

        self.button_encrypt = tk.Button(self.root, text="Cipher", command=self.cipher)
        self.button_encrypt.pack()

        self.label_message2 = tk.Label(self.root, text="Cipher :")
        self.label_message2.pack()

        self.entry_message2 = tk.Entry(self.root)
        self.entry_message2.pack()
        self.__text2 = self.entry_message2.get()

        self.button_decrypt = tk.Button(self.root, text="Decipher", command=self.decipher)
        self.button_decrypt.pack()

        self.button_clear = tk.Button(self.root, text="Clear", command=self.clearButton)
        self.button_clear.pack()

        self.canvas.bind("<Button-1>", self.putSquare)

    def clearButton(self):
        self.entry_message.delete(0, tk.END)
        self.entry_message2.delete(0, tk.END)

    def cleanText(self):
        cleaned_text = ''
        text = self.entry_message.get().lower()
        for i in text:
            if 97 <= ord(i) <= 122:
                cleaned_text += i
        return cleaned_text

    def cipher(self):
        cleaned_text = self.cleanText()
        self.__text = cleaned_text

        if not self.__text:
            tk.messagebox.showwarning("Warning", "Please enter a text to cipher.")
            return

        if not self.__square_colors:
            tk.messagebox.showerror("Error", "Please load or create a key to cipher the message.")
            return

        letters = [letter for letter in self.__text if letter.isalpha()]

        white_squares_sorted = sorted(self.__square_white, key=lambda square: (square[1], square[0]))
        grey_2_squares_sorted = sorted(self.__square_grey_2, key=lambda square: (square[1], square[0]))
        grey_3_squares_sorted = sorted(self.__square_grey_3, key=lambda square: (square[1], square[0]))
        grey_4_squares_sorted = sorted(self.__square_grey_4, key=lambda square: (square[1], square[0]))

        if (self.__size % 2 == 1) and ((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size) in self.__square_white):
            white_squares_sorted.remove((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size))

        white_square_count = len(white_squares_sorted)
        grey_2_square_count = len(grey_2_squares_sorted)
        grey_3_square_count = len(grey_3_squares_sorted)
        grey_4_square_count = len(grey_4_squares_sorted)

        total_squares_count = white_square_count + grey_2_square_count + grey_3_square_count + grey_4_square_count

        if len(letters) > total_squares_count:
            self.__suite = letters[total_squares_count:]
            letters = letters[:total_squares_count]

        if len(letters) < total_squares_count:
            letters += [chr(random.randint(97, 122)) for i in range(total_squares_count - len(letters))]


        letters_in_order = {}

        self.canvas.delete("deciphered_letters")
        self.canvas.delete("cipher_letters")

        for i, letter in enumerate(letters):
            if self.clock_var.get():
                if i < white_square_count:
                    x, y = white_squares_sorted[i]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                elif i < grey_2_square_count + white_square_count:
                    x, y = grey_2_squares_sorted[i - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                elif i < grey_3_square_count + white_square_count + grey_2_square_count:
                    x, y = grey_3_squares_sorted[i - grey_2_square_count - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                else:
                    x, y = grey_4_squares_sorted[i - grey_2_square_count - grey_3_square_count - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
            else:
                if i < white_square_count:
                    x, y = white_squares_sorted[i]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                elif i < grey_4_square_count + white_square_count:
                    x, y = grey_4_squares_sorted[i - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                elif i < grey_3_square_count + white_square_count + grey_4_square_count:
                    x, y = grey_3_squares_sorted[i - grey_2_square_count - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter
                else:
                    x, y = grey_2_squares_sorted[i - grey_4_square_count - grey_3_square_count - white_square_count]
                    self.canvas.create_text(x + self.__box_size/2, y + self.__box_size/2, text=letter, font=("Arial", 12), fill="black", tags="cipher_letters")
                    letters_in_order[(y, x)] = letter

        sorted_letters = []
        for key in sorted(letters_in_order.keys()):
            sorted_letters.append(letters_in_order[key])

        sorted_text = ''.join(sorted_letters)
        self.entry_message2.delete(0, tk.END)
        self.entry_message2.insert(0, sorted_text)

    def decipher(self):
        sorted_text = self.entry_message2.get()

        if not sorted_text:
            tk.messagebox.showwarning("Warning", "Please enter a text to decipher.")
            return

        if not self.__square_colors:
            tk.messagebox.showerror("Error", "Please load a key to decipher the message.")
            return

        white_squares_sorted = sorted(self.__square_white, key=lambda square: (square[1], square[0]))
        grey_2_squares_sorted = sorted(self.__square_grey_2, key=lambda square: (square[1], square[0]))
        grey_3_squares_sorted = sorted(self.__square_grey_3, key=lambda square: (square[1], square[0]))
        grey_4_squares_sorted = sorted(self.__square_grey_4, key=lambda square: (square[1], square[0]))

        if (self.__size % 2 == 1) and ((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size) in self.__square_white):
            white_squares_sorted.remove((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size))
        elif (self.__size % 2 == 1) and ((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size) in self.__square_grey_4):
            grey_4_squares_sorted.remove((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size))
        elif (self.__size % 2 == 1) and ((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size) in self.__square_grey_3):
            grey_3_squares_sorted.remove((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size))
        elif (self.__size % 2 == 1) and ((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size) in self.__square_grey_2):
            grey_2_squares_sorted.remove((self.__size // 2 * self.__box_size, self.__size // 2 * self.__box_size))

        deciphered_text = ""

        all_squares = white_squares_sorted + grey_2_squares_sorted + grey_3_squares_sorted + grey_4_squares_sorted
        all_squares_sorted = sorted(all_squares, key=lambda square: (square[1], square[0]))

        letters_in_order = {}

        if self.clock_var.get():
            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    color = self.__square_colors[(x, y)]
                    if color == "white":
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_2:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_3:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_4:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char
        else:
            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    color = self.__square_colors[(x, y)]
                    if color == "white":
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_4:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_3:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

            for i, char in enumerate(sorted_text):
                if i < len(all_squares_sorted):
                    x, y = all_squares_sorted[i]
                    if (x, y) in self.__square_grey_2:
                        deciphered_text += char
                    letters_in_order[(x, y)] = char

        self.canvas.delete("deciphered_letters")
        self.canvas.delete("cipher_letters")

        for y in range(0, self.__size * self.__box_size, self.__box_size):
            for x in range(0, self.__size * self.__box_size, self.__box_size):
                letter = letters_in_order.get((x, y), '')
                self.canvas.create_text(x + self.__box_size / 2, y + self.__box_size / 2, text=letter, font=("Arial", 12), fill="black", tags="deciphered_letters")

        self.entry_message.delete(0, tk.END)
        self.entry_message.insert(0, deciphered_text)

    def drawSquares(self):
        self.canvas.delete("all")
        size_text = self.entry.get()

        if size_text:
            self.__size = int(size_text)
            if self.__size > 15:
                self.__box_size = 25
            else:
                self.__box_size = 50
        else:
            return

        self.__square_colors = {}

        for i in range(self.__size):
            for j in range(self.__size):
                x1 = i * self.__box_size
                y1 = j * self.__box_size
                x2 = x1 + self.__box_size
                y2 = y1 + self.__box_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="blue")
                self.__square_colors[(x1, y1)] = "black"
                self.calculateSize()

    def drawColors(self):
        self.__square_white = []
        self.__square_grey_2 = []
        self.__square_grey_3 = []
        self.__square_grey_4 = []

        if self.__size % 2 == 0:
            n = self.__size**2 // 4
        else:
            n = ((self.__size**2) - 1) // 4

        for i in range(n):
            self.whiteSquare(self.__box_size)
            self.greySquare3(self.__box_size)
            self.greySquare4(self.__box_size)
            self.greySquare2(self.__box_size)

    def calculateSize(self):
        canvas_width = self.__size * self.__box_size
        canvas_height = self.__size * self.__box_size
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.root.geometry(f"{canvas_width + 100}x{canvas_height + 250}")

    def whiteSquare(self, size):
        self.__x0 = random.randint(0, self.__size - 1) * size
        self.__y0 = random.randint(0, self.__size - 1) * size
        if (self.__x0, self.__y0) not in self.__square_white and \
                (self.__x0, self.__y0) not in self.__square_grey_2 and \
                (self.__x0, self.__y0) not in self.__square_grey_3 and \
                (self.__x0, self.__y0) not in self.__square_grey_4 and \
                not (self.__size % 2 == 1 and self.__x0 == self.__y0 == (self.__size // 2) * self.__box_size):
            self.canvas.create_rectangle(self.__x0, self.__y0, self.__x0 + size, self.__y0 + size, fill="white", outline="black")
            self.__square_white.append((self.__x0, self.__y0))
            self.__square_colors[(self.__x0, self.__y0)] = "white"
        else:
            self.whiteSquare(size)

    def greySquare3(self, size):
        self.__x1 = (self.__size - 1) * size - self.__x0
        self.__y1 = (self.__size - 1) * size - self.__y0
        if not (self.__size % 2 == 1 and self.__x0 == self.__y0 == (self.__size // 2) * self.__box_size):
            self.canvas.create_rectangle(self.__x1, self.__y1, self.__x1 + size, self.__y1 + size, fill="grey", outline="black")
            self.__square_grey_3.append((self.__x1, self.__y1))
            self.__square_colors[(self.__x1, self.__y1)] = "grey"

    def greySquare4(self, size):
        x2 = abs(self.__y1 - self.__x1 - self.__x0)
        y2 = self.__x1
        if not (self.__size % 2 == 1 and self.__x0 == self.__y0 == (self.__size // 2) * self.__box_size):
            self.canvas.create_rectangle(x2, y2, x2 + size, y2 + size, fill="grey", outline="black")
            self.__square_grey_4.append((x2, y2))
            self.__square_colors[(x2, y2)] = "grey"

    def greySquare2(self, size):
        x3 = self.__y1
        y3 = self.__x0
        if not (self.__size % 2 == 1 and self.__x0 == self.__y0 == (self.__size // 2) * self.__box_size):
            self.canvas.create_rectangle(x3, y3, x3 + size, y3 + size, fill="grey", outline="black")
            self.__square_grey_2.append((x3, y3))
            self.__square_colors[(x3, y3)] = "grey"

    def load(self):
        file_path = filedialog.askopenfilename(title="Select a key file", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()
                self.__size = len(lines[0].strip())
                if self.__size > 15:
                    self.__box_size = 25
                else:
                    self.__box_size = 50
                self.drawSquares()
                for j, line in enumerate(lines):
                    for i, char in enumerate(line.strip()):
                        x, y = i * self.__box_size, j * self.__box_size
                        color = "white" if char == "1" else "gray"
                        self.__square_colors[(x, y)] = color

                        if color == "white":
                            self.__square_white.append((x, y))
                            self.__x0, self.__y0 = x, y
                            self.greySquare3(self.__box_size)
                            self.greySquare4(self.__box_size)
                            self.greySquare2(self.__box_size)

                        self.canvas.create_rectangle(x, y, x + self.__box_size, y + self.__box_size, fill=color, outline="black")

                self.calculateSize()

            if self.__size % 2 == 1:
                mid = self.__size // 2 * self.__box_size
                self.canvas.create_rectangle(mid, mid, mid + self.__box_size, mid + self.__box_size, fill="black", outline="black")
                self.__square_colors[(mid, mid)] = "black"

    def save(self):
        file_path = filedialog.asksaveasfilename(title="Save the key", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for j in range(self.__size):
                    for i in range(self.__size):
                        if self.__square_colors[(i * self.__box_size, j * self.__box_size)] == "white":
                            file.write("1")
                        else:
                            file.write("0")
                    file.write("\n")

    def putSquare(self, event):
        if self.create_var.get():
            if self.__size % 2 == 1 and event.x // self.__box_size == self.__size // 2 and event.y // self.__box_size == self.__size // 2:
                tk.messagebox.showwarning("Warning", "You can't fill the middle in an odd grid.")
                return

            self.__x0 = event.x // self.__box_size * self.__box_size
            self.__y0 = event.y // self.__box_size * self.__box_size
            if (self.__x0, self.__y0) not in self.__square_white and \
                    (self.__x0, self.__y0) not in self.__square_grey_2 and \
                    (self.__x0, self.__y0) not in self.__square_grey_3 and \
                    (self.__x0, self.__y0) not in self.__square_grey_4:
                self.canvas.create_rectangle(self.__x0, self.__y0, self.__x0 + self.__box_size, self.__y0 + self.__box_size, fill="white", outline="black")
                self.__square_white.append((self.__x0, self.__y0))
                self.__square_colors[(self.__x0, self.__y0)] = "white"
            self.greySquare3(self.__box_size)
            self.greySquare4(self.__box_size)
            self.greySquare2(self.__box_size)

    def run(self):
        self.root.mainloop()

app = Fleissner()
app.run()
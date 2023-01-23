import customtkinter as ctk

from random import choice

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def puzzle_digits():
    nums = [str(x) for x in range(10)]
    my_nums = []
    for _ in range(4):
        if len(my_nums) == 0:
            c = choice(nums[1:])
        else:
            c = choice(nums)
        nums.remove(c)
        my_nums.append(c)
    return my_nums


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sayi Bulmaca")
        self.geometry(f"{450}x{600}")
        self.resizable(False, True)
        self.puzzle = puzzle_digits()
        self.x_cord = 0.05
        self.y_cord = 0.02
        self.p_label = None
        self.m_label = None
        self.won = False
        self.count = 1
        self.entries = self.create_entry_boxes()
        self.entries[0].after(10, self.entries[0].focus)
        self.button = ctk.CTkButton(
            master=self, width=25, height=35,
            border_width=1, text='GUESS', corner_radius=10,
            font=('arial bold', 20), fg_color='#a47c48',
            hover_color='#d89948', text_color='#5b4d41',
            command=self.guess_number
        )
        self.button.place(relx=0.75, rely=self.y_cord)
        self.bind('<Return>', lambda event: self.guess_number())

    def create_entry_boxes(self, entry_dict: dict = None):
        entries = dict()
        for c in range(4):
            entries[c] = ctk.CTkEntry(master=self, justify=ctk.CENTER, width=25, height=25,
                                      border_width=1, font=('arial bold', 25),
                                      corner_radius=10, fg_color='#475597',
                                      )
            entries[c].place(relx=self.x_cord, rely=self.y_cord)
            self.x_cord += 0.1
        self.x_cord = 0.05
        return entries

    def replace(self, entry):
        entry.place(relx=self.x_cord, rely=self.y_cord)

    def guess_number(self):
        guess_list = [self.entries[x].get().strip() for x in self.entries]
        if '' in guess_list:
            self.info_label('Enter Number in All boxes')
            self.clear_boxes()
            return
        if not len(set(guess_list)) == 4:
            self.info_label('No Duplicates are Allowed')
            self.clear_boxes()
            return
        if not all([len(x) == 1 for x in guess_list]):
            self.info_label('Each Box Takes Only One Digit')
            self.clear_boxes()
            return
        if not all([x.isdigit() for x in guess_list]):
            self.info_label('Only Numbers Are Allowed')
            self.clear_boxes()
            return
        if guess_list[0] == str(0):
            self.info_label('First Digit Cannot be "0"')
            self.entries[0].delete(0, ctk.END)
            self.entries[0].after(10, self.entries[0].focus)
            return

        p_num, m_num = self.process_guess(guess_list)
        self.create_result_labels(p_num, m_num)

        if p_num == 4:
            self.won = True
            self.info_label(msg='CONGRATULATIONS!!!', destroy=False)
            for e in self.entries: self.entries[e].destroy()
            self.entry_to_label(guess_list=guess_list)
            self.end_game_buttons()
            return
        self.entry_to_label(guess_list=guess_list)
        if self.count > 8:
            for e in self.entries: self.entries[e].destroy()
            self.info_label(msg='BETTER LUCK NEXT TIME!', destroy=False)
            self.y_cord += 0.05
            self.info_label(msg=f'Correct number is: '
                                f'{self.puzzle[0]}{self.puzzle[1]}{self.puzzle[2]}{self.puzzle[3]}',
                            destroy=False)
            self.end_game_buttons()
            return
        self.y_cord += 0.1
        self.count += 1
        for e in self.entries:
            self.replace(self.entries[e])
            self.x_cord += 0.1
            self.entries[e].delete(0, ctk.END)
            self.entries[0].after(10, self.entries[0].focus)
        self.x_cord = 0.05
        self.button.place(relx=0.75, rely=self.y_cord)

    def process_guess(self, guess_list):
        p_num = 0
        m_num = 0
        for item in enumerate(guess_list):
            if item[1] in self.puzzle:
                if item[0] == self.puzzle.index(item[1]):
                    p_num += 1
                else:
                    m_num += 1
        return p_num, m_num

    def clear_boxes(self):
        for e in self.entries:
            self.entries[e].delete(0, ctk.END)
        self.entries[0].after(10, self.entries[0].focus)

    def info_label(self, msg, destroy: bool = True):
        text_var = ctk.StringVar(value=msg)
        info_label = ctk.CTkLabel(master=self, textvariable=text_var, corner_radius=20,
                                  height=25, fg_color='#fff1bf', text_color='#381c02',
                                  font=('arial bold', 25))
        info_label.place(relx=0.5, rely=self.y_cord + 0.1, anchor=ctk.CENTER)
        if destroy:
            info_label.after(4500, info_label.destroy)

    def create_result_labels(self, p_msg, m_msg):
        text_var = ctk.StringVar(value=f'+{p_msg}')
        self.p_label = ctk.CTkLabel(master=self, textvariable=text_var, corner_radius=10,
                                    width=45, height=35, fg_color='#37850a', text_color='#381c02',
                                    font=('arial bold', 20))
        self.p_label.place(relx=self.x_cord + 0.43, rely=self.y_cord)

        text_var = ctk.StringVar(value=f'-{m_msg}')
        self.m_label = ctk.CTkLabel(master=self, textvariable=text_var, corner_radius=10,
                                    width=45, height=35, fg_color='#fbe400', text_color='#381c02',
                                    font=('arial bold', 20))
        self.m_label.place(relx=self.x_cord + 0.55, rely=self.y_cord)

    def entry_to_label(self, guess_list: list):
        color = '#5e6caf'
        if self.won:
            color = '#a00000'

        for x in guess_list:
            text_var = ctk.StringVar(value=x)
            digit_label = ctk.CTkLabel(master=self, textvariable=text_var, corner_radius=10,
                                       width=35, height=35, fg_color=color, text_color='#381c02',
                                       font=('arial bold', 25))
            digit_label.place(relx=self.x_cord, rely=self.y_cord)
            self.x_cord += 0.1
        self.x_cord = 0.05

    def end_game_buttons(self):
        self.unbind('<Return>')
        self.button.configure(text='AGAIN!', command=lambda: self.restart_app(True),
                              fg_color='#32bbb9', hover_color='#6e37fa',
                              text_color='black')
        self.button2 = ctk.CTkButton(
            master=self, width=25, height=35,
            border_width=1, text='QUIT!', corner_radius=10,
            font=('arial bold', 20), fg_color='#b94b32',
            hover_color='#81361d', text_color='black',
            command=lambda: self.restart_app(False)
        )
        self.button2.place(relx=0.75, rely=self.y_cord - 0.1)

    def restart_app(self, decision: bool):
        self.restart = decision
        self.quit()


if __name__ == '__main__':
    while True:
        continue_game = True
        app = App()
        app.mainloop()
        if not app.restart:
            break
        app.destroy()

from tkinter import *
import tkinter.messagebox
from PIL import ImageTk
import configparser
import subprocess


class ConnectDatabase:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.window.title('Database Connection')
        # self.window.iconbitmap('images')
        self.window.resizable(False, False)
        self.database_frame = ImageTk.PhotoImage(file='/home/lks/Images/connect_database_frame.png')

        self.image_panel = Label(self.window, image=self.database_frame)
        self.image_panel.pack(fill='both', expand='yes')

        self.txt = 'Connect Database'
        self.count = 0
        self.text = ''
        self.heading = Label(self.window, text=self.txt, font=('yu gothic ui', 30, 'bold'), bg="white", fg='black', bd=5, relief=FLAT)
        self.heading.place(x=470, y=40, width=450)
        self.slider()

        """ ======Input====== """
        self.host_label = Label(self.window, text="Host Name", bg="white", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.host_label.place(x=495, y=130)

        self.host_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.host_entry.place(x=530, y=163, width=380)

        """ ==================Port Label and Entry================== """
        self.port_label = Label(self.window, text="Port", bg="white", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.port_label.place(x=495, y=225)

        self.port_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.port_entry.place(x=530, y=253, width=380)

        """ ==================Username Label and Entry================== """
        self.username_label = Label(self.window, text="Username", bg="white", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=495, y=318)

        self.username_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.username_entry.place(x=530, y=348, width=380)

        """ ==================Password Label and Entry================== """
        self.password_label = Label(self.window, text="Password", bg="white", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=495, y=410)

        self.password_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.password_entry.place(x=530, y=440, width=380)

        """ ============Placing Button============ """
        self.login = ImageTk.PhotoImage(file='/home/lks/Images/login.png')

        self.login_button = Button(self.window, image=self.login, relief=FLAT, command=self.openFile, borderwidth=0, background="white", activebackground="white", cursor="hand2")
        self.login_button.place(x=640, y=523)

    def openFile(self):
        try:
            config = configparser.ConfigParser()
            if not config.read('database.ini') == []:
                pass
            else:
                raise IOError('Cannot open configuration file')
            count = 0

            for key in config['DEFAULT']:
                if key == 'user':
                    if self.username_entry.get() == config.get('DEFAULT', 'user'):
                        count += 1
                    else:
                        tkinter.messagebox.showerror(title='Error login', message='Error user is incorrect')
                        count = 0

                if key == 'password':
                    if self.password_entry.get() == config.get('DEFAULT', 'password'):
                        count += 1
                    else:
                        tkinter.messagebox.showerror(title='Error password', message='Error password is incorrect')
                        count = 0

                if key == 'port':
                    if self.port_entry.get() == config.get('DEFAULT', 'port'):
                        count += 1
                    else:
                        tkinter.messagebox.showerror(title='Error port', message='Error port number is incorrect')
                        count = 0

                if key == 'host':
                    if self.host_entry.get() == config.get('DEFAULT', 'host'):
                        count += 1
                    else:
                        tkinter.messagebox.showerror(title='Error host', message='Error host is incorrect')
                        count = 0

            if count == 4:
                self.window.destroy()
                subprocess.run(["python", "dashboard.py"])

        except IOError as err:
            tkinter.messagebox.showerror(title='Error file', message='{}'.format(err))
            create = tkinter.messagebox.askquestion(title='Create file', message="Do you want create database file ?")

            """ create file ini """
            if create == 'yes':
                config = configparser.ConfigParser()
                config['DEFAULT'] = {
                    'user': 'root',
                    'password': '',
                    'port': '4444',
                    'host': 'localhost'
                }

                """ Write conf in database.ini """
                with open('database.ini', 'w') as configfile:
                    config.write(configfile)

    """ Slide text """
    def slider(self):
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text+self.txt[self.count]
            self.heading.config(text=self.text)

        self.count += 1

        if self.count == len(self.txt):
            self.heading.after(200)
        else:
            self.heading.after(200, self.slider)


def win():
    window = Tk()
    ConnectDatabase(window)
    window.mainloop()


if __name__ == '__main__':
    win()

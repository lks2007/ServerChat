from tkinter import *
from PIL import ImageTk, Image
import socket
import threading
import tkinter.messagebox


class Dashboard:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.window.title('Dashboard')
        # self.window.iconbitmap('images')
        self.window.resizable(False, False)

        self.load = Image.open('/home/lks444/dashboard_frame.png')
        self.render = ImageTk.PhotoImage(self.load)

        self.image_panel = Label(self.window, image=self.render)
        self.image_panel.image = self.render
        self.image_panel.pack(fill='both', expand='yes')

        """ ======Label====== """
        self.log = 'Server chat is not start !'
        self.log_label = Label(self.window, text=self.log, bg="#2f3640", fg="#ffffff", font=("yu gothic ui", 12, "bold"))
        self.log_label.place(x=1139, y=395, anchor="center", width=385, height=540)

        """ ======Input====== """
        self.host_label = Label(self.window, text="Host", bg="#3c3f41", fg="#ffffff", font=("yu gothic ui", 15, "bold"))
        self.host_label.place(x=620, y=160)

        self.host_entry = Entry(self.window, relief="flat", bg="#3c3f41", fg="#ffffff", highlightthickness=1, bd=3, font=("yu gothic ui semibold", 12))
        self.host_entry.place(x=620, y=190, width=200)

        self.port_label = Label(self.window, text="Port", bg="#3c3f41", fg="#ffffff", font=("yu gothic ui", 15, "bold"))
        self.port_label.place(x=140, y=160)

        self.port_entry = Entry(self.window, relief="flat", bg="#3c3f41", fg="#ffffff", bd=3, highlightthickness=1, font=("yu gothic ui semibold", 12))
        self.port_entry.place(x=140, y=190, width=200)

        """ ============Placing Button============ """
        self.stopIcon = Image.open('./images/stop.png')
        self.stopRender = ImageTk.PhotoImage(self.stopIcon)
        self.stopIcon_button = Button(self.window, image=self.stopRender, relief="flat", command=self.serverStop, bd=0, highlightthickness=0, background="#323232", activebackground="#323232", cursor="hand2")

        self.stopIcon_button.image = self.render
        self.stopIcon_button.pack(fill='both', expand='yes')
        self.stopIcon_button.place(x=820, y=13)


        self.boolean = True
        self.runIcon = Image.open('./images/icon.png')
        self.render = ImageTk.PhotoImage(self.runIcon)
        self.runIcon_button = Button(self.window, image=self.render, relief="flat", command=self.server, bd=0, highlightthickness=0, background="#323232", activebackground="#323232", cursor="hand2")

        self.runIcon_button.image = self.render
        self.runIcon_button.pack(fill='both', expand='yes')
        self.runIcon_button.place(x=860, y=13)

    def serverStop(self):
        self.boolean = False
        self.log = self.log + str("Server is shutdown !\n")
        self.log_label.config(text=self.log)

    def server(self):
        def portNumber():
            if not self.port_entry.get() == "":
                entry = int(self.port_entry.get())
                return entry
            else:
                tkinter.messagebox.showerror(title='Error port', message='Error port is incorrect')

        if portNumber() >= 1024 or not portNumber() == '':
            port = portNumber()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connections = []

            s.bind(('', port))
            s.listen(5)

            def handler(c, a):
                while self.boolean:
                    data = c.recv(1024)

                    for connection in connections:
                        connection.send(data)
                    if not data:
                        connections.remove(c)
                        c.close()
                        msg = '> ' + str(a[0]) + ':' + str(a[1]) + " disconnected\n"
                        self.log = self.log + msg
                        update()
                        break

            def run():
                while self.boolean:
                    c, a = s.accept()
                    cThread = threading.Thread(target=handler, args=(c, a))
                    cThread.daemon = True
                    cThread.start()
                    connections.append(c)
                    msg = '> ' + str(a[0]) + ':' + str(a[1]) + " connected\n"
                    self.log = self.log + msg
                    update()

            tthread = threading.Thread(target=run)
            tthread.daemon = True
            tthread.start()

            def update():
                self.log_label.config(text=self.log)

            self.log = str("[*] The server is start on the port: {}!\n".format(port))
            self.log = self.log + str("[*] The thread daemon run !\n")
            update()
        else:
            tkinter.messagebox.showerror(title='Error port', message='Error port is incorrect')


def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()


if __name__ == '__main__':
    win()

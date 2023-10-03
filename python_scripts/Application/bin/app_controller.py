
from tkinter import BOTTOM, LEFT
import customtkinter as ctk
from tkdnd import TkinterDnD

import controllers
import views as vs
from PIL import Image, ImageTk

class AppController(ctk.CTk, TkinterDnD.DnDWrapper):
    width = 500
    height = 500

    def file_drop(self, event):
        if event.data[0] == "{":
            event.data = event.data[1:]
        if event.data[-1] == "}":
            event.data = event.data[:-1]
        self.file_selected(event.data)

    def browse_file(self):
        filename = ctk.filedialog.askopenfilename(initialdir="/",
                                                  title="Wybierz plik")
        if filename != "":
            self.file_selected(filename)

    def file_selected(self, filename):
        self.file_path = filename
        if controllers.validate_file(self.file_path):
            if self.current_frame == self.frames[vs.StartPage]:
                self.show_frame(vs.OptionPage)
            # elif self.current_frame == self.frames[Tk.SignPage]:
            #     self.frames[Tk.SignSuccessful] = Tk.SignSuccessful(self,self,self.folder_path)
            #     self.show_frame(Tk.SignSuccessful)

        else:
            if self.current_frame == self.frames[vs.StartPage]:
                self.show_frame(vs.WrongFile)
                self.after(2000, lambda: self.show_frame(vs.StartPage))
            # elif self.current_frame == self.frames[vs.SignPage]:
            #     self.show_frame(vs.WrongFile)
            #     self.after(2000, lambda: self.show_frame(vs.SignPage))

    def credentials_validated(self):

        dir = ctk.filedialog.askdirectory(mustexist=True, initialdir="/",
                                          title="Wybierz plik")
        self.folder_path = dir
        if self.folder_path == "":
            self.show_frame(vs.SavePage)
        elif controllers.validate_folder(self.folder_path):
            try:
                if controllers.sign_file(self.credentials, self.file_path, self.folder_path, self.private_key):
                    self.frames[vs.SignSuccessful] = vs.SignSuccessful(self, self, self.folder_path)
                    self.show_frame(vs.SignSuccessful)
                    self.after(5000, lambda: self.reset_frames())
                else:
                    self.show_frame(vs.Alert)
                    self.after(2000, lambda: self.reset_frames())
            except:
                self.show_frame(vs.Alert)
                self.after(2000, lambda: self.reset_frames())
        else:
            self.show_frame(vs.WrongFolder)
            self.after(2000, lambda: self.show_frame(vs.SavePage))

    def credentials_inserted(self, credentials):
        self.credentials = credentials
        self.show_frame(vs.Bank)
        self.private_key = controllers.validate_credentials(credentials)
        if self.private_key != "":
            self.after(2000, lambda: self.show_frame(vs.BankValidated))
            self.after(4000, lambda: self.show_frame(vs.SavePage))
        else:
            self.after(2000, lambda: self.show_frame(vs.BankRefused))
            self.after(4000, lambda: self.show_frame(vs.SignPage))

    def check_signature(self):
        self.show_frame(vs.WaitForCA)
        try:
            self.credentials = controllers.get_identity(self.file_path)
            if self.credentials != "":
                self.frames[vs.FoundIdentity] = vs.FoundIdentity(self, self, self.credentials)
                self.after(2000, lambda: self.show_frame(vs.FoundIdentity))
            else:
                self.after(2000, lambda: self.show_frame(vs.WrongIdentity))
                self.after(4000, lambda: self.reset_frames())
        except:
            self.show_frame(vs.NotSignedFile)
            self.after(2000, lambda: self.reset_frames())

    def save_decrypted(self):
        self.folder_path = ctk.filedialog.askdirectory(mustexist=True, initialdir="/",
                                                       title="Wybierz miejsce zapisu")

        if self.folder_path == "":
            self.show_frame(vs.FoundIdentity)
        elif controllers.validate_folder(self.folder_path):
            try:
                controllers.save_decrypted_content(self.file_path, self.folder_path)
                self.frames[vs.SaveSuccessful] = vs.SaveSuccessful(self, self, self.folder_path)
                self.show_frame(vs.SaveSuccessful)
                self.after(2000, lambda: self.reset_frames())
            except:
                self.show_frame(vs.Alert)
                self.after(2000, lambda: self.reset_frames())
        else:
            self.show_frame(vs.WrongFolder)
            self.after(2000, lambda: self.show_frame(vs.FoundIdentity))

    def show_frame(self, cont):
        self.current_frame.pack_forget()
        self.current_frame = self.frames[cont]
        self.current_frame.pack(expand=True, fill="both")
        self.update_idletasks()

    def exit(self):
        self.destroy()

    def insert_frames(self):
        self.file_path = ""
        self.folder_path = ""
        self.credentials = ""
        for F in (vs.StartPage, vs.OptionPage, vs.Alert, vs.SignPage,
                  vs.InvalidSignature, vs.Bank, vs.BankValidated,
                  vs.WaitForCA, vs.WrongFile, vs.SavePage, vs.NotSignedFile,
                  vs.WrongFolder, vs.WrongIdentity, vs.BankRefused):
            frame = F(master=self, controller=self)
            self.frames[F] = frame
        self.current_frame = self.frames[vs.StartPage]
        self.show_frame(vs.StartPage)

    def reset_frames(self):
        self.file_path = ""
        self.folder_path = ""
        self.credentials = ""
        self.private_key = ""
        self.show_frame(vs.StartPage)
        if self.frames.get(vs.FoundIdentity) is not None:
            self.frames[vs.FoundIdentity].destroy()
            self.frames[vs.FoundIdentity] = None
        if self.frames.get(vs.SignSuccessful) is not None:
            self.frames[vs.SignSuccessful].destroy()
            self.frames[vs.SignSuccessful] = None
        if self.frames.get(vs.SaveSuccessful) is not None:
            self.frames[vs.SaveSuccessful].destroy()
            self.frames[vs.SaveSuccessful] = None
        self.frames[vs.SignPage].destroy()
        self.frames[vs.SignPage] = vs.SignPage(master=self, controller=self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")
        self.credentials = None
        self.current_frame = None
        self.TkdndVersion = TkinterDnD._require(self)
        self.resizable(width=False, height=False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.x_pos = (screen_width / 2) - (AppController.width / 2)
        self.y_pos = (screen_height / 2) - (AppController.height / 2)
        self.geometry('%dx%d+%d+%d' % (AppController.width, AppController.height, self.x_pos, self.y_pos))
        self.title("Projekt WDC")

        ico = Image.open('../media/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)
        
        self.frames = {}
        self.file_path = None
        self.insert_frames()
        frame = ctk.CTkFrame(self, height=20)
        frame.pack(padx=5, pady=5, side=BOTTOM)
        home_button = ctk.CTkButton(frame, width=40)
        home_button.configure(text="Start", command=lambda: self.reset_frames())
        home_button.pack(expand=True, side=LEFT, padx=2)

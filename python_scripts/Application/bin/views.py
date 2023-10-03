from PIL import Image, ImageTk

import customtkinter as ctk
from tkdnd import DND_FILES


class Alert(ctk.CTkFrame):
    def __init__(self, master: any, controller, msg=None, **kwargs):
        super().__init__(master, **kwargs)
        self.text = "Nieznany błąd" if msg is None else msg
        bg = Image.open("../media/error.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)
        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)
        title = ctk.CTkLabel(master=self, text=self.text, font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=False)


class WrongFile(Alert):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, controller, "Wybrany plik jest nieprawidłowy", **kwargs)


class WrongFolder(Alert):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, controller, "Wybrany folder jest nieprawidłowy", **kwargs)


class WrongIdentity(Alert):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, controller, "Nie odnaleziono\nwłaściciela podpisu", **kwargs)


class BankRefused(Alert):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, controller, "Dane logowania są nieprawidłowe", **kwargs)


class NotSignedFile(Alert):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, controller, "Plik nie został podpisany", **kwargs)


class OptionPage(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)
        title = ctk.CTkLabel(master=self, text="Wybierz opcję", font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=False)
        box = ctk.CTkFrame(master=self)
        box.pack(expand=True)
        button = ctk.CTkButton(master=box, text="Sprawdź podpis",
                               command=lambda: controller.check_signature())
        button.pack(pady=10, padx=20)
        button2 = ctk.CTkButton(master=box, text="Podpisz",
                                command=lambda: controller.show_frame(SignPage))
        button2.pack(pady=10, padx=20)


class SignSuccessful(ctk.CTkFrame):
    def __init__(self, master: any, controller, folder, **kwargs):
        super().__init__(master, **kwargs)
        bg = Image.open("../media/ok.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)
        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)
        title = ctk.CTkLabel(master=self,
                             text=f"Podpisany plik został\n pomyślnie zapisany\nw folderze\n {folder} ",
                             font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)

class SaveSuccessful(ctk.CTkFrame):
    def __init__(self, master: any, controller, folder, **kwargs):
        super().__init__(master, **kwargs)
        bg = Image.open("../media/ok.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)
        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)
        title = ctk.CTkLabel(master=self,
                             text=f"Plik został\n pomyślnie zapisany\nw folderze\n {folder} ",
                             font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)


class Bank(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)

        bg = Image.open("../media/lock.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)

        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)

        title = ctk.CTkLabel(master=self, text="Weryfikujemy dane logowania", font=("Didot", 26))
        title.pack(fill="both", expand=True)


class BankValidated(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)

        bg = Image.open("../media/key.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)

        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)

        title = ctk.CTkLabel(master=self, text="Dane logowania są prawidłowe",
                             font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)


class WaitForCA(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)

        bg = Image.open("../media/certificate.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)

        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.pack(expand=True)

        title = ctk.CTkLabel(master=self, text="Trwa weryfikowanie podpisu",
                             font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)


class FoundIdentity(ctk.CTkFrame):
    def __init__(self, master: any, controller, identity, **kwargs):
        super().__init__(master, **kwargs)
        title = ctk.CTkLabel(master=self, text=f"Plik został podpisany elektronicznie\nprzez: "
                                               f"{identity}", font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)
        button = ctk.CTkButton(master=self, text="Zapisz", command=lambda: controller.save_decrypted())
        button.pack(pady=10, padx=20)


class InvalidSignature(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)
        title = ctk.CTkLabel(master=self, text="Sygnatura nieprawidłowa", font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=True)


class SignPage(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)
        title = ctk.CTkLabel(master=self, text="Podpis", font=("Didot", 26))
        title.pack(pady=40, padx=40, fill="both", expand=False)

        frame = ctk.CTkFrame(master=self)
        frame.pack(expand=True)
        drag = ctk.CTkLabel(master=frame, text="Podaj login")
        drag.pack(expand=False)
        textbox = ctk.CTkEntry(master=frame, width=400, height=50, justify='center')
        # textbox.tag_config("center", justify='center')
        textbox.pack(expand=False)
        drag2 = ctk.CTkLabel(master=frame, text="Podaj hasło")
        drag2.pack(expand=False)
        passbox = ctk.CTkEntry(master=frame, width=400, height=50, justify='center', show="*")
        passbox.pack(expand=False)

        button = ctk.CTkButton(master=self, text="Dalej",
                               command=lambda: controller.credentials_inserted({"login": textbox.get(),
                                                                                "password": passbox.get()}))
        button.pack(pady=10, padx=20, expand=True)


class StartPage(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(corner_radius=10)

        title = ctk.CTkLabel(master=self, text="Podpis cyfrowy", font=("Didot", 26))
        title.pack(pady=5, padx=10, fill="both", expand=False)

        bg = Image.open("../media/folder.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)

        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")
        canvas.drop_target_register(DND_FILES)
        canvas.dnd_bind('<<Drop>>', controller.file_drop)

        canvas.pack(expand=True)
        drag = ctk.CTkLabel(master=self, text="Przeciągnij i upuść aby wczytać plik")
        drag.pack()

        button = ctk.CTkButton(master=self, text="wybierz ręcznie", command=controller.browse_file)
        button.pack(pady=10, padx=20)


class SavePage(ctk.CTkFrame):
    def __init__(self, master: any, controller, **kwargs):
        super().__init__(master, **kwargs)

        title = ctk.CTkLabel(master=self, text="Wybierz miejsce zapisu", font=("Didot", 26))
        title.pack(pady=5, padx=10, fill="both", expand=True)

        bg = Image.open("../media/save.png")
        bg = bg.resize((200, 200))
        img = ImageTk.PhotoImage(bg)

        canvas = ctk.CTkLabel(master=self, image=img, width=50, height=50, text="")

        canvas.pack(expand=True)
        button = ctk.CTkButton(master=self, text="Wybierz folder", command=lambda: controller.credentials_validated())
        button.pack(pady=10, padx=20)

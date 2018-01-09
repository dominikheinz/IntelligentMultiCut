from tkinter import *
from tkinter.ttk import Progressbar
from src.classes.view.View import View
from tkinter import filedialog
import sys, os
import time
from src.classes.view.ThumbnailCreator import *
from src.classes.view.ConfigWindow import ConfigWindow


class GUI(View):
    __configWindow = ConfigWindow

    def __init__(self):

        # Rufe übergeordneten Konstruktor auf
        super(GUI, self).__init__()

        # Menge der zugelassenen Kameras ( Videofiles )
        self.__cameras = self.config.get("max_cameras")

        # Kontainer zum speichern der ausgewählten Pfade
        self.__sourcePaths = []

        # Farben
        self.color_bg = self.config.get("color_bg")
        self.color_fg = self.config.get("color_fg")
        self.__red = self.config.get("color_red")
        self.font_color = self.config.get("font_color")

        # Passwort für easteregg
        self.__pw = "masterpaul"

        # Applikationsname
        self.__app_title = self.config.get("app_title")
        self.__app_version = self.config.get("app_version")

        self.__progress_var = 0

        # Kontainer zum speichern von Buttons und Frames
        self.__dynamicWidgets = []

        # Einstellungen für das Hauptfenster
        self.root = Tk()

        # Hintergundfarbe
        self.root.configure(
            background=self.color_bg
        )

        # Titel für Fensters
        self.root.title(self.__app_title + " v" + str(self.__app_version))

        # Icon für Fensters
        if os.name == "nt":
            self.root.iconbitmap(self.root,'static/icon.ico')

        # Erstelle Frame, welcher alle Widgets enthalten wird
        self.container = Frame(self.root)
        self.container.grid()

        # Manuelles padding durch einstellen der Mindestgröße (Zeile/Spalte)
        self.container.columnconfigure(0, minsize=30)
        self.container.columnconfigure(4, minsize=30)
        self.container.grid_rowconfigure(9, minsize=20)
        self.container.grid_rowconfigure(11, minsize=20)

        self.container.configure(bg=self.color_bg)

        # Textfeld zum Ausgeben von debug - bzw. Informationsausgaben
        self.textbox_output = Text(
            self.container,
            width=80,
            height=8,
            relief=SUNKEN,
            bd=2,
            state='disabled',
            bg=self.color_bg,
            fg='white',
            insertbackground='white'
        )

        # Textfeld in Fenster platzieren
        self.textbox_output.grid(
            row=12,
            column=0,
            columnspan=self.__cameras,
            sticky=W + E
        )

        # Verhindern dass Größe des Fensters vom Benutzer angepasst werden kann
        if (self.__cameras > 6):
            self.console_out("Only up to 6 files allowed")
            self.__cameras = 6

        if (self.__cameras < 2):
            self.console_out("Minimum of cameras is 2")
            self.__cameras = 2

        # Überschrift
        label_header = Label(
            self.container,
            text=" Welcome to " + self.__app_title + " v" + str(self.__app_version),
            fg='white',
            bg=self.color_fg
        )

        # Schrift des Labels ändern
        label_header.configure(
            font=(None, 10, 'bold')
        )

        # Label in Fenster platzieren
        label_header.grid(
            row=0,
            column=0,
            sticky=W + E,
            columnspan=self.__cameras
        )

        # Überschrift(subtitle)
        label_subtitle = Label(
            self.container,
            text="Select at least 2 videofiles to be processed",
            fg='white',
            bg=self.color_bg,
            font=(None, 13)
        )


        label_subtitle.grid(
            row=2,
            column=1,
            sticky=W,
            pady=20,
            columnspan=self.__cameras
        )
        # Kontainer zum Speichern der Pfade (nur GUI-intern verwenden)
        self.__sourcePaths = [None] * self.__cameras

        # Kontainer für Videothumbnails
        self.__photos = [None] * self.__cameras

        # Suchboxen auf Fenster
        self.row_index = 0
        self.button_count = 0
        for i in range(0, self.__cameras):

            # Box welche den Button enthalten wird
            self.box_filebrowse = Frame(
                self.container,
                bg=self.color_bg,
                height=90 * 2,
                width=160 * 2
            )

            self.box_filebrowse.grid(
                row=self.row_index + 3,
                column=i % 3 + 1,
                sticky=W + E,
                padx=2,
                pady=2,
            )

            # Buttons dürfen Box ausfüllen aber nicht vergrößern
            self.box_filebrowse.columnconfigure(0, weight=1)
            self.box_filebrowse.rowconfigure(0, weight=1)
            self.box_filebrowse.grid_propagate(False)

            # Erstelle Suchknöpfe
            button_filebrowse = Button(
                self.box_filebrowse,
                text="+",
                font=(None, 40),
                bg=self.color_bg,
                fg=self.font_color,
                command=lambda i=i: self.browsepath(i)
            )

            button_filebrowse.configure(
                activeforeground=self.color_fg,
                activebackground=self.color_bg,
                bd=0,
                padx=2,
                pady=2,
            )

            button_filebrowse.bind(
                "<Enter>",
                button_filebrowse.config(cursor="hand2")
            )
            button_filebrowse.bind(
                "<Leave>",
                button_filebrowse.config(cursor=None)
            )

            # Erstelle 'Delete' - Knopf
            self.button_delete = Button(
                self.box_filebrowse,
                text="-",
                font='bold',
                bg=self.__red,
                fg='white',
                activebackground=self.color_bg,
                activeforeground=self.color_fg,
                command=lambda index=i: self.remove_path(index),
                bd=0,
            )

            self.button_delete.bind(
                "<Enter>",
                self.button_delete.config(cursor="hand2")
            )
            self.button_delete.bind(
                "<Leave>",
                self.button_delete.config(cursor=None)
            )

            self.__dynamicWidgets.append({
                "box": self.box_filebrowse,
                "button": button_filebrowse,
                "delete": self.button_delete})

            # Wenn 3 Buttons in dieser Zeile -> springe in die nächste
            if (i != 0 and (i + 1) % 3 == 0):
                self.row_index += 2

            # Status text für Suchknöpfe
            self.set_status(button_filebrowse, "Browse for a video file")

        # Zeige ersten Knopf an
        self.__dynamicWidgets[0]['button'].grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=W + E + N + S
        )
        self.__dynamicWidgets[0]['box'].config(bg=self.color_fg)

        # Erstelle quit button
        self.button_quit = Button(
            self.container,
            text="Quit",
            bg=self.__red,
            fg='white',
            command=self.quit
        )

        # Konfiguriere quit button
        self.button_quit.configure(
            height=2,
            width=15,
            activeforeground='white',
            activebackground=self.__red,
            bd=0
        )

        # Ändere Cursor zu "hand2" wenn über button
        self.button_quit.bind(
            "<Enter>",
            self.button_quit.config(cursor="hand2")
        )

        # Cursor Änderung rückgängig machen
        self.button_quit.bind(
            "<Leave>",
            self.button_quit.config(cursor=None)
        )

        # Button auf Fenster platzieren
        self.button_quit.grid(
            row=10,
            column=1,
            pady=5,
            padx=4,
        )

        # Zeige Funktion des buttons in statusbar
        self.set_status(self.button_quit, "Quit")

        # Erstelle process button
        self.button_process = Button(
            self.container,
            text="Process",
            bg=self.color_fg,
            fg='white',
            state=DISABLED,
            command=lambda: [
                self.progressbar.grid(row=14, column=0, columnspan=self.config.get("max_cameras"), sticky="we"),
                self.process(),
                self.button_process.config(state="disabled")
            ]
        )

        # Konfiguriere process button
        self.button_process.configure(
            height=2,
            width=25,
            activeforeground=self.color_fg,
            activebackground=self.color_bg,
            bd=0,
        )

        # Ändere Cursor zu "hand2" wenn über button
        self.button_process.bind(
            "<Enter>",
            self.button_process.config(cursor="hand2")
        )

        # Cursor Änderung rückgängig machen
        self.button_process.bind(
            "<Leave>",
            self.button_process.config(cursor=None)
        )

        # Button auf Fenster platzieren
        self.button_process.grid(
            row=10,
            column=3,
            pady=5,
            padx=4,
        )

        # Zeige Funktion des buttons in statusbar
        self.set_status(self.button_process, "Process videos and cut them")


        # Erstelle Settings button
        self.button_settings = Button(
            self.container,
            text="Settings",
            bg=self.color_fg,
            fg='white',
            command=lambda :[self.button_settings.config(state=DISABLED),self.__configWindow(self)]
        )


        # Konfiguriere Setting button
        self.button_settings.configure(
            height=2,
            width=25,
            activeforeground=self.color_fg,
            activebackground=self.color_bg,
            bd=0,
        )

        # Ändere Cursor zu "hand2" wenn über button
        self.button_settings.bind(
            "<Enter>",
            self.button_settings.config(cursor="hand2")
        )

        # Cursor Änderung rückgängig machen
        self.button_settings.bind(
            "<Leave>",
            self.button_settings.config(cursor=None)
        )

        # Zeige Funktion des buttons in statusbar
        self.set_status(self.button_settings, "Open settings")

        # Button auf Fenster platzieren
        self.button_settings.grid(
            row=10,
            column=2,
            pady=5,
            padx=4,
        )

        # status Bar
        self.status = Label(
            self.container,
            bg=self.color_bg,
            fg='white',
            bd=1,
            relief=SUNKEN,
            anchor=W
        )

        self.status.grid(
            row=15,
            column=0,
            columnspan=self.__cameras,
            sticky=W + E
        )

        # scrollbar
        self.scrollbar = Scrollbar(
            self.container,
            orient="vertical",
            command=self.textbox_output.yview,
            background=self.color_bg
        )

        self.scrollbar.grid(
            row=12,
            column=0,
            sticky=N + S + E,
            pady=2,
            columnspan=self.__cameras
        )

        self.textbox_output['yscrollcommand'] = self.scrollbar.set

        if (self.config.get("debug")):
            self.console_out("[Debug]: Debugmode is enabled")

        # bind easter egg shortcut STR + SHIFT + 4
        self.root.bind(
            '<Control-dollar>',
            lambda x,
                   y=self.container: self.easter_egg(y)
        )

        # Erstelle progressbar
        self.progressbar = Progressbar(
            self.container,
            max=100,
            variable=self.__progress_var,
            orient=HORIZONTAL,
            length=100,
            mode='determinate'
        )

        self.progressbar["value"] = 0
        self.progressbar["maximum"] = 100
        self.root.geometry('+50+50')
        self.root.resizable(
            height=False,
            width=False
        )

        #  handler zum schließen des Fensters
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    # Neuen status text für ein Widget anlegen
    def set_status(self, element, text):

        # Wenn Maus sich über element befindet
        element.bind(
            "<Enter>",
            lambda x,
                   txt=text: self.status.config(
                text=txt
            )
        )

        # Wenn Maus element verlässt
        element.bind(
            "<Leave>",
            lambda x,
                   txt='': self.status.config(
                text=txt
            )
        )

    # Setze den Fortschritt der Progressbar neu
    def set_progress(self, val):
        self.__progress_var = val
        self.progressbar["value"] = self.__progress_var

    def get_progress(self):
        return self.__progress_var


    # Gib einen Text auf der Konsole aus
    def console_out(self, text):

        self.textbox_output.config(
            state='normal'
        )

        self.textbox_output.insert(
            INSERT,
            str(text) + '\n'
        )

        self.textbox_output.config(
            state='disabled'
        )

        self.textbox_output.see("end")

    # Öffne Filebrowser und wähle eine Videodatei ( .mp4/.avi )
    def browsepath(self, index):

        # Hole Pfad aus Filebrowser
        path = filedialog.askopenfilename(
            filetypes=[
                ("MPEG_4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("WMV files", "*.wmv"),
                ("MOV files", "*.mov"),
            ]
        )

        filename = path.split("/")
        filename = filename[-1]

        # Wenn Pfad gültig dann füge den Pfad der Pfadliste hinzu
        if (self.valid_path(path)):

            self.__sourcePaths[index] = path

            # Gib Namen der ausgewählten Videodatei aus
            self.console_out(filename + " was selected")

            # Ersetze Knopf durch Thumbnail

            tc = ThumbnailCreator(path, 0)
            photo = tc.get_thumbnailTK()

            self.__photos[index] = photo
            self.__dynamicWidgets[index]['button'].config(image=photo)
            self.__dynamicWidgets[index]['button'].image = self.__photos[index]

            # Zeige den nächsten Suchknopf an
            if (index + 1 < self.__cameras):
                self.__dynamicWidgets[index + 1]['button'].grid(
                    row=0,
                    column=0,
                    padx=2,
                    pady=2,
                    sticky=W + E + N + S
                )
                self.__dynamicWidgets[index + 1]['box'].config(bg=self.color_fg)

            # Zeige den Löschen - Knopf an
            self.__dynamicWidgets[index]['button'].bind(
                "<Enter>",
                lambda x, i=index:
                self.add_button(i),

            )

            # Nur anzeigen wenn über Thumbnail
            self.__dynamicWidgets[index]['box'].bind(
                "<Leave>", lambda x, i=index:
                self.remove_button(i)
            )

            self.resize_filepaths()

    # Füge einen Löschen - Knopf hinzu mit dem das eingelesene Video gelöscht werden kann
    def add_button(self, index):
        self.__dynamicWidgets[index]["delete"].grid(
            row=0,
            column=0,
            sticky='wes',
            padx=2,
            pady=2,
        )

    # Entferne Löschen - Knopf
    def remove_button(self, index):
        self.__dynamicWidgets[index]["delete"].grid_forget()

    # Entferne Pfad von Kontainer
    def remove_path(self, index):

        for i in range(index, len(self.filepaths)):

            if (i < len(self.filepaths) - 1 and i < self.__cameras - 1):
                self.__photos[i] = self.__photos[i + 1]
                self.__dynamicWidgets[i]["button"].config(image=self.__photos[i + 1])
                self.__dynamicWidgets[i]["button"].image = self.__photos[i + 1]
                self.__sourcePaths[i] = self.__sourcePaths[i + 1]
                self.__dynamicWidgets[i + 1]["button"].config(image='')
                self.__sourcePaths[i + 1] = None

            if (i == len(self.filepaths) - 1):
                self.__dynamicWidgets[i]["button"].config(image='')
                self.__dynamicWidgets[i]["delete"].grid_forget()
                self.__dynamicWidgets[i]["button"].unbind('<Enter>')
                self.__sourcePaths[i] = None

                if (i < self.__cameras - 1):
                    self.__dynamicWidgets[i + 1]["button"].grid_forget()
                    self.__dynamicWidgets[i + 1]["box"].config(bg=self.color_bg)

        self.resize_filepaths()

    # Überprüfe ob Pfad ein Gültiger ist
    def valid_path(self, path):
        valid = True

        if (path == ""):
            valid = False

        for i in self.__sourcePaths:

            if (path == i):
                self.console_out("File already imported")
                valid = False

        return valid

    # Aktualisiere Pfadkontainer
    def resize_filepaths(self):
        self.filepaths.clear()
        for file in self.__sourcePaths:
            if (file != None):
                self.filepaths.append(file)

        if (len(self.filepaths) >= 2):
            self.button_process.config(state=NORMAL)
        else:
            self.button_process.config(state=DISABLED)

    # easter egg
    def easter_egg(self, master):

        element = Entry(
            master,
            bg=self.color_bg,
            fg=self.color_fg,
            relief=SUNKEN
        )

        element.grid(
            row=14,
            column=0,
            columnspan=self.__cameras,
            sticky=W + E
        )

        element.focus()

        # bind RETURN key to check the password
        element.bind(
            '<Return>',
            lambda x,
                   e=element: self.key_pass(e)
        )

    # Überprüfe eingegebenes Passwort um easteregg zu öffnen
    def key_pass(self, widget):

        str = widget.get()

        if (str == self.__pw):
            self.console_out("Master Paul legt auf....")

        widget.grid_forget()

    # Methode um Pfadkontainer zu holen
    def get_paths(self):
        return self.filepaths

    # Verlasse den Thread und Zerstöre alle Fenster + Speicher
    def quit(self):

        # quit all running processes
        self.quit_thread()

        # close window
        self.root.destroy()

        print("[Status]: See you later ... 	Alligator");
        os._exit(0)

    def show_complete_window(self):

        self.complete_win = Toplevel(self.root)

        self.complete_win.grab_set()
        self.complete_win.configure(
            background=self.color_bg
        )

        self.complete_win.title("Save File")
        self.complete_win.resizable(
            height=False,
            width=False
        )

        self.complete_win.columnconfigure(0, minsize=30)
        self.complete_win.columnconfigure(3, minsize=30)
        self.complete_win.grid_rowconfigure(0, minsize=20)
        self.complete_win.grid_rowconfigure(9, minsize=20)
        self.complete_win.grid_rowconfigure(11, minsize=20)

        complete_message=Label(
            self.complete_win,
            text="Processing completed!",
            bg=self.color_bg,
            fg=self.font_color,
            font=(None, 13, 'bold')
        )
        complete_message.grid(
            row=1,
            column=1,
            columnspan=2,
            pady=5,
            padx=10
        )

        save_message = Label(
            self.complete_win,
            text="Do you want to save your file?",
            bg=self.color_bg,
            fg=self.font_color
        )
        save_message.grid(
            row=2,
            column=1,
            columnspan=2,
            pady=5,
            padx=10
        )

        self.button_quit = Button(
            self.complete_win,
            text="Cancel",
            bg=self.__red,
            fg='white',
            command=lambda: [self.complete_win.destroy(),self.complete_win.grab_release()]
        )

        self.button_quit.configure(
            height=2,
            width=10,
            activeforeground='white',
            activebackground=self.color_bg,
            bd=0
        )

        self.button_quit.bind(
            "<Enter>",
            self.button_quit.config(cursor="hand2")
        )
        self.button_quit.bind(
            "<Leave>",
            self.button_quit.config(cursor=None)
        )

        self.button_quit.grid(
            row=10,
            column=1,
            pady=5,
            padx=50,
            sticky=W
        )

        self.button_save = Button(
            self.complete_win,
            text="Save as",
            bg=self.color_fg,
            fg="white",
            command=lambda:[self.save_file(),self.complete_win.destroy()]
        )
        self.button_save.config(
            height=2,
            width=10,
            bd=0,
            activeforeground=self.color_fg,
            activebackground=self.color_bg
        )

        self.button_save.bind(
            "<Enter>",
            self.button_save.config(cursor="hand2")
        )
        self.button_save.bind(
            "<Leave>",
            self.button_save.config(cursor=None)
        )

        self.button_save.grid(
            row=10,
            column=2,
            pady=5,
            padx=50,
            sticky=E,
        )

        x = (self.root.winfo_x() + self.root.winfo_reqwidth() - self.complete_win.winfo_reqwidth())/2
        y = (self.root.winfo_y() + self.root.winfo_reqheight() - self.complete_win.winfo_reqwidth())/2
        self.complete_win.geometry("+%d+%d" % (x, y))


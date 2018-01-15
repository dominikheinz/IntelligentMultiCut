from tkinter import *
from tkinter.ttk import Combobox
import os
from tkinter.ttk import Style
from tkinter import messagebox
from src.classes.view.View import View
import json

class ConfigWindow(View):

    __settings = ""
    __framecnt = 0
    __frames = {}
    __widgets = {}
    __variables = {}
    __amount_widgets_frames = {}

    def __init__(self,window):
        # Erstelle Fenster
        self.root = Toplevel()
        self.gui=window

        #Lade Fenster Eigenschaften
        self.load_theme()
        self.set_padding()

        # Erstelle "Speicher" und "Quit" Button
        self.create_buttons()

        # Lade config-file
        self.load_settings()

        # Erstelle einen neuen Frame mit Überschrift
        self.create_frame("Theme")
        self.create_frame("Resolution")
        self.create_frame("Algorithm")
        self.create_frame("Miscellaneous")


        # Füge Checkboxen zu frames hinzu
        self.insert_checkbox_button("Miscellaneous", "Debug","debug")
        self.insert_checkbox_button("Miscellaneous", "Display OpenPose","display_openpose")
        self.insert_checkbox_button("Miscellaneous", "Display Cutter Preview", "display_cutterpreview")
        self.insert_checkbox_button("Miscellaneous", "Facetracking", "openpose_facetracking")
        self.insert_checkbox_button("Miscellaneous", "Show Algorithm Graphs", "show_algo_graphs")
        self.insert_checkbox_button("Miscellaneous", "Auto Sync Videos", "auto_sync")
        self.insert_checkbox_button("Miscellaneous", "Open output folder", "openfolder")

        # Füge radiobuttons zu frames hinzu
        self.insert_radiobuttons("Theme", ["Dark-Mode", "Light-Mode"], "theme")
        self.insert_radiobuttons("Algorithm",["Single - Person", "Distance - Detection","Multiperson - Amount","Multiperson - Closeup"],"algorithm")

        #Füge dropdown Menü für auflösung hinzu
        self.insert_resolution_dropdown("Resolution")

        #Handler für event (X-Knopf)
        self.root.protocol("WM_DELETE_WINDOW",lambda: [self.gui.button_settings.config(state="normal"),self.root.destroy()])

    # Erstelle "Save" und "Quit" Button
    def create_buttons(self):
        self.button_quit = Button(
            self.root,
            text="Quit",
            bg=self.red,
            fg='white',
            command=lambda: [self.gui.button_settings.config(state="normal"),self.root.destroy()]
        )

        self.button_quit.configure(
            height=2,
            width=15,
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
            row=19,
            column=1,
            pady=5,
            padx=4,
            sticky=W
        )

        self.button_save = Button(
            self.root,
            text="Save",
            bg=self.color_fg,
            fg="white",
            command=lambda:[self.gui.button_settings.config(state="normal"),self.save_settings()]
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
            row=19,
            column=2,
            sticky=E
        )

    # Padding für Fenster
    def set_padding(self):
        self.root.geometry('+50+50')
        self.root.resizable(
            height=False,
            width=False
        )
        self.root.columnconfigure(0, minsize=50)
        self.root.columnconfigure(20, minsize=50)
        self.root.rowconfigure(0, minsize=50)
        self.root.rowconfigure(18, minsize=30)
        self.root.rowconfigure(20, minsize=30)

    # Lade Einstellungen aus config
    def load_settings(self):

        # Versuche das settings file zu öffnen und zu parsen
        try:
            with open("config.json") as data_file:
                self.__settings = json.load(data_file)
            data_file.close()
        except Exception:
            print("[Error]: config file not found")

    # Speichere geänderte Einstellungen in config-file
    def save_settings(self):

        # Debug speichern
        if self.__variables['debug'].get() == True:
            self.config.set('debug', True)
        else:
            self.config.set('debug', False)


        # Display OpenPose speichern
        if self.__variables['display_openpose'].get() == True:
            self.config.set('display_openpose', True)
        else:
            self.config.set('display_openpose', False)

        # Show Graph speichern
        if self.__variables['show_algo_graphs'].get() == True:
            self.config.set('show_algo_graphs', True)
        else:
            self.config.set('show_algo_graphs', False)

        # Show Graph speichern
        if self.__variables['auto_sync'].get() == True:
            self.config.set('auto_sync', True)
        else:
            self.config.set('auto_sync', False)

        # Cutter Preview speichern
        if self.__variables['display_cutterpreview'].get() == True:
            self.config.set('display_cutterpreview', True)
        else:
            self.config.set('display_cutterpreview', False)


        # Facetracking speichern
        if self.__variables['openpose_facetracking'].get() == True:
            self.config.set('openpose_facetracking', True)
        else:
            self.config.set('openpose_facetracking', False)

        if self.__variables['openfolder'].get() == True:
            self.config.set('openfolder', True)
        else:
            self.config.set('openfolder', False)

        # Theme speichern
        if (self.__variables['theme'].get()== 0):
            self.config.set("color_bg", "#1D1D1D")
            self.config.set("font_color", "white")
            self.config.set("theme", 0)

        if (self.__variables['theme'].get() == 1):
            self.config.set("font_color", "black")
            self.config.set("color_bg", "white")
            self.config.set("theme", 1)
        if(self.__settings['theme'] != self.__variables['theme'].get()):

            # Wende Theme an (Nicht implementiert)
            self.apply_theme()

        else :
            self.root.destroy()


        # Algorithmus speichern
        if(self.__variables['algorithm'].get() == 0):
            self.config.set("algorithm",0)

        if (self.__variables['algorithm'].get() == 1):
            self.config.set("algorithm", 1)

        if (self.__variables['algorithm'].get() == 2):
            self.config.set("algorithm", 2)

        if (self.__variables['algorithm'].get() == 3):
            self.config.set("algorithm", 3)


        # Videoauflösung speichern
        resolution=self.__variables['resolution'].get()
        values=resolution.split("x")
        self.config.set('video_width', int(values[0]))
        self.config.set('video_height', int(values[1]))

    # Lade Theme Eigenschaften + Icon und Titel für Fenster
    def load_theme(self):

        self.color_bg = self.gui.color_bg
        self.color_fg = self.gui.color_fg
        self.red = self.gui.red
        self.font_color = self.gui.font_color

        self.root.configure(
            background=self.color_bg
        )

        if os.name == "nt":
            self.root.iconbitmap(self.root,'static/icon.ico')

        self.root.title("Settings")

    # Erstelle neuen Frame mit Überschrift
    def create_frame(self,header):

        new_frame=Frame(
            self.root,
            bg=self.color_bg,
            highlightbackground=self.color_fg,
            highlightthickness=1,
        )

        new_frame.grid(
            row=int(self.__framecnt/2)+1,
            column=(self.__framecnt%2)+1,
            pady=2,
            padx=5,
            sticky=W+E+N+S
        )

        new_frame.columnconfigure(5,minsize=100)

        header_label=Label(
            new_frame,
            text=header,
            bg=self.color_bg,
            fg=self.font_color,
            font="Verdana 10 bold"
        )
        header_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=2,
            sticky=W
        )

        self.__framecnt += 1

        self.__frames[header]=new_frame
        self.__amount_widgets_frames[header]=1

    #Füge neue checkbox zu Frame hinzu
    def insert_checkbox_button(self,frame_name,widget_label,config_entry):

        new_variable=BooleanVar()

        new_checkbox=Checkbutton(
            self.__frames[frame_name],
            text=widget_label,
            variable=new_variable,
            bg=self.color_bg,
            activebackground=self.color_bg,
            activeforeground=self.font_color,
            fg=self.font_color,
            selectcolor=self.color_bg
        )

        new_checkbox.grid(
            row=self.__amount_widgets_frames[frame_name],
            column=0,
            sticky=W,
            padx=10
        )

        self.__widgets[config_entry] = new_checkbox
        self.__variables[config_entry] = new_variable

        # Lade einstellungen aus config-file
        if (self.__settings[config_entry] == True):
            self.__widgets[config_entry].select()
        else:
            self.__widgets[config_entry].deselect()

        self.__amount_widgets_frames[frame_name]+=1


    def insert_radiobuttons(self,frame_name,radio_labels,config_entry):
        # Variable die mit Radiobuttons verknüpft werden
        new_variable = IntVar()

        for label_count in range(0, len(radio_labels)):
            new_radio = Radiobutton(
                self.__frames[frame_name],
                text=radio_labels[label_count],
                variable=new_variable,
                value=label_count,
                bg=self.color_bg,
                activebackground=self.color_bg,
                activeforeground=self.font_color,
                fg=self.font_color,
                selectcolor=self.color_bg
            )

            new_radio.grid(
                row=self.__amount_widgets_frames[frame_name],
                column=0,
                sticky=W,
                padx=10
            )

            try:
                if (self.__settings[config_entry] == label_count):
                    new_variable.set(label_count)
            except:
                self.__settings[config_entry] = None

            self.__amount_widgets_frames[frame_name] += 1


        self.__variables[config_entry] = new_variable



    def insert_resolution_dropdown(self, frame_name):

        OPTIONS = [
            "1920x1080",
            "1080x1920",
            "1280x720",
            "720x1280"
        ]

        new_variable = StringVar()

        new_dropdown = Combobox(
            self.__frames[frame_name],
            textvariable=new_variable,
        )

        new_dropdown['values']=OPTIONS
        new_dropdown['state'] = 'readonly'

        new_dropdown.grid(
            row=self.__amount_widgets_frames[frame_name],
            column=0,
            columnspan=6,
            sticky=W+E,
            padx= 10
        )

        # new_dropdown.configure(
        #     bg=self.color_bg,
        #     activebackground=self.color_bg,
        #     activeforeground=self.font_color,
        #     highlightbackground=self.color_fg,
        #     highlightthickness=1,
        #     fg=self.font_color,
        #     font="Verdana 10",
        #
        # )
        # new_dropdown['menu'].config(
        #     bg=self.color_bg,
        #     fg=self.font_color,
        # )
        #
        # new_dropdown.bind(
        #     "<Enter>",
        #     new_dropdown.config(cursor="hand2")
        # )
        # new_dropdown.bind(
        #     "<Leave>",
        #     new_dropdown.config(cursor=None)
        # )
        #
        # new_dropdown.grid(
        #     row=self.__amount_widgets_frames[frame_name],
        #     column=0,
        #     columnspan=6,
        #     sticky=W+E,
        #     padx= 10
        # )
        try:
                new_variable.set(str(self.__settings['video_width'])+"x"+str(self.__settings['video_height']))
        except:
            self.__settings['video_width'] = None
            self.__settings['video_height'] = None

        self.__variables['resolution']=new_variable
        self.__amount_widgets_frames[frame_name] += 1

    def apply_theme(self):
        if messagebox.askyesno("Reload MultiCut?", "To apply theme changes, you have to restart the application. Do you want to restart now? "):
            self.gui.restart = True
            self.gui.quit()
        else:
            self.root.destroy()


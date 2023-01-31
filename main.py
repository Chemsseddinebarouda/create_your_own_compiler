import subprocess
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os



class Mini_editeur:
    def __init__(self):
        # Declararation des variables
        self.filepath = ""
        self.filename = "New"
        self.filetypes = (["Python File", "*.py"], ["All Files", "*.*"])
        # Creation du fenetre
        self.root = Tk()

        # fenetre

        self.scroll = Scrollbar(self.root, bg="#44475a")
        run_btn = PhotoImage(file='run.png')
        photoimage = run_btn.subsample(3, 3)

        # Let us create a dummy button and pass the image

        self.bouton = Button(self.root, text="Run", compound=LEFT, image=photoimage, command=self.Run, bg="#44475a",
                        borderwidth=0)
        self.output = Text(self.root, yscrollcommand=self.scroll.set, bg="#44475a", fg="white")
        self.codeEditor = Text(self.root, undo=1, tabs=1, yscrollcommand=self.scroll.set, font=35, bg="#44475a",
                               fg="white")
        self.frame = Frame(self.root, bg="#44475a")

        self.root.title(f"Mini_editeur - {self.filename}")

        self.ConfigureMenus()

        # placement des composant
        self.frame.pack(side=LEFT, fill=Y)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.codeEditor.pack(fill=BOTH, ipady=10)
        self.scroll.config(command=self.codeEditor.yview)
        self.output.insert("end-1c", "Le resultat sera afficher ici.....")
        self.bouton.pack(side=RIGHT, ipady=100)
        self.bouton.config()
        self.output.config(state=DISABLED)
        self.scroll.config(command=self.output.yview)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.output.pack(fill=X, side=BOTTOM)
        self.scroll.config(command=self.codeEditor.yview)

        photo = PhotoImage(file="logo2.png")
        self.root.iconphoto(False, photo)
        self.root.geometry("1100x600")
        self.root.configure(bg="red")

        # clÃƒÂ© clavier
        self.root.bind_all("<Control-o>", self.Ouvrir)
        self.root.bind_all("<Control-s>", self.Enregistrer)
        self.root.bind_all("<Control-r>", self.Run)
        self.root.bind_all("Control-n", self.Nouveau)
        # afficher l'interface
        self.root.mainloop()



    def Copier(self):
        selected = self.codeEditor.get(SEL_FIRST, SEL_LAST)
        self.codeEditor.clipboard_clear()
        self.codeEditor.clipboard_append(selected)

    def coller(self):
        self.codeEditor.insert(INSERT, self.codeEditor.clipboard_get())

    def Supprimer(self):
        self.codeEditor.delete(SEL_FIRST, SEL_LAST)

    def couper(self):
        self.Copier()
        self.Supprimer()

    def selectionner_tout(self):
        self.codeEditor.tag_add(SEL, "1.0", END)


    def ConfigureMenus(self):
        self.menu = Menu(self.root)

        self.projectMenu = Menu(self.menu, tearoff=0, bg='#44475a', fg='white')

        self.projectMenu.add_command(label="Ouvrir L'emplacement", command=self.Ouvre_EMpla)
        self.projectMenu.add_command(label="Ouvrir Terminale", command=self.Ouvre_Terminale)
        self.fileMenu = Menu(self.menu, tearoff=0, bg='#44475a', fg='white')
        self.fileMenu.add_command(label="Ouvrir Fihier", command=self.Ouvrir, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Nouveau Fichier", command=self.Nouveau, accelerator="Ctrl+N")
        self.fileMenu.add_command(label="Sauvgarder", command=self.Enregistrer, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="Enregistrer Sous", command=self.EnrSous)
        self.fileMenu.add_separator()
        self.RunMenu = Menu(self.menu, tearoff=0, bg='#44475a', fg='white')
        self.RunMenu.add_command(label="Run", command=self.Run, accelerator="Ctrl+R")

        self.fileMenu.add_command(label="Quitter", command=self.Quitter)
        # Create the Edit Menu
        self.editer_Menu = Menu(self.menu, tearoff=0, bg='#44475a', fg='white')
        self.editer_Menu.add_command(label="Copier", command=self.Copier, accelerator="Ctrl+C")
        self.editer_Menu.add_command(label="Coller", command=self.coller, accelerator="Ctrl+V")
        self.editer_Menu.add_command(label="Supprimer", command=self.Supprimer, accelerator="Delete")
        self.editer_Menu.add_command(label="Couper", command=self.couper, accelerator="Ctrl+X")
        self.editer_Menu.add_separator()
        self.editer_Menu.add_command(label="Selectionner Tout", command=self.selectionner_tout, accelerator="Ctrl+A")


        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Editer", menu=self.editer_Menu)
        self.menu.add_cascade(label="Projet", menu=self.projectMenu)
        self.menu.add_cascade(label="Run", menu=self.RunMenu)
        self.root.config(menu=self.menu)
    def Ouvrir(self, event=None):
        try:
            # ouvrir le fichier et recuperer le contenu de ce fichier
            self.file = filedialog.askopenfile(parent=self.root, filetypes=self.filetypes)
            # enregister le lien de fichier
            self.filepath = self.file.name
            self.fileContents = self.file.read()  # contenu du fichier
            # fermer fichier
            self.file.close()
            # copier en editeur
            self.codeEditor.delete(0.0, END)
            self.codeEditor.insert(END, self.fileContents)

            self.filename = os.path.split(self.filepath)[1]  # nom de fichier
            self.root.title(f"Mini_editeur - {self.filename}")
        except PermissionError:
            messagebox.showerror("Oops!", "t'es pas capable d'ouvrir le fichier")

    def Enregistrer(self, event=None):
        try:
            if self.filepath != "":
                self.file = open(self.filepath, "w", encoding='utf-8')
                self.file.write(self.codeEditor.get(0.0, END))
                self.file.close()
                return True
            else:
                self.EnrSous()
        except PermissionError:
            messagebox.showerror( "t'es pas capable de modifier le fichier")
        except:
            messagebox.showerror("erreur!")

    def Nouveau(self, event=None):
        self.filepath = ""
        self.filename = "New"
        self.codeEditor.delete(0.0, END)
        self.root.title(f"Mini_editeur - {self.filename}")

    def Run(self, event=None):
        if not self.Enregistrer():
            return
        self.output.delete('1.0', END)
        self.process = subprocess.Popen(f"py {self.filepath}", stdout=subprocess.PIPE, shell=True,
                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.out, self.err = self.process.communicate()
        # aficher element de sortie
        self.output.config(state=NORMAL)
        self.output.delete(0.0, END)
        self.output.insert("end-1c", self.out)
        self.output.insert("end-1c", self.err)
        self.output.config(state=DISABLED)
    def Ouvre_EMpla(self):
        # change des slaches/
        self.nouveau_fich = self.filepath.replace("/", "\\")
        subprocess.Popen(rf'explorer /select, "{self.nouveau_fich}"')

    def Quitter(self):
        self.root.destroy()

    def Ouvre_Terminale(self):
        self.nouveau_fich = self.filepath.replace("/", "\\")
        os.system(rf"start cmd /K cd {self.nouveau_fich}")

    def EnrSous(self):
        try:
            self.file = filedialog.asksaveasfile(mode="w", initialfile=self.filename, defaultextension="*.txt",
                                                 filetypes=self.filetypes)
            self.file.write(self.codeEditor.get(0.0, END))
            self.filepath = self.file.name
            self.file.close()
            self.filename = os.path.split(self.file.name)[1]
            self.root.title(f"Mini_editeur - {self.filename}")
            return True
        except AttributeError:
            pass

window = Mini_editeur()



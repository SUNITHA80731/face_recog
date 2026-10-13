from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
#from PIL import ImageTk, Image
from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Segoe UI', size=18, weight="bold")
        self.button_font = tkfont.Font(family='Segoe UI', size=11, weight="bold")
        self.label_font = tkfont.Font(family='Segoe UI', size=12, weight="bold")
        self.title("Face Recognition System")
        self.resizable(False, False)
        self.geometry("600x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#1e88e5"
        self.secondary_color = "#0d47a1"
        self.accent_color = "#ff6f00"
        self.text_color = "#212121"
        self.configure(bg=self.bg_color)
        
        container = tk.Frame(self, bg=self.bg_color)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=controller.bg_color)
            self.controller = controller
            
            # Try to load image, if not found create placeholder
            try:
                render = PhotoImage(file='homepagepic.png')
                img = tk.Label(self, image=render, bg=controller.bg_color)
                img.image = render
                img.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=15, pady=10)
            except:
                # Placeholder if image missing
                img = tk.Label(self, text="👤", font=('Arial', 80), bg=controller.bg_color, fg=controller.primary_color)
                img.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=15, pady=10)
            
            label = tk.Label(self, text="Face Recognition System", font=self.controller.title_font, fg=self.controller.primary_color, bg=controller.bg_color)
            label.grid(row=0, sticky="ew", pady=15)
            
            button1 = tk.Button(self, text="   Sign up  ", fg="#ffffff", bg=self.controller.primary_color, font=controller.button_font, activebackground=self.controller.secondary_color, command=lambda: self.controller.show_frame("PageOne"), relief="flat", padx=15, pady=10)
            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg=self.controller.primary_color, font=controller.button_font, activebackground=self.controller.secondary_color, command=lambda: self.controller.show_frame("PageTwo"), relief="flat", padx=15, pady=10)
            button3 = tk.Button(self, text="Quit", fg=self.controller.primary_color, bg="#ffffff", font=controller.button_font, activebackground="#e0e0e0", command=self.on_closing, relief="flat", padx=15, pady=10)
            
            button1.grid(row=1, column=0, ipady=8, ipadx=10, padx=10, pady=8)
            button2.grid(row=2, column=0, ipady=8, ipadx=10, padx=10, pady=8)
            button3.grid(row=3, column=0, ipady=8, ipadx=10, padx=10, pady=8)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller
        
        title_label = tk.Label(self, text="Create New User", font=controller.title_font, fg=controller.primary_color, bg=controller.bg_color)
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=20)
        
        name_label = tk.Label(self, text="Enter your name:", fg=controller.text_color, font=controller.label_font, bg=controller.bg_color)
        name_label.grid(row=1, column=0, pady=15, padx=15, sticky="w")
        
        self.user_name = tk.Entry(self, borderwidth=2, bg="#ffffff", font=('Segoe UI', 11), relief="flat")
        self.user_name.grid(row=1, column=1, columnspan=2, pady=15, padx=15, sticky="ew", ipady=8)
        
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg=controller.primary_color, font=controller.button_font, activebackground="#e0e0e0", command=lambda: controller.show_frame("StartPage"), relief="flat", padx=15)
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg=controller.primary_color, font=controller.button_font, activebackground=controller.secondary_color, command=self.start_training, relief="flat", padx=15)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg=controller.accent_color, font=controller.button_font, activebackground="#e65100", relief="flat", padx=15)
        
        self.buttoncanc.grid(row=2, column=0, pady=20, ipadx=10, ipady=8, padx=10)
        self.buttonext.grid(row=2, column=1, pady=20, ipadx=10, ipady=8, padx=10)
        self.buttonclear.grid(row=2, column=2, pady=20, ipadx=10, ipady=8, padx=10)
        
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        global names
        self.controller = controller
        
        title_label = tk.Label(self, text="Select a Trained User", font=controller.title_font, fg=controller.primary_color, bg=controller.bg_color)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=20)
        
        label = tk.Label(self, text="Select user:", fg=controller.text_color, font=controller.label_font, bg=controller.bg_color)
        label.grid(row=1, column=0, padx=15, pady=15, sticky="w")
        
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg=controller.primary_color, font=controller.button_font, activebackground="#e0e0e0", relief="flat", padx=15)
        self.menuvar = tk.StringVar(self)
        
        # Build list of users: include signed-up names and trained classifier names
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        classifiers_dir = os.path.join(script_dir, 'data', 'classifiers')
        trained_users = []
        if os.path.exists(classifiers_dir):
            for f in os.listdir(classifiers_dir):
                if f.endswith('_classifier.xml'):
                    user = f.replace('_classifier.xml', '')
                    trained_users.append(user)

        # Combine global `names` (signed-up users) with trained users, keep order and unique
        combined = []
        for n in list(names):
            if n and n not in combined:
                combined.append(n)
        for t in trained_users:
            if t and t not in combined:
                combined.append(t)

        # If there are no users, show an informative placeholder
        if not combined:
            combined = ['']

        self.dropdown = tk.OptionMenu(self, self.menuvar, *combined)
        self.dropdown.config(bg="#ffffff", fg=controller.text_color, font=controller.label_font, activebackground=controller.primary_color, activeforeground="#ffffff", relief="flat", bd=1)
        self.dropdown["menu"].config(bg="#ffffff", fg=controller.text_color, font=('Segoe UI', 11))
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg=controller.primary_color, font=controller.button_font, activebackground=controller.secondary_color, relief="flat", padx=15)
        
        self.dropdown.grid(row=1, column=1, ipadx=8, padx=15, pady=15, sticky="ew")
        self.buttoncanc.grid(row=2, ipadx=10, ipady=8, column=0, pady=20, padx=10)
        self.buttonext.grid(row=2, ipadx=10, ipady=8, column=1, pady=20, padx=10)
        
    def next_foo(self):
        name = self.menuvar.get()
        if not name:
            messagebox.showerror("ERROR", "Please select a user first!")
            return

        # Check if classifier exists for selected user
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        classifier_path = os.path.join(script_dir, 'data', 'classifiers', f'{name}_classifier.xml')
        if not os.path.exists(classifier_path):
            # Prompt to capture/train now
            res = messagebox.askyesno("User Not Trained", f"User '{name}' has no trained classifier.\nDo you want to capture data and train now?")
            if res:
                self.controller.active_name = name
                self.controller.show_frame("PageThree")
            else:
                messagebox.showinfo("Info", "User not trained. You can train later from Sign up -> Capture -> Train.")
            return

        # Classifier exists: proceed to recognition page
        self.controller.active_name = name
        self.controller.show_frame("PageFour")
        
    def clear(self):
        self.user_name.delete(0, 'end')
        
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))
            
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller
        
        title_label = tk.Label(self, text="Capture & Train Model", font=controller.title_font, fg=controller.primary_color, bg=controller.bg_color)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=20)
        
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font=controller.label_font, fg=controller.text_color, bg=controller.bg_color)
        self.numimglabel.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15, padx=15)
        
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg=controller.primary_color, font=controller.button_font, activebackground=controller.secondary_color, command=self.capimg, relief="flat", padx=15, pady=8)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg=controller.accent_color, font=controller.button_font, activebackground="#e65100", command=self.trainmodel, relief="flat", padx=15, pady=8)
        
        self.capturebutton.grid(row=2, column=0, ipadx=10, ipady=10, padx=15, pady=20)
        self.trainbutton.grid(row=2, column=1, ipadx=10, ipady=10, padx=15, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller

        title_label = tk.Label(self, text="Face Recognition", font=controller.title_font, fg=controller.primary_color, bg=controller.bg_color)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=20)
        
        button1 = tk.Button(self, text="Start Recognition", command=self.openwebcam, fg="#ffffff", bg=controller.primary_color, font=controller.button_font, activebackground=controller.secondary_color, relief="flat", padx=20, pady=8)
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg=controller.primary_color, font=controller.button_font, activebackground="#e0e0e0", relief="flat", padx=20, pady=8)
        
        button1.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=10, padx=15, pady=15)
        button4.grid(row=1, column=1, sticky="ew", ipadx=10, ipady=10, padx=15, pady=15)

    def openwebcam(self):
        main_app(self.controller.active_name)


app = MainUI()
try:
    app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
except:
    pass  # Icon not found, continue without it
app.mainloop()


from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
import os
import shutil

os.chdir(os.path.dirname(__file__))


class plot_window():

    def __init__(self, scene, plot):
        self.win = Toplevel(scene)
        self.win.title("Plot visualisation")
        self.raw_plot = plot
        self._create_menu_bar()
        self._load_plot()


    def _create_menu_bar(self):
        self.menu_bar_plot = Menu(self.win)
        self.win['menu'] = self.menu_bar_plot

        self.menu_file = Menu(self.menu_bar_plot, tearoff=0)
        self.menu_file.add_command(label="Save plot Ctrl + S", command = self._save_plot)
        self.menu_bar_plot.add_cascade(label = "Save", menu = self.menu_file)

        self.menu_stat = Menu(self.menu_bar_plot, tearoff = 0)
        self.menu_stat.add_command(label = "Size and labels", command = self.win_label)
        self.menu_stat.add_command(label = "Color", command = None)
        self.menu_stat.add_command(label = "Sub groups", command = None)
        self.menu_bar_plot.add_cascade(label="Customisation", menu = self.menu_stat)

        self.win.bind_all("<Control-s>", lambda x: self._save_plot)
  

    def _load_plot(self):
        self.img = PhotoImage(file="tmp/plot_raw.png")
        img_width = self.img.width()
        img_height = self.img.height()

        # Ajuster la taille de la fenêtre et du canvas en fonction de la taille de l'image
        self.win.geometry(f"{img_width}x{img_height}")
        self.canva = Canvas(self.win, width=img_width, height=img_height)
        self.canva.pack()

        self.canva.create_image(0, 0, anchor=NW, image=self.img)

    def _save_plot(self):
        file_path = asksaveasfilename(defaultextension=".png",
                                      filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.raw_plot.plot.save(file_path)
            shutil.rmtree("tmp") # delete the tmp folder

    def win_label(self):
        self.custom_label = Toplevel(self.win)
        self.custom_label.title("Customisation panel")

        self.list_label = {
            "Title" : [self.raw_plot.Title],
            "Title size" : [self.raw_plot.Title_size],
            "xlab title" : [self.raw_plot.xlab_title],
            "xlab size" : [self.raw_plot.xlab_size],
            "ylab title" : [self.raw_plot.ylab_title],
            "ylab size" : [self.raw_plot.ylab_size],      
        }
        if self.raw_plot.test != "None":
            self.list_label["Star size"] = [self.raw_plot.Star_size]
            self.list_label["Star space size"] = [self.raw_plot.Star_space_size]
            self.list_label["Line space size"] = [self.raw_plot.Line_space_size]

        self.row = 0
        for label, var in self.list_label.items():
            self.text = Label(self.custom_label, text=label)
            self.text.grid(row=self.row, column=0, pady=10, padx=10, sticky=W)
            
            if "size" in label:
                self.box = Spinbox(self.custom_label, from_= var[0], to=100)
            else:
                self.box = Entry(self.custom_label)
                self.box.insert(0, var[0])
            
            self.box.grid(row=self.row, column=1, pady=10, padx=10, sticky=W)
            self.list_label[label].append(self.box)
            self.row += 1

        self.update_button = Button(self.custom_label, text="Apply", command=self.update_var)
        self.update_button.grid(row=self.row, column=0, columnspan=2, pady=10, padx=10)

    def update_var(self):
        """
        Method to update the size and the title of the plot
        """
        for label, var in self.list_label.items(): # browse the label and the attributes
            self.new_val = var[1].get() # get the entry by the user
            if "size" in label :
                try:
                    self.new_val = float(self.new_val)
                except Exception as e:
                    messagebox.showerror(f"Please use the . to specify a float number in a spinbox : \n {e}")
            setattr(self.raw_plot, label.replace(" ", "_"), self.new_val) # update the object with the new value
        self.raw_plot.plot_data()
        self.canva.destroy()
        self._load_plot() # refresh the plot
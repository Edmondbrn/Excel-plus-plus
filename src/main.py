import os
import pandas as pd
from plot_window import plot_window
from plot import *
try:
    from tkinter import * 
    from tkinter.ttk import *
    from tkinter.filedialog import askopenfilename
    from tkinter import messagebox
except ImportError:
    os.system("pip3 install tk")
    from tkinter import *

os.chdir(os.path.dirname(os.path.dirname(__file__)))
class excel(Tk):


    def __init__(self):
        Tk.__init__(self)
        self.frame = Frame(self)
        self.frame.pack(expand=True, fill=BOTH)
        self.menu_bar()
        self.title("Excel ++")
        self.geometry("1200x720")
    
    def menu_bar(self):
        """
        Method to create the menu tool bar at the top of the window
        """
        self.menu_bar = Menu(self.frame)

        self.menu_file = Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Open...  Ctrl + O", command = self.open_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label = "File", menu = self.menu_file)

        self.menu_stat = Menu(self.menu_bar, tearoff = 0)
        self.menu_stat.add_command(label = "Plot Ctrl + P", command = self.var_window)
        self.menu_stat.add_command(label = "Statistic Ctrl + T", command = self.stat_window)
        self.menu_bar.add_cascade(label="Analysis", menu = self.menu_stat)

        self.menu_help = Menu(self.menu_bar, tearoff=0)
        self.menu_help.add_command(label="Help Ctrl + H")
        self.menu_bar.add_cascade(label="About", menu = self.menu_help)

        self.bind_all("<Control-h>", lambda x: self.help)
        self.bind_all("<Control-o>", lambda x: self.open_file())
        self.bind_all("<Control-q>", lambda x: self.quit)
        self.bind_all("<Control-t>", lambda x: self.stat_window)
        self.bind_all("<Control-p>", lambda x: self.var_window)

        self.config(menu=self.menu_bar)

    def open_file(self):
        self.file = askopenfilename(title="Choose the file to open",
                                filetypes=[("CSV file", ".csv"), ("excel file", ".xlsx"), ("text files", ".txt")]) # store the  absolute path of the chosen file
        if type(self.file) == tuple or self.file == None: # cut the process of no file has been chosen
            print("teste")
            return
        try:
            if self.file.endswith(".xlsx"):
                self.data = pd.read_excel(self.file)
                self.load_table(self.data) # display the table
            else:
                # Create a new window to select the separator
                self.separator_window = Toplevel(self.frame)
                self.separator_window.title("Select CSV Separator")

                self.separator_label = Label(self.separator_window, text="Choose the separator used in the CSV file:")
                self.separator_label.pack(pady=10)

                self.separator_var = StringVar(self.separator_window)
                self.separator_var.set(",")  # default value

                self.separator_options = [",", ";", "Tab", "|", "Space"]
                self.separator_menu = OptionMenu(self.separator_window, self.separator_var, *self.separator_options)
                self.separator_menu.pack(pady=10)

                load_button = Button(self.separator_window, text="Load CSV", command = self.load_csv) # confirmation button
                load_button.pack(pady=10)

                
        except Exception as e:
            messagebox.showwarning("Error loading", f"An error occurred while reading the file.\nPlease check the specified file format.\nError: {e}")
    
    
    def var_window(self):
        """
        Method to create the window for the variable selection
        """
        self.graph_window = Toplevel(self.frame)
        self.graph_window.title("Plot menu options")
        self.var_label = Label(self.graph_window, text = "Choose both variables to use")
        self.check_vars = []  # Liste pour stocker les variables IntVar

        try:
            self.row = 1
            self.col = 0
            for var in self.data.columns:
                var_int = IntVar()  # Créez une variable pour chaque case à cocher
                self.check_vars.append((var, var_int))  # Ajoutez la variable à la liste
                self.box = Checkbutton(self.graph_window, text=str(var), variable=var_int)
                self.box.grid(row=self.row, column=self.col, padx=5, pady=5)  # Grid to organise the chip by 4

                self.col += 1
                if self.col == 4:  # go to the next row
                    self.col = 0
                    self.row += 1
            
            # Bouton pour valider la sélection
            self.submit_button = Button(self.graph_window, text="Confirm", command=self.get_checked_vars)
            self.submit_button.grid(row=self.row + 1, column=0, columnspan=4, pady=10)  # Utilisation de grid pour le bouton
        except Exception as e:
            messagebox.showwarning("Error data.", "Please first load a data table\n" + str(e))
        

    def get_checked_vars(self):
        """
        Get the variable to plot the graph and display the menu to choose the type of graph
        """
        self.checked_vars = [var for var, var_int in self.check_vars if var_int.get() == 1] # if the box is checked, so value equals 1
        self.graph_type = StringVar(self.graph_window) # list for the type of plot
        self.test_type = StringVar(self.graph_window) # list for the type of plot
        self.param_X = StringVar(self.graph_window)
        self.param_Y = StringVar(self.graph_window)
        self.param_Col = StringVar(self.graph_window)

        try :
            if hasattr(self, 'separator_plot'):
                self.separator_plot.destroy()  # reset the widgets if the button is pressed again
            if hasattr(self, 'plot_label'):
                self.plot_label.destroy()
            if hasattr(self, 'test_label'):
                self.test_label.destroy()
            if hasattr(self, 'param_label'):
                self.param_label.destroy()
            if hasattr(self, 'separator_test'):
                self.separator_test.destroy()
            if hasattr(self, 'separator_param'):
                self.separator_param.destroy()
            if hasattr(self, 'separator_param_X'):
                self.separator_param_X.destroy()
            if hasattr(self, 'separator_param_Y'):
                self.separator_param_Y.destroy()
            if hasattr(self, 'separator_param_Col'):
                self.separator_param_Col.destroy()
        except AttributeError as e:
            print(e)
        
        self.plot_label = Label(self.graph_window, text = "Please choose the type of plot and the test to perform:") # create the menu for choosing the type of plot
        self.graph_type.set("violin")
        self.graph_value = ["violin", "box", "bar", "scatter", "regression"]
        self.separator_plot = OptionMenu(self.graph_window, self.graph_type, self.graph_value[0],*self.graph_value)

        self.test_type.set("ttest") # menu for the test
        self.test_value = ["ttest", "wilcox", "chi2", "fisher", "Pearson correlation", "linear regression", "Anova", "Kruskall"]
        self.separator_test = OptionMenu(self.graph_window, self.test_type, self.test_value[0],*self.test_value)

        self.plot_param = Label(self.graph_window, text = "Please choose the parameters for the plot:") # create the menu for choosing the parameters for the plot
        self.plot_param_X = Label(self.graph_window, text = "X axis :") # create the menu for choosing the parameters for the plot
        self.plot_param_Y = Label(self.graph_window, text = "Y axis :") # create the menu for choosing the parameters for the plot
        self.plot_param_Col = Label(self.graph_window, text = "Color by :") # create the menu for choosing the parameters for the plot

        self.param_X.set(self.checked_vars[0]) # menu for the parameters
        self.param_Y.set(self.checked_vars[0]) # menu for the parameters
        self.param_Col.set(self.checked_vars[0]) # menu for the parameters
        self.separator_param_X = OptionMenu(self.graph_window, self.param_X, self.checked_vars[0], *self.checked_vars)
        self.separator_param_Y = OptionMenu(self.graph_window, self.param_Y, self.checked_vars[0], *self.checked_vars)
        self.separator_param_Col = OptionMenu(self.graph_window, self.param_Col, self.checked_vars[0], *self.checked_vars)

        self.plot_label.grid(row = self.row + 2, column = 0, columnspan = 4) # add the menu to the screen
        self.separator_test.grid(row = self.row + 3, column = 0, columnspan = 4, pady = 10)
        self.separator_plot.grid(row = self.row + 4, column = 0, columnspan = 4, pady = 10)

        self.plot_param.grid(row = self.row + 5, column = 0, columnspan = 4)

        self.plot_param_X.grid(row=self.row + 6, column=0, padx=1, columnspan = 2)  # align to the right
        self.separator_param_X.grid(row=self.row + 6, column=0, columnspan=4, padx=1, pady=5)  # align to the left

        self.plot_param_Y.grid(row=self.row + 7, column=0, padx=1, columnspan = 2)  # align to the right
        self.separator_param_Y.grid(row=self.row + 7, column=0, columnspan=4, padx=1, pady=5)  # align to the left

        self.plot_param_Col.grid(row=self.row + 8, column=0, padx=1, columnspan = 2)  # align to the right
        self.separator_param_Col.grid(row=self.row + 8, column=0, columnspan=4, padx=1, pady=5)  # align to the left

        self.plot_button = Button(self.graph_window, text="Plot!", command=self.start_window_plot)
        self.plot_button.grid(row=self.row + 9, column=0, columnspan=4, pady=10) 

    def start_window_plot(self):
        self.plot_raw = plot(self.data, self.graph_type.get(), self.param_X.get(), self.param_Y.get(), self.param_Col.get())
        self.plot_raw.plot_data() # create the first raw plot
        self.plot_window = plot_window(self.frame, self.plot_raw)
    
    def stat_window(self):
        pass

    def load_csv(self):
        """
        Method to load and display the table from a csv file
        """
        self.separator = self.separator_var.get()
        if self.separator == "Tab":
            self.separator = "\t"
        elif self.separator == "space":
            self.separator = " "
        elif self.separator == "": # if nothing is chosen
            return
        self.data = pd.read_csv(self.file, sep=self.separator)
        self.separator_window.destroy()
        self.file = None
        self.load_table(self.data)

    def clean_window(self):
        """
        Method to remove the element of the window
        """
        try:
            self.treeview.destroy() # clean the variable for further use
            self.h_scroll.destroy() # I could put them in a frame, but for three objects, it's okay
            self.v_scroll.destroy()
        except:
            pass

    def load_table(self, df : pd.DataFrame):
        """
        Method to create the table from a file read by pandas
        """
        self.clean_window()
        self.col_widths = dict()
        self.treeview = Treeview(self.frame, columns = list(df.columns), show = "headings") # create the treeview with the column name from the table
        self.treeview.heading("#0", text = "row") # specify the first column as the row number column
        
        for col in df.columns: # create all the column in the windows
            self.treeview.heading(str(col), text = col)
            self.treeview.column(col, anchor='center')  # Center the values in the column
            self.col_widths[col] = 1 # initialise the dictionnary for the size adjustment
        for i in range(df.shape[0]): # insert the value of each line
            self.value = df.iloc[i].tolist()
            for y in range(len(self.value)): # browse the value to see if there is a numeric value and round it if necessary
                try:
                    num = float(self.value[y])
                except:
                    num = 0
                else:
                    self.value[y] = round(num, 3)
                self.col_widths[df.columns[y]] = max(self.col_widths[df.columns[y]], len(str(self.value[y])))
            if i % 2 == 0:
                tag_cell = "gray"
            else:
                tag_cell = "white"
            self.treeview.insert("", # insert the value in the table
                                END,
                                text=str(i),
                                values= self.value,
                                tag = tag_cell
                                )
            self.treeview.tag_configure('gray', background='#cccccc')
            self.treeview.tag_configure('white', background='#ffffff')

            
        for col, width in self.col_widths.items(): # resize the cell size
            self.treeview.column(col, width=max(width * 12, len(str(col)) *12))  # Adjust the multiplier as needed for better fit

        self.format_table() # add the scroll bar and some shape lines
        self.treeview.pack(expand=True, fill=BOTH)  # Assurez-vous que le Treeview est empaqueté correctement

    def format_table(self):
        self.style = Style()
        self.style.configure("Treeview.Heading", borderwidth=1, relief="solid")
        self.style.configure("Treeview", rowheight=50, borderwidth=1, relief="solid", background="white", foreground="black", fieldbackground="white")
        self.style.map("Treeview", background=[('selected', 'darkblue')], foreground=[('selected', 'white')])

        self.v_scroll = Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.treeview.configure(yscrollcommand=self.v_scroll.set)

        # Create horizontal scrollbar
        self.h_scroll = Scrollbar(self.frame, orient="horizontal", command=self.treeview.xview)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.treeview.configure(xscrollcommand=self.h_scroll.set)



    def start(self):
        self.mainloop()


gui = excel()
gui.start()
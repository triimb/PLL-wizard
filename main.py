import time
from tkinter import *
import tkinter.messagebox
import customtkinter
import PLL_design
import pyglet, os
import LTSpice_simulation

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title("PLL Wizard")
        self.geometry(f"{720}x{514}")
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageIntermediate, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(customtkinter.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)
        label = customtkinter.CTkLabel(self, text="PLL Wizard", font=("Roboto-Bold", 40, "bold"))
        label.place(rely=0.3, relx=0.5, anchor=CENTER)

        button = customtkinter.CTkButton(self, text="Start", font=("Roboto-Bold", 15),
                           command=lambda: controller.show_frame(PageOne))
        button.place(rely=0.55, relx=0.5, anchor=CENTER)

        button2 = customtkinter.CTkButton(self, text="Quit", font=("Roboto-Bold", 15),
                            command=lambda:self.quit())
        button2.place(rely=0.65, relx=0.5, anchor=CENTER)


class PageOne(customtkinter.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        # Contraintes par défaut
        self.default_constraints_name = PLL_design.get_default_constraints_and_unit()
        self.results_names = PLL_design.get_results_paramaters_names()

        # Centrage ligne et colonnes
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Texte principal
        main_title = customtkinter.CTkLabel(self, text="PLL Design", font=("Roboto-Bold", 30, "bold"))
        main_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(30, 50))

        # == Frame Gauche == #
        self.entry_frame = ConstraintsFrame(self, title="Specifications", values=self.default_constraints_name)
        self.entry_frame.grid(row=1, column=0, padx=10, pady=10)

        self.button_dimensionnement = customtkinter.CTkButton(self, text="Design", command=self.dimensionnement_processing)
        self.button_dimensionnement.grid(row=2, column=0, padx=10, pady=30)

        # == Frame Droite == #
        self.result_frame = ResultFrame(self, title="Results", values=self.results_names)
        self.result_frame.grid(row=1, column=1, padx=10, pady=10)

        self.button_simulate = customtkinter.CTkButton(self, text="Simulate", state='disabled', fg_color='grey', command=lambda x=controller: self.change_frame_for_simulation(x))
        self.button_simulate.grid(row=2, column=1, padx=10, pady=30)

    def change_frame_for_simulation(self, controller):
        controller.show_frame(PageIntermediate)
        self.after(500, lambda: PageIntermediate.simulation_start(controller))

    def dimensionnement_processing(self):
        global all_param
        #Getting user parameter inputs
        user_input = self.entry_frame.get_user_input()
        print(f"User param input : {user_input}")

        #Processing design
        designed_parameters = PLL_design.get_design_pll(user_input)
        all_param = PLL_design.get_all_paramaters(user_input, designed_parameters)
        print(f"Param designed : {all_param}")

        #Changing value in second frame
        result_entries = self.result_frame.get_result_entries()

        param = list(designed_parameters.values())
        for i in range(len(result_entries)):
            result_entries[i].configure(state='normal')
            result_entries[i].configure(placeholder_text="{:.2e}".format(param[i]))
            result_entries[i].configure(state='disabled')


        # Enable autorization to simulate
        self.button_simulate.configure(fg_color=('#3B8ED0', '#1F6AA5'))
        self.button_simulate.configure(state='normal')



class ResultFrame(customtkinter.CTkScrollableFrame):

    SPACE_BTWN_CONSTRAINT = 10
    SIZE_ENTRY = 100

    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.configure(width=350, height=250)

        self.values = values
        self.constraints = {}

        i = 0
        for parameter_name, unit in self.values.items():
            label_parameter = customtkinter.CTkLabel(self, text=f"{parameter_name} :", fg_color="transparent")
            label_parameter.grid(row=i, column=0, padx=(30,0), pady=(ResultFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="w")

            entry = customtkinter.CTkEntry(self, placeholder_text=f"", width=ResultFrame.SIZE_ENTRY, state='disabled')
            entry.grid(row=i, column=1, padx=10, pady=(ResultFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="w")

            label_unit = customtkinter.CTkLabel(self, text=f"{unit}", fg_color="transparent")
            label_unit.grid(row=i, column=2, padx=(1, 0), pady=(ResultFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="w")

            self.constraints[parameter_name] = entry
            i += 1

    def get_result_entries(self):
        return list(self.constraints.values())


class ConstraintsFrame(customtkinter.CTkScrollableFrame):

    SPACE_BTWN_CONSTRAINT = 10
    SIZE_ENTRY = 80

    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.configure(width=350, height=250)

        self.values = values
        self.constraints = {}

        i = 0
        for constraint_name, lst_constr in self.values.items():
            label_constr = customtkinter.CTkLabel(self, text=f"{constraint_name} : ", fg_color="transparent")
            label_constr.grid(row=i, column=0, padx=(30,0), pady=(ConstraintsFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="e")

            entry = customtkinter.CTkEntry(self, placeholder_text="{:.2e}".format(lst_constr[0]), width=ConstraintsFrame.SIZE_ENTRY)
            entry.grid(row=i, column=1, padx=10, pady=(ConstraintsFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="w")

            label_unit = customtkinter.CTkLabel(self, text=f"{lst_constr[1]}", fg_color="transparent")
            label_unit.grid(row=i, column=2, padx=(1, 0), pady=(ConstraintsFrame.SPACE_BTWN_CONSTRAINT, 0), sticky="w")

            self.constraints[constraint_name] = entry
            i += 1

    def get_user_input(self):
        dic_user_constraints = {}
        default_constraints = PLL_design.get_default_constraints()

        for constraint_name, entry in self.constraints.items():
            if entry.get() =='':
                dic_user_constraints[constraint_name] = default_constraints[constraint_name]
            else:
                try:
                    dic_user_constraints[constraint_name] = float(entry.get())
                except ValueError:
                    dic_user_constraints[constraint_name] = default_constraints[constraint_name]
        return dic_user_constraints



class PageTwo(customtkinter.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)
        main_title = customtkinter.CTkLabel(self, text="Simulation results", font=("Roboto-Bold", 30, "bold"))
        main_title.place(relx = 0.5, rely=0.1, anchor=CENTER)

        #Mettre sous forme de classe la simulation

        self.button_time_response = customtkinter.CTkButton(self, text="Show \n V(in), V(out)", command=self.show_vin_vout)
        self.button_time_response.place(relx=0.15, rely=0.5, anchor='w')

        self.button_range = customtkinter.CTkButton(self, text="Show \n Step response", command=self.show_step_response)
        self.button_range.place(relx=0.4, rely=0.5, anchor='w')

        self.button_ac_response = customtkinter.CTkButton(self, text="Show characteritics", command=self.show_carac)
        self.button_ac_response.place(relx=0.65, rely=0.5, anchor='w')


        self.button_previous = customtkinter.CTkButton(self, text="Previous",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                            command=lambda: controller.show_frame(PageOne))
        self.button_previous.place(relx=0.05, rely=0.95, anchor='w')

        self.toplevel_window = None

    def show_vin_vout(self):
        simulation.plot_vin_vout(results)

    def show_step_response(self):
        consigne, reponse, time, steps = simulation.get_step_response(results)
        simulation.plot_step_response(consigne, reponse, time, steps)

    def show_carac(self):
        global carac
        consigne, reponse, time, steps = simulation.get_step_response(results)

        carac = simulation.analyze_response(consigne, reponse, time, PLL_design.get_abbaque_phase_margin())

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x350")

        self.label = customtkinter.CTkLabel(self, text="Characteristics of PLL", font=("Roboto-Bold", 20, "bold"))
        self.label.pack(padx=20, pady=20)

        for i, (key, value) in enumerate(carac.items()):
            label_text = f"{key}: "

            if isinstance(value, str):
                label_text += str(value)
            elif isinstance(value, tuple):
                label_text += f"{value[0]}° < Mϕ < {value[1]}°"
            else:
                value = float(value)
                if 'First overshoot' in key:
                    label_text += f"{value * 100:.1f}%"
                elif 'time' in key.lower() or 'settling' in key.lower():
                    if value < 1e-6:
                        label_text += f"{value * 1e9:.0f} ns"
                    elif value < 1e-3:
                        label_text += f"{value * 1e6:.0f} µs"
                    elif value < 1:
                        label_text += f"{value * 1e3:.0f} ms"
                    else:
                        label_text += f"{value:.0f} s"
                else:
                    label_text += f"{value:.1f}"

            label = customtkinter.CTkLabel(self, text=label_text)
            label.pack()


class PageIntermediate(customtkinter.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.main_title = customtkinter.CTkLabel(self, text="Running Simulation...", font=("Roboto-Bold", 13))
        self.main_title.place(relx = 0.5, rely=0.5, anchor=CENTER)

    @staticmethod
    def simulation_start(controller):
        global simulation, results
        #Start Simulation
        simulation = LTSpice_simulation.PLLSimulation()
        simulation.launch_simulation(all_param)
        results = simulation.get_simulation_results()

        #Changing page
        controller.show_frame(PageTwo)


app = App()
app.mainloop()

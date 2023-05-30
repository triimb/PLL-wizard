from PyLTSpice import SimRunner, SpiceEditor, LTspice, RawRead
import PLL_design
import PLL_design as pll_design
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


class PLLSimulation:
    def __init__(self):
        # Constants for simulation
        self.SCHEMATIC_FILENAME = "PLL_Wizard_Python.asc"
        self.NETLIST_OUT_FILENAME = "PLL_WIZ"
        self.SIM_RESULT_FOLDER = "Sim"

        # Constants for plotting
        self.NUMBER_PERIODS_SIMULATED = 100
        self.NUMBER_PERIODS_PLOT = 10

    def launch_simulation(self, design_param, add_instruction="; no more instructions"):
        # Configures the simulator to use and output folder
        runner = SimRunner(output_folder=f"./{self.SIM_RESULT_FOLDER}", simulator=LTspice)

        # Open the Spice Model, and creates the .net
        netlist = SpiceEditor(self.SCHEMATIC_FILENAME)

        netlist.set_parameters(mark=design_param['mark'], space=design_param['space'], cycles=design_param['N'],
                               Icp=design_param['Icp'])

        # Set components parameters
        netlist.set_component_value('R2', str(design_param['R2']))
        netlist.set_component_value('C2', str(design_param['C2']))
        netlist.set_component_value('C1', str(design_param['C1']))
        netlist.set_element_model('VIN_ALIM', "SINE(0 1 {})".format(str(int(design_param['Fin']))))
        netlist.set_element_model('V§DC_ALIM', "{}".format(str(design_param['Vdd'])))

        # Set instructions
        SIM_PERIOD = (1 / design_param['Fin']) * self.NUMBER_PERIODS_SIMULATED

        netlist.add_instructions(
            ".tran 0 {} 0 .01".format(str(SIM_PERIOD)),
            f".meas tran T1_PLL1 find time when V(out_pll)=0 td={0.5 * SIM_PERIOD} rise 1",
            f".meas tran T2_PLL1 find time when V(out_pll)=0 td={0.5 * SIM_PERIOD} rise 11",
            ".meas tran  Frequency_PLL param 10/(T2_PLL1-T1_PLL1)",
            f".meas tran T1_IN find time when V(in)=0 td={0.5 * SIM_PERIOD} rise 1",
            f".meas tran T2_IN find time when V(in)=0 td={0.5 * SIM_PERIOD} rise 11",
            ".meas tran  Frequency_IN param 10/(T2_IN-T1_IN)",
            add_instruction
        )

        # Overriding the automatic netlist naming
        raw, log = runner.run_now(netlist, run_filename=f"{self.NETLIST_OUT_FILENAME}.net")

    def get_simulation_results(self):
        LTR = RawRead(f"{self.SIM_RESULT_FOLDER}/{self.NETLIST_OUT_FILENAME}.raw")
        return LTR

    def get_frequency_measurement(self, file_path):
        frequencies = {}
        with open(file_path, 'r') as log_file:
            log_content = log_file.read()
            frequency_pll_line = log_content.find("frequency_pll")
            if frequency_pll_line != -1:
                start_index = log_content.find("=", frequency_pll_line) + 1
                end_index = log_content.find("\n", start_index)
                frequency_pll_value = log_content[start_index:end_index].strip()
                frequencies["frequency_pll"] = frequency_pll_value

            frequency_in_line = log_content.find("frequency_in")
            if frequency_in_line != -1:
                start_index = log_content.find("=", frequency_in_line) + 1
                end_index = log_content.find("\n", start_index)
                frequency_in_value = log_content[start_index:end_index].strip()
                frequencies["frequency_in"] = frequency_in_value

        return frequencies

    def plot_vin_vout(self, LTR):
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('Signaux V(in) et V(out)')

        vout_trace = LTR.get_trace("V(out_pll)")
        vin_trace = LTR.get_trace("V(in)")
        time_trace = LTR.get_trace('time')  # Gets the time axis
        steps = LTR.get_steps()

        for step in range(len(steps)):
            ax1.plot(time_trace.get_wave(step), vin_trace.get_wave(step), label="V(in)")
            ax2.plot(time_trace.get_wave(step), vout_trace.get_wave(step), label="V(out)", color='green')

        measured_frequencies = self.get_frequency_measurement(
            f"{self.SIM_RESULT_FOLDER}/{self.NETLIST_OUT_FILENAME}.log")
        period_in = 1 / float(measured_frequencies['frequency_in'])
        period_out = 1 / float(measured_frequencies['frequency_pll'])
        x_min_in, x_max_in = 0, self.NUMBER_PERIODS_PLOT * period_in
        x_min_out, x_max_out = 0.8*self.NUMBER_PERIODS_SIMULATED * period_out, 0.8*self.NUMBER_PERIODS_SIMULATED* period_out + self.NUMBER_PERIODS_PLOT*period_out
        print(f"xmin, xmax for Vin : {x_min_in}, {x_max_in}")
        print(f"xmin, xmax for Vout : {x_min_out}, {x_max_out}")
        ax1.set_xlim(x_min_in, x_max_in)
        ax2.set_xlim(x_min_out, x_max_out)

        text_content_ax1 = f"$f_{{in}}: {float(measured_frequencies['frequency_in']):.1e} Hz$"
        x_margin_ax1 = 0.02  # Margin from the right edge
        y_margin_ax1 = 0.08  # Margin from the bottom edge

        # Set the coordinates for the text in ax1
        x_ax1 = x_max_in - x_margin_ax1 * (x_max_in - x_min_in)
        y_ax1 = ax1.get_ylim()[0] + y_margin_ax1 * (ax1.get_ylim()[1] - ax1.get_ylim()[0])

        # Add a translucent background box to ax1
        bbox_props_ax1 = dict(boxstyle="square,pad=0.3", facecolor="white", alpha=0.5)
        ax1.text(x_ax1, y_ax1, text_content_ax1, fontsize=10, va='bottom', ha='right', bbox=bbox_props_ax1)

        # Your text content and coordinates for ax2
        text_content_ax2 = f"$f_{{out}}: {float(measured_frequencies['frequency_pll']):.1e} Hz$"
        x_margin_ax2 = 0.02  # Margin from the right edge
        y_margin_ax2 = 0.08  # Margin from the bottom edge

        # Set the coordinates for the text in ax2
        x_ax2 = x_max_out - x_margin_ax2 * (x_max_out - x_min_out)
        y_ax2 = ax2.get_ylim()[0] + y_margin_ax2 * (ax2.get_ylim()[1] - ax2.get_ylim()[0])

        # Add a translucent background box to ax2
        bbox_props_ax2 = dict(boxstyle="square,pad=0.3", facecolor="white", alpha=0.5)
        ax2.text(x_ax2, y_ax2, text_content_ax2, fontsize=10, va='bottom', ha='right', bbox=bbox_props_ax2)


        ax1.set_xlabel("Time")
        ax1.set_ylabel("Voltage (V)")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Voltage (V)")

        plt.subplots_adjust(hspace=0.5)

        ax1.legend(loc='upper right')
        ax2.legend(loc='upper right')
        plt.show()


    def get_step_response(self, LTR):
        vout_pfd_trace = LTR.get_trace("V(out_pfd)")
        consigne_trace = LTR.get_trace("V(consigne)")
        time_trace = LTR.get_trace('time')
        steps = LTR.get_steps()
        return consigne_trace.get_wave(), vout_pfd_trace.get_wave(), time_trace.get_wave(), steps

    def plot_step_response(self, consigne_trace, vout_pfd_trace, time_trace, steps):
        fig, ax = plt.subplots()

        ax.plot(time_trace, vout_pfd_trace, label=f"V(out_pfd)")
        ax.plot(time_trace, consigne_trace, label=f"V(consigne)")


        ax.set_xlabel("Time")
        ax.set_ylabel("Voltage (V)")
        ax.legend()
        ax.set_title("Step Response")

        plt.show()

    def find_range(self, numbers, target):
        left = 0
        right = len(numbers) - 1

        while left <= right:
            mid = (left + right) // 2

            if numbers[mid] == target:
                return numbers[mid], numbers[mid]
            elif numbers[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        if right < 0:
            return None, numbers[0]
        if left >= len(numbers):
            return numbers[-1], None

        return numbers[right], numbers[left]


    def analyze_response(self, consigne, response, time, phase_margin_chart):
        characteristics = {}

        start_index = int(consigne[0])
        end_index = int(response[-1])

        # Consigne
        setpoint = consigne[-1]
        characteristics['Setpoint'] = setpoint

        # Final value
        final_value = np.mean(response[end_index:])
        characteristics['Final value'] = final_value

        # First overshoot
        max_value = np.max(response)
        time_of_max = time[np.argmax(response)]
        characteristics['First overshoot (%)'] = (max_value - final_value) / final_value
        characteristics['Time of first overshoot'] = time_of_max

        if time_of_max >= (time[end_index] - time[start_index]) * 0.95:
            oscillatory_regime = False
            characteristics['Regime'] = "Oscillatory regime damped"
        else:
            oscillatory_regime = True

        # Gain
        static_gain = final_value / setpoint
        characteristics['Static gain'] = static_gain

        if oscillatory_regime:
            # Damping coefficient
            overshoot_percent = abs((max_value - final_value) / final_value)
            damping_coefficient = np.sqrt(
                (np.log(overshoot_percent) ** 2) / (np.pi ** 2 + np.log(overshoot_percent) ** 2))
            characteristics["Damping coefficient"] = damping_coefficient

            # Natural frequency
            if damping_coefficient > 1:
                characteristics['Regime'] = "Aperiodic regime"
            elif damping_coefficient == 1:
                characteristics['Regime'] = "Critical regime"
            else:
                natural_frequency = np.pi / (time_of_max * np.sqrt(1 - damping_coefficient ** 2))
                characteristics["Natural frequency"] = natural_frequency

        # Other regimes
        if not oscillatory_regime:
            # Time constant
            tau_index = np.where(response >= final_value * 0.63)
            time_constant = time[tau_index[0][0]]
            characteristics["Time constant"] = time_constant

            # 5% settling time
            tr5_index = np.where(response >= final_value * 0.95)
            settling_time_5_percent = time[tr5_index[0][0]]
            characteristics["Settling time (5%)"] = settling_time_5_percent

            # Phase margin
            upper_bound, lower_bound = self.find_range(sorted(list(phase_margin_chart.keys())), characteristics["First overshoot (%)"] * 100)
            characteristics["Phase margin"] = (phase_margin_chart[lower_bound], phase_margin_chart[upper_bound])

        #print(characteristics)
        return characteristics



    def find_rise_time(self, response, start_index, end_index, setpoint):
        for i in range(start_index, end_index):
            if response[i] >= setpoint:
                return i - start_index

    def calculate_phase_margin(self, consigne, response, time, phase_margin_chart):
        phase_margin_curve = []
        consigne_in_rad = np.deg2rad(consigne)
        response_in_rad = np.deg2rad(response)
        difference = response_in_rad - consigne_in_rad

        for i in range(len(time)):
            if i in phase_margin_chart:
                phase_margin_curve.append(difference[i])

        phase_margin = min(phase_margin_curve)
        return phase_margin


# Utilisation de la classe PLLSimulation

if __name__ == "__main__":
    simulation = PLLSimulation()

    dflt_constr = PLL_design.get_default_constraints()
    pll_param = PLL_design.get_all_paramaters(dflt_constr, PLL_design.get_design_pll(dflt_constr))

    #simulation.launch_simulation(pll_param)
    results = simulation.get_simulation_results()
    simulation.plot_vin_vout(results)


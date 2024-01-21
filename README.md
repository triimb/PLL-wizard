# Wizard de dimensionnement de PLL

This project consists of a Phase-Locked Loop (PLL) sizing tool developed in Python. It allows for the sizing of a PLL with an architecture that includes a Phase-Frequency Detector (PFD), charge pump, phase correction filter, Voltage-Controlled Oscillator (VCO), and frequency divider. To validate proper sizing, a simulation using LTSpice is performed.

The initial window allows the definition of specifications. If no values are entered, default values will be used. The simulation is initiated by clicking the simulation button, which may take some time (up to 30 seconds). If the window becomes unresponsive, please wait.

<img src="figures/dimensionnement_fig.png" alt= “” width="50%" height="50%">

The result window allows observation of proper PLL sizing in three aspects:

1. Observation of input and output signals of the PLL to verify correct frequency division/multiplication. Frequency measurements are based on simulated signals, not theoretical values.

<img src="figures/vin_vout_fig.png" alt= “” width="40%" height="40%">

2. Observation of the PLL's response to a step, in this case, the voltage at the output of the filter driving the VCO.

<img src="figures/step_response_fig.png" alt= “” width="40%" height="40%">

3. PLL Characteristics:
- Setpoint
- Final value
- First overshoot (%)
- Time of first overshoot
- Regime
- Static gain
- Time constant
- Settling time
- Phase Margin Interval (according to the Overshoot vs. Phase Margin graph)

<img src="figures/charac_fig.png" alt= “” width="30%" height="30%">


## Installation

1. Ensure you have Python and Git installed.
2. Clone this repository to your machine: git clone https://github.com/TriTriCPE/PLL_Wizard
3. Navigate to the project directory: cd PLL_Wizard
4. Install dependencies using pip: pip install -r requirements.txt

## Usage

1. Run the main script: python main.py
2.Follow the on-screen instructions to provide the required parameters for PLL sizing.
3.The wizard will calculate the values of various PLL components based on the entered parameters.
4. Simulation results will be displayed at the end of execution.

## Project Structure

The project is organized as follows:

- `main.py` : The main script that interacts with the user and performs PLL sizing.
- `LTSpice_simulation.py` : The module that initiates LTSpice simulations using the PYLTSpice library.
- `PLL_design.py` : The module containing functions and calculations necessary for PLL sizing.
- `PLL_Wizard_Python.asc` : The "schematic" file enabling circuit simulation on LTSpice.
- `Sim/` : Folder containing simulation results in .NETLIST and .RAW formats.
- `requirements.txt` : File containing the list of dependencies required to run the project.

## Auteurs

- IMBERT Tristan
- BOUVET Victor

## Licence

This project is under the MIT License. You are free to use it for personal or commercial purposes. Refer to the LICENSE file for more information.

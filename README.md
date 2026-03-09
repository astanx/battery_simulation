# Battery simulation

https://github.com/user-attachments/assets/1158006c-c256-4927-a30b-19cf256f4405

## Contents
- [How to use](#how-to-use)
  - [Installation](#installation)
  - [Controls](#controls)
  - [Configuration](#configuration)
- [Formulas](#formulas)

## How to use

### Installation
  To run the simulation, you need to either clone the repository or download the code.
  
  ```bash
  git clone https://github.com/astanx/battery_simulation
  cd battery_simulation
  ```

  Before the installation of dependencies you may want to setup virtual environment for python

  ##### Windows
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

  ##### MacOS/Linux
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

  #### Install dependencies
  
  ```bash
  pip install -r requirements.txt
  ```

  Before running the code you may want to adjust the settings in [config.py](./config.py), for example:
  ```python
  useUI = True
  ```
  To input specific values for square humidity and temperature

  To start the simulation, run:  
  ```bash
  python main.py
  ```
---

### Controls
You can use keyboard to control the simulation

- ESCAPE: close the simulation
- SPACE: stop the simulation, but charge will still be consumed
- ENTER: pause the simulation, everything will be paused
- ARROW_UP: move the selected battery one square up
- ARROW_DOWN: move the selected battery one square down
- ARROW_LEFT: select the battery to the left of the current one
- ARROW_RIGHT: select the battery to the right of the current one

### Configuration
You can customize energy consumption and cell behavior by modifying:
- [src/cell/cell_constants.py](./src/cell/cell_constants.py)
- [src/cell/hydrogen_cell_constants.py](./src/cell/hydrogen_cell_constants.py)
- [src/cell/lithium_cell_constants.py](./src/cell/lithium_cell_constants.py)

Also you can configure the application by modifying [config.py](./config.py)

---

## Formulas

### Lithium battery
  - #### [Arrhenius‑Type Temperature Dependence](https://en.wikipedia.org/wiki/Arrhenius_equation)
      ##### Used in code
      ```python
      RT = R_ref * exp(E_a / R * (1/temperature - 1/T_ref))
      ```
      Modified form of Arrhenius equation, used to model temperature dependence of internal resistance and reaction behavior inside the battery.

  - #### [Open‑Circuit Voltage (OCV)](https://en.wikipedia.org/wiki/Open-circuit_voltage)
      ##### Used in code
      ```python
      OCV = OCV_ref + alpha * (self.SOC - 0.5) + g * (temperature - T_ref)
      ```
      OCV is the voltage of a battery when no current is flowing. In the code it is approximated by adjusting a reference OCV with SOC and temperature terms

  - #### [Effective Internal Resistance](https://en.wikipedia.org/wiki/Internal_resistance)
      ##### Used in code
      ```python
      R = self.arrhenius_equation(temperature)
      ```
      It depends on many factors including temperature and battery chemistry. In the code in is approximated using [Arrhenius‑Type Temperature Dependence](arrhenius‑type-temperature-dependence)
  
  - #### [Polarization Voltage (Over‑potential)](https://en.wikipedia.org/wiki/Polarization_(electrochemistry))
      ##### Used in code
      ```python
      R_pol = R_ref * exp(E_pol / R * (1/temperature - 1/T_ref))
      V_pol = self.current * R_pol
      ```
      Polarization voltage refers to additional voltage losses beyond ohmic resistance that occur when current is flowing, due to kinetic and diffusion limitations inside electrodes.

  - #### [SOC (State of Charge)](https://en.wikipedia.org/wiki/State_of_charge)
      ##### Used in code
      ```python
      d_SOC = (self.current * efficiency * dt) / (self.capacity * 3600)
      ```
      SOC quantifies how much charge is left in a battery relative to its capacity. 
      In the simualtion SOC decreases proportionally with current drawn over time.

### Hydrogen battery
  - #### [Nernst Equation](https://en.wikipedia.org/wiki/Nernst_equation)
      ##### Used in code
      ```python
      argument = (H * vapor) / (P_H2 * pow(P_O2, 0.5))
      E_nernst = E - (R * temperature / (2 * F)) * log(argument)
      ```
      In a hydrogen fuel cell, it tells the theoretical maximum voltage the battery could produce under given conditions
  
  - #### [Exchange Current Density (Arrhenius‑like)](https://en.wikipedia.org/wiki/Arrhenius_equation)
      ##### Used in code
      ```python
      I_O = I_O_ref * exp((-E_a / R) * (1/temperature - 1/T_ref))
      ```
      This expression models how the exchange current density varies with temperature, using an Arrhenius‑type dependence.

  - #### [Butler–Volmer Equation](https://en.wikipedia.org/wiki/Butler%E2%80%93Volmer_equation)
      ##### Used in code
      ```python
      E = (R * temperature / (a * n * F)) * log(self.current_density / I_O)
      ```
      It is simplified to reflect how the current density deviates from the exchange current density due to reaction kinetics.

  - #### [Springer Membrane Conductivity Model](https://www.mdpi.com/2077-0375/10/11/310)
      ##### Used in code
      ```python
      sigma_mem = (0.005139 * l - 0.00326) * exp(1268 * (1/303 - 1/temperature)) * 100
      n_ohmic = self.current_density * (d_mem / sigma_mem)
      ```
      This represents the resistive losses in the proton exchange membrane due to proton transport resistance.
      This model quantifies how much voltage is lost as protons travel through the membrane, which behaves as a resistor.

  - #### [Nernstian Concentration Overpotential](https://www.mdpi.com/2076-3417/9/6/1066)
      ##### Used in code
      ```python
      I_lim = n * F * D_O2 * C_bulk / d_GDL
      C_surface = C_bulk * (1 - self.current_density / I_lim)
      E = (R * temperature / (n * F)) * log(C_bulk / C_surface)
      ```
      This models mass concentration losses: as current increases, reactants (like Oxygen) get depleted at the reaction surface faster than they can diffuse from the bulk gas.

 

E = 1.229 # Standart half-cell reduction potential
R = 8.314 # Gas constant (J/mol * K)
F = 96485 # Faraday constant (C/mol)

k_H_ref = 7.81 * pow(10, 4) # Henry`s constant at reference temperature 298K (Pa * m^3/mol)
t_sen = -1600 # Temperature sensitivity parameter (K)

P_H2 = 1.6 * pow(10, 5) # Hydrogen partial pressure (Pa)
P_O2 = 0.3 * pow(10, 5) # Oxygen partial pressure (Pa)
D_O2 = 2.5 * pow(10, -6) # Effective oxygen diffusion coefficient (m^2/s)
M_H2O = 0.018  # Molar mass of water (kg/mol)
I_O_ref = 1 # Reference exchange current density (A/m^2)
E_a = 50 * pow(10, 3) # Activation energy (J/mol)
d_mem = 100 * pow(10, -6) # Membrane thickness (meter)
d_GDL = 200 * pow(10, -6) # Gas diffusion layer thickness (meter)

a = 0.5 # Charge transfer coefficient
n = 2 # Number of electrons in the rate-determining step
R_ref = 50 * pow(10, -3) # Reference resistance at T_ref (50 milliohms)
OCV_ref = 3.7 # Reference OCV at 25°C
n_ref = 0.05 # Reference polarization coefficient
E_a = 20 * pow(10, 3) # Activation energy (J/mol)
E_pol = 15 * pow(10, 3) # Activation energy for polarization (J/mol)

Q_nom = 3500 * pow(10, -3) # Nominal capacity in Ah (3500 mAh)

b = 3500 # Arrhenius parameter
d = 2000 # Activation parameter
g = 0.005 # Temperature coefficient
k = 0.001 # Humidity degradation coefficient
n = 0.99 # Coulombic efficiency
a = 0.005 # Low-temperature capacity fade coefficient 
alpha = 0.8 # SOC voltage coefficient
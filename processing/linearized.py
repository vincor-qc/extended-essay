import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

TRIALS = 5
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = "STIXgeneral"

# ensure tex is also in stixgeneral font
plt.rcParams['mathtext.fontset'] = 'stix'

fig, ax = plt.subplots()

# Read from data/average.csv
data = np.genfromtxt('data/average.csv', delimiter=',')
x_p = data[:, 0]
y_p = data[:, 1]

# read uncertainties from data/uncertainties.csv
uncertainties = np.genfromtxt('data/uncertainties.csv', delimiter=',')
y_unc = uncertainties[:, 1]

##### Linearize the data #####
x_p_lin = np.sqrt(x_p)
y_p_lin = np.log(y_p - 20)

plt.figure(figsize=(10,6))

y_lin_upper = np.log(y_p + y_unc - 20) 
y_lin_lower = np.log(y_p - y_unc - 20)

y_lin_uncertainity = (y_lin_upper - y_lin_lower)/2


##### Plot the data points #####
plt.errorbar(
    x_p_lin, y_p_lin, xerr=0.05*x_p_lin, yerr=y_lin_uncertainity,
    fmt='.', capsize=3, capthick=0.5, elinewidth=0.5, color='#6022bd',
    label='Trial Averages'
)
plt.legend()

##### Calculate the bestfit #####
def f(x, b,):
    return -0.0161 * x + b

def linear(x, m, b):
    return m * x + b

popt, pcov = curve_fit(f, x_p_lin, y_p_lin)

# plot max slope
max_linespace = np.linspace(x_p_lin[0] - x_p_lin[0] * 0.05, x_p_lin[-1] + x_p_lin[-1] * 0.05, 1000)
max_slope = ((y_p_lin[0] - y_lin_uncertainity[0]) - (y_p_lin[-1] + y_lin_uncertainity[-1]))/(max_linespace[0] - max_linespace[-1])
max_y_intercept = y_p_lin[0] - y_lin_uncertainity[0] - max_slope * max_linespace[0]

plt.plot(max_linespace, linear(max_linespace, max_slope, max_y_intercept), color='#8ee650', label='Max Slope', zorder=5)


# plot min slope
min_linespace = np.linspace(x_p_lin[0] + x_p_lin[0] * 0.05, x_p_lin[-1] - x_p_lin[-1] * 0.05, 1000)
min_slope = ((y_p_lin[0] + y_lin_uncertainity[0]) - (y_p_lin[-1] - y_lin_uncertainity[-1]))/(min_linespace[0] - min_linespace[-1])
min_y_intercept = y_p_lin[0] + y_lin_uncertainity[0] - min_slope * min_linespace[0]

plt.plot(min_linespace, linear(min_linespace, min_slope, min_y_intercept), color='#f5bf2c', label='Min Slope', zorder=50)

# print average y intercept and its uncertainty given by max-min/2
y_intercept = (max_y_intercept + min_y_intercept)/2
y_intercept_uncertainty = (max_y_intercept - min_y_intercept)/2

slope_uncertainty = (max_slope - min_slope)/2

print("y intercept: ", y_intercept)
print("y intercept uncertainty: ", y_intercept_uncertainty)
print("slope uncertainty", (max_slope - min_slope)/2)

##### Plot the model #####
# Fan Speed
x_m = np.linspace(350, 1700, 1200)

# Final Temperature
y_m = 22.2 + (60 - 22.2) * np.exp(-0.0158 * np.sqrt(x_m))

x_m_lin = np.sqrt(x_m)
y_m_lin = np.log(y_m - 22.2)

y_m_lin_upper = np.log(0.2 + (38.7) * np.exp(-0.0150 * pow(x_m, 0.5)))
y_m_lin_lower = np.log(-0.2 + (36.9) * np.exp(-0.0166 * pow(x_m, 0.5)))


# Plot the model
plt.plot(x_m_lin, y_m_lin, label='Model', color='r')
plt.legend()

# Plot the uncertainties
plt.fill_between(
    x_m_lin, y_m_lin_upper, y_m_lin_lower,
    color='#ff7f7f', alpha=0.5, label='Model Uncertainty'
)
plt.legend()

# Add labels
plt.title(r'ln(Temperature above Environment) vs. $\sqrt{\mathrm{Fan\;Speed}}$', fontdict={'fontsize': 18})

plt.xlabel(r'$\sqrt{\mathrm{Fan\;Speed}\;(RPM)}$', fontdict={'fontsize': 14})
plt.ylabel(r'$\ln(T-T_{\infty})$', fontdict={'fontsize': 14})


# Plot the bestfit
x_b = np.linspace(x_m_lin[0], x_m_lin[-1], 1000)

# Final Temperature
y_b = f(x_b, *popt)

# Plot the bestfit
plt.plot(x_b, y_b, label='Best fit', color='#0d9dd6', zorder=10)
plt.legend()

bftext = "Best fit equation: $\ln(T - T_\infty) = -(0.016 \pm {}) \sqrt{{n_f}} + (3.5 \pm {})$".format(round(slope_uncertainty, 3), round(y_intercept_uncertainty, 1))

mdtext = "Model equation: $\ln(T - T_\infty) = -(0.0158 \pm 0.0008) \sqrt{{n_f}} + (3.63 \pm 0.02)$"

plt.text(
    0.0, 0.0,
    bftext + "\n" + mdtext,
    transform=ax.transAxes,
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round', pad=0.5, edgecolor='grey')
)

# Change axes
plt.xlim(x_m_lin[0], x_m_lin[-1])
#plt.ylim(31, 49)

plt.grid(True, color='#C5C5CA')

# Save the plot to a file
plt.savefig('images/linearized.png')


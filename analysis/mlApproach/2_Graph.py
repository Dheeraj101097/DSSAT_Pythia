import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Set seaborn style globally
sns.set_theme(style="whitegrid", context='talk', font_scale=0.6)

def add_metrics_text(ax, actual, predicted):
    r2 = r2_score(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    nrmse = rmse / np.mean(actual)

    text = f"$R^2$ = {r2:.2f}\nRMSE = {rmse:.2f}\nNRMSE = {nrmse:.2f}"
    
    ax.text(
        0.95, 0.05, text,
        ha='right', va='bottom',
        transform=ax.transAxes,
        fontsize=14,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray")
    )

# --- CALIBRATION PLOT ---
results_cal = pd.read_csv('soybean_predictions_97_12.csv')

plt.figure(figsize=(8, 8))
ax1 = sns.scatterplot(
    x='ACTUAL', 
    y='PREDICTED', 
    data=results_cal, 
    color='lightblue',
    s=30
)

max_val = max(results_cal['ACTUAL'].max(), results_cal['PREDICTED'].max())
plt.plot([0, max_val], [0, max_val], 'r--', label='Perfect Prediction (y = x)')

plt.xlabel('Actual Yield (HWAM)')
plt.ylabel('Predicted Yield (HWAM)')
plt.title('Actual vs Predicted Yield (1997–2012)')
plt.legend()

add_metrics_text(ax1, results_cal['ACTUAL'], results_cal['PREDICTED'])

plt.tight_layout()
plt.savefig("Ml_cal_plotr2.png", dpi=300)
plt.show()


# --- VALIDATION PLOT ---
results_val = pd.read_csv('soybean_predictions_13_20.csv')

plt.figure(figsize=(8, 8))
ax2 = sns.scatterplot(
    x='ACTUAL', 
    y='PREDICTED', 
    data=results_val, 
    color='lightgreen',
    s=30
)

max_val = max(results_val['ACTUAL'].max(), results_val['PREDICTED'].max())
plt.plot([0, max_val], [0, max_val], 'r--', label='Perfect Prediction (y = x)')

plt.xlabel('Actual Yield (HWAM)')
plt.ylabel('Predicted Yield (HWAM)')
plt.title('Actual vs Predicted Yield (2013–2020)')
plt.legend()

add_metrics_text(ax2, results_val['ACTUAL'], results_val['PREDICTED'])

plt.tight_layout()
plt.savefig("Ml_val_plotr2.png", dpi=300)
plt.show()

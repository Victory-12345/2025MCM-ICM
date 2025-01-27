import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Load the data from the Excel file
file_path = 'grouped_results.xlsx'
df = pd.read_excel(file_path)

# Prepare the data for the radar chart
categories = df['NOC'].tolist()
values = df['medal'].tolist()

# Number of variables
N = len(categories)

# Create the radar chart
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

# Make the radar chart a circle
values += values[:1]  # Repeat the first value to close the circle
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='blue', alpha=0.25)
ax.plot(angles, values, color='blue', linewidth=2)

# Set the labels (categories)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, rotation=90)

# Title and display
plt.title('Radar Chart of Medal Values by NOC', size=14)
plt.show()

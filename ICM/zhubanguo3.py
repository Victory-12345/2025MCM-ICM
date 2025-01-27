import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Define the medal data for each country (this is just an example, replace with actual data)
data = {
    "Country": ["Japan", "Great Britain", "Spain"] * 10,  # Example of 10 data points per country
    "Gold Medals": [
        -6.885768, 0.401069, -2.396737, -1.149798, 11.304898, -3.342981, -2.338022, 4.418641, 10.582320727272727, 1.101148,  # Japan
        -4.056148, -4.757041, -6.499170, 4.639990, 2.696511, 9.505111, 9.6420441, 7.957043, -1.432484, -11.121097,  # Great Britain
        5.696511, 7.037163, -8.000012, -7.368295, -6.662918, 1.906474, -0.360653, 2.765238, -2.160460, 0.633248 # Spain
        # Add more data points as needed
    ]
}

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Set the theme for the plot
sns.set_theme(style="ticks")

# Initialize the figure with a logarithmic x axis
f, ax = plt.subplots(figsize=(7, 6))

# Plot the boxplot with the medal data
sns.boxplot(
    x="Country", y="Gold Medals", data=df, 
    whis=[0, 100], width=.6, palette="vlag", ax=ax
)

# Add in points to show each observation (strip plot)
sns.stripplot(
    x="Country", y="Gold Medals", data=df, 
    size=4, color=".3", jitter=True, ax=ax
)

# Tweak the visual presentation
ax.yaxis.grid(True)
ax.set(xlabel="", ylabel=" Gold Medals")
sns.despine(trim=True, left=True)

# Show the plot
plt.title(" Gold Medal from 1988-2024(revised)")
plt.show()

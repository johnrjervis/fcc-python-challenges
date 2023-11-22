import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data
    df = pd.read_csv("epa-sea-level.csv")

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 4))
    df.plot(x="Year", y="CSIRO Adjusted Sea Level", kind="scatter", ax=ax)

    # Create first line of best fit
    relationship1 = linregress(x=df["Year"], y=df["CSIRO Adjusted Sea Level"])
    years1 = [i for i in range(1880, 2051)]
    predicted_sea_level1 = [relationship1.slope * year + relationship1.intercept for year in years1]
    ax.plot(years1, predicted_sea_level1, "k--")

    # Create second line of best fit
    df_2000 = df[df["Year"] >= 2000]
    relationship2 = linregress(x=df_2000["Year"], y=df_2000["CSIRO Adjusted Sea Level"])
    years2 = [i for i in range(2000, 2051)]
    predicted_sea_level2 = [relationship2.slope * year + relationship2.intercept for year in years2]
    ax.plot(years2, predicted_sea_level2, "r--")

    # Add labels and title
    props = {
        "title": "Rise in Sea Level",
        "xlabel": "Year",
        "ylabel": "Sea Level (inches)",
    }
    ax.set(**props)

    fig.savefig("sea_level_plot.png")

if __name__ == "__main__":
    draw_plot()

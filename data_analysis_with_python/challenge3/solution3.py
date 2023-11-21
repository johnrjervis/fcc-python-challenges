import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def binary_limit(value, threshold=1):
    """Returns one if value is greater than the threshold; returns zero otherwise"""
    return 1 if (value > threshold) else 0

# Import data
df = pd.read_csv("medical_examination.csv")

# Add overweight column and normalise (1 = bad for BMI > 25, else 0 = good)
df["overweight"] = (df["weight"] / ((df["height"] / 100) ** 2)).apply(binary_limit, threshold=25)

# Normalise the cholesterol and glucose columns (1 for values > 1, else 0)
df["cholesterol"] = df["cholesterol"].apply(binary_limit)
df["gluc"] = df["gluc"].apply(binary_limit)

pressure_mask = df["ap_lo"] <= df["ap_hi"]
height_mask = (df["height"] >= df["height"].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975))
weight_mask = (df["weight"] >= df["weight"].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))

cleaned_df = df[pressure_mask & height_mask & weight_mask]

def draw_cat_plot():
    # Create df for the cat plot with melt and only include the columns that will be used in the chart
    df_cat = df.melt(id_vars=["cardio"], value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])

    # Group and reformat to show the counts of each feature split by cardio
    # The dictionary supplied for the columns argument of rename is {0: "total"} in the Replit version of my solution
    df_cat = df_cat.groupby(["cardio", "variable"]).value_counts().reset_index().rename(columns={"count": "total"})

    # Draw the cat plot
    catplot = sns.catplot(data=df_cat, kind="bar", x="variable", y="total", hue="value", col="cardio")

    # Access the figure
    fig = catplot.figure

    # Save the figure
    fig.savefig("catplot.png")

def draw_heat_map():
    # Clean the data
    pressure_mask = df["ap_lo"] <= df["ap_hi"]
    height_mask = (df["height"] >= df["height"].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975))
    weight_mask = (df["weight"] >= df["weight"].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))

    df_heat = df[pressure_mask & height_mask & weight_mask]

    # Calculate the correlation matix
    corr = df_heat.corr()

    # Generate a mask for the top right portion (including elements on the diagonal) of the matrix
    mask_comp = [[(i>=j) for i in range(len(corr))] for j in range(len(corr))]
    diagonal_mask = pd.DataFrame(mask_comp, index=corr.index, columns=corr.columns)

    # Create a matplotlib figure
    fig, ax = plt.subplots(constrained_layout=True)

    # Create the heat map
    sns.heatmap(corr, mask=diagonal_mask, annot=True, fmt=".1f", linewidth=0.5, robust=True, square=True, ax=ax)

    # Save the figure
    fig.savefig("heatmap.png")

if __name__ == "__main__":
    draw_cat_plot()
    draw_heat_map()

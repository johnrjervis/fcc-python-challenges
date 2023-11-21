import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=["date"])

# Clean data
middle_95_per_cent_mask = (df["value"] > df["value"].quantile(0.025)) & (df["value"] < df["value"].quantile(0.975))
df = df[middle_95_per_cent_mask]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(10, 4))
    props = {
        "title": "Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
        "xlabel": "Date",
        "ylabel": "Page Views",
    }
    ax.set(**props)
    ax.plot(df, color="r")

    fig.savefig("lineplot.png")

def draw_bar_plot():
    # Copy and modify dataframe
    df_bar = df.copy()
    df_bar = df_bar.resample("M", kind="period").mean()
    df_bar.reset_index(inplace=True)
    df_bar["year"] = [d.year for d in df_bar.date]
    df_bar["month"] = [d.month for d in df_bar.date]
    df_bar = df_bar.pivot(index="year", columns="month", values="value")
    df_bar.rename(columns=convert_month_number_to_name, inplace=True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 7))
    df_bar.plot(kind="bar", ax=ax)
    props = {
        "xlabel": "Years",
        "ylabel": "Average Page Views",
    }
    ax.set(**props)
    ax.legend(title="Months")

    fig.savefig("barplot.png")

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]
    df_box["month_number"] = [d.strftime("%m") for d in df_box.date]

    # Draw box plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    sns.boxplot(data=df_box, x="year", y="value", hue="year", palette=sns.color_palette(), ax=ax1)
    sns.boxplot(data=df_box.sort_values(by=["month_number"]), x="month", y="value", hue="month", ax=ax2)
    props1 = {
        "xlabel": "Year",
        "ylabel": "Page Views",
        "title": "Year-wise Box Plot (Trend)",
    }
    ax1.set(**props1)
    ax1.get_legend().remove()
    props2 = {
        "xlabel": "Month",
        "ylabel": "Page Views",
        "title": "Month-wise Box Plot (Seasonality)",
    }
    ax2.set(**props2)

    fig.savefig("boxplot.png")

def convert_month_number_to_name(number):
    """Converts a month number (1-12) into the equivalent full month name"""
    date = datetime(year=2000, month=number, day=1)
    return date.strftime("%B")

if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()

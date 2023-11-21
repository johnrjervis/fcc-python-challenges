import pandas as pd

def calculate_demographic_data():
    # Skip initial space was not needed in the solution that I posted on Replit
    df = pd.read_csv("adult_data.csv", skipinitialspace=True)

    # Create a series that lists the number of people for each race in the data
    race_count = df.groupby("race")["race"].count()

    # Calculate the average age of all men in the data
    average_age_men = round(df[df["sex"]=="Male"]["age"].mean(), 1)

    # Calculate the percentage of people in the data with a Bachelor's degree
    percentage_bachelors = round(len(df[df["education"]=="Bachelors"]) * 100 / len(df), 1)

    # Calculate the percentage of people who have salaries over 50k for those with a higher education (Bachelor's, Master's, or Doctorate) and those without

    # Create separate DFs for those with a higher education and those without
    higher_mask = (df["education"]=="Bachelors") | (df["education"]=="Masters") | (df["education"]=="Doctorate") 
    higher_education = df[higher_mask]
    lower_education = df[~higher_mask]

    # Calculate percentages of people earning >50k for the higher education and lower education datasets
    higher_education_rich = round(len(higher_education[higher_education["salary"]==">50K"]) * 100 / len(higher_education), 1)
    lower_education_rich = round(len(lower_education[lower_education["salary"]==">50K"]) * 100 / len(lower_education), 1)

    # Get the minimum number of hours worked per week according to the dataset
    min_work_hours = df["hours-per-week"].min()

    # Calculate the percentage of those working the minimum number of hours who earn >50k
    num_min_workers = len(df[df["hours-per-week"]==min_work_hours])
    rich_and_min_hours_mask = (df["hours-per-week"]==min_work_hours) & (df["salary"]==">50K")

    rich_percentage = round(len(df[rich_and_min_hours_mask]) * 100 / num_min_workers, 1)

    # Find the country that has the highest percentage of people who earn >50k
    rich_by_country = df[df["salary"]==">50K"].groupby("native-country")["salary"].count()
    percentage_rich_by_country = rich_by_country * 100 / df.groupby("native-country")["salary"].count()

    highest_earning_country = percentage_rich_by_country.sort_values(ascending=False).index[0]
    highest_earning_country_percentage = round(percentage_rich_by_country.loc[highest_earning_country], 1)

    # Find the most common occupation amongst people from India who earn >50k
    ind_rich_mask = (df["native-country"]=="India") & (df["salary"]==">50K")
    top_IN_occupation = df[ind_rich_mask].groupby("occupation").count().sort_values(by="salary", ascending=False).index[0]

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }

if __name__ == "__main__":
    result = calculate_demographic_data()

    for item in result:
        print(f'{item}: {result[item]}')

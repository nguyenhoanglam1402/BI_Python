import numpy
import pandas as pd
from pandas.core.frame import DataFrame


def openCSVFile(path):
    file = pd.read_csv(path)
    pd.set_option('display.max_columns', 4)
    return file


def getCVSLines(path):
    with open(path) as f:
        for i, line in enumerate(f):
            print("line {0} = {1}".format(i, line.split()))


def fillCSVCollumn(columns, group_by_name, top, comparation_param, src_file):
    data = pd.DataFrame(src_file[columns])
    if(top != 0):
        dataFrame = data[columns].groupby(group_by_name).sum()
        result = dataFrame.sort_values(
            comparation_param, ascending=False).head(top)
    else:
        if(group_by_name != ''):
            result = data[columns].groupby(group_by_name).sum()
        else:
            result = data[columns]
    return result


def predict(years, file):
    data = DataFrame(file)
    total_average = data["Average_daily_particles_inside_EEZ"].sum()
    predict_result = ((total_average * 30)*12) * years
    difference = predict_result - predict_result/years
    return predict_result, difference


def incomeTotalPlastic(file, country_name, current_value):
    data = DataFrame(file)
    country_total = data.loc[data["Country_from"] == country_name]
    total_each_country = country_total["Total_number_particles_released"]
    result = int((total_each_country * current_value)*30*12)
    return result


def main():
    # Path of the Dataset file.
    path = 'D:\Python Code\ASM\Resource\dataset.csv'

    # Open dataset.csv
    file = openCSVFile(path)
    print("[OPENING CVS FILE]\n\n", file, '\n\n')

    # Display file Lines
    print("[RUNNING GET CVS FOLLOWING LINES]\n =>{}\n\n".format(getCVSLines(path)))

    # Define Select column: Country from, Average daily inside
    fill_result = fillCSVCollumn(
        columns=["Country_from", "Average_daily_particles_inside_EEZ"],
        top=0,
        group_by_name='',
        comparation_param='',
        src_file=file
    )
    print("[FILL RESULT] => [Country from, Average daily inside]\n\n{}\n\n".format(
        fill_result))

    # Define Select column: Country from, Total number release
    fill_result_of_total = fillCSVCollumn(
        columns=["Country_from", "Total_number_particles_released"],
        top=0,
        comparation_param='',
        group_by_name='',
        src_file=file,
    )
    print("[FILL RESULT] => [Country from, Total number release]\n\n{}\n\n".format(
        fill_result_of_total))

    # Define function “Sum(Average or Total) of each country per day”  (Total sum)
    fill_result = fillCSVCollumn(
        columns=["Country_from", "Average_daily_particles_inside_EEZ",
                 "Total_number_particles_released"],
        group_by_name='Country_from',
        top=0,
        comparation_param='',
        src_file=file,
    )
    print("[FILL RESULT] => [Sum(Average or Total) of each country]\n\n{}\n\n", fill_result)

    # Select Top 10 of Max(total Sum ) of all country
    fill_result = fillCSVCollumn(
        columns=["Country_from", "Average_daily_particles_inside_EEZ",
                 "Total_number_particles_released"],
        group_by_name='Country_from',
        top=0,
        comparation_param='',
        src_file=file,
    )
    print("[FILL RESULT] => [Sum(Average or Total) of each country]\n\n{}\n\n".format(
        fill_result))

    # Select Top 10 of Max(total Sum ) of all country
    fill_result = fillCSVCollumn(
        columns=["Country_from", "Total_number_particles_released"],
        group_by_name="Country_from",
        top=10,
        comparation_param='Total_number_particles_released',
        src_file=file
    )
    print('[Filtered results] => Select Top 10 of Max(total Sum ) of all country\n\n{}\n\n'.format(
        fill_result))

    # Average of Total number particles released
    data = DataFrame(file)
    average_total = data["Total_number_particles_released"].mean()
    print("Average of Total number particles released: ",
          round(average_total, 2), '\n\n')
    # Input how many(year)
    year = int(input("Enter the number of year you wanna predict: "))
    predict_result, diff = predict(years=year, file=file)
    print("[PREDICT RESULT] - In next {} year(s), average will be {} and increases {}"
          .format(year, round(predict_result, 2), round(diff, 2)))

    country_name = input("Which country you wanna know?\n>_ ")

    result_income = incomeTotalPlastic(
        file=fill_result_of_total, country_name=country_name, current_value=60)
    print(result_income)
    print("[RESULT VALUE] => The income of {} by sell Plastic recycle are {}".format(
        country_name, result_income))


main()

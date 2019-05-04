import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid", color_codes=True)


def birth_death_ratio(df, df2):
    """
    In this function, we have performed analysis in terms of race or ethnicity of an individual. This analysis is
    further done on basis of poverty and birth to death ratio in a particular county.
    This analysis is further bifurcated on county wise and state wise. The function returns a dataframe that is used
    to provide a detailed graphical representation.

    :param df: We are passing the demographics data-frame for the analysis.
    :param df2: We are passing the birth_death_measure data-frame for the analysis.
    :return: returns two data-frames consisting of analysis based on the race or ethnicity and grouped by county and
    state names.

    >>> df = pd.read_csv("Testfile_DEMO.csv")
    >>> df2 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df3 , df4 = birth_death_ratio(df,df2)
    >>> print((df3[["CHSI_County_Name","Poverty","birth_death_ratio"]]).head(5))
      CHSI_County_Name  Poverty  birth_death_ratio
    0            Adams     11.2         102.618057
    1        Alexander     22.2          94.186047
    2             Bond     10.8          89.892802
    3            Boone      7.7          48.572345
    4            Brown     11.6         101.206897

    >>> print(df4[["CHSI_State_Name","Poverty","Total_Deaths"]])
      CHSI_State_Name  Poverty  Total_Deaths
    0        Illinois    10.74       4001.82

    """
    df1 = df[
        ["CHSI_County_Name", "CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic", "Poverty",
         "Population_Size"]]
    df_1 = df1[df1["Poverty"] >= 0].copy()
    df_1['Others'] = df_1['Native_American'] + df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    birth_death = df2[["CHSI_County_Name", "CHSI_State_Name", "Total_Births", "Total_Deaths"]].copy()
    birth_death = birth_death.loc[(birth_death["Total_Births"] >= 0) & (birth_death["Total_Deaths"] >= 0)]
    birth_death["birth_death_ratio"] = birth_death['Total_Deaths'] / birth_death['Total_Births'] * 100
    data = pd.merge(df_1, birth_death, on=['CHSI_County_Name', 'CHSI_State_Name'])
    pd.set_option('display.max_columns', None)
    # print(data.sort_values(by = 'Poverty',ascending=False))                             #jadhgjsagvjhsajvksbdahfvhsjdak

    dfa = df_1.groupby(["CHSI_State_Name"], as_index=False).agg(
        {"White": "mean", "Black": "mean", "Others": "mean", "Hispanic": "mean", "Poverty": "mean"})
    dfb = birth_death.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Births": "mean", "Total_Deaths": "mean"})
    final_df = pd.merge(dfa, dfb, on="CHSI_State_Name")
    final_df = final_df.round(2)
    final_df = final_df.sort_values(by=["Poverty"], ascending=False)
    return data, final_df


def plot_birth_death_ratio(x, y):
    """
    This function is used to provide a graphical representation of the analysis done in the previous function, i.e.
    birth_death_ratio().
    :param x: the data-frame on used to complete the plot
    :param y: data-frame used to create the bar graph plot
    :return: Returns the plot for the dataframes and comparison done
    """

    df_1, df_2 = birth_death_ratio(x, y)
    plt.subplot(2, 1, 1)
    plt.scatter(x=df_1['Poverty'], y=df_1["White"], color="DarkGreen", label="White")
    plt.scatter(x=df_1['Poverty'], y=df_1["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=df_1['Poverty'], y=df_1["Others"], color="Red", label="Others")
    plt.scatter(x=df_1['Poverty'], y=df_1["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.title("County & Race-wise Poverty")
    plt.grid(linewidth=0.5, color="grey")

    plt.subplot(2, 1, 2)
    plt.scatter(x=df_2['Poverty'], y=df_2["White"], color="DarkGreen", label="White")
    plt.scatter(x=df_2['Poverty'], y=df_2["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=df_2['Poverty'], y=df_2["Others"], color="Red", label="Others")
    plt.scatter(x=df_2['Poverty'], y=df_2["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.grid(linewidth=0.5, color="grey")
    plt.title("State & Race-wise Poverty")
    plt.show()


def population_poverty(df):
    """
    In this function, we have performed analysis of poverty and population for the given dataset and the data is
    further divided on state names. The end result of this function gives us distribution where we can relate how population is
    affected by the poverty value of a particular county. This function gives us idea of the population to poverty
    ratio.
    :param df: We are passing the demographics data-frame for the analysis
    :return: returns the fata-frame with the analysis.

    >>> df1 = pd.read_csv("Testfile_DEMO.csv")
    >>> df2 = population_poverty(df1)
    >>> print(df2)
      CHSI_State_Name  Population_Size  Poverty  Pop_Poverty_ratio
    0        Illinois        125131.09    10.74           11646.47

    """
    df1 = df[["CHSI_State_Name", "Poverty", "Population_Size"]]
    df1 = df1[df1["Poverty"] >= 0]
    df_2 = df1.groupby(["CHSI_State_Name"], as_index=False).agg({"Population_Size": "mean", "Poverty": "mean"})
    df_2["Pop_Poverty_ratio"] = df_2["Population_Size"] / df_2["Poverty"]
    df_2 = df_2.sort_values(by=["Pop_Poverty_ratio"], ascending=True)
    df_2 = df_2.round(2)
    return df_2


def death_factors(df1, df2):
    """
    In this function, we have performed analysis to demonstrate how the deaths among the different races or
    different ethnic groups in United States. The data is sorted on basis of highest death rate. The final data
    is then used to create plots for demonstrating the same.
    :param df1: We are passing the demographics data-frame for the analysis
    :param df2: We are passing the birth_death_measure data-frame for the analysis
    :return: The function returns two data-frames, the actual analysis and other data-frame used to create plots to
    demonstrate the analysis.
    >>> df1 = pd.read_csv("Testfile_DEMO.csv")
    >>> df2 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df3 , df4, df5 = death_factors(df1, df2)
    >>> print(df4[["CHSI_State_Name", "Total_Deaths"]])
      CHSI_State_Name  Total_Deaths
    0        Illinois        4002.0

    """
    df = df1[["CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic"]]
    df_2 = df2[["CHSI_State_Name", "Total_Deaths"]]
    df_1 = df.copy()
    df_3 = df_2.copy()
    df_1["Others"] = df_1['Native_American'] + df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    population = df_1.groupby(["CHSI_State_Name"], as_index=False).agg(
        {"Black": "mean", "White": "mean", "Others": "mean", "Hispanic": "mean"})
    population = population.round(2)
    deaths = df_2.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Deaths": "mean"})
    deaths = deaths.round(0)
    pop_deaths = pd.merge(population, deaths, on="CHSI_State_Name")
    pop_deaths = pop_deaths.sort_values(by=["Total_Deaths"], ascending=False)
    first_10 = pop_deaths.head(10)
    last_10 = pop_deaths.tail(10)
    # print(first_20)
    return pop_deaths, first_10, last_10


def plot_death_factors(x, y):
    """
    This function is used to plot and demonstrate the analysis done in the previous function, i.e. death_factors.
    :param x: the first data-frame used, i.e. we are passing the demographics data-frame for the analysis
    :param y: the second data-frame used, i.e. we are passing the birth_death_measure data-frame for the analysis
    :return: the function plots the resultant data-frame of the death_factors function.
    """

    pop_deaths, first_10, last_10 = death_factors(x, y)
    p1 = plt.bar(first_10["CHSI_State_Name"], first_10["White"], width=1, color="DarkGreen", edgecolor="black",
                 label="White")
    p2 = plt.bar(first_10["CHSI_State_Name"], first_10["Black"], width=1, bottom=first_10["White"], color="Blue",
                 edgecolor="black", label="Black")
    p3 = plt.bar(first_10["CHSI_State_Name"], first_10["Others"], width=1,
                 bottom=np.array(first_10["White"]) + np.array(first_10["Black"]),
                 color="Red", edgecolor="black", label="Others")
    p4 = plt.bar(first_10["CHSI_State_Name"], first_10["Hispanic"], width=1,
                 bottom=np.array(first_10["White"]) + np.array(first_10["Black"]) + np.array(first_10["Others"]),
                 color="Orange", edgecolor="black", label="Hispanic")

    r1 = plt.bar(last_10["CHSI_State_Name"], last_10["White"], width=1, color="DarkGreen", edgecolor="black")
    r2 = plt.bar(last_10["CHSI_State_Name"], last_10["Black"], width=1, bottom=last_10["White"], color="Blue",
                 edgecolor="black")
    r3 = plt.bar(last_10["CHSI_State_Name"], last_10["Others"], width=1,
                 bottom=np.array(last_10["White"]) + np.array(last_10["Black"]),
                 color="Red", edgecolor="black")
    r4 = plt.bar(last_10["CHSI_State_Name"], last_10["Hispanic"], width=1,
                 bottom=np.array(last_10["White"]) + np.array(last_10["Black"]) + np.array(last_10["Others"]),
                 color="Orange", edgecolor="black")

    plt.xlabel("Top & Last 10 States")
    plt.ylabel("Race-wise Pop percent")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.xticks(rotation="vertical")
    plt.grid(linewidth=0.5, color="grey")
    plt.title("Top 10 & last 10 states ")
    plt.show()


def merge_dataframes(dataframe1, dataframe2, dataframe3, dataframe4):
    """
    In this function, we are combining the required data obtained by various data-frames and merged them into different data-frames, according to
    the required conditions.
    :param dataframe1: We are passing the risk_factors dataframe for the analysis
    :param dataframe2: We are passing the demographics dataframe for the analysis
    :param dataframe3: We are passing the birth_death_measure dataframe for the analysis
    :param dataframe4: We are passing the vulnerable_pops dataframe for the analysis
    :return: df_demo_risk_bd_unemp as the final dataframe to be used in the future analysis
    """
    df_demo = dataframe2[["CHSI_County_Name", "CHSI_State_Name", "Poverty", "Population_Size"]]
    df_riskfactor = dataframe1[
        ["CHSI_County_Name", "CHSI_State_Name", "No_Exercise", "Obesity", "High_Blood_Pres", "Few_Fruit_Veg", "Smoker",
         "Diabetes", "Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Prim_Care_Phys_Rate"]]
    df_measurebd = dataframe3[
        ["State_FIPS_Code", "County_FIPS_Code", "CHSI_County_Name", "CHSI_State_Name", "Late_Care", "Infant_Mortality",
         "Total_Deaths", "Total_Births"]]
    df_unemp = dataframe4[["State_FIPS_Code", "County_FIPS_Code", "CHSI_County_Name", "CHSI_State_Name", "Unemployed"]]
    df_demo_risk = pd.merge(df_demo, df_riskfactor, on=['CHSI_State_Name', 'CHSI_County_Name'])
    df_demo_risk_bd = pd.merge(df_demo_risk, df_measurebd, on=['CHSI_State_Name', 'CHSI_County_Name'])
    df_demo_risk_bd_unemp = pd.merge(df_demo_risk_bd, df_unemp, on=['CHSI_State_Name', 'CHSI_County_Name'])

    pd.set_option('display.max_columns', None)

    return df_demo_risk_bd_unemp


def analysis_1(df):
    """
    In this function we are analysing the co relation between Poverty , Total_deaths and various risk factors like Poverty", "Total_Deaths", "No_Exercise", "Obesity",
        "Few_Fruit_Veg", "Smoker", "Diabetes", "High_Blood_Pres" ,etc. These risk factors are either by choice or circumstantial.
    Also , in addition to that we have analyzed the co-relation between  Poverty , Total_deaths and various factors related to medical care provided.
    :param df: We are passing the result dataframe for the analysis which is obtained from merge_dataframes function.
    :return:returns the data frame with the desired analysis
    """
    df_final_1 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], np.nan)
    df_1 = df_final_1[
        ["CHSI_County_Name", "CHSI_State_Name", "Population_Size", "Poverty", "Total_Deaths", "No_Exercise", "Obesity",
         "Few_Fruit_Veg", "Smoker", "Diabetes", "High_Blood_Pres"]]
    df_1 = df_1.groupby(["CHSI_State_Name"], as_index=False)[
        "Poverty", "Total_Deaths", "Population_Size", "No_Exercise", "Obesity", "Few_Fruit_Veg", "Smoker", "Diabetes", "High_Blood_Pres"].mean()
    df_1 = df_1.sort_values(by=["Poverty", "Total_Deaths"], ascending=False)
    df_1["Mortality_Rate"] = df_1["Total_Deaths"] / df_1["Population_Size"] * 100
    df_1 = df_1.drop(["Total_Deaths", "Population_Size"], axis=1)
    df_1 = df_1.round(2)
    # print(df_1.head(10))

    df_2 = df_final_1[
        ["CHSI_County_Name", "CHSI_State_Name", "Population_Size", "Poverty", "Uninsured", "Elderly_Medicare",
         "Disabled_Medicare", "Late_Care", "Prim_Care_Phys_Rate", "Total_Deaths"]]
    df_2 = df_2.groupby(["CHSI_State_Name"], as_index=False)[
        "Population_Size", "Poverty", "Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Late_Care", "Prim_Care_Phys_Rate", "Total_Deaths"].mean()
    df_2 = df_2.sort_values(by=["Poverty", "Total_Deaths"], ascending=False)
    df_2["Mortality_Rate"] = df_2["Total_Deaths"] / df_2["Population_Size"] * 100
    df_2 = df_2.drop(["Total_Deaths", "Population_Size"], axis=1)
    df_2 = df_2.round(2)
    pd.set_option('display.max_columns', None)
    return df_1, df_2


def plot_analysis_1(df):
    """
    In this function, we are trying to plot between the Poverty on basis of various factors and population size of a
    particular county.
    :param df: thee dataframe used to create the plot
    :return: returns the plot for the analysis
    """
    df_1, df_2 = analysis_1(df)
    df_2 = df_2.dropna()
    sns.heatmap(df_2.corr(), xticklabels=df_2.corr().columns, yticklabels=df_2.corr().columns, cmap='RdYlGn', center=0,
                annot=True)
    plt.title('Correlogram of Poverty', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
    # print(df_2.head(10))


def other_risk_factors(df1, df2):
    """
    in this function, we are analysing other risk factors like "Premature", "Under_18", "Over_40", "Late_Care"
    and sort the values based on Poverty and Birth Death ratio.
    It shows that counties with high poverty rate generally have high "Premature", "Under_18", "Over_40", "Late_Care" ratio.
    :param df1: We are passing the demographics data-frame for the analysis
    :param df2: We are passing the birth_death_measure data-frame for the analysis
    :return: The functions returns the analysed data in the form of a data-frame, which is used to create plots to
    demonstrate the analysis.
    >>> df1 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df2 = pd.read_csv("Testfile_DEMO.csv")
    >>> df3 = other_risk_factors(df1,df2)
    >>> print((df3[["CHSI_County_Name", "Poverty"]].head(10)))
       CHSI_County_Name  Poverty
    1         Alexander     22.2
    76          Pulaski     19.8
    38          Jackson     19.3
    54        McDonough     15.9
    29         Gallatin     15.8
    82           Saline     15.0
    34           Hardin     14.8
    27         Franklin     14.8
    81        St. Clair     14.5
    15             Cook     14.5

    """

    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "LBW", "VLBW", "Premature", "Under_18", "Over_40", "Late_Care",
                "Total_Births", "Total_Deaths"]]
    df_1 = df_1.replace([-1111.1, -2222.2], np.nan)
    df_1["Birth_Death_Ratio"] = df_1["Total_Deaths"] / df_1["Total_Births"] * 100
    df_1["LBW_VLBW"] = df_1["LBW"] + df_1["VLBW"]
    df_1 = df_1.drop(["Total_Deaths", "Total_Births", "LBW", "VLBW"], axis=1)
    df_2 = df2[["CHSI_County_Name", "CHSI_State_Name", "Poverty", "Population_Size"]]
    df_2 = df_2.replace([-1111.1, -2222.2], np.nan)
    df_3 = pd.merge(df_1, df_2, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_3 = df_3.sort_values(by=["Poverty", "Birth_Death_Ratio"], ascending=[False, False])
    # print(df_3.head(20))
    # print(df_3.tail(20))
    return df_3


def plot_other_risk_factors(a, b):
    """
    In this function, we are trying to plot the factors responsible for mortality rates on basis of county.
    :param a: data frame used to create the plot
    :param b: date frame used to create the plot
    :return: the function returns the plot of the previous function.
    """
    df = other_risk_factors(a, b)
    df_4 = df.groupby(["CHSI_State_Name"], as_index=False)[
        "Premature", "Under_18", "Over_40", "Late_Care", "LBW_VLBW", "Birth_Death_Ratio", "Poverty"].mean()
    df_4 = df_4.sort_values(by=["Poverty", "Birth_Death_Ratio"], ascending=[False, False])
    df_4 = df_4.round(2)
    # print(df_4.head(10))
    # print(df_4.tail(10))

    df_5 = df_4.head(10)
    df_6 = df_4.tail(10)
    # print(df_5)
    # print(df_6)
    df_7 = pd.concat([df_5, df_6])
    # print(df_7)
    plt.subplot(2, 2, 1)
    plt.bar(df_7["CHSI_State_Name"], df_7["Poverty"])
    plt.ylabel("State-wise Poverty Distribution")
    plt.xticks([])

    plt.subplot(2, 2, 3)
    plt.bar(df_7["CHSI_State_Name"], df_7["Under_18"])
    plt.ylabel("Under_18_births")
    plt.xticks(df_7["CHSI_State_Name"], rotation="vertical")

    plt.subplot(2, 2, 2)
    plt.bar(df_7["CHSI_State_Name"], df_7["Premature"])
    plt.ylabel("Premature_births")
    plt.xticks([])

    plt.subplot(2, 2, 4)
    under_18 = plt.bar(df_7["CHSI_State_Name"], df_7["Late_Care"])
    plt.ylabel("Late_Care_births")
    plt.xticks(df_7["CHSI_State_Name"], rotation="vertical")
    plt.show()


def genetic_deaths(df1, df2):
    """
    This function helps us to understand and provide information regarding the mortality rate in all the counties or
    states in the United States of America based on birth defects.
    The factors taken into consideration are State name and Birth defects in different ethnic groups, for every county.
    This data is then calculated for each state by taking the total of all county data, for a particular state.

    :param df1: Here we have provided leading causes of deaths data frame.
    :param df2: Here we have provided birth_death_measure dataframe
    :return: Returns the resultant data frame

    >>> df1 = pd.read_csv("Testfile_LCOD.csv")
    >>> df2 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df3 = pd.merge(df1,df2, on= ["CHSI_County_Name","CHSI_State_Name"])
    >>> df3 = df3.replace(to_replace=[-9999, -2222, -2222.2, -2, -1111.1, -1111, -1], value=0)
    >>> df3 = df3.groupby("CHSI_State_Name")["A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"].sum()
    >>> print(df3["Total_Births"])
    CHSI_State_Name
    Illinois    639809
    Name: Total_Births, dtype: int64
    """
    df = pd.merge(df1, df2, on=["CHSI_County_Name", "County_FIPS_Code", "CHSI_State_Name", "State_FIPS_Code"])
    df_1 = df[['CHSI_State_Name', "A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"]]
    df_1 = df_1.replace(to_replace=[-9999, -2222, -2222.2, -2, -1111.1, -1111, -1], value=0)
    df_1 = df_1.groupby("CHSI_State_Name")[
        "A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"].sum()
    df_1["Total_Deaths"] = df_1["A_Wh_BirthDef"] + df_1["A_Bl_BirthDef"] + df_1["A_Ot_BirthDef"] + df_1["A_Hi_BirthDef"]
    df_1["Mortality_Rate"] = (df_1["Total_Deaths"] / df_1["Total_Births"]) * 100
    df_1 = df_1.drop(["Total_Deaths", "Total_Births"], axis=1)
    df_1.reset_index()
    df_1 = df_1.sort_values(by="Mortality_Rate", ascending=False)
    pd.set_option('display.max_columns', None)
    return df_1
    # print(df_1.head(10))


def air_quality_death(df1, df2, df3):
    """
    Here we are analysing the various factors which affect the air quality for all the states. These factors are then sorted,
    and then we compare the death ratio in that particular state with respect to the values of these factors.

    :param df1: We are passing the birth_death_measure dataframe for the analysis.
    :param df2: We are passing the air_quality dataframe for the analysis.
    :param df3: We are passing the demographics dataframe for the analysis.
    :return: We are returning the final dataframe 'data_1' obtained after the analysis

    >>> df1 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df2 = pd.read_csv("Testfile_AAQI.csv")
    >>> df3 = pd.read_csv("Testfile_DEMO.csv")
    >>> df4 = air_quality_death(df1,df2,df3)
    >>> print((df4[["County", "Max AQI"]]).head(10))
           County  Max AQI
    21   Tazewell      200
    16    Madison      151
    10       Lake      156
    22     Wabash      160
    0       Adams      122
    1   Champaign       87
    2       Clark       90
    3        Cook      140
    4      DuPage      110
    5   Effingham      105

    """
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Population_Size"]]
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "Total_Deaths"]]
    df4 = pd.merge(df_1, df_3, on=["CHSI_County_Name", "CHSI_State_Name"])
    df4["Mortality_Rate"] = df4["Total_Deaths"] / df4["Population_Size"] * 100
    df4 = df4.drop(["Population_Size", "Total_Deaths"], axis=1)
    df4 = df4.round(2)
    df4.columns = ["County", "State", "Mortality_Rate"]
    df4 = df4[df4["Mortality_Rate"] > 0]
    (df4.sort_values(by="Mortality_Rate", ascending=True))
    df_2 = df2[["County", "State", "Max AQI", "Unhealthy Days", "Very Unhealthy Days", "Hazardous Days"]]
    data = pd.merge(df4, df_2, on=["County", "State"])
    pd.set_option('display.max_columns', None)
    data_1 = data.sort_values(by=["Hazardous Days", "Very Unhealthy Days", "Unhealthy Days"],
                              ascending=[False, False, False])

    return data_1


def plot_air_quality_death(a, b, c):
    """

    :param a: the data-frame on used to complete the plot
    :param b: the data-frame on used to complete the plot
    :param c: the data-frame on used to complete the plot
    :return:
    """
    data_1 = air_quality_death(a, b, c)
    df_4 = data_1.head(15)
    df_5 = data_1.tail(15)
    df_6 = pd.concat([df_4, df_5])
    df_6["Total_Unhealthy_days"] = df_6["Hazardous Days"] + df_6["Unhealthy Days"] + df_6["Very Unhealthy Days"]
    df_6 = df_6.drop(["Hazardous Days", "Very Unhealthy Days", "Unhealthy Days"], axis=1)
    sns.scatterplot(x=df_6["State"], y=df_6["Mortality_Rate"], size=df_6["Total_Unhealthy_days"], data=df_6)
    plt.xticks(rotation="vertical")
    plt.legend(loc="upper left", fontsize="x-small")
    plt.title("")
    plt.show()


def disease_pollution(df1, df2, df3, df4):
    """
    We have performed the analysis on various diseases like lung cancer, breast cancer, Col_cancer_d. We check the occurences of these diseases
    based on the AQI and toxic chemicals in a particular state.
    :param df1: We are passing the birth_death_measure dataframe for the analysis.
    :param df2: We are passing the air_quality dataframe for the analysis.
    :param df3: We are passing the vulnerable_pops dataframe for the analysis.
    :param df4: We are passing the demographics dataframe for the analysis.
    :return: We are returning the final dataframe 'data_7' obtained after the analysis
    >>> df1 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df2 = pd.read_csv("Testfile_AAQI.csv")
    >>> df3 = pd.read_csv("Testfile_VPAEH.csv")
    >>> df4 = pd.read_csv("Testfile_DEMO.csv")
    >>> df5 = disease_pollution(df1,df2,df3,df4)
    >>> print((df5[["County","Toxic_Chem"]].head(5)))
         County  Toxic_Chem
    14   Peoria    31953727
    3      Cook    12221689
    13  Madison    11328080
    12    Macon     7163343
    19     Will     5328100

    """
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "Lung_Cancer", "Brst_Cancer", "Col_Cancer"]]
    df_1 = df_1[(df_1["Lung_Cancer"] > 0) & (df_1["Brst_Cancer"] > 0) & (df_1["Col_Cancer"] > 0)]
    # print(df_1.sort_values(by="Brst_Cancer", ascending=True))
    df_2 = df2[["County", "State", "Max AQI"]]
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Toxic_Chem"]]
    df_3 = df_3[df_3["Toxic_Chem"] > 0]
    df_4 = df4[["CHSI_County_Name", "CHSI_State_Name", "Population_Size"]]
    df_5 = pd.merge(df_1, df_4, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_5["Lung_Cancer_d"] = (df_5["Lung_Cancer"] * df_5["Population_Size"]) / 100000
    df_5["Brst_cancer_d"] = (df_5["Brst_Cancer"] * df_5["Population_Size"]) / 100000
    df_5["Col_cancer_d"] = (df_5["Col_Cancer"] * df_5["Population_Size"]) / 100000
    df_5 = df_5.drop(["Lung_Cancer", "Brst_Cancer", "Col_Cancer"], axis=1)
    df_5 = df_5.round()
    df_5["Total_cancer_deaths"] = df_5["Lung_Cancer_d"] + df_5["Brst_cancer_d"] + df_5["Col_cancer_d"]
    # print(df_5.head(10))
    df_6 = pd.merge(df_5, df_3, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_6.columns = ["County", "State", "Population_Size", "Lung_Cancer_d", "Brst_cancer_d", "Col_cancer_d",
                    "Total_cancer_deaths", "Toxic_Chem"]
    df_7 = pd.merge(df_6, df_2, on=["County", "State"])
    df_7 = df_7.sort_values(by=["Toxic_Chem", "Max AQI"], ascending=[False, False])
    pd.set_option("display.max_columns", None)
    return df_7
    # print(df_7.head(10))
    # print(df_7.tail(10))


def plot_disease_pollution(df1, df2, df3, df4):
    """

    :param df1: the data-frame on used to complete the plot
    :param df2: the data-frame on used to complete the plot
    :param df3: the data-frame on used to complete the plot
    :param df4: the data-frame on used to complete the plot
    :return:
    """
    df_7 = disease_pollution(df1, df2, df3, df4)
    df_8 = df_7.head(7)
    df_9 = df_7.tail(7)
    df_10 = pd.concat([df_8, df_9])
    plt.subplot(2, 2, 1)
    plt.scatter(x=df_10["County"], y=df_10["Total_cancer_deaths"], color="c")
    plt.plot(x=df_10["County"], y=df_10["Total_cancer_deaths"], color="c")
    plt.xticks(rotation="vertical")
    plt.ylabel("Cancer_deaths")
    plt.title("Total cancer deaths for top & last 10 counties")

    plt.subplot(2, 2, 2)
    plt.scatter(x=df_10["County"], y=df_10["Max AQI"], color="m")
    plt.plot(x=df_10["County"], y=df_10["Max AQI"], color="m")
    plt.xticks(rotation="vertical")
    plt.ylabel("Max AQI")
    plt.title("Max AQI for top & last 10 counties")

    plt.subplot(2, 2, 3)
    plt.scatter(x=df_10["County"], y=df_10["Toxic_Chem"], color="darkgreen")
    plt.plot(x=df_10["County"], y=df_10["Toxic_Chem"], color="darkgreen")
    plt.xticks(rotation="vertical")
    plt.ylabel("Toxic Chemicals")
    plt.title("Toxic Chemicals for top & last 10 counties")

    plt.show()


def death_other_factors(df1, df2, df3):
    """
    We have performed the analysis on various factors like Major_Depression, Unemployment, Recent_Drug_Use,Suicide,Homicide based on the poverty for
    a particular region.Further we have compared the number of deaths depending on these factors.
    :param df1: We are passing the vulnerable_pops dataframe for the analysis.
    :param df2: We are passing the birth_death_measure dataframe for the analysis.
    :param df3: We are passing the demographics dataframe for the analysis.
    :return: We are returning the final dataframe 'data_5' obtained after the analysis
    >>> df1 = pd.read_csv("Testfile_VPAEH.csv")
    >>> df2 = pd.read_csv("Testfile_MOBAD.csv")
    >>> df3 = pd.read_csv("Testfile_DEMO.csv")
    >>> df4 = death_other_factors(df1,df2,df3)
    >>> print(df4[["CHSI_County_Name","Deaths_Suicide"]].head(5))
       CHSI_County_Name  Deaths_Suicide
    0         Alexander             1.0
    5           Jackson             5.0
    16        St. Clair            24.0
    2              Cook           398.0
    18        Vermilion             8.0
    """
    df_1 = df1[["CHSI_County_Name", "CHSI_State_Name", "Major_Depression", "Unemployed", "Recent_Drug_Use"]]
    df_1 = df_1[df_1["Unemployed"] > 0]
    df_2 = df2[["CHSI_County_Name", "CHSI_State_Name", "Suicide", "Homicide"]]
    df_2 = df_2[(df_2["Suicide"] > 0) & (df_2["Homicide"] > 0)]
    df_3 = df3[["CHSI_County_Name", "CHSI_State_Name", "Population_Size", "Poverty"]]
    df_3 = df_3[df_3["Poverty"] > 0]
    df_4 = pd.merge(df_2, df_3, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_4["Deaths_Suicide"] = (df_4["Suicide"] * df_4["Population_Size"]) / 100000
    df_4["Deaths_Homicide"] = (df_4["Homicide"] * df_4["Population_Size"]) / 100000
    df_4["Number of people Below Poverty Line"] = (df_4["Poverty"] * df_4["Population_Size"]) / 100
    df_4 = df_4.drop(["Homicide", "Suicide", "Poverty"], axis=1)
    df_4 = df_4.round()
    df_5 = pd.merge(df_1, df_4, on=["CHSI_County_Name", "CHSI_State_Name"])
    df_5["Poverty Ratio"] = (df_5["Number of people Below Poverty Line"] / df_5["Population_Size"]) * 100
    df_5 = df_5.sort_values(["Poverty Ratio"], ascending=False)
    df_5 = df_5.drop(["Population_Size", "Number of people Below Poverty Line"], axis=1)
    pd.set_option("display.max_columns", None)
    return df_5


def age_poverty(df):
    """
    The state wise output shows that the percent of population for Age_85_and_Over is slightly greater in top 10 states with Low Poverty index
    as compared to that of states with high poverty index.
    :param df: We are passing the demographics dataframe for the analysis.
    :return: We are returning the final dataframe 'data_5' obtained after the analysis

    """
    df_1 = df[
        ["CHSI_County_Name", "CHSI_State_Name", "Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"]]
    df_1 = df_1.replace([-1111.1, -2222.2], np.nan)
    df_2 = df_1.groupby(["CHSI_County_Name", "CHSI_State_Name"], as_index=False)[
        "Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"].mean()
    df_3 = df_2.sort_values(by="Poverty", ascending=False)
    df_3 = df_3.round(2)
    print(df_3.head(10))
    print(df_3.tail(10))

    df_4 = df_1.groupby(["CHSI_State_Name"], as_index=False)[
        "Age_19_Under", "Age_19_64", "Age_65_84", "Age_85_and_Over", "Poverty"].mean()
    df_5 = df_4.sort_values(by="Poverty", ascending=False)
    df_5 = df_5.round(2)
    return df_5
    # print(df_5.head(10))
    # print(df_5.tail(10))


def read_dataframes():
    """
        In this function,  we are are reading the required csv files from the dataset into dataframes.

        :return: We return the demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops as dataframes after reading the csv files.
    """
    demographics = pd.read_csv("DEMOGRAPHICS.csv")
    lead_death_cause = pd.read_csv("LEADINGCAUSESOFDEATH.csv")
    birth_death_measure = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")
    risk_factors = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")
    vulnerable_pops = pd.read_csv("VUNERABLEPOPSANDENVHEALTH.csv")
    air_quality = pd.read_csv("annual_aqi_by_county_2010.csv")
    return demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops, air_quality


if __name__ == '__main__':
    demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops, air_quality = read_dataframes()
    a, b = birth_death_ratio(demographics, birth_death_measure)
    print("The relational analysis of Poverty with respect to different races in different counties: \n")
    print((a.sort_values(by='Poverty', ascending=False)).head(5))
    print("\n Analysis based on how poverty in a state is biased on basis of race of an individual: \n")
    print(b.head(10))
    print("\n The graph for the same can be depicted as: \n")
    plot_birth_death_ratio(demographics, birth_death_measure)
    c, d, e = death_factors(demographics, birth_death_measure)
    print("\n The total number of deaths in a particular county. The data is distributed and related on basis of race"
          "of an individual \n")
    print("\nStates with highest number of deaths (race-wise distribution) : \n")
    print("---------------------------------------------------------------------\n\n")
    print(d)
    print("\nStates with lowest number of deaths (race-wise distribution) : \n")
    print("---------------------------------------------------------------------\n\n")
    print(e)
    print("\nThe plot for the above analysis is as follows: \n\n")
    plot_death_factors(demographics, birth_death_measure)
    f = other_risk_factors(birth_death_measure, demographics)
    pd.set_option('display.max_columns', None)
    print(
        "\n The mortality rate and Poverty analysis based on various risk factors like premature birth, birth to females both below age 18 and above 40, etc. for different counties in each state."
        " These values show the top 5 counties for the given analysis. \n")
    print("---------------------------------------------------------------------\n")
    print(f.head())
    print(
        "\nThe mortality rate and Poverty analysis based on various risk factors like premature birth, birth to females "
        "both below age 18 and above 40, etc. for different counties in each state."
        " These values show the lowest 5 counties for the given analysis.")
    print("---------------------------------------------------------------------\n")
    print(f.tail())
    print("\n The graph demontrating the above analysis: \n")
    plot_other_risk_factors(birth_death_measure, demographics)
    g = population_poverty(demographics)
    print("\n The ratio of population to poverty for every state has been analysed. The analysis is as follows: \n")
    print("---------------------------------------------------------------------\n")
    print(g)
    result = merge_dataframes(risk_factors, demographics, birth_death_measure, vulnerable_pops)
    h, i = analysis_1(result)
    print("\n Co-relation between Poverty , Total_Death , various risk factors and medical assistance provided is done. The analysis is as follows: \n")
    print("---------------------------------------------------------------------\n")
    print(h.head())
    print(i.head())
    print("\n The correlation between various risk factors, poverty")
    plot_analysis_1(result)
    j = genetic_deaths(lead_death_cause, birth_death_measure)
    print("\n\n The mortality rate based on genetic defects has been analyzed. The analysis can be demonstrated as: \n")
    print("---------------------------------------------------------------------\n")
    print("\n", j.head(10))
    k = air_quality_death(birth_death_measure, air_quality, demographics)
    print(
        "\n This analysis is based on how pollution(AQI index) adds to cause of fata diseases in different counties. The analysis can be demonstrated as: \n")
    print("---------------------------------------------------------------------\n")
    print(k.head())
    print("The graphical representation of the data is done as follows: \n")
    plot_air_quality_death(birth_death_measure, air_quality, demographics)
    l = disease_pollution(birth_death_measure, air_quality, vulnerable_pops, demographics)
    print(
        "\n This analysis provides information about the total number of cases of fatal diseases like various types of cancer due to pollution and toxic chemicals for each county. This can be shown as : \n")
    print("---------------------------------------------------------------------\n")
    print(l.head(10))
    print("\n The plot to demonstrate the above analysis is as follows: \n")
    plot_disease_pollution(birth_death_measure, air_quality, vulnerable_pops, demographics)
    m = death_other_factors(vulnerable_pops, birth_death_measure, demographics)
    print(
        "\n This analysis shows the mortality rate based on various other human-centric factors. The analysis is done for each county.\n")
    print("---------------------------------------------------------------------\n")
    print(m.head(10))
    n = age_poverty(demographics)
    print(
        "\n The analysis shows state wise output for percent of population for Age_85_and_Over is slightly greater in top 10 states with Low Poverty index "
        "as compared to that of states with high poverty index. The analysis can be demonstrated as: \n")
    print("---------------------------------------------------------------------\n")
    print(n.head(10))
    print("---------------------------------------------------------------------\n")

    print("Analysis Complete")



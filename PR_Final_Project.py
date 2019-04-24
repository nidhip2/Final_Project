import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir("C:/Users/rajku/Downloads/chsi_dataset/")
demographics = pd.read_csv("DEMOGRAPHICS.csv")
causes = pd.read_csv("LEADINGCAUSESOFDEATH.csv")
measures = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")

#print(measures.isnull().sum())

def birth_death_ratio(df, df2):
    df1 = df[["CHSI_County_Name", "CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic", "Poverty", "Population_Size"]]
    df_1 = df1[df1["Poverty"]>=0].copy()
    df_1['Others'] = df_1['Native_American']+df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    birth_death = df2[["CHSI_County_Name", "CHSI_State_Name", "Total_Births", "Total_Deaths"]].copy()
    birth_death = birth_death.loc[(birth_death["Total_Births"] >= 0) & (birth_death["Total_Deaths"] >= 0)]
    birth_death["birth_death_ratio"] = birth_death['Total_Deaths']/birth_death['Total_Births']*100
    data = pd.merge(df_1, birth_death, on = ['CHSI_County_Name', 'CHSI_State_Name'])
    pd.set_option('display.max_columns', None)
    print(data.sort_values(by = 'Poverty',ascending=False))
    plt.scatter(x=data['Poverty'], y=data["White"], color="DarkGreen", label="White pop")
    plt.scatter(x=data['Poverty'], y=data["Black"], color="DarkBlue", label="Black pop")
    plt.show()

    dfa = df_1.groupby(["CHSI_State_Name"], as_index=False).agg({"White":"mean", "Black":"mean", "Others":"mean", "Hispanic":"mean", "Poverty":"mean"})
    dfb = birth_death.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Births":"mean", "Total_Deaths":"mean"})
    final_df = pd.merge(dfa, dfb, on="CHSI_State_Name")
    final_df = final_df.round(2)
    print(final_df.sort_values(by=["Poverty"], ascending=False))


birth_death_ratio(demographics, measures)

def population_poverty(df):
    df1 = df[["CHSI_State_Name", "Poverty", "Population_Size"]]
    df1 = df1[df1["Poverty"]>=0]
    df_2 = df1.groupby(["CHSI_State_Name"], as_index=False).agg({"Population_Size":"mean", "Poverty":"mean"})
    df_2["Poverty_Death_ratio"] = df_2["Population_Size"]/df_2["Poverty"]
    df_2 = df_2.sort_values(by=["Poverty_Death_ratio"], ascending=False)
    print(df_2.round(2))



def death_factors(df1, df2):
    df = df1[["CHSI_State_Name", "White", "Black", "Native_American", "Asian", "Hispanic"]]
    df_2 = df2[["CHSI_State_Name","Total_Deaths"]]
    df_1 = df.copy()
    df_3 = df_2.copy()
    df_1["Others"] = df_1['Native_American']+df_1['Asian']
    df_1 = df_1.drop(["Native_American", "Asian"], axis=1)
    population = df_1.groupby(["CHSI_State_Name"], as_index=False).agg({"Black":"mean", "White":"mean", "Others":"mean", "Hispanic":"mean"})
    population = population.round(2)
    deaths = df_2.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Deaths":"mean"})
    deaths = deaths.round(0)
    pop_deaths = pd.merge(population, deaths, on="CHSI_State_Name")
    pop_deaths = pop_deaths.sort_values(by=["Total_Deaths"], ascending=False)
    first_20 = pop_deaths.head(10)
    print(first_20)

    p1 = plt.bar(first_20["CHSI_State_Name"], first_20["White"], width=1, color="DarkGreen", edgecolor="black")
    p2 = plt.bar(first_20["CHSI_State_Name"], first_20["Black"], width=1, bottom=first_20["White"], color="Blue", edgecolor="black")
    p3 = plt.bar(first_20["CHSI_State_Name"], first_20["Others"], width=1, bottom=np.array(first_20["White"]) + np.array(first_20["Black"]),
                 color="Red", edgecolor="black")
    p4 = plt.bar(first_20["CHSI_State_Name"], first_20["Hispanic"], width=1,
                 bottom=np.array(first_20["White"]) + np.array(first_20["Black"]) + np.array(first_20["Others"]),
                 color="Orange", edgecolor="black")
    last_20 = pop_deaths.tail(10)
    r1 = plt.bar(last_20["CHSI_State_Name"], last_20["White"], width=1, color="DarkGreen", edgecolor="black")
    r2 = plt.bar(last_20["CHSI_State_Name"], last_20["Black"], width=1, bottom=last_20["White"], color="Blue", edgecolor="black")
    r3 = plt.bar(last_20["CHSI_State_Name"], last_20["Others"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]),
                 color="Red", edgecolor="black")
    r4 = plt.bar(last_20["CHSI_State_Name"], last_20["Hispanic"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]) + np.array(last_20["Others"]),
                 color="Orange", edgecolor="black")
    print(last_20)
    plt.xticks(rotation="vertical")
    plt.show()
birth_death_ratio(demographics, measures)
population_poverty(demographics)
death_factors(demographics, measures)
# print(demographics.info())
# print(demographics.isnull().sum())
# print(causes.info())
# print(causes.isnull().sum())

df = causes[["CHSI_County_Name", "CHSI_State_Name", "A_Wh_Comp", "A_Bl_Comp", "A_Ot_Comp", "A_Hi_Comp", "A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef"]]
df = df.replace(-1111,0)
#print(df['A_Bl_Comp'].head(50))
# df1 = df.groupby(["CHSI_State_Name", "CHSI_County_Name"])["A_Wh_Comp", "A_Bl_Comp", "A_Ot_Comp", "A_Hi_Comp", "A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef"].sum()
df1 = df.groupby("CHSI_State_Name").sum()
#print(df1.head(50))

df2 = demographics[["CHSI_County_Name", "CHSI_State_Name", "Population_Size", "Poverty"]]
#print(df2.isnull().sum())
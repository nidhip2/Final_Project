import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



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

    dfa = df_1.groupby(["CHSI_State_Name"], as_index=False).agg(
        {"White": "mean", "Black": "mean", "Others": "mean", "Hispanic": "mean", "Poverty": "mean"})
    dfb = birth_death.groupby(["CHSI_State_Name"], as_index=False).agg({"Total_Births": "mean", "Total_Deaths": "mean"})
    final_df = pd.merge(dfa, dfb, on="CHSI_State_Name")
    final_df = final_df.round(2)
    final_df = final_df.sort_values(by=["Poverty"], ascending=False)
    print(final_df)

    plt.subplot(2, 1, 1)
    plt.scatter(x=data['Poverty'], y=data["White"], color="DarkGreen", label="White")
    plt.scatter(x=data['Poverty'], y=data["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=data['Poverty'], y=data["Others"], color="Red", label="Others")
    plt.scatter(x=data['Poverty'], y=data["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.title("County & Race-wise Poverty")
    plt.grid(linewidth=0.5, color = "grey")

    plt.subplot(2, 1, 2)
    plt.scatter(x=final_df['Poverty'], y=final_df["White"], color="DarkGreen", label="White")
    plt.scatter(x=final_df['Poverty'], y=final_df["Black"], color="DarkBlue", label="Black")
    plt.scatter(x=final_df['Poverty'], y=final_df["Others"], color="Red", label="Others")
    plt.scatter(x=final_df['Poverty'], y=final_df["Hispanic"], color="Orange", label="Hispanic")
    plt.xlabel("Poverty")
    plt.ylabel("Race-wise Pop")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.grid(linewidth=0.5, color="grey")
    plt.title("State & Race-wise Poverty")
    plt.show()


def population_poverty(df):
    df1 = df[["CHSI_State_Name", "Poverty", "Population_Size"]]
    df1 = df1[df1["Poverty"]>=0]
    df_2 = df1.groupby(["CHSI_State_Name"], as_index=False).agg({"Population_Size":"mean", "Poverty":"mean"})
    df_2["Pop_Poverty_ratio"] = df_2["Population_Size"]/df_2["Poverty"]
    df_2 = df_2.sort_values(by=["Pop_Poverty_ratio"], ascending=True)
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
    last_20 = pop_deaths.tail(10)
    print(first_20)

    p1 = plt.bar(first_20["CHSI_State_Name"], first_20["White"], width=1, color="DarkGreen", edgecolor="black", label="White")
    p2 = plt.bar(first_20["CHSI_State_Name"], first_20["Black"], width=1, bottom=first_20["White"], color="Blue", edgecolor="black", label="Black")
    p3 = plt.bar(first_20["CHSI_State_Name"], first_20["Others"], width=1, bottom=np.array(first_20["White"]) + np.array(first_20["Black"]),
                 color="Red", edgecolor="black", label="Others")
    p4 = plt.bar(first_20["CHSI_State_Name"], first_20["Hispanic"], width=1,
                 bottom=np.array(first_20["White"]) + np.array(first_20["Black"]) + np.array(first_20["Others"]),
                 color="Orange", edgecolor="black", label="Hispanic")

    r1 = plt.bar(last_20["CHSI_State_Name"], last_20["White"], width=1, color="DarkGreen", edgecolor="black")
    r2 = plt.bar(last_20["CHSI_State_Name"], last_20["Black"], width=1, bottom=last_20["White"], color="Blue", edgecolor="black")
    r3 = plt.bar(last_20["CHSI_State_Name"], last_20["Others"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]),
                 color="Red", edgecolor="black")
    r4 = plt.bar(last_20["CHSI_State_Name"], last_20["Hispanic"], width=1,
                 bottom=np.array(last_20["White"]) + np.array(last_20["Black"]) + np.array(last_20["Others"]),
                 color="Orange", edgecolor="black")

    plt.xlabel("Top & Last 10 States")
    plt.ylabel("Race-wise Pop percent")
    plt.legend(loc="upper right", fontsize="x-small")
    plt.xticks(rotation="vertical")
    plt.grid(linewidth=0.5, color = "grey")
    plt.title("Top 10 & last 10 states ")
    plt.show()


def merge_dataframes(dataframe1, dataframe2, dataframe3, dataframe4):
    df_demo = dataframe2[["CHSI_County_Name","CHSI_State_Name","Poverty","Population_Size"]]
    df_riskfactor = dataframe1[["CHSI_County_Name","CHSI_State_Name","No_Exercise","Obesity","High_Blood_Pres","Smoker","Diabetes","Uninsured","Elderly_Medicare","Disabled_Medicare","Prim_Care_Phys_Rate"]]
    df_measurebd = dataframe3[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Late_Care","Infant_Mortality","Total_Deaths","Total_Births"]]
    df_unemp = dataframe4[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Unemployed"]]
    df_demo_risk = pd.merge(df_demo, df_riskfactor, on=['CHSI_State_Name','CHSI_County_Name'])
    df_demo_risk_bd = pd.merge(df_demo_risk, df_measurebd, on=['CHSI_State_Name','CHSI_County_Name'])
    df_demo_risk_bd_unemp = pd.merge (df_demo_risk_bd, df_unemp, on=['CHSI_State_Name','CHSI_County_Name'])

    pd.set_option('display.max_columns', None)

    return df_demo_risk_bd_unemp


def analysis_1 (df):

    df_final_1 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], 0)
    df_final_1 = df_final_1.groupby(['CHSI_State_Name'], as_index = False)["No_Exercise", "Obesity", "Poverty", "High_Blood_Pres", "Smoker", "Diabetes", "Total_Deaths", "Total_Births"].mean()
    df = df_final_1.loc[(df_final_1 != 0).any(axis=1)]
    print(df.isnull().sum())

    pd.set_option('display.max_columns', None)

    b = (df.sort_values(by=["Poverty","Total_Deaths"], ascending=False).head(20))
    b = b.round(2)
    print (b.head())
    print(b.tail())


def analysis_2 (df):

    df_final_2 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], 0)
    df_final_2 = df_final_2.groupby(['CHSI_State_Name'], as_index = False)["Unemployed","Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Prim_Care_Phys_Rate", "Late_Care", "Infant_Mortality","Total_Deaths","Poverty"].mean()
    df_final_2 = df_final_2.loc[(df_final_2 != 0).any(axis=1)]

    pd.set_option('display.max_columns', None)

    c = (df_final_2.sort_values(by=["Poverty", "Total_Deaths"], ascending=False).head(20))
    print(c.head())


def genetic_deaths(df1,df2):
    df = pd.merge(df1,df2, on = ["CHSI_County_Name","County_FIPS_Code","CHSI_State_Name","State_FIPS_Code"])
    df_1 = df[['CHSI_State_Name', "A_Wh_BirthDef","A_Bl_BirthDef","A_Ot_BirthDef","A_Hi_BirthDef","Total_Births"]]
    df_1 = df_1.replace(to_replace=[-9999, -2222, -2222.2, -2, -1111.1, -1111, -1], value=0)
    df_1 = df_1.groupby("CHSI_State_Name")["A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"].sum()
    df_1.reset_index()
    pd.set_option('display.max_columns', None)
    print(df_1)


def read_dataframes():
    demographics = pd.read_csv("DEMOGRAPHICS.csv")
    lead_death_cause = pd.read_csv("LEADINGCAUSESOFDEATH.csv")
    birth_death_measure = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")
    risk_factors = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")
    vulnerable_pops = pd.read_csv("VUNERABLEPOPSANDENVHEALTH.csv")
    return demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops


if __name__ == '__main__':

    demographics, lead_death_cause, birth_death_measure, risk_factors, vulnerable_pops  = read_dataframes()
    birth_death_ratio(demographics, birth_death_measure)
    population_poverty(demographics)
    death_factors(demographics, birth_death_measure)
    result = merge_dataframes(risk_factors, demographics, birth_death_measure, vulnerable_pops)
    analysis_1(result)
    analysis_2(result)
    genetic_deaths(lead_death_cause, birth_death_measure)
import warnings; warnings.simplefilter("ignore")
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

information_columns = pd.ExcelFile("CHSI DataSet.xls")
dataframe1 = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")
dataframe2 = pd.read_csv("DEMOGRAPHICS.csv")
dataframe3 = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")
dataframe4 = pd.read_csv("VUNERABLEPOPSANDENVHEALTH.csv")


def read_dataframes ():
    df_demo = dataframe2[["CHSI_County_Name","CHSI_State_Name","Poverty","Population_Size"]]

    df_riskfactor = dataframe1[["CHSI_County_Name","CHSI_State_Name","No_Exercise","Obesity","High_Blood_Pres","Smoker","Diabetes","Uninsured","Elderly_Medicare","Disabled_Medicare","Prim_Care_Phys_Rate"]]

    df_measurebd = dataframe3[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Late_Care","Infant_Mortality","Total_Deaths","Total_Births"]]

    df_unemp = dataframe4[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","Unemployed"]]

    df_demo_risk = pd.merge(df_demo, df_riskfactor, on=['CHSI_State_Name','CHSI_County_Name'])

    df_demo_risk_bd = pd.merge(df_demo_risk, df_measurebd, on=['CHSI_State_Name','CHSI_County_Name'])

    df_demo_risk_bd_unemp = pd.merge (df_demo_risk_bd, df_unemp, on=['CHSI_State_Name','CHSI_County_Name'])

    pd.set_option('display.max_columns', None)
    # print (df_demo_risk_bd.head(10))
    # print(df_demo_risk_bd_unemp.head(10))
    # print(df_demo_risk.head(10))
    # print(df_measurebd.head(10))
    # print(df_riskfactor.head(10))
    # print (df_demo.head(10))

    return df_demo_risk_bd_unemp

def analysis_1 (df):

    df_final_1 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], 0)
    df_final_1 = df_final_1.groupby(['CHSI_State_Name'], as_index = False)["No_Exercise", "Obesity", "Poverty", "High_Blood_Pres", "Smoker", "Diabetes", "Total_Deaths", "Total_Births"].mean()
    df_final_1 = df_final_1[df_final_1.No_Exercise !=0]
    df_final_1 = df_final_1[df_final_1.Obesity != 0]
    df_final_1 = df_final_1[df_final_1.Poverty != 0]
    df_final_1 = df_final_1[df_final_1.High_Blood_Pres != 0]
    df_final_1 = df_final_1[df_final_1.Smoker != 0]
    df_final_1 = df_final_1[df_final_1.Diabetes != 0]
    df_final_1 = df_final_1[df_final_1.Total_Deaths != 0]
    df_final_1 = df_final_1[df_final_1.Total_Births != 0]
    pd.set_option('display.max_columns', None)
    # Total_Death_1 = df_final_1.groupby(["CHSI_County_Name"], as_index=False).agg({"Total_Deaths":"mean"})
    #Poverty_1 = df_final_1.groupby(["CHSI_County_Name"],["CHSI_State_Name"], as_index=False).agg({"Poverty": "mean"})
    # a = pd.merge(risk_factor_1, Total_Death_1, on=['CHSI_County_Name'])
    #b = pd.merge(a, Poverty_1, on=["CHSI_State_Name","CHSI_County_Name"])
    b = (df_final_1.sort_values(by=["Poverty","Total_Deaths"], ascending=False).head(20))
    print (b.head())
    print(b.tail())

def analysis_2 (df):

    df_final_2 = df.replace([-1111, -1111.1, -1, -2222.2, -2222, -2], 0)
    df_final_2 = df_final_2.groupby(['CHSI_State_Name'], as_index = False)["Unemployed","Uninsured", "Elderly_Medicare", "Disabled_Medicare", "Prim_Care_Phys_Rate", "Late_Care", "Infant_Mortality","Total_Deaths","Poverty"].mean()
    df_final_2 = df_final_2[df_final_2.Uninsured != 0]
    df_final_2 = df_final_2[df_final_2.Elderly_Medicare != 0]
    df_final_2 = df_final_2[df_final_2.Disabled_Medicare != 0]
    df_final_2 = df_final_2[df_final_2.Prim_Care_Phys_Rate != 0]
    df_final_2 = df_final_2[df_final_2.Late_Care != 0]
    df_final_2 = df_final_2[df_final_2.Unemployed != 0]
    df_final_1 = df_final_2[df_final_2.Infant_Mortality != 0]

    pd.set_option('display.max_columns', None)

    c = (df_final_1.sort_values(by=["Poverty", "Total_Deaths"], ascending=False).head(20))
    print(c.head())

if __name__ == '__main__':

    df = read_dataframes()
    analysis_1(df)
    analysis_2(df)
import pandas as pd
import matplotlib.pyplot as plt

Demo = pd.read_csv("DEMOGRAPHICS.csv")
Deaths = pd.read_csv("LEADINGCAUSESOFDEATH.csv")
Measures = pd.read_csv("MEASURESOFBIRTHANDDEATH.csv")
Vulnerable = pd.read_csv("VUNERABLEPOPSANDENVHEALTH.csv")
Risk = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")

def genetic_deaths(df1,df2):
    df = pd.merge(df1,df2, on = ["CHSI_County_Name","County_FIPS_Code","CHSI_State_Name","State_FIPS_Code"])
    df_1 = df[['CHSI_State_Name', "A_Wh_BirthDef","A_Bl_BirthDef","A_Ot_BirthDef","A_Hi_BirthDef","Total_Births"]]
    df_1 = df_1.replace(to_replace=[-9999, -2222, -2222.2, -2, -1111.1, -1111, -1], value=0)
    df_1 = df_1.groupby("CHSI_State_Name")["A_Wh_BirthDef", "A_Bl_BirthDef", "A_Ot_BirthDef", "A_Hi_BirthDef", "Total_Births"].sum()
    df_1.reset_index()
    pd.set_option('display.max_columns', None)
    return(df_1)

if __name__ == '__main__':

    dfd=genetic_deaths(Deaths, Measures)
    print("The statewise data for deaths due to genetic defects is as follows: \n")
    print(dfd)


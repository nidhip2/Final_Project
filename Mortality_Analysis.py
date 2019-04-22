import warnings; warnings.simplefilter("ignore")
import pandas as pd
import numpy as np
import csv

def read_dataframes ():

    #Read the whole workbook and page wise to view the desired data for analysis
    information_columns = pd.ExcelFile("CHSI DataSet.xls")
    # page_1 = pd.read_excel("CHSI DataSet.xls", sheet_name=0)
    # page_2 = pd.read_excel("CHSI DataSet.xls", sheet_name=1)
    # page_3 = pd.read_excel("CHSI DataSet.xls", sheet_name=2)
    # page_4 = pd.read_excel("CHSI DataSet.xls", sheet_name=3)
    # page_5 = pd.read_excel("CHSI DataSet.xls", sheet_name=4)
    # page_6 = pd.read_excel("CHSI DataSet.xls", sheet_name=5)
    # page_7 = pd.read_excel("CHSI DataSet.xls", sheet_name=6)
    # page_8 = pd.read_excel("CHSI DataSet.xls", sheet_name=7)
    # page_9 = pd.read_excel("CHSI DataSet.xls", sheet_name=8)
    # page_10 = pd.read_excel("CHSI DataSet.xls", sheet_name=9)
    # page_11 = pd.read_excel("CHSI DataSet.xls", sheet_name=10)

    # print the data if needed.
    #print(page_4)
    # gives the names of the excel sheets in the dataset.
    read_page_names = information_columns.sheet_names
    print(read_page_names)

    # Load the dataset into dataframes
    dataframe1 = pd.read_csv("RISKFACTORSANDACCESSTOCARE.csv")
    dataframe2 = pd.read_csv("DEMOGRAPHICS.csv")

    # Select the desired columns into another dataframe for dataframe1
    df_1 = dataframe2[["CHSI_County_Name","CHSI_State_Name","Poverty","Max_Poverty","Min_Poverty","Population_Size","County_FIPS_Code","State_FIPS_Code"]]
    # print (df_1.head(20))

    # Select the desired columns into another dataframe for dataframe1
    df_2 = dataframe1[["State_FIPS_Code","County_FIPS_Code","CHSI_County_Name","CHSI_State_Name","No_Exercise","Obesity","High_Blood_Pres","Smoker","Diabetes","Uninsured","Elderly_Medicare","Disabled_Medicare","Prim_Care_Phys_Rate"]]
    df_2 = df_2.replace(-1111,0)
    df_2 = df_2.replace(-1111.1,0)
    df_2 = df_2.replace(-1, 0)
    df_2 = df_2.replace(-2222.2, 0)
    df_2 = df_2.replace(-2222, 0)
    df_2 = df_2.replace(-2, 0)
    # print(df_2.groupby("County_FIPS_Code")["No_Exercise","Obesity","High_Blood_Pres"].sum())

    df = pd.merge(df_1, df_2, on=['CHSI_State_Name','CHSI_County_Name'])
    #print (df.head(20))
    # print(df.info())
    # print(df_1)
    # print(df_2)
    print(df.groupby(['CHSI_State_Name','CHSI_County_Name'])["No_Exercise","Obesity","Poverty","High_Blood_Pres","Smoker","Diabetes","Uninsured","Elderly_Medicare","Disabled_Medicare","Prim_Care_Phys_Rate"].sum())
# print(df_2[["No_Exercise","Obesity","High_Blood_Pres"]])
# print (dataframe2[['Poverty', 'Min_Poverty', 'Max_Poverty']])


if __name__ == '__main__':

    read_dataframes()
import pandas as pd

data_CO2 = pd.read_csv("D:/Python/PyCharm projects/pythonProject_Zal/Data/co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv")
data_GPD = pd.read_csv("D:\Python\PyCharm projects\pythonProject_Zal\Data\API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562\API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv"
                 ,skiprows=[0,1,2])
data_PPL = pd.read_csv("D:\Python\PyCharm projects\pythonProject_Zal\Data\API_SP.POP.TOTL_DS2_en_csv_v2_4751604\API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv"
                 ,skiprows=[0,1,2])
#In first few columns there is meta text (not data). We can eather use skiprows comend or manualy edit data


# print(data_CO2.head())
# print(data_CO2.tail())
#print(data_CO2['Year'][0:10])    wybrana kolumna
#print(data_CO2[data_CO2['Year'] == 2000])      wybrane wiersze na bazie warunku kolumnowego
#print(data_CO2['Year'].unique())   unikatowe wartości

#NA values
# print(data_CO2[data_CO2.isna().any(axis=1)])
# print(data_CO2[data_CO2['column name'].isna()])

# print(data_CO2[0:1])

print('data CO2')
pusteCO2 = []
for col in data_CO2:
    if len(data_CO2[col].unique()) == 1 :
        pusteCO2.append(col)
print("Puste kolumny dla CO2: " + f"{pusteCO2}")

print('data GPD')
pusteGPD = []
for col in data_GPD:
    if len(data_GPD[col].unique()) == 1 :
        pusteGPD.append(col)
print("Puste kolumny dla GPD: " + f"{pusteGPD}")


print('data PPL')
pustePPL = []
for col in data_PPL:
    if len(data_PPL[col].unique()) == 1 :
        pustePPL.append(col)
print("Puste kolumny dla PPL: " + f"{pustePPL}")

#Lets get ride of those columns ['Indicator Name', 'Indicator Code', 'Unnamed: 66'] for PPL and GPD
data_CO2 = data_CO2.loc[:, ~data_CO2.columns.isin(pusteCO2)]
data_GPD = data_GPD.loc[:, ~data_GPD.columns.isin(pusteGPD)]
data_PPL = data_PPL.loc[:, ~data_PPL.columns.isin(pustePPL)]



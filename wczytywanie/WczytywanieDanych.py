import argparse
import os
import pandas as pd
import numpy as np


# argparse - module makes it easy to write user-friendly command-line interfaces, including automatically generates help
# and usage messages. It allow us to define what arguments it requires and it will issue errors when users give the program invalid arguments.

# os -This module implements some useful functions on pathnames

def validate_file(filepath):
    if not os.path.exists(filepath):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(filepath))
    return filepath


def read_table(file_name, mode):
    if mode == 'GDP' or mode == 'LM':
        return pd.read_csv(file_name, skiprows=[0, 1, 2])
    if mode == 'CO2':
        return pd.read_csv(file_name)
    raise RuntimeError('Bad mode :c, select form : (GPD, LM, CO2)')


def UsunSzcztuczneKol(df):
    puste = []
    for col in df:
        if len(df[col].unique()) == 1:
            puste.append(col)
    df = df.loc[:, ~df.columns.isin(puste)]
    return (df)


def wide_to_long(df, id_vars, var_name, value_name):
    result = pd.melt(df, id_vars=id_vars, var_name=var_name,value_name=value_name)
    return result


# CHOOSING ONLY YEARS PRESENT IN ALL DATAFRAMES
def WspolneLata(df1, df2, df3):
    df1['Year'] = df1['Year'].astype('str')
    df2['Year'] = df2['Year'].astype('str')
    df3['Year'] = df3['Year'].astype('str')

    wspolne_lata = set(df2['Year']).intersection(set(df3['Year']))
    wspolne_lata = wspolne_lata.intersection(set(df1['Year']))
    wspolne_lata = list(wspolne_lata)

    df1 = df1.loc[[lata in wspolne_lata for lata in df1['Year']]]
    df3 = df3.loc[[lata in wspolne_lata for lata in df3['Year']]]
    df2 = df2.loc[[lata in wspolne_lata for lata in df2['Year']]]

    return df1, df2, df3


def Unifikacja(df):
    df = df.rename(columns = {'Country Name': 'Country'})
    df['Country'] = df['Country'].str.upper()
    return df


# There is the same set of Country names in data data_GPD2 and data_PPL2 but there is some times small differences
# between thouse two and data_CO2, for eg. 'BAHAMAS' and 'BAHAMAS, THE'
# Lets serch for thouse "similar" Countries

# co2_uni = data_CO2['Country'].unique()
# inner_uni = inner['Country'].unique()
# diif_co2 = list(set(co2_uni) - set(inner_uni))
# diff_uni = list(set(inner_uni) - set(co2_uni))
#
# minim = min([len(x) for x in diff_uni])
# pierwsze = []
# for word in diff_uni:
#     pierwsze.append(word[:minim])
#
# j = 0
# for ww in pierwsze:
#     print(f'{ww} : {diff_uni[j]}')
#     j = j+1
#     for x in diif_co2:
#         if x.find(ww) != -1:
#             print(x)



def JednoliteKrajeCO2(df):
    conv_dict = {
        'PLURINATIONAL STATE OF BOLIVIA': 'BOLIVIA',
        'LIBYAN ARAB JAMAHIRIYAH': 'LIBYA',
        'UNITED STATES OF AMERICA': 'UNITED STATES',
        'MYANMAR (FORMERLY BURMA)': 'MYANMAR',
        'ISLAMIC REPUBLIC OF IRAN': 'IRAN, ISLAMIC REP.',
        'ST. VINCENT & THE GRENADINES': 'ST. VINCENT AND THE GRENADINES',
        'ITALY (INCLUDING SAN MARINO)': 'ITALY',
        'KYRGYZSTAN': 'KYRGYZ REPUBLIC',
        'MACAU SPECIAL ADMINSTRATIVE REGION OF CHINA': 'MACAO SAR, CHINA',
        'ANTIGUA & BARBUDA': 'ANTIGUA AND BARBUDA',
        'REPUBLIC OF CAMEROON': 'CAMEROON',
        'LAO PEOPLE S DEMOCRATIC REPUBLIC': 'LAO PDR',
        'SAO TOME & PRINCIPE': 'SAO TOME AND PRINCIPE',
        'BRUNEI (DARUSSALAM)': 'BRUNEI DARUSSALAM',
        'FRANCE (INCLUDING MONACO)': 'FRANCE',
        'VIET NAM': 'VIETNAM',
        'REPUBLIC OF MOLDOVA': 'MOLDOVA',
        'CZECH REPUBLIC': 'CZECHIA',
        'BAHAMAS': 'BAHAMAS, THE',
        'EGYPT': 'EGYPT, ARAB REP.',
        'YEMEN': 'YEMEN, REP.',
        'HONG KONG SPECIAL ADMINSTRATIVE REGION OF CHINA': 'HONG KONG SAR, CHINA',
        'TURKEY': 'TURKIYE',
        'COTE D IVOIRE': 'COTE D\'IVOIRE',
        'GUINEA BISSAU': 'GUINEA-BISSAU',
        'TIMOR-LESTE (FORMERLY EAST TIMOR)': 'TIMOR-LESTE',
        'CONGO': 'CONGO, REP.',
        'REPUBLIC OF KOREA': 'KOREA, REP.',
        'FEDERATED STATES OF MICRONESIA': 'MICRONESIA, FED. STS.',
        'DEMOCRATIC REPUBLIC OF THE CONGO (FORMERLY ZAIRE)': 'CONGO, DEM. REP.',
        'GAMBIA': 'GAMBIA, THE',
        'VENEZUELA': 'VENEZUELA, RB',
        'CHINA (MAINLAND)': 'CHINA',
        'REPUBLIC OF SOUTH SUDAN': 'SOUTH SUDAN',
        'ST. KITTS-NEVIS': 'ST. KITTS AND NEVIS',
        'UNITED REPUBLIC OF TANZANIA': 'TANZANIA',
        'BOSNIA & HERZEGOVINA': 'BOSNIA AND HERZEGOVINA',
        'SLOVAKIA': 'SLOVAK REPUBLIC',
    }
    df['Country'] = df['Country'].replace(conv_dict)
    return df


def MergeAll(df1, df2, df3):
    data_merge = pd.merge(pd.merge(df1,df2,on=["Year","Country"]),df3,on=["Year","Country"])
    # inner = pd.merge(df1, df2)
    # data_merge = pd.merge(inner, df3)
    return data_merge


# Create dataframe where for each year we choose 5 countries with highest income (PDG) per person
def Top5Income(df):
    d = {'Year': df['Year'], 'Country': df['Country'],
         'PDG per person': df['value_GPD'].div(df['value_PPL'])}
    data_income_full = pd.DataFrame(data=d)
    data_income_full = data_income_full.sort_values(by=['Year', 'PDG per person'], ascending=False)
    # We dont know if there is 5 countries data for each year, but if there is fewer we want to know also about them
    Year_len = [len(data_income_full[data_income_full['Year'] == y]) for y in data_income_full['Year'].unique()]
    upto5 = [min(5, x) for x in Year_len]
    i = 0
    data_income5 = pd.DataFrame(columns=['Year', 'Country', 'PDG per person'])
    for y in data_income_full['Year'].unique():
        Top_income_set_Year = data_income_full[data_income_full['Year'] == y][:upto5[i]]
        data_income5 = pd.concat([data_income5, Top_income_set_Year], ignore_index=True, sort=False)
        i = i + 1

    return data_income5


def Top5CO2(df):
    d = {'Year': df['Year'], 'Country': df['Country'],
         'CO2 per person': df['Total'].div(df['value_PPL'])}
    data_emission_full = pd.DataFrame(data=d)
    data_emission_full = data_emission_full.sort_values(by=['Year', 'CO2 per person'], ascending=False)
    # We dont know if there is 5 countries data for each year, but if there is fewer we want to know also about them
    Year_len = [len(data_emission_full[data_emission_full['Year'] == y]) for y in data_emission_full['Year'].unique()]
    upto5 = [min(5, x) for x in Year_len]
    i = 0
    data_emissio5 = pd.DataFrame(columns=['Year', 'Country', 'CO2 per person'])
    for y in data_emission_full['Year'].unique():
        Top_emission_set_Year = data_emission_full[data_emission_full['Year'] == y][:upto5[i]]
        data_emissio5 = pd.concat([data_emissio5, Top_emission_set_Year], ignore_index=True, sort=False)
        i = i + 1

    return data_emissio5

def CO2Diff(df):
    d = {'Year': df['Year'], 'Country': df['Country'],
         'co2_pp': df['Total'].div(df['value_PPL'])}
    data_emission_full = pd.DataFrame(data=d)
    results = dict()
    for kraj in data_emission_full['Country'].unique():
        subdf = data_emission_full.loc[data_emission_full['Country'] == kraj].copy(deep=True)
        subdf["Year"] = subdf["Year"].astype(int)
        max_year = subdf['Year'].max()
        print(f"{kraj=} {max_year=}")
        max_m_10 = max_year - 10
        if max_m_10 not in subdf['Year'].values:
            print(f"{kraj} does not contain needed data")
            continue
        v = subdf.loc[subdf["Year"] == max_year, "co2_pp"].values[0] - subdf.loc[subdf["Year"] == max_m_10, "co2_pp"].values[0]
        results[kraj] = v
    print(f"Country with biggest increase CO2 per person {max(results, key=results.get)}")
    print(f"Country with biggest decrease CO2 per person {min(results, key=results.get)}")


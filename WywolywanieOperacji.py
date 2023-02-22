#The argparse module’s support for command-line interfaces is built around an instance of argparse.ArgumentParser.
import WczytywanieDanych
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="Paths for data sets")
    parser.add_argument("-GDP", "--GDP", type=WczytywanieDanych.validate_file,
                        help="Input file path for GDP data")
    parser.add_argument("-LM", "--Liczba_mieszkancow", type=WczytywanieDanych.validate_file,
                        help="Input file path for Liczba mieszkancow data")
    parser.add_argument("-CO2", "--Emisja_CO2", type=WczytywanieDanych.validate_file,
                        help="Input file path for Emisja CO2 data")
    args = parser.parse_args()
    return args

#The ArgumentParser.add_argument() method attaches individual argument specifications to the parser.
# We can choose it to be a `path` argument which satisfies our dir_path function
#parser.add_argument(sciezka, type=dir_path, help='Podaj sciezke do danych') #argument type
#args = parser.parse_args()

def main():
    args = parse_arguments()

    data_CO2 = WczytywanieDanych.read_table(args.Emisja_CO2, 'CO2')
    data_GDP = WczytywanieDanych.read_table(args.GDP, 'GDP')
    data_PPL = WczytywanieDanych.read_table(args.Liczba_mieszkancow, 'LM')


    data_CO2 = WczytywanieDanych.UsunSzcztuczneKol(data_CO2)
    data_GDP = WczytywanieDanych.UsunSzcztuczneKol(data_GDP)
    data_PPL = WczytywanieDanych.UsunSzcztuczneKol(data_PPL)


    data_GDP = WczytywanieDanych.wide_to_long(data_GDP, data_GDP.columns[[0, 1]], 'Year', 'value_GPD')
    data_PPL = WczytywanieDanych.wide_to_long(data_PPL, data_PPL.columns[[0, 1]], 'Year', 'value_PPL')
    # WczytywanieDanych.NowaKolumnaDat(data_GDP)
    # WczytywanieDanych.NowaKolumnaDat(data_PPL)

    data_CO2, data_PPL, data_GDP = WczytywanieDanych.WspolneLata(data_CO2, data_PPL, data_GDP)

    data_CO2 = WczytywanieDanych.Unifikacja(data_CO2)
    data_GDP = WczytywanieDanych.Unifikacja(data_GDP)
    data_PPL = WczytywanieDanych.Unifikacja(data_PPL)

    data_CO2 = WczytywanieDanych.JednoliteKrajeCO2(data_CO2)


    data_merge = WczytywanieDanych.MergeAll(data_CO2, data_PPL, data_GDP)

    data_income = WczytywanieDanych.Top5Income(data_merge)
    print("Top 5 countries per year with highest GDP per person")
    print(data_income)
    data_emission = WczytywanieDanych.Top5CO2(data_merge)
    print("Top 5 countries per year with biggest emission CO2 per person")
    print(data_emission)
    WczytywanieDanych.CO2Diff(data_merge)

    print('Thank u for listening to my pep talk')




if __name__ == '__main__':
    main()
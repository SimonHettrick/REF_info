#!/usr/bin/env python
# encoding: utf-8

import csv
import os
import time
import pandas as pd

DATAFILENAME = "./all-panel-members-list-v6-111019.csv"
DATASTORE = './'

def read_csv_as_list(filename):
    """
    Imports a csv file into a list
    :params: a filename to a csv
    :return: a list
    """

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        all_info_in_pdf = list(reader)


    return all_info_in_pdf


def export_to_csv(df, filename, index_write):
    """
    Exports a df to a csv file
    :params: a df and a location in which to save it
    :return: nothing, saves a csv
    """

    return df.to_csv(DATASTORE + filename + '.csv', index=index_write, encoding='utf-8-sig')


def clean_up_list(all_info_in_pdf):
    """
    Get the string ready for processing by removing unnecessary info
    :param all_info_in_pdf:
    :return: a cleaned list
    """

    # Convert list of lists into list of strings
    all_info_in_pdf = [str(i) for i in all_info_in_pdf]

    # Remove first 2 and last 2 characters from each string
    all_info_in_pdf = [i[2:-2] for i in all_info_in_pdf]

    # There's a regular sentence in the data explaining what the asterisks mean. This removes them.
    # There's also page numbers, which are only 1 char long. This removes them
    for x in all_info_in_pdf:
        if '* denotes' in x:
            all_info_in_pdf.remove(x)
        if len(x) == 1:
            all_info_in_pdf.remove(x)


    return(all_info_in_pdf)


def chop_into_panels(all_info_in_pdf):
    """
    Parse the text from the pdf into name and institution, what panel they're on, what sub-panel, their role, etc
    :param all_info_in_pdf: all the text in the pdf separated into lines
    :return: parsed_ref_panel: a dict containing all the data on each REF panelist
    """

    # initialise a dict and some variables used to store panelist info
    parsed_ref_panel = {}
    main_panel = None
    role = None
    sub_panel = None
    name = None

    # So I can text for this string OR this string OR ... I set up these sets for use in the later if statements
    role_strings = {'Chair', 'Deputy Chair', 'Members', 'Observers', 'Secretariat', 'Additional assessment phase members'}
    title_strings = {'Pr', 'Dr', 'Mr', 'Mi', 'Ms'}

    for x in all_info_in_pdf:
        #print(x)
        if 'Main Panel' in x:
            main_panel = x
            sub_panel = 'Main panel'
        if 'Sub-panel' in x:
            sub_panel = x
        if x in role_strings:
            role = x
        if x[:2] in title_strings:
            name = x
            parsed_ref_panel[name] = {'main panel': main_panel, 'sub-panel': sub_panel, 'role': role}

    #print(parsed_ref_panel)

    return parsed_ref_panel


def create_df(parsed_ref_panel):
    """
    Write out results as a dataframe for easy conversion to a csv table
    :param parsed_ref_panel: a dict containing ref details for each panelist
    :return: nothing. Instead it writes out a dataframe of the parsed details
    """

    df = pd.DataFrame.from_dict(data=parsed_ref_panel, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'name and institution'}, inplace=True)
    df.sort_values(by=['main panel', 'sub-panel'], inplace=True)
    df['name'] = df['name and institution'].str.split(' ').str[:3].str.join(sep=' ')
    df['institution'] = df['name and institution'].str.split(' ').str[3:].str.join(sep=' ')
    # Re-order purely to produce a prettier csv
    df = df[['name', 'institution', 'main panel', 'sub-panel','role', 'name and institution']]


    export_to_csv(df,'REF_panelists', False)
    return



def main():
    """
    Main function to run program
    """
    all_info_in_pdf = read_csv_as_list(DATAFILENAME)

    all_info_in_pdf = clean_up_list(all_info_in_pdf)

    parsed_ref_panel = chop_into_panels(all_info_in_pdf)

    create_df(parsed_ref_panel)

if __name__ == '__main__':
    main()
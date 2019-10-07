#!/usr/bin/env python
# encoding: utf-8

import csv
import os
import time

DATAFILENAME = "./All_REF_panel_members.csv"

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

    for x in all_info_in_pdf:
        if '* denotes' in x:
            all_info_in_pdf.remove(x)
        if len(x) == 1:
            all_info_in_pdf.remove(x)


    return(all_info_in_pdf)


def chop_into_panels(all_info_in_pdf):

    ref_panel = {}
    main_panel = None
    role = None
    panel = None
    name = None


    for x in all_info_in_pdf:
        #print(x)
        if 'Main Panel' in x:
            ref_panel[main_panel] = x
            ref_panel[panel] = [x]
        if 'Sub-panel' in x:
            ref_panel[panel] = x
        if 'Chair' or 'Deputy Chair' or 'Members' or 'Observers' or 'Secretariat' or 'Additional assessment phase members' in x:
            ref_panel[role] = x
        if 'Professor' or 'Dr' or 'Mr' or 'Mrs' or 'Miss' or 'Ms' in x:
            ref_panel[name] = x

    print(ref_panel)

        #print(main_panel, panel, role, name)

        #if not os.path.exists(directory):
        #    os.makedirs(directory)

        #time.sleep(0.5)

    return


def main():
    """
    Main function to run program
    """
    all_info_in_pdf = read_csv_as_list(DATAFILENAME)

    all_info_in_pdf = clean_up_list(all_info_in_pdf)

    chop_into_panels(all_info_in_pdf)



if __name__ == '__main__':
    main()
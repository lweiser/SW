#!/usr/bin/env python

import json
import pandas as pd
import sw_exceptions
import sys

"""
    gameboard_csv_to_json.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains functions for manipulating SW gameboard.
    It includes code for writing json gameboard from a csv input file,
    (gameboard_csv_to_json).
"""

def gameboard_csv_to_json(in_csv,out_json):
    """ Reads in csv formatted SW gameboard information (in_csv)
    and writes out json formatted gameboard information (out_json).

    Input:

    in_csv: a csv file containing gameboard informationself.
        Shoud contain columns:
            space_id:int,terrain:string,lost_tribes:boolean,
            symbol_*:string,neighbor_*:int
        Where:
            -space_ids should be sequential integers
            -space_id,terrain,lost_tribes are filled for all spaces
            -any number of symbol_ or neighbor_ columns are alowed
            -the symbol and neighbor columns may be empty

    Output:

    out_json: file containing all of the board information coded in json formatted

    """

    #check for correct check for correct inputs
    if not in_csv.endswith('.csv'):
        raise sw_exceptions.InputError('First file must be a csv file.')
    if not out_json.endswith('.json'):
        raise sw_exception.InputError('Please choose output ending with .json')


    #read in board data using pandas csv reader
    space_data = pd.read_csv(in_csv)
    space_data.head()

    # fill in empty column values in the neighbor list
    neighbor_cols= [val for val in space_data.columns.values
                    if val.startswith('neighbor')]
    space_data[neighbor_cols]=space_data[neighbor_cols].fillna(0).astype(int)

    #dictionary and json data are very similar
    #store spaces as a dict of dicts for easy conversion with json module
    spaces=dict()
    for idx,data in space_data.iterrows():

        # store each space as it's own dictionary
        space = dict()
        space['id'] = str(data['space_id'])
        space['terrain'] = data['terrain']
        space['is_edge'] = str(data['is_edge'])
        space['lost_tribes'] = str(data['lost_tribes'])

        # check that symbol_1 contains a string value
        if isinstance(data['symbol_1'],str):
            #initialize key as list then loop through adding attributes
            space['symbols']=[]
            for col in [val for val in space_data.columns.values
                        if val.startswith('symbol')]:
                if isinstance(data[col],str):
                    space['symbols'].append(data[col])

        # initialize 'neighbors' key to list and add all neighbors
        space['neighbors'] = []
        for col in [val for val in space_data.columns.values
                        if val.startswith('neighbor')]:
            if data[col] > 0:
                space['neighbors'].append(str(data[col]))

        #create the string key for the space & add to spaces dict
        space_key = 'space_' + str(space['id'])
        spaces[space_key]=space

    #write data to a json file.
    with open(out_json, 'w') as outfile:
        json.dump(spaces, outfile,sort_keys=True,indent=4)

if __name__ == '__main__':
    gameboard_csv_to_json(sys.argv[1],sys.argv[2])

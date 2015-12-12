#!/usr/bin/env python
# Function for grabbing one test data set
# for Matt Rueben's 2-d tree implementation. 

def get_iris_data():
    x = []
    y = []
    with open('../data/iris', 'r') as f:
        entries = f.readlines()
        for entry in entries:
            parsed = entry.split('\t')
            x.append(float(parsed[0]))
            y.append(float(parsed[1]))
    return x, y

#!/usr/bin/env python
import sys
import argparse
import re
import logging
import os


logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))
log = logging.getLogger("floyd")
#log.setLevel(level)
log.info("Info enabled")
log.debug("Debug enabled")


parser = argparse.ArgumentParser()
parser.add_argument("file",type=argparse.FileType('r'))
args = parser.parse_args()


file1 = args.file
# read the first line
line1 = file1.readline().strip()
line1_values = re.match("(?P<num_vertex>\d+)",line1)
num_vertex = int(line1_values.group('num_vertex')) + 1

log.info(f"size {num_vertex}")

max_value = "MAX"
end=num_vertex

vertex = [[max_value for j in range(num_vertex)] for i in range(num_vertex)]
#vertex[1][2] = 2
#vertex[2][3] = -4
#vertex[3][5] = 5
#vertex[4][5] = -5
#vertex[1][4] = -5


Lines = file1.readlines()
vertex_regex = re.compile("(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<weight>-?\d+)")
count = 0
for line in Lines:
    count += 1
    log.debug(f"Line is {line}")
    m = vertex_regex.match(line.strip())
    i_index = int(m.group('start'))
    j_index = int(m.group('end'))
    weight = int(m.group('weight'))

    if vertex[i_index][j_index] == max_value or weight < vertex[i_index][j_index]:
        vertex[i_index][j_index] = weight
    

log.info("VERTEX data after reading in")
for j in reversed(range(1,num_vertex)):
    log_info = [f"{vertex[i][j]}" for i in range(1,num_vertex)]
    log.info(f"j={j} {log_info}")  

log.info("")

log.info("RESULTS initializations")
results = [[[max_value for j in range(num_vertex)] for i in range(num_vertex)] for k in range(num_vertex)]

for i in range(1,num_vertex):
    for j in range(1,num_vertex):
        if i == j:
            # if there is a negative weight path defined from this 
            # vertex to itself, then use that as the starting point 
            # (this graph will have a negative cycle)
            log.debug(f"Init {i} {j} {vertex[i][j]}")
            if vertex[i][j] != max_value and vertex[i][j] < 0:
                results[0][i][j] = vertex[i][j]
            else:
                # otherwise the starting point is 0
                results[0][i][j] = 0

        elif vertex[i][j] != max_value:
            results[0][i][j] = vertex[i][j]
        else:
            results[0][i][j] == max_value

log.debug("Display Results after init ")
for k in range(0,end):
    for j in reversed(range(1,num_vertex)):
        log.debug(f"Show k {k},j {j}")
        log_info =  [f"{results[k][i][j]:3}" for i in range(1,num_vertex)]
        log.debug(f"k={k}  j={j} {log_info}")
    log.debug(f"End -------- k{k} j{j}\n")


log.debug("Start Processing")

for k in range(1,end):
    log.debug(f"k={k}")
    for i in range(1,num_vertex):
        for j in range(1,num_vertex):
            value1 = results[k-1][i][j]

            if results[k-1][i][k] != max_value and results[k-1][k][j] != max_value:
                value2 = results[k-1][i][k]  + results[k-1][k][j]
                if value1 != max_value:
                    results[k][i][j] = min(value1, value2)
                else:
                    results[k][i][j] = value2
            else: 
                results[k][i][j] = value1

            log.debug(f"i,j = ({i},{j})  i/j {results[k-1][i][j]}  i/k {results[k-1][i][k]} k/j {results[k-1][k][j]}")
            log.debug(f"                 v1 {value1} v2 {value2} result: {results[k][i][j]}")
    log.debug("")
    for j in reversed(range(1,num_vertex)):
        for i in range(1,num_vertex):
            result = results[k][i][j]
            log.debug(f"     k={k}  j={j} result={result}")   
                
        debug_row = "".join([f"{results[k][i][j]:3} " for i in range(1,num_vertex)]);
        log.debug(f"k={k}  j={j} => {debug_row}")


print("\nFinal Matrix")
for k in range(0,end):
    print(f"Vertex #",[f"{i:3}" for i in range(1,num_vertex)])
    print("--------"*num_vertex,)
    for j in reversed(range(1,num_vertex)):
        print(f"k={k}  j={j}",  [f"{results[k][i][j]:3}" for i in range(1,num_vertex)])
    print("--------\n")



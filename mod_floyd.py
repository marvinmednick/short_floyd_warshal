#!/usr/bin/env python
import sys
import argparse
import re
import logging
import os


logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))
log = logging.getLogger("knap")
#log.setLevel(level)
log.info("Info enabled")
log.debug("Debug enabled")


#parser = argparse.ArgumentParser()
#parser.add_argument("file",type=argparse.FileType('r'))
#args = parser.parse_args()


#file1 = args.file
# read the first line
#line1 = file1.readline().strip()
#line1_values = re.match("(?P<size>\d+)\s+(?P<num_vertex>\d+)",line1)
#knapsack_size = int(line1_values.group('size'))+1
#num_vertex = int(line1_values.group('num_vertex'))

#log.info(f"size {num_vertex} {knapsack_size}")
#Lines = file1.readlines()

num_vertex=7+1
max_value = "MAX"
end=num_vertex

vertex = [[max_value for j in range(num_vertex)] for i in range(num_vertex)]
vertex[1][2] = 1
vertex[1][4] = 1
vertex[2][3] = 1
#vertex[2][5] = 7 
vertex[3][5] = 1
vertex[4][5] = 1
#vertex[6][7] = 1
#vertex[4][3] = 1
vertex[1][6] = 1
vertex[6][5] = 1
#vertex[7][5] = 1
#vertex[7][8] = 1
#vertex[8][5] = 1
vertex[4][6] = 1
vertex[6][7] = 1
vertex[7][5] = 1
vertex[6][1] = 1

log.info("VERTEX")
for j in reversed(range(1,num_vertex)):
    log_info = f"j={j}",  [f"{vertex[i][j]}" for i in range(1,num_vertex)]
    log.info(log_info)

log.info("")
#vertex_regex = re.compile("(?P<value>\d+)\s+(?P<weight>\d+)")
#count = 0
# Strips the newline character
#for line in Lines:
#    count += 1
#    m = vertex_regex.match(line.strip())
#    vertex.append({'id': count,  'value': int(m.group('value')), 'weight': int(m.group('weight'))})



#for v in vertex:
#    log.debug(v)

log.info("RESULTS")
results = [[[max_value for j in range(num_vertex)] for i in range(num_vertex)] for k in range(num_vertex)]

for i in range(1,num_vertex):
    for j in range(1,num_vertex):
        if i == j:
            results[0][i][j] = 0
        elif vertex[i][j] != max_value:
            results[0][i][j] = 1
        else:
            results[0][i][j] = 0

log.debug("START")
for k in range(0,end):
    for j in reversed(range(1,num_vertex)):
        log_info = f"k={k}  j={j}",  [f"{results[k][i][j]:3}" for i in range(1,num_vertex)]
        log.debug(log_info)
    log.debug("--------\n")


for k in range(1,end):
    log.debug(f"k={k}")
    for i in range(1,num_vertex):
        for j in range(1,num_vertex):
            value = results[k-1][i][j]  + results[k-1][i][k]  * results[k-1][k][j]
            results[k][i][j] = value
            log.debug(f"i,j = ({i},{j})  i/j {results[k-1][i][j]}  i/k {results[k-1][i][k]} k/j {results[k-1][k][j]} result: value")

    log.debug("")
    for j in reversed(range(1,num_vertex)):
        log_info = f"k={k}  j={j}",  [f"{results[k][i][j]:3}" for i in range(1,num_vertex)]
        log.debug(log_info)

index = "      i= "
for i in range(1,num_vertex):
    index += f"  {i:3}  "

print("\nFinal")
for k in range(0,end):
    for j in reversed(range(1,num_vertex)):
        print(f"k={k}  j={j}",  [f"{results[k][i][j]:3}" for i in range(1,num_vertex)])
    print(index,"\n")


exit()

for i in range(0,num_vertex):
    for x in range(0,knapsack_size):
        log.debug(f"i{i} x{x} w {vertex[i]['weight']}")

        if x >= 0 and i-1 >= 0:
            result1 = results[x][i-1] 
            if not results_valid[x][i-1]: log.critical(f"Result x{x} i-1{i-1} not yet set") 
        else:
            result1 = 0

        if x >= vertex[i]['weight']:
            x_index = x - vertex[i]['weight'] 
            result2 = results[x_index][i-1]+vertex[i]['value'] if i > 0 else vertex[i]['value']
            if i > 0 and not results_valid[x_index][i-1]: log.critical(f"Result  x-weight(i) {x_index} i {i-1} not yet set result={result2}")
        else:
            result2 = 0 
            

        log.debug(f"{i} {x} R1 {result1}, R2 {result2}")
        results[x][i] = max(result1,result2)
        results_valid[x][i] = True 
    log.debug(f"Result for i={i}")
    for j in reversed(range(0,knapsack_size)):
        loginfo = f"{j}",[f"{results[j][i]:.2f}" for i in range(num_vertex)]
        log.debug(loginfo)


#print("Final")
#for j in reversed(range(0,knapsack_size)):
#    print(f"{j}",[f"{results[j][i]:.2f}" for i in range(num_vertex)])


print(f"{results[knapsack_size-1][num_vertex-1]}")



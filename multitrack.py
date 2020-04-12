# this script should take an input folder of igc files and shift them to a common
# timestamp, so they can be uploaded to ayvri and viewed together
# by Tabor Henderson, released under GNU Public License
# Ayvri, please consider this my application for a role as an engineer

import os, shutil, math

def mapTimestringToTimestamp(ts):
    return [int(ts[0:2]), int(ts[2:4]), int(ts[4:6])]

def mapTimestampToString(ts):
    s = ""
    for v in ts:
        v_str = str(v)
        if len(v_str) == 1:
            v_str = "0" + v_str
        s = s + v_str
    return s

def timestampDiff(a, b):
    a_s = timestampToSecs(a)
    b_s = timestampToSecs(b)
    v =  a_s - b_s
    out = secsToTimestamp(v)
    return out

def timestampToSecs(ts):
    return ts[2] + ts[1]*60 + ts[0]*3600

def secsToTimestamp(s):
    # print(s)
    ts = [0, 0, 0] #HHMMSS
    ts[0] = int(math.floor(float(s)/3600)) % 24
    s = s - (ts[0]*3600) # remainder
    ts[1] = int(math.floor(float(s)/60)) % 60
    ts[2] = s - (ts[1]*60) # remainder
    # print(ts)
    return ts

# collect files - preserve alpha order! use list of strings to start
file_dir = os.getcwd() + "/files"
# set up output folder
out_dir = os.getcwd() + "/shifted"
if os.path.isdir(out_dir):
    # it already exists, delete it
    shutil.rmtree(out_dir)
# (re)create it
os.mkdir(out_dir)

for i, filename in enumerate(os.listdir(file_dir)):
    if filename != ".DS_Store":
        print("Timeshifting file: " + filename)
        with open(os.path.join(file_dir, filename), 'r') as f:
           lines = f.read().splitlines()
           lines[1] = "HFDTE010190" # author's birthday, buy him a present
           # shift timestamps
           first_line = lines[15]
           first_timestamp = mapTimestringToTimestamp(first_line[1:7])
           # add i to seconds ensure flights start in the expected order
           # first_timestamp[2] += i
           f_shifted = open(os.path.join(out_dir, str(i)+"_shifted.igc"), "w+")
           for l in lines:
               new_line = l
               if l[0] == "B" or l[0] == "F":
                   ts = mapTimestringToTimestamp(l[1:7])
                   # print(ts, first_timestamp)
                   shifted_time = timestampDiff(ts, first_timestamp)
                   # f_shifted.write(l[1:7] + ", " + mapTimestampToString(shifted_time) + "\n")
                   new_line = l[0] + mapTimestampToString(shifted_time) + l[7:]
               f_shifted.write(new_line + "\n")
           f_shifted.close()

# filename = "flattened/2020-02-16-XSD-GPB-01.igc"




# write files

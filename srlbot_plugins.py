import requests
import csv
import numpy as np

def R_index():
    # Making a GET request
    r = requests.get("https://space.fmi.fi/image/realtime/UT/NUR/NURdata_01.txt")

    data = r.content.decode().splitlines()
    x = list(csv.reader(data, delimiter = " "))
    x.reverse()

    Bdata = np.array([[val for val in row if val != ""] for row in x[:60]])[:,-3:].astype(float)

    R_index_1 = np.abs(Bdata[:29, 0]-Bdata[1:30, 0]) + np.abs(Bdata[:29, 1]-Bdata[1:30, 1]) + np.abs(Bdata[:29, 2]-Bdata[1:30, 2])
    R_index_2 = np.abs(Bdata[30:-1, 0]-Bdata[31:, 0]) + np.abs(Bdata[30:-1, 1]-Bdata[31:, 1]) + np.abs(Bdata[30:-1, 2]-Bdata[31:, 2])
    R_data = [np.sum(R_index_1), np.sum(R_index_2)]
    R_index = (R_data[0] + 2 * R_data[1])/3 /600 *1350 - 140
    
    return R_index
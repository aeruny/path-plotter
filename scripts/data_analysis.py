# This is where I will read simulation data and visualize it
import pandas as pd
import matplotlib.pyplot as plt


class SimData:
    def __init__(self):
        self.hostage_time = []
        self.drone_time = []
        self.dataset = pd.DataFrame()

    def read_data(self, data):
        data_list = [x.split(",") for x in data]
        data_list = self.clear_invalid_data(data_list)
        self.dataset = pd.DataFrame(data_list[1:])
        self.dataset.columns = data_list[0]

    def clear_invalid_data(self, data: list):
        output = []
        for row in data:
            if row[0] != "":
                output.append(row)
        return output

    def print_data(self):
        print(self.dataset)

    def print_dataset(self):
        print(self.dataset)


file_path = "../data/simulation_data.csv"

simData = SimData()
with open(file_path) as file:
    simData.read_data(file.readlines())
simData.print_dataset()

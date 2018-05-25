# -*- coding: utf-8 -*-

import sys
import csv

class Args(object):

    def __init__(self, args):
        self.args = args
    def __parse_arg(self, arg):
        try:
            argStr = self.args[self.args.index(arg)+1]
        except:
            argStr = None
        return argStr
    def get_arg(self, arg):
        argStr = self.__parse_arg(arg)
        if argStr is None:
            print("argument error")
        return argStr

class Config(object):
    
    def __init__(self, filename):
        self.JL, self.JH, self.rateSs = self.__parse_config(filename)
    def __parse_config(self, filename):
        JL = 0
        JH = 0
        rateSs = 0
        with open(filename) as f:
            for line in f:
                key, value = line.split("=")
                key = key.strip()
                try:
                    value = float(value.strip())
                except:
                    print ("config value error")
                if key == "JiShuL":
                    JL = value
                elif key == "JiShuH":
                    JH = value
                else:
                    rateSs += value
            
            return JL, JH, rateSs 

class UserData(object):
    
    def __init__(self, filename):
        self.data = self._read_users_data(filename)
    def _read_users_data(self, filename):
        data = []
        with open(filename) as f:
            for line in f:
                empeeId, income = line.split(",")
                try:
                    empeeInfo = (int(empeeId), int(income))
                except:
                    print("employee data error")
                data.append(empeeInfo)
        return data
    def __iter__(self):
        return iter(self.data)

class IncomeTaxCalculator(object):
    taxTable = [
        (80000, 0.45, 13505),
        (55000, 0.35, 5505),
        (35000, 0.3, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0),]

    def __init__(self, config):
        self.config = config
    def calculate(self, data_item):
        empeeId, income = data_item
        if income < self.config.JL:
            taxSs = self.config.JL * self.config.rateSs
        elif income > self.config.JH:
            taxSs = self.config.JH * self.config.rateSs
        else:
            taxSs = income * self.config.rateSs
         
        incomeDeSs = income - taxSs
        taxableIncome = incomeDeSs - 3500
        if taxableIncome < 0:
            tax = 0
        else:
            for item in self.taxTable:
                if taxableIncome > item[0]:
                    tax = taxableIncome * item[1] - item[2]
                    break
        incomeReal = incomeDeSs - tax
        return str(empeeId),str(income),"{:.2f}".format(taxSs),"{:.2f}".format(tax),"{:.2f}".format(incomeReal)

class Exporter:

    def __init__(self, filename):
        self.filename = filename
    def export(self, data):
        content = ""
        for item in data:
            line = ",".join(item) + "\n"
            content += line
        with open(self.filename, "w") as f:
            f.write(content)
            
if __name__ == "__main__":
    args = Args(sys.argv[1:])
    config = Config(args.get_arg("-c"))
    empeeData = UserData(args.get_arg("-d"))
    exporter = Exporter(args.get_arg("-o"))
    calculator = IncomeTaxCalculator(config)

    results = []
    for item in empeeData:
        result = calculator.calculate(item)
        results.append(result)
    exporter.export(results)

import csv

'''
=============================================
    TODO: Implement CSV saving capabilities
=============================================
'''
class SaveFile:

    def __init__(self):
        with open('telemetry.csv','w') as save_file:
            pass
    
    def save(self,data):
        with open('telemetry.csv','a') as save_file:
            saver= csv.writer(save_file, delimiter=",",
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for i in range(len(data[0])):
                row = []
                for el in data:
                    row.append(el[i])
                saver.writerow(row)        
    

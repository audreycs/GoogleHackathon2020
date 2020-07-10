import csv
import json

csvfile = open("./data_info.txt",'r',encoding='utf-8')
jsonfile = open("./data_info.js",'w',encoding='utf-8')

Virus = set()
HostProtein = set()
VirusProtein = set()
Drug = set()

fieldnames = ("head","relation","tail")
reader = csv.DictReader(csvfile,fieldnames)
for row in reader:
    if(row['relation'] == "type_is"):
        if(row['tail'] == "Virus"):
            Virus.add(row['head'])
        if(row['tail'] == "HostProtein"):
            HostProtein.add(row['head'])
        if(row['tail'] == "VirusProtein"):
            VirusProtein.add(row['head'])
        if(row['tail'] == "Drug"):
            Drug.add(row['head'])
csvfile.close()
Virus = list(Virus)
Virus.sort()
jsonfile.write("var Virus = ")
json.dump(Virus,jsonfile)
jsonfile.write(';\n\n')
HostProtein = list(HostProtein)
HostProtein.sort()
jsonfile.write("var HostProtein = ")
json.dump(HostProtein,jsonfile)
jsonfile.write(';\n\n')
VirusProtein = list(VirusProtein)
VirusProtein.sort()
jsonfile.write("var VirusProtein = ")
json.dump(VirusProtein,jsonfile)
jsonfile.write(';\n\n')
Drug = list(Drug)
Drug.sort()
jsonfile.write("var Drug = ")
json.dump(Drug,jsonfile)
jsonfile.write(';\n')
jsonfile.close()
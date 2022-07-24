import yaml
import csv

with open('probs.yaml', 'rb') as file:
    probs = yaml.load(file, yaml.Loader)

with open('report.txt', 'r') as report:
    strs = report.readlines()

strs = [i.split(' ') for i in strs]
strs = [i[1:len(i)-1] for i in strs]

classes = list()

for i in probs['classes']:
    for j in i:
        classes.append(j)

restrictions = ['тело', 'голова', 'глаза', 'губы']
classesClean = list()

for i in classes:
    if i not in restrictions:
        classesClean.append(i)

classes = classesClean

header = ['number']
for i in classes:
    header.append(i)

with open('report.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    counter = 0
    for i in strs:
        row = [counter]
        counter += 1
        for c in classes:
            value = 'Zero'
            for j in probs['classes']:
                for k in j:
                    if k == c:
                        for h in j[k]:
                            if h['name'] in i:
                                value = h['name']
            row.append(value)
        writer.writerow(row)

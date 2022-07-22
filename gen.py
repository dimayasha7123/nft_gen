from PIL import Image
import yaml
import os
from random import randint
import time


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def CheckAll(probsConfig, order, files):
    clss = list()
    for i in probsConfig['classes']:
        for j in i:
            for k in i[j]:
                clss.append(k['name'])
    nothingCount = clss.count('Nothing')
    for i in range(nothingCount):
        clss.remove('Nothing')
    files = list(map(lambda item: item[0:len(item)-4], files))
    
    print('Есть в конфиге, но нет файлов:', list(set(clss) - set(files)))
    print('Есть файл, но его нет в конфиге:', list(set(files) - set(clss)))
    
    print('Есть в основном конфиге, но нет в конфиге слоев:', list(set(clss) - set(order)))
    print('Есть в конфиге слоев, но нет в основном:', list(set(order) - set(clss)))


if __name__ == "__main__":

    with open('probs.yaml', 'rb') as file:
        probs = yaml.load(file, yaml.Loader)
    
    with open('order.yaml', 'rb') as file:
        orderMap = yaml.load(file, yaml.Loader)

    order = list()
    for i in orderMap['layers']:
        order.append((i['name'], i['order']))

    orderWithoutProbs = list(map(lambda item: item[0], order))

    export_path = r'./export/'
    output_path = r'./output/'


    fileList = os.listdir(export_path)

    CheckAll(probs, orderWithoutProbs, fileList)

    imageDict = dict()
    for file in fileList:
        imageDict[file[0:len(file)-4]] = Image.open(export_path + file)

    classes = list()
    for cl in probs['classes']:
        classes.append(list(cl.keys())[0])

    # проходимся по всем классам и считаем сумму вероятностей на класс
    sumProbsMap = dict()
    for i in probs['classes']:
        for j in i:
            sumProb = 0
            for k in i[j]:
                sumProb += k['prob']
            sumProbsMap[j] = sumProb
            # print(j, len(i[j]), sumProb)
    
    # идем по классам
    for t in range(10):
        newImageLayers = list()
        for i in probs['classes']:
            for j in i:
                gen_prob = randint(1, sumProbsMap[j])
                sum = 0
                for k in i[j]:
                    sum += k['prob']
                    if sum >= gen_prob:
                        newImageLayers.append(k['name'])
                        break
        
        nothingCount = newImageLayers.count('Nothing')
        for i in range(nothingCount):
            newImageLayers.remove('Nothing')
        
        newImageLayersWithPrior = list()
        
        for i in newImageLayers:
            if i in orderWithoutProbs:
                newImageLayersWithPrior.append((i, dict(order)[i]))

        newImageLayersWithPrior.sort(key = lambda i: i[1])
        newImageLayersWithPrior.reverse()

        sizeIm = Image.open(export_path + fileList[0])

        output = Image.new("RGBA", sizeIm.size)
        for l in newImageLayersWithPrior:
            lname = l[0]
            try:
                image = Image.open(export_path + lname + '.png')
            except:
                break
            output = Image.alpha_composite(output, image)

        output.save(output_path + str(time.time()) + '.png')

    # составляем новую генерацию пройдясь по циклам, добавляем картинки в список и сортим по порядку слоев, сливаем и так далее

    # l1 = Image.open("./export3/Баллончик-краски.png")
    # l2 = Image.open("./export3/Кисть-для-предмета.png")

    # output = Image.new("RGBA", l1.size)
    # output = Image.alpha_composite(output, l1)
    # output = Image.alpha_composite(output, l2)

    # output.save("./output/test1.png")
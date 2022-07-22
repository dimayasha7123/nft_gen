from PIL import Image
import yaml
import os


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def CheckAll(probsConfig, orderConfig, files):
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
    
    order = list()
    for i in orderConfig['layers']:
        order.append(i['name'])
    
    print('Есть в основном конфиге, но нет в конфиге слоев:', list(set(clss) - set(order)))
    print('Есть в конфиге слоев, но нет в основном:', list(set(order) - set(clss)))


if __name__ == "__main__":

    with open('probs.yaml', 'rb') as file:
        probs = yaml.load(file, yaml.Loader)
    
    with open('order.yaml', 'rb') as file:
        order = yaml.load(file, yaml.Loader)

    export_path = r'./export/'
    output_path = r'./output/'


    fileList = os.listdir(export_path)

    CheckAll(probs, order, fileList)

    imageDict = dict()
    for file in fileList:
        imageDict[file[0:len(file)-4]] = Image.open(export_path + file)

    classes = list()
    for cl in probs['classes']:
        classes.append(list(cl.keys())[0])

    # сделать функцию проверки соответствия конфига и файлов
    # составляем новую генерацию пройдясь по циклам, добавляем картинки в список и сортим по порядку слоев, сливаем и так далее

    # l1 = Image.open("./export3/Баллончик-краски.png")
    # l2 = Image.open("./export3/Кисть-для-предмета.png")

    # output = Image.new("RGBA", l1.size)
    # output = Image.alpha_composite(output, l1)
    # output = Image.alpha_composite(output, l2)

    # output.save("./output/test1.png")
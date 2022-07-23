from PIL import Image
import yaml
import os
from random import randint
import time


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

    print('Есть в основном конфиге, но нет в конфиге слоев:',
          list(set(clss) - set(order)))
    print('Есть в конфиге слоев, но нет в основном:',
          list(set(order) - set(clss)))


if __name__ == "__main__":
    start = time.time()

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

    # удаляем все из output
    filesToDelete = [f for f in os.listdir(output_path) if f.endswith(".png")]
    for f in filesToDelete:
        os.remove(os.path.join(output_path, f))

    print(f'Удалено {len(filesToDelete)} файлов')

    generated = list()
    constrObjectList = list(map(lambda x: x['object'], probs['constraints']))
    constrClassList = list(map(lambda x: x['class'], probs['constraints']))


    # сама генерация тонны картиночек
    countOfDoubles = 0
    countOfNotFound = 0
    t = 0
    while t < 100:
        newImageLayers = list()
        for i in probs['classes']:
            for j in i:
                if j in constrClassList and not constrObjectList[constrClassList.index(j)] in newImageLayers:
                    # осторожно
                    print(f'Ооо, я нашел ограничение для класса {j}')
                    continue
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

        # добавляем приоритет по слоям и сортим
        for i in newImageLayers:
            if i in orderWithoutProbs:
                newImageLayersWithPrior.append((i, dict(order)[i]))
            else:
                print(f'Приоритет для {i} не найден!')
                countOfNotFound+=1

        newImageLayersWithPrior.sort(key=lambda i: i[1])
        newImageLayersWithPrior.reverse()

        newImageLayersSorted = list()
        for l in newImageLayersWithPrior:
            newImageLayersSorted.append(l[0])

        if newImageLayersSorted in generated:
            print('Ооо нет, у нас уже есть такая картинка... Лааадно, сделаем новую')
            countOfDoubles += 1
            continue
        else:
            generated.append(newImageLayersSorted)

        output = Image.new("RGBA", Image.open(export_path + fileList[0]).size)
        for l in newImageLayersSorted:
            # скипаем, если не смогли найти нужную пнгху
            try:
                image = Image.open(export_path + l + '.png')
            except:
                print(f'Файл {l}.png не найден!')
                break
            output = Image.alpha_composite(output, image)

        output.save(output_path + str(t) + '.png')
        print(f'Сохранил картинку №{t}')
        t += 1

    print('Дубликатов:', countOfDoubles)
    print('Не найдено слоев (всего):', countOfNotFound)


    # вывод файла отчета по картинкам
    # по хорошему это вынести в отдельный конфиг
    restrictions = ['Тело', 'пришелец', 'ГЛАЗА-1', 'губы-1']

    with open('report.txt', 'w') as report:
        counter = 0
        for picData in generated:
            s = str(counter)
            counter += 1
            s += ': '
            for l in picData:
                if l in restrictions:
                    continue
                s += l
                s += ', '
            s = s[0: len(s) - 2]
            s += '\n'
            report.write(s)

    end = time.time()
    print("The time of execution of above program is:", end-start)
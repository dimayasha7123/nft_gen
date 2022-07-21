from sqlalchemy import true
import win32com.client as client
import yaml
import time

start = time.time()

app = client.GetActiveObject("Illustrator.Application")

doc = app.ActiveDocument

layers = doc.Layers

# config_data = dict()

# print(doc.Width, doc.Height)
# config_data["document_width"] = doc.Width
# config_data["document_height"] = doc.Height
# print(layers.Count)

png_export_options = client.Dispatch("Illustrator.ExportOptionsPNG24")
png_export_options.AntiAliasing = True
png_export_options.Transparency = True
png_export_options.ArtBoardClipping = True

# создание конфига с порядком слоев
orderList = list()
for i in range(1, layers.Count + 1):
    l = layers(i)
    orderList.append({'name': l.Name.replace(' ', '-'), 'order': i})
conf_data = {'layers': orderList}
with open(r'order.yaml', 'w') as file:
     outputs = yaml.dump(conf_data, file, allow_unicode=True)

# экспорт слоев в пнгшки
# layers_data = list()
# for i in range(1, layers.Count + 1):
#     l = layers(i)
#     l.Visible = False

# print("All layers unvisible")

# for i in range(1, layers.Count + 1):
#     l = layers(i)
#     l.Visible = True
#     # print(i, l.Name, l.Visible)
#     doc.Export(
#         ExportFile=r"C:\Users\dimya\OneDrive\Рабочий стол\seva_nft_gen\export3\{file_name}"
#         .format(file_name=l.Name),
#         ExportFormat=5,
#         Options=png_export_options
#     )
#     l.Visible = False
#     print(f"{i} Layer {l.Name} exported")

#     items = l.PathItems
#     min_x = 9999999
#     min_y = -9999999
#     for j in range (1, items.Count + 1):
#         item = items(j)
#         pos = item.Position
#         min_x = min(min_x, pos[0])
#         min_y = max(min_y, pos[1])

#     l_data = {"name": l.Name, "x": min_x, "y": -1 * min_y}
#     layers_data.append(l_data)

# config_data["layers"] = layers_data

# with open(r'config.yaml', 'w') as file:
#     outputs = yaml.dump(config_data, file, allow_unicode=True)


end = time.time()
print("The time of execution of above program is:", end-start)

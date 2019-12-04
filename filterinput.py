import numpy as np
from functools import reduce


def merge_lines(stack: dict, label: str, filename: str) -> str:
    x_float = list(map(lambda x: float(x), stack['x']))
    y_float = list(map(lambda y: float(y), stack['y']))
    width_float = list(map(lambda width: float(width), stack['width']))
    height_float = list(map(lambda height: float(), stack['height']))

    x_mean = reduce(lambda x1, x2: x1 + x2, x_float) / len(x_float)
    y_mean = reduce(lambda y1, y2: y1 + y2, y_float) / len(y_float)
    width_mean = reduce(lambda w1, w2: w1 + w2, width_float) / len(width_float)
    height_mean = reduce(lambda h1, h2: h1 + h2, height_float) / len(height_float)

    return filename + ',' + label + ',' + str(x_mean) + ',' + str(y_mean) + ',' + str(width_mean) + str(
        height_mean) + '\n'


def clear_stack(stack: dict):
    stack['x'].clear()
    stack['y'].clear()
    stack['width'].clear()
    stack['height'].clear()


def append_stack(stack, splitted):
    stack['x'].append(splitted[2])
    stack['y'].append(splitted[3])
    stack['width'].append(splitted[4])
    stack['height'].append(splitted[5])


def aggregateLabels():
    """
    Aggregiert die csv-Datei mit den Labeln.
    Die Trainingsdaten werden zusammengefasst.
    Für jedes Bild gibt es nun n=n1+n2 Zeilen in der csv,
    falls n1 Reiter und n2 Pferde gelabelt wurden.
    :return: csv mit reduzierter Anzahl an Zeilen
    """
    with open('rimondo_filtered.csv') as fp:
        output = ''
        threshold = 0.2
        line = fp.readline()
        fix_filename = line.split(',')[0]
        fix_label = line.split(',')[1]
        fix_x = line.split(',')[2]
        line = fp.readline()
        stack = {
            'x': [],
            'y': [],
            'width': [],
            'height': []
        }

        while line:
            splitted = line.split(',')
            label = splitted[1]
            x = splitted[2]
            if fix_label != label or get_norm(x, fix_x) > threshold:
                append_stack(stack, splitted)
                output += merge_lines(stack, fix_label, fix_filename)
                fix_x = x
                fix_label = label
                fix_filename = splitted[0]
                clear_stack(stack)
            else:
                append_stack(stack, splitted)

            line = fp.readline()
        return output


def get_norm(x, y):
    return np.linalg.norm(float(x) - float(y))


print(aggregateLabels())

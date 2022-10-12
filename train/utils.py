import numpy as np


def sequence_filter(source_queryset, destination_queryset):
    source_list = []
    destination_list = []
    for source_ in source_queryset:
        source_list.append(source_.sequence)

    for destination_ in destination_queryset:
        destination_list.append(destination_.sequence)

    arr_list = np.subtract(np.array(source_list),
                           np.array(destination_list)).tolist()
    seq_index = [arr_list.index(i) for i in arr_list if i < 0][0]

    return seq_index, source_list

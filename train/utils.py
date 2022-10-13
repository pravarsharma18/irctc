import numpy as np


def sequence_filter(source_queryset, destination_queryset):
    source_list = [source.sequence for source in source_queryset]
    destination_list = [
        destination.sequence for destination in destination_queryset]

    arr_list = np.subtract(np.array(source_list),
                           np.array(destination_list)).tolist()
    seq_index = [arr_list.index(i) for i in arr_list if i < 0][0]

    return seq_index, source_list

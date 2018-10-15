def merge_sort(array):
    if len(array) == 1:
        return array
    else:
        mid = int(len(array)/2)
        left_array = merge_sort(array[:mid])
        right_array = merge_sort(array[mid:])
        return merge(left_array, right_array)


def merge(left_array, right_array):
    merged = []
    i = j = 0
    left_array_length = len(left_array)
    right_array_length = len(right_array)
    while i < left_array_length or j < right_array_length:
        if left_array[i] < right_array[j]:
            merged.append(left_array[i])
            i += 1
        else:
            merged.append(right_array[j])
            j += 1
    while i < left_array_length:
        merged.append(left_array[i])
        i += 1
    while j < right_array_length:
        merged.append(right_array[j])
        j += 1
    return merged


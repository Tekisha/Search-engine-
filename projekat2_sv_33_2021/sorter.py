def quick_sort(sequence):
    lenght = len(sequence)

    if lenght<=1:
        return sequence
    else:
        pivot = sequence.pop()

    

    items_greater = []
    items_lower = []

    for item in sequence:
        if item[1]>pivot[1]:
            items_greater.append(item)
        else:
            items_lower.append(item)
    
    return quick_sort(items_greater)+[pivot]+quick_sort(items_lower)


if __name__=="__main__":
    print(quick_sort([2,0,5,3,10,2]))
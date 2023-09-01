intList = []
try:
    count = 0
    while(count < 5):
        intList.insert(count,int(input(str(count + 1) + "つ目の数字を入力")))
        count+=1
except ValueError:
    print("Invalid input! Please enter only integer values.")

sortedList = []
for num in range(len(intList)):
    print("num is " + str(num))
    if(num == 0):
        sortedList.append(intList[0])
    else:
        val = intList[num]
        inserted = False
        for index in range(len(sortedList)):
            print("index is " + str(index))
            if sortedList[index] >= val:
                sortedList.insert(index , val)
                inserted = True
                break
        if not inserted:
            sortedList.append(val)
print(sortedList)



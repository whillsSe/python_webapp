import json
isExited = False
inputList = []
while(not isExited):
    inputedVal = input("文字列を入力してください('exit'で終了)")
    if(inputedVal != "exit"):
        inputList.append(inputedVal)
    else:
        break
inputList.sort()
with open('./output/python_basis_02_02.txt',mode='w',encoding='utf-8') as f:
    f.write(json.dumps(inputList))
    f.close

countDict = dict()
with open('./output/python_basis_02_02.txt',mode='r',encoding='utf-8') as f:
    loadedList = json.load(f)
    print(loadedList)
    for val in loadedList:
        if(val in countDict):
            countDict[val] += 1
        else:
            print(val + "is not contained!")
            countDict[val] = 1
    f.close
def inverse_lookup(d,x):
    keys = []
    for k,v in d.items():
        if(x == v):
            keys.append(k)
    return keys
maxCount = sorted(countDict.values(),reverse=True)[0]
famousWords = inverse_lookup(countDict,maxCount)
print(famousWords)

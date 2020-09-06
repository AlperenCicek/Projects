import cv2
import numpy as np
from random import seed
from random import randint

class ImageCompressing:
    def __init__(self, data, typ):
        self.data = data
        self.type = typ
        self.head = None
        self.process()

    def process(self):
        print("Data: ")
        print(self.data)
        if self.type == 'c':
            convertedArray = self.convertingWordToArray(self.data)
        elif self.type == 'i':
            convertedArray = self.convertingArrayToOneDimension(self.data)
        print("Converted Values: ")
        print(convertedArray)
        sameValues = self.gettingSameValues(convertedArray)
        print("Same Values: ")
        print(sameValues)
        orderedValues = self.orderingArray2D(sameValues)
        print("Ordered Values: ")
        print(orderedValues)
        self.convertingArraysToNodes(orderedValues)
        self.huffmanRecursive(self.head)
        self.printPreorder(self.head)

    def convertingWordToArray(self, word):
        tempArray = []
        for value in word:
            tempArray.append(str(value))
        return np.array(tempArray)

    def convertingArrayToOneDimension(self, array):
        temp = np.zeros(array.size, dtype = int)
        tempIndex = 0
        for col in array:
            for num in col:
                temp[tempIndex] = num
                tempIndex = tempIndex + 1
        return temp

    def gettingSameValues(self, array):
        currentIndex = 0
        tempArray = []
        tempArrayNumber = []
        isItAvailiableInArray = False
        for value in array:
            currentIndex = 0
            for element in tempArray:
                if value != element:
                    isItAvailiableInArray = False
                    currentIndex = currentIndex + 1
                else:
                    isItAvailiableInArray = True
                    break
            if isItAvailiableInArray:
                tempArrayNumber[currentIndex] = tempArrayNumber[currentIndex] + 1
            else:
                tempArray.append(value)
                tempArrayNumber.append(int(1))
        tempArray = np.vstack((tempArray, tempArrayNumber))
        return tempArray

    def orderingArray2D(self, array):
        for i in range(0, len(array[1]) - 1): 
            min = i 
            for j in range(i + 1, len(array[1])): 
                if array[1][min] > array[1][j]: 
                    min = j 
                       
            array[0][i], array[0][min] = array[0][min], array[0][i]
            array[1][i], array[1][min] = array[1][min], array[1][i]
        return array

    def convertingArraysToNodes(self, array):
        for row0 in array[0]:
            newNode = Node(data = "(" + str(row0) + ")")
            if self.head == None:
                self.head = newNode
            else:
                head = self.head
                while head.next is not None:
                    head = head.next
                newNode.prev = head
                head.next = newNode
        head = self.head
        for row1 in array[1]:
            head.weight = int(row1)
            if head.next != None:
                head = head.next
    
    def huffmanRecursive(self, root):
        if root != None and root.next == None:
            while root.head:
                root = root.head
            self.head = root
        else:
            newNode = Node(data = ("{ " + str(root.data) + " And " + str(root.next.data) + " }"), weight = (int(root.weight) + int(root.next.weight)))
            if root.weight <= root.next.weight:
                newNode.left = root
                newNode.right = root.next
            else:
                newNode.right = root
                newNode.left = root.next
            newNode.left.head = newNode
            newNode.right.head = newNode
            newNode.left.bit = str (0)
            newNode.right.bit = str (1)
            while newNode.weight >= root.weight:
                if root.next != None:
                    root = root.next
                else:                        
                    break
            root.prev.next = newNode
            newNode.next = root
            newNode.prev = newNode.prev
            root.prev = newNode
            self.head.next.next.prev = None
            tempRoot = self.head.next.next
            self.head.next.next = None
            self.head.next.prev = None
            self.head.next = None
            self.head = tempRoot
            newNode.left.next = None
            newNode.left.prev = None
            newNode.right.next = None
            newNode.right.prev = None
            self.huffmanRecursive(self.head)

    def printPreorder(self, root):
        f = open("text.bin", "a+")
        if root:
            print("Node: ", root.data)
            print("Bit: ", root.bit)
            f.write(f.read() + str(root.bit))
            f.close()
            if root.left != None:
                root.left.bit = str(root.bit) + str(root.left.bit)
                self.printPreorder(root.left)
            if root.right != None:
                root.right.bit = str(root.bit) + str(root.right.bit)
                self.printPreorder(root.right)

    def printNodes(self):
        head = self.head
        while head.next != None:
            print(head.data)
            print(head.next.data)
            if(head.prev is not None):
                print(head.prev.data)
            print("********")
            head = head.next

class Node:
    def __init__(self, data = None, weight = None):
        self.data = data
        self.weight = weight
        self.head = None
        self.next = None
        self.prev = None
        self.left = None
        self.right = None
        self.bit = ""

numbers1 = np.array(([1, 3, 4, 2, 5], [1, 4, 3, 2, 3], [2, 2, 1, 4, 2], [3, 1, 3, 4, 5], [5, 5, 1, 3, 4]), dtype= int)
numbers2 = np.array(([1,5,4,3,2], [1, 2, 1, 4, 1], [1, 2, 5, 3, 4]))

image = np.ones((10,10))
for i in range(10):
    image[i][i] = randint(1, 5)

img = cv2.imread('image.jpg', 0)
imageArray = np.array(img)
def compress(bottomIndex, increase, imageArray):
    tempArray = []
    asd = 0
    for i in range(bottomIndex, imageArray[1].size, increase):
        for j in range(imageArray[0].size):
            tempArray.append(imageArray[j][i : i + increase])
            ImageCompressing(np.array(tempArray), 'i')
            tempArray.clear()
            asd = asd + 1
    print(asd)
#ImageCompressing(numbers1, 'i')
print(imageArray[1].size)
compress(0, 10, imageArray)


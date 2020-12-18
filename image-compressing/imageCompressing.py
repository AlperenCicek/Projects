import cv2
import numpy as np

class ImageCompressing:
    def __init__(self, imageName):
        self.imageName = imageName
        self.data = None
        self.head = None
        self.orderedValues = None
        self.convertedArray = None
        self.process()

    def process(self):
        img = cv2.imread(self.imageName, 0)
        self.data = np.array(img)
        print("Data: ")
        print(self.data)
        self.convertedArray = self.convertingArrayToOneDimension(self.data)
        print("Converted Values: ")
        print(self.convertedArray)
        sameValues = self.gettingSameValues(self.convertedArray)
        print("Same Values: ")
        print(sameValues)
        self.orderedValues = self.orderingArray2D(sameValues)
        print("Ordered Values: ")
        print(self.orderedValues)
        self.convertingArraysToNodes(self.orderedValues)
        self.huffmanRecursive(self.head)
        #self.printPreorder(self.head)

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
            max = i 
            for j in range(i + 1, len(array[1])): 
                if array[1][max] < array[1][j]: 
                    max = j 
                       
            array[0][i], array[0][max] = array[0][max], array[0][i]
            array[1][i], array[1][max] = array[1][max], array[1][i]
        tempArray = [[], []]
        for i in range(10, 0, -1):
            tempArray[0].append(array[0][i])
            tempArray[1].append(array[1][i])
        return tempArray

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
            if root.left != None:
                root.left.bit = str(root.bit) + str(root.left.bit)
                self.printPreorder(root.left)
            if root.right != None:
                root.right.bit = str(root.bit) + str(root.right.bit)
                self.printPreorder(root.right)
            if (root.left and root.right) == None:
                f.write(f.read() + str(root.data) + ":" + str(root.bit))
                f.close()

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
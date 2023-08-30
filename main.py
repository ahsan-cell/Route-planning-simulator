import numpy as np
import tkinter as tk
from tkinter import messagebox
import math
import heapq
import copy as cp
array=np.empty(shape=(60,60))
sourceI=None
sourceJ=None
destinationI=None
destinationJ=None
row,col=array.shape
array.fill(0)
roads=[]
import random

class MyGUI:
    
    bloclSize=12
    insertingRoads=False
    insertingLowTraffic=False
    insertingHighTraffic=False
    insertingSource=False
    insertingDestination=False
    alreadyInsertingSomething=False
    
    def __init__(self,root):
        self.root=root
        root.geometry("1280x720")
        root.title("Route Planning Simulation")
        self.leftFrame=tk.Frame(root)
        self.leftFrame.pack(side=tk.LEFT)
        self.rightFrame=tk.Frame(root)
        self.rightFrame.pack(side=tk.LEFT,padx=20,pady=20)

        self.canvas=tk.Canvas(self.leftFrame,width=720,height=720,bg='white')
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>",self.canvasClick)
        self.canvas.bind("<Button-1>",self.canvasClick)
        
        self.insertRoadsButton=tk.Button(self.rightFrame,text="Insert Roads",padx=10,pady=10,command=self.pressedInsertRoads,background='white')
        self.insertRoadsButton.grid(row=0,column=0,sticky=tk.W+tk.E,padx=10,pady=10)

        self.insertLowTrafficButton=tk.Button(self.rightFrame,text="Insert Low traffic",padx=10,pady=10,command=self.pressedInsertLowTrffic,background='white')
        self.insertLowTrafficButton.grid(row=1,column=0,sticky=tk.W+tk.E,padx=10,pady=10)

        self.insertHighTrafficButton=tk.Button(self.rightFrame,text="Insert High traffic",padx=10,pady=10,background='white',command=self.pressedInsertHighTrffic)
        self.insertHighTrafficButton.grid(row=2,column=0,sticky=tk.W+tk.E,padx=10,pady=10)

        self.insertSourceButton=tk.Button(self.rightFrame,text="Insert Source",padx=10,pady=10,background='white',command=self.pressedInsertSource)
        self.insertSourceButton.grid(row=3,column=0,sticky=tk.W+tk.E,padx=10,pady=10)

        self.insertDestinationButton=tk.Button(self.rightFrame,text="Insert Destination",padx=10,pady=10,background='white',command=self.pressedInsertDestnation)
        self.insertDestinationButton.grid(row=4,column=0,sticky=tk.W+tk.E,padx=10,pady=10)

        self.startButton=tk.Button(self.rightFrame,text="START",padx=10,pady=10,background='white',command=self.pressedStartButton)
        self.startButton.grid(row=5,column=0,sticky=tk.W+tk.E,padx=10,pady=10)



    def pressedInsertRoads(self):
        #print(self.alreadyInsertingSomething,self.insertingRoads,self.insertingLowTraffic)
        if not self.insertingRoads and not self.alreadyInsertingSomething:
            self.insertRoadsButton.configure(relief=tk.SUNKEN,background='red')
            self.insertingRoads=True
            self.alreadyInsertingSomething=True
        elif self.insertingRoads and self.alreadyInsertingSomething:
            self.insertRoadsButton.configure(relief=tk.RAISED,background='white')
            self.insertingRoads=False
            self.alreadyInsertingSomething=False

    def pressedInsertLowTrffic(self):
        #print(self.alreadyInsertingSomething,self.insertingRoads,self.insertingLowTraffic)
        if not self.insertingLowTraffic and not self.alreadyInsertingSomething:
            self.insertLowTrafficButton.configure(relief=tk.SUNKEN,background='red')
            self.insertingLowTraffic=True
            self.alreadyInsertingSomething=True
        elif self.insertingLowTraffic and self.alreadyInsertingSomething:
            self.insertLowTrafficButton.configure(relief=tk.RAISED,background='white')
            self.insertingLowTraffic=False
            self.alreadyInsertingSomething=False

    def pressedInsertHighTrffic(self):
        #print(self.alreadyInsertingSomething,self.insertingRoads,self.insertingLowTraffic)
        if not self.insertingHighTraffic and not self.alreadyInsertingSomething:
            self.insertHighTrafficButton.configure(relief=tk.SUNKEN,background='red')
            self.insertingHighTraffic=True
            self.alreadyInsertingSomething=True
        elif self.insertingHighTraffic and self.alreadyInsertingSomething:
            self.insertHighTrafficButton.configure(relief=tk.RAISED,background='white')
            self.insertingHighTraffic=False
            self.alreadyInsertingSomething=False
    
    def pressedInsertSource(self):
        #print(self.alreadyInsertingSomething,self.insertingRoads,self.insertingLowTraffic)
        if not self.insertingSource and not self.alreadyInsertingSomething:
            self.insertSourceButton.configure(relief=tk.SUNKEN,background='red')
            self.insertingSource=True
            #self.alreadyInsertingSomething=True
    
    def pressedInsertDestnation(self):
        #print(self.alreadyInsertingSomething,self.insertingRoads,self.insertingLowTraffic)
        if not self.insertingDestination and not self.alreadyInsertingSomething:
            self.insertDestinationButton.configure(relief=tk.SUNKEN,background='red')
            self.insertingDestination=True
            #self.alreadyInsertingSomething=True
    
    def pressedStartButton(self):
        if sourceI!=None and destinationI!=None:
            self.insertRoadsButton.configure(state=tk.DISABLED)
            self.insertDestinationButton.configure(state=tk.DISABLED)
            self.insertSourceButton.configure(state=tk.DISABLED)
            self.insertHighTrafficButton.configure(state=tk.DISABLED)
            self.insertLowTrafficButton.configure(state=tk.DISABLED)
            self.showCanvas(array)
            # for i in range(60):
            #     print(array[i])
            des=A_STAR()
            self.tracePath(des)
            # print(sourceI)
            # print(sourceJ)
            # print(destinationI)
            # print(destinationJ)
            # print(roads)
            
           
        else:
            messagebox.showinfo('invalid input','Insert source and destination')
           

    
    def showEmptySpace(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='grey',activeoutline='white')

    
    def canvasClick(self,event):
        i=int(event.x/12)
        j=int(event.y/12)
        if self.insertingRoads:
            if array[j,i]==0 or array[j,i]==2 or array[j,i]==4:
                array[j,i]=1
                # print(array)
                roads.append([j,i,1])
        elif self.insertingLowTraffic:
            if array[j,i]==1 or array[j,i]==4:
                array[j,i]=2
                roads.append([j,i,2])
        elif self.insertingHighTraffic:
            if array[j,i]==1 or array[j,i]==2:
                array[j,i]=4
                roads.append([j,i,4])
        elif self.insertingSource:
            array[j,i]=-1
            global sourceI,sourceJ
            sourceI=j
            sourceJ=i
            self.insertSourceButton.configure(relief=tk.RAISED,background='white',state=tk.DISABLED)
            self.insertingSource=False
        elif self.insertingDestination:
            array[j,i]=-2
            global destinationI,destinationJ
            destinationI=j
            destinationJ=i
            self.insertDestinationButton.configure(relief=tk.RAISED,background='white',state=tk.DISABLED)
            self.insertingDestination=False
        # print(i," ",j)
        # print(event)
        self.showCanvas(array,changedi=i,changedj=j)

    def tracePath(self,destinationNode):
        # print("path: ")
        if destinationNode==None:
            return None
        destinationNode=destinationNode.parentNode
        while destinationNode.i!=sourceI or destinationNode.j!=sourceJ:
            # print(destinationNode.i,destinationNode.j)
            array[destinationNode.i,destinationNode.j]=8
            self.showPath(destinationNode.j,destinationNode.i)
            destinationNode=destinationNode.parentNode
           
    def showRoads(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='black',activeoutline='white')

    def showLowTraffic(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='black',activeoutline='white')
        self.canvas.create_rectangle(x+2,y+2,x+self.bloclSize-2,y+self.bloclSize-2,fill='#c7807b',activeoutline='white')
    
    def showHighTraffic(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='black',activeoutline='white')
        self.canvas.create_rectangle(x+2,y+2,x+self.bloclSize-1,y+self.bloclSize-1,fill='#d63e33',activeoutline='white')
    
    def showSource(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='yellow',activeoutline='white')
        self.canvas.create_text(x+self.bloclSize/2,y+self.bloclSize/2,text='S',fill='black',font=('Arial 9 bold'))

    def showDestination(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y,x+self.bloclSize,y+self.bloclSize,fill='yellow',activeoutline='white')
        self.canvas.create_text(x+self.bloclSize/2,y+self.bloclSize/2,text='D',fill='black',font=('Arial 9 bold'))
    
    def showPath(self,x,y):
        x=x*self.bloclSize
        y=y*self.bloclSize
        self.canvas.create_rectangle(x,y+2,x+self.bloclSize,y+self.bloclSize-2,fill='yellow',activeoutline='white')

    
    def showCanvas(self,matrix,changedi=None,changedj=None):
        if changedi == None and changedj==None:
            self.canvas.delete("all")
            row,col=matrix.shape
            for i in range(row):
                for j in range(col):
                    if matrix[j,i]==0:
                        self.showEmptySpace(i,j)
                    elif matrix[j,i]==1:
                        self.showRoads(i,j)
                        #print("fahja",i,j)
                    elif matrix[j,i]==2:
                        self.showLowTraffic(i,j)
                    elif matrix[j,i]==4:
                        self.showHighTraffic(i,j)
                    elif matrix[j,i]==-1:
                        self.showSource(i,j)
                    elif matrix[j,i]==-2:
                        self.showDestination(i,j)
        else:
            if matrix[changedj,changedi]==0:
                self.showEmptySpace(changedi,changedj)
            elif matrix[changedj,changedi]==1:
                self.showRoads(changedi,changedj)
                #print("changed")
            elif matrix[changedj,changedi]==2:
                self.showLowTraffic(changedi,changedj)
            elif matrix[changedj,changedi]==4:
                self.showHighTraffic(changedi,changedj)
            elif matrix[changedj,changedi]==-1:
                self.showSource(changedi,changedj)
            elif matrix[changedj,changedi]==-2:
                self.showDestination(changedi,changedj)
           


class node:
    i=None
    j=None
    parentNode=None
    f=None
    g=None
    def __init__(self,i,j,parentNode=None) -> None:
        self.i=i
        self.j=j
        self.parentNode=cp.copy(parentNode)

    def computeF(self,g):
         self.g=g
         self.f=self.g+math.dist((self.i,self.j),(destinationI,destinationJ))
         return self.f
    
    def __lt__(self,next):
        return self.f<next.f

def canMove(i,j):
    if i<row and i>=0 and j<col and j>=0 and array[i,j]!=0 and array[i,j]!=-3:
        return True
    else:
        return False


def A_STAR():
    openedList=[]
    closedList=[]
    costSoFar=0
    sourceNode=node(sourceI,sourceJ,None)
    sourceNode.g=0
    heapq.heappush(openedList,sourceNode)
    destinationReached=False
    destinationNode=None

    while len(openedList)!=0:

        current=heapq.heappop(openedList)
        costSoFar=current.g
        if current.i==destinationI and current.j==destinationJ:
            # print('destination found and cost: ',costSoFar)
            destinationReached=True
            destinationNode=current
            break
        # print("i,j= ",current.i,current.j)
       
        closedList.append(current)
        array[current.i,current.j]=-3#-3 means visited

        #move north
        if canMove(current.i-1,current.j):
            x=node(current.i-1,current.j,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        #move south
        if canMove(current.i+1,current.j):
            x=node(current.i+1,current.j,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        #move east
        if canMove(current.i,current.j+1):
            x=node(current.i,current.j+1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)

        # move west
        if canMove(current.i,current.j-1):
            x=node(current.i,current.j-1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        # move noth west
        if canMove(current.i-1,current.j-1):
            x=node(current.i-1,current.j-1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        # move north east
        if canMove(current.i-1,current.j+1):
            x=node(current.i-1,current.j+1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        # move south east
        if canMove(current.i+1,current.j+1):
            x=node(current.i+1,current.j+1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
        
        # move south west
        if canMove(current.i+1,current.j-1):
            x=node(current.i+1,current.j-1,current)
            if array[x.i,x.j]==-2:#compensating the -2 weight of destination which is used for forntend
                x.computeF(costSoFar+1)
            else:    
                x.computeF(costSoFar+array[x.i,x.j])
            heapq.heappush(openedList,x)
    if not destinationReached:
        messagebox.showinfo('info','Cannot reach destination')
        return None
    else:
        # x=destinationNode
        # print("path: ")
        # while x.i!=sourceI and x.j!=sourceJ:
        #     print(x.i,x.j)
        #     array[x.i,x.j]=8
        #     x=x.parentNode
        return destinationNode
    





class GA:
    populationSize=15
    population=[]
    def __init__(self):
        upperChromosomeSize=len(roads)
        lowerChromosomeSize=int(math.dist((sourceI,sourceJ),(destinationI,destinationJ)))
        for i in range(self.populationSize):
            chromosomeSize=random.unifrom(lowerChromosomeSize,upperChromosomeSize)
            chromosome=[]

            addedRoads={}
            randomRoad=random.uniform(0,len(roads))
            addedRoads.add(randomRoad)
            chromosome.add(randomRoad)
            for j in range(chromosomeSize-1):
                randomRoad=random.uniform(0,len(roads))
                if randomRoad not in addedRoads:
                    chromosome.add(randomRoad)
                    addedRoads.add(randomRoad)
            self.population.add(chromosome)
    # print(population)
                    
                





        
root=tk.Tk()
g=MyGUI(root)
g.showCanvas(array)

root.mainloop()



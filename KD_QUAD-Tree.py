import numpy
import os
import time
import math
import kdtree
import csv
from termcolor import colored,cprint
from operator import itemgetter
import sys
import scipy
from scipy.spatial.distance import cdist, squareform
import timeit
from functools import wraps
import random
from random import uniform
from scipy.spatial import distance
import itertools
import collections
from collections import Counter
import weakref

class QuadNode:
    def __init__(self, nechild, nwchild , swchild , sechild, depth,qdata=0,data=0,data2=0,):
        self.data = data
        self.data2=data2
        self.qdata=qdata
        self.ne = nechild
        self.nw = nwchild
        self.sw = swchild
        self.se = sechild
        self.depth = depth

class Tree2():
    def __init__(self):
        self.root = 0
        self.dim = 0

    def create_root2(self,data,r):
        global a,dim,type;
        depth = 0
        if len(data) == 1:
            ne=0
            nw=0
            se=0
            sw=0
            qdata=0
        else:
         temp=self.calc_average(data)
         ne=temp[0]
         se=temp[1]
         nw=temp[2]
         sw=temp[3]
         qdata=temp[4]
        self.root = QuadNode(ne,nw,sw,se ,depth,qdata)
        depth = depth +1
        self.create_tree2(self.root, depth)

    def create_tree2(self, node, depth):
        global a,dim,check1,check2,check3,check4,data;
        self.dim = dim-1
        check1="n"
        check2="n"
        check3="n"
        check4="n"
        if node.nw:
            newdata = node.nw
            check1 = "nw"
            self.child2(depth,newdata,node)
        if node.ne:
            newdata = node.ne
            check2 = "ne"
            self.child2(depth, newdata, node)
        if node.sw:
            newdata = node.sw
            check3 = "sw"
            self.child2(depth, newdata, node)
        if node.se :
            newdata = node.se
            check4 = "se"
            self.child2(depth,newdata,node)

    def child2(self,depth,newdata,node):
            global el,a,data,dim,check1,check2,check3,check4;
            ne = list()
            se = list()
            nw = list()
            sw = list()
            qdata=list()

            if len(newdata) > 1:
               temp=self.calc_average(newdata)
               ne = temp[0]
               se = temp[1]
               nw = temp[2]
               sw = temp[3]
               qdata=temp[4]

            elif len(newdata) == 1:
             ne=0
             nw=0
             se=0
             sw=0
             qdata=newdata
            # print (newdata)
            #print (qdata)
            if check1 == "nw":
                if len(newdata) == 1:
                        x = list()
                        #for i in range(el):
                        if qdata[0][0] == newdata[0][0] and qdata[0][1]==newdata[0][1]: #make [[]] to []
                                x.append(newdata[0][0])
                                x.append(newdata[0][1])
                        qdata = x
                        #print (qdata)
                        node.nw = QuadNode(ne, nw, sw, se, depth,0,qdata)
                else:
                  node.nw = QuadNode( ne,nw,sw,se, depth,qdata)
                self.create_tree2(node.nw, depth + 1)
            if check2 == "ne":
                if len(newdata) == 1:
                    x = list()
                    #for i in range(el):
                    if qdata[0][0] == newdata[0][0] and qdata[0][1] == newdata[0][1]:
                        x.append(newdata[0][0])
                        x.append(newdata[0][1])
                    qdata = x
                    node.ne = QuadNode (ne, nw, sw, se, depth,0,qdata)
                else:
                 node.ne = QuadNode( ne, nw, sw, se, depth,qdata)
                self.create_tree2(node.ne, depth + 1)
            if check3 == "sw":
                if len(newdata)==1:
                    x = list()
                    #for i in range(el):
                    if qdata[0][0] == newdata[0][0] and qdata[0][1] == newdata[0][1]:
                        x.append(newdata[0][0])
                        x.append(newdata[0][1])
                    qdata = x
                    node.sw = QuadNode( ne, nw, sw, se, depth,0,qdata)
                else:
                 node.sw = QuadNode( ne, nw, sw, se, depth,qdata)
                self.create_tree2(node.sw, depth + 1)
            if check4 == "se":
                if len(newdata)==1:
                    x = list()
                    #for i in range(el):
                    if qdata[0][0] == newdata[0][0] and qdata[0][1] == newdata[0][1]:
                        x.append(newdata[0][0])
                        x.append(newdata[0][1])
                    qdata = x
                    node.se = QuadNode( ne, nw, sw, se, depth,0,qdata)
                else:
                 node.se = QuadNode(ne, nw, sw, se, depth,qdata)
                self.create_tree2(node.se, depth + 1)

    def insert(self, insert, node=0):
       global data,a;
       if not node:
            node = self.root
       if node.nw or node.ne or node.se or node.sw:
        if insert[0] < node.qdata[0] and insert[1] < node.qdata[1] : #compare
            if not node.sw : # if smaller create lchild node if lchild node does not exist
                node.sw =QuadNode(0,0,0,0, node.depth+1,0,insert)
                return 1
            else:
                return self.insert(insert, node.sw)
        elif insert[0] < node.qdata[0] and insert[1] > node.qdata[1] :
            if not node.nw :
                node.nw = QuadNode(0,0,0,0, node.depth+1,0,insert)
                return 1
            else:
                return self.insert(insert, node.nw)
        elif insert[0] > node.qdata[0] and insert[1] < node.qdata[1] : #compare
            if not node.se:
                node.se = QuadNode(0,0,0,0, node.depth+1,0,insert)
                return 1
            else:
                return self.insert(insert, node.se)
        elif insert[0] >= node.qdata[0] and insert[1] >= node.qdata[1]:  # compare
                if not node.ne:
                    node.ne = QuadNode(0,0,0,0, node.depth+1,0,insert)
                    return 1
                else:
                    return self.insert(insert, node.ne)
       else:
          if  node.data2 == 0:
              node.data2 = insert
              return 1
          else:
              x=list()
              x.append(node.data)
              x.append(node.data2)
              x.append(insert)
              temp = self.calc_average(x)
              node.data2 = 0
              ne = temp[0]
              se = temp[1]
              nw = temp[2]
              sw = temp[3]
              qdata = temp[4]
              node.data=0
              node.qdata=qdata
              #print("ne", ne, "\nnw", nw, "\nsw", sw, "\nse", se, "\nnode",qdata, "\n")
              if ne:
               if len(ne)==1:
                node.ne = QuadNode(0, 0, 0, 0, node.depth + 1,0,ne[0])
               else:
                   for i in range(len(ne)-1 ):
                       node.ne = QuadNode( 0, 0, 0, 0, node.depth + 1,0,ne[i])
                       self.insert(ne[i + 1], node.ne)
              if nw:
                  if len(nw) == 1:
                      node.nw = QuadNode(0, 0, 0, 0, node.depth + 1,0,nw[0])
                  else:
                      for i in range(len(nw)-1):
                          node.nw = QuadNode( 0, 0, 0, 0, node.depth + 1,0,nw[i])
                          self.insert(nw[i + 1], node.nw)
              if sw:
                  if len(sw) == 1:
                      node.sw = QuadNode( 0, 0, 0, 0, node.depth + 1,0,sw[0])
                  else:
                      for i in range(len(sw)-1):
                          node.sw = QuadNode( 0, 0, 0, 0, node.depth + 1,0,sw[i])
                          self.insert(sw[i + 1], node.sw)
              if se:
                  if len(se) == 1:
                      node.se = QuadNode( 0, 0, 0, 0, node.depth + 1,0,se[0])
                  else:
                      for i in range(len(se)-1):
                          node.se = QuadNode(0, 0, 0, 0, node.depth + 1,0,se[i] )
                          self.insert(se[i + 1], node.se)
              return 1

    def delete(self, delete, node=0, prevnode=0,c="n"):
        global dim,data;
        check= 0
        check2=0
        if not node:
            node = self.root
        if node.data:
         for i in range(dim):
           #print (node.data[i], delete[i])
           if (node.data[i] - delete[i])!=0:
             check=0
             break
           else:
             check= 1
        if node.data2!=0:
         for i in range(dim):
                #print (node.data2[i], delete[i])
                if (node.data2[i] - delete[i])!=0:
                   check2=0
                   break
                else:
                  check2= 1
        if check == 1 or check2==1: #delete leaf
                if c == "ne":
                 if check==1:
                   if node.data2!=0:
                     node.data=node.data2
                     node.data2=0
                   else:
                       prevnode.ne = 0
                 else:
                     node.data2=0
                elif c=="nw":
                    if check == 1:
                        if node.data2!=0:
                            node.data = node.data2
                            node.data2 = 0
                        else:
                            prevnode.nw = 0
                    else:
                        node.data2 = 0
                elif c=="se":
                    if check == 1:
                        if node.data2!=0:
                            node.data = node.data2
                            node.data2 = 0
                        else:
                            prevnode.se = 0
                    else:
                        node.data2 = 0
                elif c=="sw":
                    if check == 1:
                        if node.data2!=0:
                            node.data = node.data2
                            node.data2 = 0
                        else:
                            prevnode.sw = 0
                    else:
                        node.data2 = 0
                return 1

        elif node.data2!=0:
           if node.data2[0] < delete[0] and node.data2[1] < delete[1]:
            if not node.ne:
                return 0
            return self.delete(delete, node.ne, node,"ne")
           elif node.data2[0] < delete[0] and node.data2[1] > delete[1]:
            if not node.se:
                return 0
            return self.delete(delete, node.se, node, "se")
           elif node.data2[0] > delete[0] and node.data2[1] < delete[1]:
            if not node.nw:
                return 0
            return self.delete(delete, node.nw, node, "nw")
           elif node.data2[0] > delete[0] and node.data2[1] > delete[1]:
            if not node.sw:
                return 0
            return self.delete(delete, node.sw, node, "sw")


        elif node.qdata[0] < delete[0] and node.qdata[1] < delete[1] :
            if not node.ne:
               return 0
            return self.delete(delete, node.ne, node, "ne")
        elif node.qdata[0] < delete[0] and node.qdata[1] > delete[1] :
           if not node.se:
               return 0
           return self.delete(delete, node.se, node, "se")
        elif node.qdata[0] > delete[0] and node.qdata[1] < delete[1] :
           if not node.nw:
              return 0
           return self.delete(delete, node.nw, node, "nw")
        elif node.qdata[0] > delete[0] and node.qdata[1] > delete[1] :
          if not node.sw:
            return 0
          return self.delete(delete, node.sw, node, "sw")

    def point_search(self, exact, node=0):
        global data;
        if not node:
            node = self.root
        if node.data2:
            if node.data2 == exact:
                return 1
            elif node.data:
              if node.data == exact:
                return 1
        elif node.data:
            if node.data == exact:
                return 1
        elif exact[0] <= node.qdata[0] and exact[1] <= node.qdata[1] : #compare
            if not node.sw:
                return 0
            return self.point_search(exact, node.sw)
        elif exact[0] < node.qdata[0] and exact[1] > node.qdata[1] : #compare
            if not node.nw:
                return 0
            return self.point_search(exact, node.nw)
        elif exact[0] > node.qdata[0] and exact[1] < node.qdata[1] : #compare
            if not node.se:
                return 0
            return self.point_search(exact, node.se)
        elif exact[0] > node.qdata[0] and exact[1] > node.qdata[1] : #compare
            if not node.ne:
                return 0
            return self.point_search(exact, node.ne)

    def range_search(self, ranges, res, node=0):
       global data;
       if not node :
            node = self.root
       #print (node.qdata)
       if node.nw or node.ne or node.se or node.sw:
        #print (node.qdata[0],node.qdata[1])
        #print (ranges[1][0], ranges[1])
        if node.qdata[0] >= ranges[0][0] and node.qdata[0] <= ranges[1][0] and node.qdata[1] >= ranges[0][1] and node.qdata[1] <= ranges[1][1] :
            if node.qdata == 0:
                res.append(node.data)
                if node.data2:
                  res.append(node.data2)
            if node.sw :
                res = self.range_search(ranges, res, node.sw)
            if node.nw :
                res = self.range_search(ranges, res, node.nw)
            if node.se :
                res = self.range_search(ranges, res, node.se)
            if node.ne :
                res = self.range_search(ranges, res, node.ne)
        #elif node.qdata[0] > ranges[0][0] and node.qdata[0] < ranges[1][0] and node.qdata[1] < ranges[1][1] and node.qdata[1] > ranges[0][1] :
        else:
            if node.sw :
              res = self.range_search(ranges, res, node.sw)
        #elif node.qdata[0] > ranges[0][0] and node.qdata[1] < ranges[1][1]:
            if node.nw:
               res = self.range_search(ranges, res, node.nw)
        #elif node.qdata[0] < ranges[1][0] and node.qdata[1] > ranges[0][1]:
            if node.se:
               res = self.range_search(ranges, res, node.se)
        #elif node.qdata[0] < ranges[1][0] and node.qdata[1] < ranges[1][1]:
            if node.ne :
             res = self.range_search(ranges, res, node.ne)
       else: #we are at leafs
           #print (node.data)
           check=0
           if node.data[0] >= ranges[0][0] and node.data[0] <= ranges[1][0] and node.data[1] >= ranges[0][1] and \
                   node.data[1] <= ranges[1][1]:
               #check = 0
                if node.qdata == 0:
                   res.append(node.data)
                   #if node.data2:
                    #   res.append(node.data2)


           if node.data2:
            if node.data2[0] >= ranges[0][0] and node.data2[0] <= ranges[1][0] and node.data2[1] >= ranges[0][1] and \
                   node.data2[1] <= ranges[1][1]:
               #check=0
                if node.qdata == 0:
                   res.append(node.data2)
                   #if node.data2:
                    #   res.append(node.data2)

       return res

    def dist(self,x, y):
        return numpy.sqrt(numpy.nansum((x - y) ** 2))

    def kNN(self, kNN, k,dst,l,node=0):
         global data,el,depth,a;
         if not node:
             node = self.root
         if node.data:
           tempdata =numpy.array(node.data)
           tempkNN=numpy.array(kNN)
           dst.append(self.dist(tempdata, tempkNN ))
           l.append(node.data)
         if node.data2:
             tempdata = numpy.array(node.data2)
             tempkNN = numpy.array(kNN)
             dst.append(self.dist(tempdata, tempkNN))
             l.append(node.data2)
         if node.nw:
          self.kNN(kNN,k,dst, l,node.nw)
         if node.ne:
          self.kNN(kNN,k,dst, l,node.ne)
         if node.sw:
          self.kNN(kNN,k,dst, l,node.sw)
         if node.se:
          self.kNN(kNN, k, dst, l,node.se)

         dst,l = zip(*sorted(zip(dst,l)))
         l=l[:k]
         #print(dst,x)
         return l

    def visual2(self):
        global data, tree1, dim, vtree, new, tree, type,tree2;
        tree2.visual_tree2()
        input("Press Enter to continue...\n")
        main_menu(tree2)

    def visual_tree2(self, node=0):
        if not node:
            node = self.root
            print("root", node.data)
        if node.nw:
            print("nw", node.nw.data)
            if node.nw.data2!=0:
             print ("nw2", node.nw.data2)
            self.visual_tree2(node.nw)
        if node.ne:
            print("ne", node.ne.data)
            if node.ne.data2!=0:
             print ("ne2", node.ne.data2)
            self.visual_tree2(node.ne)
        if node.sw:
            print("sw", node.sw.data)
            if node.sw.data2!=0:
             print ("sw2", node.sw.data2)
            self.visual_tree2(node.sw)
        if node.se:
            print("se", node.se.data)
            if node.se.data2!=0:
             print ("se2", node.se.data2)
            self.visual_tree2(node.se)

    def size2(self,x,node=0):
        global treesize;
        treesize= x
        if not node:
             node = self.root
             x = x + sys.getsizeof(node)
             self.size2(x, node)
        if node.nw:
            x = x + sys.getsizeof(node.nw)
            self.size2(x,node.nw)
        if node.ne:
            x = x + sys.getsizeof(node.ne)
            self.size2(x,node.ne)
        if node.sw:
            x = x + sys.getsizeof(node.sw)
            self.size2(x,node.sw)
        if node.se:
            x = x + sys.getsizeof(node.se)
            self.size2(x,node.se)
        return treesize

    def calc_average(self, data):
        # print (data)
        ne = []
        se = []
        nw = []
        sw = []
        qdata = []
        x = 0
        y = 0
        for i in range(len(data)):
            x = x + data[i][0]
            y = y + data[i][1]
        x = x / len(data)
        x=float(round(x, 5))
        y = y / len(data)
        y=float(round(y, 5))
        #print(x,y)
        for i in range(len(data)):
            if data[i][0] >= x and data[i][1] >= y:
                ne.append(data[i])
            elif data[i][0] >= x and data[i][1] <= y:
                se.append(data[i])
            elif data[i][0] <= x and data[i][1] >= y:
                nw.append(data[i])
            elif data[i][0] <= x and data[i][1] <= y:
                sw.append(data[i])
        qdata.append(x)
        qdata.append(y)
        return ne, se, nw, sw, qdata

'''-------------------------------------------------------------'''

class Node:
    def __init__(self, axis, data, lchild, rchild, depth):
        global dim,type;
        self.axis = axis
        self.data = data
        self.lchild = lchild
        self.rchild = rchild
        self.depth = depth

class Tree:
    def __init__(self):
        self.root = 0
        self.dim = 0

    def create_root(self,data,r):
        global a,dim,type;
        #print (data)
        a = len(data[0])  # assumes all nodes have the same dimension
        axis = r
        depth = 0
        if len(data) == 1:
            left  = 0
            right = 0
            median = 0
        else:
            data.sort(key=itemgetter(axis)) #sort by axis by x or by y or by z etc.
            median =float(len(data)) / 2
            if len(data) % 2 != 0:
             median = int(median - 0.5)
            else:
             median = int(median)
        if median == 0:
            left = 0
            right = data[median+1:]
        elif median == len(data) - 1:
            left = data[:median]
            right = 0
        else:
         left = data[: median]
         right = data[median+1:]
        self.root = Node(axis, data[median], left, right, depth)
        depth = depth +1
        self.create_tree(self.root, depth)

    def create_tree(self, node, depth):
        global a,dim,rcheck,lcheck,data;
        self.dim = dim-1
        rcheck ="n"
        lcheck="n"
        if node.lchild:
            newdata = node.lchild
            lcheck = "l"
            self.child(depth,newdata,node)
        if node.rchild :
            newdata = node.rchild
            rcheck = "r"
            self.child(depth,newdata,node)

    def child(self,depth,newdata,node):
            global a, dim;
            axis = depth % a
            if len(newdata) > 1:
                newdata.sort(key=itemgetter(axis))
                median = float(len(newdata)) / 2
                if len(newdata) % 2 != 0:
                    median = int(median - 0.5)
                else:
                    median = int(median)
                if median == 0:
                    lchild = 0
                    rchild = newdata[median+1:]
                elif median == len(newdata)-1:
                    lchild = newdata[:median]
                    rchild = 0
                else:
                    lchild = newdata[:median]
                    rchild = newdata[median+1:]
            elif len(newdata) == 1:
             lchild = 0
             rchild = 0
             median = 0
            if lcheck == "l":
             node.lchild = Node(axis, newdata[median], lchild, rchild, depth)
             self.create_tree(node.lchild, depth + 1)
            if rcheck == "r":
             node.rchild = Node(axis, newdata[median], lchild, rchild, depth)
             self.create_tree(node.rchild, depth + 1)

    def insert(self, insert, node=0):
        global data,a;
        if not node:
            node = self.root
        axis= node.depth % a
        if insert[axis] < node.data[axis]  : #compare
            if not node.lchild : # if smaller create lchild node if lchild node does not exist
                node.lchild = Node(axis, insert, 0, 0, node.depth + 1)
                return 1
            else:
                return self.insert(insert, node.lchild)
        elif insert[axis] >= node.data[axis]:
            if not node.rchild : #if bigger create rchild node if rchild node does not exist
                node.rchild = Node(axis, insert, 0, 0, node.depth + 1)
                return 1
            else:
                return self.insert(insert, node.rchild)

    def delete(self, delete, node=0, prevnode=0,c="c"):
        global dim, data,tempmax;
        check= 0
        if not node:
            node = self.root
        axis = node.axis
        for i in range(dim):
         if (node.data[i] - delete[i])!=0:
            check=0
            break
         else:
            check= 1
        if check == 1:
                if node.rchild:
                    node.data = node.rchild.data  #replace
                    return self.delete(node.data, node.rchild, node,"r") #delete leaf which is double
                elif node.lchild:
                    tempmax=self.maxvalue(node.lchild, axis)
                    node.data = self.maxvalue(node.lchild, axis) #replace with max of left subtree
                    return self.delete(node.data, node.lchild, node, "l")  # delete leaf which is double
                else: #delete leaf
                 if c == "l":
                   prevnode.lchild = 0
                 elif c == "r":
                   prevnode.rchild = 0
                return 1
        elif node.data[axis] > delete[axis]:
            if not node.lchild:
                if tempmax:
                 return self.delete(delete, node.rchild, node, "r")
                else:
                 return 0
            return self.delete(delete, node.lchild, node,"l")
        elif node.data[axis] <= delete[axis]:
            #print (node.data)
            if not node.rchild:
                if tempmax:
                 return self.delete(delete, node.lchild, node, "l")
                else:
                 return 0
            return self.delete(delete, node.rchild, node,"r")

    def maxvalue(self, node, axis):  # max of left subtree
        x = list()
        if node.lchild:
            x.append(node.lchild)
        if node.rchild:
            x.append(node.rchild)
        max = node.data[axis]
        maxnode = node
        while len(x) > 0:
            if x[0].lchild:
                x.append(x[0].lchild)
            if x[0].rchild:
                x.append(x[0].rchild)
            if x[0].data[axis] > max:
                max = x[0].data[axis]
                maxnode = x[0]
            x.remove(x[0])
        return maxnode.data

    def point_search(self, exact, node=0):
        global data;
        if not node:
            node = self.root
        axis = node.axis
        if node.data[axis] > exact[axis]:
            if not node.lchild:
                return 0
            return self.point_search(exact, node.lchild)
        elif node.data[axis] < exact[axis]:
            if not node.rchild:
                return 0
            return self.point_search(exact, node.rchild)
        elif node.data == exact:
            return 1
        elif node.data[axis] == exact[axis]:
            if not node.rchild :
                return 0
            return self.point_search(exact, node.rchild)

    def range_search(self, ranges, res, node=0):
        global data;
        if not node :
            node = self.root
        axis = node.axis
        if node.data[axis] >= ranges[0][axis] and node.data[axis] <= ranges[1][axis] :
            check = 0
            for i in range(len(ranges[0])):
                if ranges[0][i] <= node.data[i]  and ranges[1][i] >= node.data[i] :
                    check += 1
            if check == self.dim + 1:
                res.append(node.data)
            if node.lchild :
                res = self.range_search(ranges, res, node.lchild)
            if node.rchild :
                res = self.range_search(ranges, res, node.rchild)
        elif node.data[axis] > ranges[1][axis]:
            if node.lchild :
                res = self.range_search(ranges, res, node.lchild)
        elif node.data[axis] <= ranges[0][axis]:
            if node.rchild :
                res = self.range_search(ranges, res, node.rchild)
        return res

    def dist(self,x, y):
        return numpy.sqrt(numpy.nansum((x - y) ** 2))

    def kNN(self, kNN, k,dst,l,node=0):
         global data,el,depth,a;
         if not node:
             node = self.root
         tempdata =numpy.array(node.data)
         tempkNN=numpy.array(kNN)
         dst.append(self.dist(tempdata, tempkNN ))
         l.append(node.data)
         if node.lchild:
          self.kNN(kNN,k,dst, l,node.lchild)
         if node.rchild:
             self.kNN(kNN, k, dst, l,node.rchild)
         dst,l = zip(*sorted(zip(dst,l)))
         l=l[:k]
         return l

    def visual(self):
        global  data, dim, vtree, new, tree, type, newtree;
        print(colored("\n----------------------------\nV I S U A L\n----------------------------", "red"))
        kdtree.visualize(vtree)
        input("Press Enter to continue...\n")
        tree.visual_tree()
        input("Press Enter to continue...\n")
        main_menu(tree)

    def visual_tree(self,node=0):
     if not node:
        node = self.root
        print("root", node.data)
     if node.lchild:
        print("left", node.lchild.data)
        self.visual_tree(node.lchild)
     if node.rchild:
        print("right", node.rchild.data)
        self.visual_tree(node.rchild)

    def size(self,x,node=0):
        global treesize;
        treesize= x
        if not node:
             node = self.root
             x = x + sys.getsizeof(node)
             self.size(x, node)
        if node.lchild:
            x = x + sys.getsizeof(node.lchild)
            self.size(x,node.lchild)
        if node.rchild:
            x = x + sys.getsizeof(node.rchild)
            self.size(x,node.rchild)
        return treesize

'''-------------------------------------------------------------'''

def read_file(filename, dim, el):
    global data;
    data = []
    try:
        f = open(filename, "r")
        for i in range(el):
            x = f.readline()
            x = x[:-1]
            x = x.split(" -")
            tp = []
            for j in range(dim):
                tp.append(float(x[j]))
            data.append(tp)
        f.close()
        #print (data)
        return data
    except IOError:
        print("Wrong input, can't open {}.".format(filename))
        exit(0)
    except ValueError:
        print("Wrong input\n")
        run()

def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def file_dim(filename):
  with open(filename) as f:
    reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
    first_row = next(reader)
    num_cols = len(first_row)-1
    return num_cols

def type_of_tree():
    global type,tree,dim;
    type = 0
    try:
     while type != 1 and type != 2:
        type = int(input("\nAvailable options : \nChoose 1 for K-D Tree\nChoose 2 for Quad Tree\n"))

    except ValueError:
      print("Wrong input\n")
      type_of_tree()

def run():
    global el,dim,type,vtree,type,new,tree,tree2,treesize;
    try:
        option = int(input("\nWhat you want to do? \nChoose 1 for Default file\nChoose 2 to Insert file\n"))
    except ValueError:
        print("Wrong input\n")
        run()
    if option == 1:
        filename = ("data.txt")
        el = file_len(filename)
        dim = file_dim(filename)
        data = read_file(filename, dim, el)
    elif option == 2:
      filename = input("Enter a filepath : ")
      while (os.path.exists(filename) == False):
          print("Wrong Path \n")
          filename= input('Enter a filepath : ')
      el = file_len(filename)
      dim = file_dim(filename)
      data = read_file(filename, dim, el)

    else:
        print ("Wrong input\n")
        run()
    type_of_tree()
    print("\nPleae wait while the tree is being created ...")
    if type == 2:
        i = 0
        tree2 = Tree2()
        timer = time.time()
        tree2.create_root2(data, i)
    else:
       i=0
       tree = Tree()
       timer = time.time()
       tree.create_root(data, i)
    print ("Done!")
    print(time.time() - timer, colored('seconds to create the tree with',"red"),len(data),colored(' elements.',"red"))
    if type ==1:
      print("\nSize of tree is : ", tree.size(0))
    else:
      print("\nSize of tree is : ", tree2.size2(0))
    vtree = kdtree.create(data,dim)
    input("\nPress Enter to continue...\n")
    if type ==2:
      main_menu(tree2)
    else :
      main_menu(tree)

def main_menu(tree):
    global el,data,vtree,dim,type;
    if type == 1:
     try:
        print(colored("\n----------------------------\nMAIN MENU       K-D TREE\n----------------------------\n","grey"
                     ,attrs=["bold","dark" ]))
        option = int(input(colored("Available options :\n Choose 1 for Insertion\n Choose 2 for Deletion"
                           "\n Choose 3 for Point Search\n Choose 4 for Range Search\n Choose 5 for Find KNN\n"
                           " Choose 6 for Visualitation of the K-D Tree\n Choose 7 to Go Back\n"
                            " Choose 8 to Exit\n",attrs=["bold" ])))

     except ValueError:
        print("Wrong input")
        main_menu(tree)
    else:
        try:
            print(colored("\n----------------------------\nMAIN MENU    QUAD TREE\n----------------------------\n", "grey"
                         ,attrs=["bold", "dark"]))
            option = int(input(colored("Available options :\n Choose 1 for Insertion\n Choose 2 for Deletion"
                           "\n Choose 3 for Point Search\n Choose 4 for Range Search\n Choose 5 for Find KNN\n"
                           " Choose 6 for Visualitation of the K-D Tree\n Choose 7 to Go Back\n"
                            " Choose 8 to Exit\n",attrs=["bold" ])))

        except ValueError:
            print("Wrong input")
            main_menu(tree)

    if option == 1: #Insert
            insert = []
            for i in range(tree.dim + 1):
                try:
                    insert.append(float(input("Dimension {} to insert : ".format(i + 1))))
                except ValueError:
                    print("Wrong input")
                    main_menu(tree)
            timer = time.time()
            data.append(insert)
            if tree.insert(insert):
                print(time.time() - timer, colored('seconds for insertion.', "red"))
                print(colored("\nInserted successfully", "red"))
                el = el + 1
                vtree.add(insert)
            else:
                print("Wrong input, can't insert element")
            input("Press Enter to continue...\n")
            main_menu(tree)

    elif option == 2: #Delete
        delete = []
        for i in range(tree.dim + 1):
            try:
                delete.append(float(input("Dimension {} to delete : ".format(i + 1))))
            except ValueError:
                print("Wrong input")
                main_menu(tree)
        x = 0
        for i in range(el): # check if exists
            if delete == data[i]:
                x = 1
        if x == 1:
           timer = time.time()
           if tree.delete(delete):
            data.remove(delete)
            print(time.time() - timer, colored('seconds for deletion', "red"))
            print(colored("\nElement deleted", "red"))
            el = el-1
            vtree.remove(delete)
        else:
            print(colored("\nElement not in the K-D Tree", "red"))
        input("Press Enter to continue...\n")
        main_menu(tree)

    elif option == 3:  #Exact search
        element = []
        for i in range(tree.dim + 1):
            try:
                element.append(float(input("Dimension {} : ".format(i + 1))))
            except ValueError:
                print("Wrong input")
                main_menu(tree)
        timer = time.time()
        if tree.point_search(element):
            print(colored("Element found","red"))
        else:
            print (colored("\nElement not in the tree","red"))
        print(time.time() - timer, colored('seconds for point search.',"red"))
        input("Press Enter to continue...\n")
        main_menu(tree)

    elif option == 4: #Range search
        min_element = []
        max_element = []
        for i in range(tree.dim + 1):
            try:
                min_element.append(float(input("Dimension {} min : ".format(i + 1))))
            except ValueError:
                print("Wrong input")
                main_menu(tree)
        for i in range(tree.dim + 1):
            try:
                max_element.append(float(input("Dimension {} max : ".format(i + 1))))
            except ValueError:
                print("Wrong input")
                main_menu(tree)
        timer = time.time()
        res = tree.range_search([min_element, max_element], [])
        print(colored("\nFound","red"), len(res),colored("elements in that range","red"))
        print(colored("Elements", attrs=["bold"]))
        print( time.time() - timer, colored('seconds for range search.','red'))
        columns = int(math.ceil(len(res) / el))
        for i in range(min(el, len(res))):
            for j in range(columns):
                next_column_i = i + el * j
                if next_column_i < len(res):
                    print(res[next_column_i], end =" " )
            print()
        input("Press Enter to continue...\n")
        main_menu(tree)

    elif option == 5: #KNN
        dim_kNN = []
        for i in range(tree.dim + 1):
            try:
                dim_kNN.append(float(input("Dimension {} to find kNN : ".format(i + 1))))
            except ValueError:
                print("Wrong input")
                main_menu(tree)
        try:
            k = int(input("Number of neighbors : \n"))
        except ValueError:
            print("Wrong input")
            main_menu(tree)
        dst=list()
        l=list()
        timer = time.time()
        kNN = tree.kNN(dim_kNN, k,dst,l)
        rows = k
        columns = int(math.ceil(len(kNN) / rows))
        for i in range(min(rows, len(kNN))):
            for j in range(columns):
                next_column_i = i + rows * j
                if next_column_i < len(kNN):
                    print(kNN[next_column_i],end =" " )
            print()
        print(colored("\nFound ","red"),k ,colored("NN in","red"), time.time() - timer, colored("second","red"))
        input("Press Enter to continue...\n")
        main_menu(tree)

    elif option == 6:
        if type==1:
           tree.visual()
        else:
           tree.visual2()

    elif option == 7:
        run()

    elif option == 8 or option == exit:
        exit(0)

    else:
        main_menu(tree)

'''-------------------------------------------------------------'''
run()

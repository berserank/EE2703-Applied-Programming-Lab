
#         EE2703 Applied Programming Lab 
#         Assignment 2
#         Aditya Nanda Kishore
#         EE20B062  

from sys import argv, exit
import numpy as np


CIRCUIT = '.circuit\n'
END = '.end'
END1 = '.end\n'
AC = '.ac'
ac_flag = 0 #This becomes 1 if it's an AC Circuit

if len(argv) != 2:
    print("Invalid Input. Please enter 2 arguments") 
    exit()
try:
    f = open(argv[1])
    lines = f.readlines()
    f.close()
    start = 0
    try :
        while(lines[start] != CIRCUIT):
            start = start+1
    except:
        print("Please Verify your .netlist file again, There is no .circuit ")
        exit(0) #This places start at the index of .circuit
    end = start
    try:
        while(lines[end] != END and lines[end] != END1):
            end = end+1
    except:
        print("Please Verify your .netlist file again.There is no .end")
        exit(0) #This places end at the index of .end
    ac = end
    try:
        while(lines[ac][0:3] != AC):
            ac += 1
        
        ac_flag = 1

    except:
        pass

except IOError:
    print('Invalid file')
    exit()

#this function converts and returns the strings of any form to float
def numerise(a) :
    if ( a.isdigit() == True ):
        return float(a)
    else :
        return (float(a.split('e')[0]))* (10**(float(a.split('e')[1]))) #returns integer values for exponentials
#Defining Classes for Every Element Possible in the circuit
freq = 1
if (ac_flag == 1):
    freq = numerise(lines[ac].split()[2])

#Voltage Source
class voltage_source :
    def __init__(self, a) :
        words = a.split()
        self.name = words[0]
        self.begin = words[1]
        self.end = words[2]
        if (ac_flag == 1):
            self.val = complex( (numerise(words[4])* (np.cos(numerise(words[5]))))/2 , (numerise(words[4])* (np.sin(numerise(words[5]))))/2 )
        else:
            self.val = complex(numerise(words[3]),0)

#Current Source
class current_source :
    def __init__(self,a) :
        words = a.split()
        self.name = words[0]
        self.begin = words[1]
        self.end = words[2]
        if (ac_flag == 1):
            self.val = complex( (numerise(words[4])* (np.cos(numerise(words[5]))))/2 , (numerise(words[4])* (np.sin(numerise(words[5]))))/2 )
        else:
            self.val = complex(numerise(words[3]),0)


#Resistor
class resistor :
    def __init__(self, a) :
        words = a.split()
        self.name = words[0]
        self.begin = words[1]
        self.end =  words[2]
        self.val = complex(numerise(words[3]),0)

#Inductor
class inductor :
    def __init__(self, a) :
        words = a.split()
        self.name = words[0]
        self.begin = words[1]
        self.end =  words[2]
        self.val = complex(0, 2*freq*np.pi*numerise(words[3]))

#Capacitor
class capacitor :
    def __init__(self, a) :
        words = a.split()
        self.name = words[0]
        self.begin = words[1]
        self.end =  words[2]
        self.val = complex(0, -1/(2*np.pi*freq*numerise(words[3])))

Elements = {}
#Solving the Circuit
#This for loop adds every element separately to the dictionary created above
no_of_voltage_sources = 0
for line in lines[start+1:end]:
    if (line[0] == 'R'):
        R = resistor(line)
        Elements[R.name] = [R.begin, R.end, R.val]
    elif (line[0] == 'V'):
        V = voltage_source(line)
        Elements[V.name] = [V.begin, V.end, V.val]
        no_of_voltage_sources += 1
    elif (line[0] == 'I'):
        I = current_source(line)
        Elements[I.name] = [I.begin, I.end, I.val]
    elif (line[0] == 'C'):
        C = capacitor(line)
        Elements[C.name] = [C.begin, C.end, C.val]
    elif (line[0] == 'L'):
        L = inductor(line)
        Elements[L.name] = [L.begin, L.end, L.val]

    
#print(Elements)

node_set = {''}
for element in Elements.keys() :
    node_set.add(Elements[element][0])
    node_set.add(Elements[element][1])
#print(node_set)
node_set.remove('')
node_set = list(node_set)#This is our final set of all nodes
no_of_variables = len(node_set)+no_of_voltage_sources# This is going to be the order of our Conductance Matrix in MNA


A = np.zeros((no_of_variables, no_of_variables), dtype = complex)#Matrix of coefficients of variables
B = np.zeros((no_of_variables, 1), dtype = complex)#Matrix of Sources

#Defining the iterating variables that keeps changing throughout the matrix
row_pos = 0
column_pos = 0
keys = list(Elements.keys())#Set of Nodes
voltage_sources = []
for element in keys:
    if(element[0] == 'V'):
        voltage_sources.append(element)
iterator = 0

"""

Adding values to the matrix
I started with building each row in A at once
So for that I need to take a node from node set. We have two cases here, If it's GND and If it's not

If it's not GND, check for the elements that have that particular node 
as a from node / a to node. 

If It's a resistor/capacitor/inductor we have to iterate column position to index of that node in node_set 
and subtract the admittance of resistor/capacitor/inductor in that position.

If It's a voltage source, we have two things to do:
  1.Writing KCL at the node, by taking current through V1 as our variable. For that we can look for 
  index of voltage source in set of voltage sources and set column position to (no_of_ nodes)+ index and 
  iterate the value to 1 if it's a from node/ -1 if it's a to node.Meanwhile B[row position] would be zero.

  2.Writing the (Voltage at "to node" - Voltage at "from node") = V. For this we have to iterate row position to 
  (no_of_ nodes)+ index and set column position to indices of those particular nodes and appropriately we use 1,-1 
  as cooefficients.We have to revert the value row position after this.Meanwhile B[row position] would be the value of 
  voltage source.

If it's a Current Source, We have to amend B Matrix only.We can add The value of current source at the current row
position in B if it's a to node and subtract if it's a from node.


Now If it's GND
I have to iterate row and column position to the index of GND in node_Set and change the value to -1.
B[row] would be zero


After building A and B, I have to multiply all diagonal elements in conductance matrix with -1 to make them positive.
I made them all negative to make the code simpler.

"""
for node in node_set:
    if (node != 'GND'):
        for element in Elements:
            if ((element[0] == 'R' or element[0] == 'C' or element[0] == 'L') and ((Elements[element][0] == node or Elements[element][1] == node))):
                column_pos = node_set.index(Elements[element][1])
                A[row_pos, column_pos] -= (1/Elements[element][2])
                column_pos = node_set.index(Elements[element][0])
                A[row_pos, column_pos] -= (1/Elements[element][2])
                B[row_pos,0] = 0
            elif ((element[0] == 'V') and ((Elements[element][0] == node or Elements[element][1] == node))):
                B[row_pos,0] = 0
                column_pos = no_of_variables - no_of_voltage_sources + voltage_sources.index(element)
                if ( Elements[element][0] == node ) :
                    A[row_pos, column_pos] = 1
                else :
                    A[row_pos,column_pos]  = -1      
                temp_val = row_pos
                row_pos = ((no_of_variables - no_of_voltage_sources))+ voltage_sources.index(element)
                if ( Elements[element][0] == node ) :
                    column_pos = node_set.index(Elements[element][0])
                    A[row_pos,column_pos] = 1
                    column_pos = node_set.index(Elements[element][1])
                    A[row_pos,column_pos] = -1
                else :
                    column_pos = node_set.index(Elements[element][0])
                    A[row_pos,column_pos] = -1
                    column_pos = node_set.index(Elements[element][1])
                    A[row_pos,column_pos] = 1
                B[row_pos,0] = Elements[element][2]
                row_pos = temp_val              
            elif ((element[0] == 'I') and ((Elements[element][0] == node or Elements[element][1] == node))):
                if (Elements[element][0] == node) :
                    temp = node_set.index(Elements[element][0])
                    B[temp] -= Elements[element][2]
                else:
                    temp = node_set.index(Elements[element][1])
                    B[temp] += Elements[element][2]
            
        row_pos += 1
        column_pos = 0     
    elif (node == 'GND'):
        A[row_pos,row_pos] = -1
        B[row_pos,0] = 0
        row_pos += 1
        column_pos = 0 

for i in range(no_of_variables):
    A[i,i] = A[i,i] * (-1)
#print(A)
#print(B)        
#Solving the matrix
x = np.linalg.solve(A, B)
#print(x)
#Printing the final answer in a readable way
if (ac_flag == 1):
    for i in node_set:
        if (i != 'GND') :
            print("Voltage at",i,"wrt GND is", x[node_set.index(i),0],"V")
    for i in range(no_of_voltage_sources):
        print("Current through", voltage_sources[i], "is", x[-no_of_voltage_sources+no_of_variables+i,0],"A")
else:
    for i in node_set:
        if (i != 'GND') :
            print("Voltage at",i,"wrt GND is", x[node_set.index(i),0].real, "V")
    for i in range(no_of_voltage_sources):
        print("Current through", voltage_sources[i], "is", x[-no_of_voltage_sources+no_of_variables+i,0].real, "A")



    











        








        
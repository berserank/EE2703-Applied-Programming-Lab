"""

Author      : G Abhiram <gabhiram@smail.iitm.ac.in>
Roll no     : EE20B037
Course      : EE2703 - Applied Programming Lab
Assignment  : 1
Date Created: Jan 24, 2022
Description : Read a .netlist file, reverse the each component string and print each component string

"""
#Importing the useful librares/modules
import sys
from os.path import exists
args = sys.argv

"""
It's a good practice to check if the user has given required and only the required inputs
Otherwise, show them the expected usage.
"""
try:
    if(len(args) != 2):
        sys.exit('Invalid number of arguments. Please enter two arguments.')
#Accepting the netlist file as a commandline argument. 
    
    f = open(args[1], 'r')
except Exception:
        print('''\t\tFile doesn't exist in this directory.
                Make sure that the filename is typed correctly
                and you are in the correct directory.''')
        sys.exit(0)

#Parse the file starting from .circuit to .end
data = f.read().splitlines()

start_index = 0
try:
    while(data[start_index]!='.circuit'): #to find the index of the '.circuit\n'
        start_index = start_index +1
except Exception:
    print("There is an issue with the netlist file.")
    sys.exit(0)

end_index = start_index
while(data[end_index]!='.end'):   #to find the index of the '.end\n'
    end_index = end_index + 1

ref_data = data[start_index+1:end_index]  #Data cleaning to compress the array to retain only the required elements

final_data = []
#print(ref_data)
for n in ref_data:
    #print(n)
    final_data.append(n)

choice =input("Do you want to see the parsed values printed?\n Enter Yes then.\n")
#print(final_data)

database = []
word_array = []

#Parsing each component string and getting information about the nature of source, component and value etc.
def parser(input_database,line): 
    words = line.split()
    #print(words)
    for p in range(len(words)):
        if (words[p][0] == '#'):
            words = words[0:p]
            break
    #print(words)
    word_array.append(words)
    ckt_dict = { }   #Create an empty dictionary
    N = len(words)
    if (N==4):
        
        ckt_dict['Type'] = 'Independent'
        ckt_dict['Name'] = words[0][0:2]
        if (words[0][0] == 'R'):
            ckt_dict["Element"] = 'Resistor'
        
        elif (words[0][0] == 'L'):
            ckt_dict["Element"] = 'Inductor'
        
        elif (words[0][0] == 'C'):
            ckt_dict["Element"] = 'Capacitor'
        
        elif (words[0][0] == 'V'):
            ckt_dict["Element"] = 'Independent Voltage Source'

        elif (words[0][0] == 'I'):
            ckt_dict["Element"] = "Independent Current Source"

        else:
            ckt_dict["Element"] = "Unknown Element"
        
        ckt_dict['From Node'] = words[1]
        ckt_dict['To Node'] = words[2]
        ckt_dict["Value of the element:"] = float(words[3])
        return ckt_dict

    if (N==6):
        ckt_dict["Type"] = "Dependent"
        ckt_dict['Name'] = words[0][0:2]
        if (words[0][0] == 'E'):
            ckt_dict["Element"] = "VCVS"
        
        elif (words[0][0] == 'G'):
            ckt_dict["Element"] = "VCCS"

        elif (words[0][0] == 'H'):
            ckt_dict["Element"] = "CCVS"
        
        elif (words[0][0] == 'F'):
            ckt_dict["Element"] = "CCCS"
        
        else:
            ckt_dict["Element"] = "Unknown Element"
        
        ckt_dict['From Node'] = words[1]
        ckt_dict['To Node'] = words[2]
        ckt_dict['Dependent From Node'] = words[3]
        ckt_dict['Dependent To Node'] = words[4]
        ckt_dict["Value of the element: "] = float(words[5])
        return ckt_dict

    input_database.append(ckt_dict)
    if ((choice =='Yes')|(choice == 'yes')|(choice=='YES')):
        print(f"{ckt_dict}\n")

for a in final_data:
    parser(database,a)
print(word_array)

if ((choice =='Yes')|(choice == 'yes')|(choice=='YES')):
    print("Note that here,\n")
    print("VCCS : Voltage Controlled Current Source\nVCVS : Voltage Controlled Voltage Source\nCCVS : Current Controlled Voltage Source\nCCCS : Current Controlled Current Source\n")
 

choice2 = input("Do you want to see the file values printed in reverse order?\nEnter Yes then.\n")
if ((choice =='Yes')|(choice == 'yes')|(choice=='YES')):
    reverse_list = list(reversed(word_array))
    for element in reverse_list:
        reverse_words = list(reversed(element))
        tempstr = ''
        for word in reverse_words:
            tempstr = tempstr+' '+word
        print(f"{tempstr}")

#         EE2703 Applied Programming Lab 
#         Assignment 1
#         Aditya Nanda Kishore
#         EE20B062  

from sys import argv, exit

CIRCUIT = '.circuit\n'
END = '.end'
END1 = '.end\n'

if len(argv) != 2:
    print("Invalid Input. Please enter 2 arguments") #This checks whether given input has a netlist file or  not in the code
    exit()

# """
# The use might input a wrong file name by mistake.
# In this case, the open function will throw an IOError.
# Make sure you have taken care of it using try-catch


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
    
    for line in lines[end-1:start:-1]:
            line_without_comments = line.split('#')[0]
            words = line_without_comments.split()
            reversed_words = reversed(words)
            valid_line = ' '.join(reversed_words)
            print(valid_line)
        

# What it does is,
# It takes every line from bottom( above '.end')and splits the line at '#' at only considers the section of line before '#' 
# and it later splits the formed section at space and reverses the words and joins them again with space.
# This takes a lot of code and time to run in C, python made the code simple.


except IOError:
    print('Invalid file')
    exit()

import os
import random
import math
def to_bit_list(array,name_list):
    for byte in array:
        buf = bin(byte)
        name_list.append(buf[2:].zfill(8))

def index_to_actual(array,index):
    row = math.floor(index / 8)
    column = index % 8
    return array[row][column]

def to_container(altered,container,psp1_list):
    '''Modifying container with altered key.
        psp1_list - container;
       container - container copy;
       altered - altered key;
    '''
    for i in range(len(altered)):
        b = psp1_list[i]
        a = altered[i]
        container.append(bin(int(b,2) ^ int(a,2))[2:].zfill(8))
    if (len(container) < len(psp1_list)):
        container.extend(psp1_list[len(container):])

def to_altered(psp2_list,altered,name_list):
    '''Modifying key with data.
        psp2_list - key;
       altered - key copy;
       name_list - data;
    '''
    global_index = 0
    for i in range(len(psp2_list) * 8):
        row = math.floor(i / 8)
        column = i % 8
        b = psp2_list[row][column]
        if psp2_list[row][column] == '1' and (global_index < len(name_list) * 8):
            altered[row] = psp2_list[row][:column] + str(int(index_to_actual(name_list,global_index)) ^ int(b)) + psp2_list[row][column + 1:]
            global_index+=1
#variables
name_list = []
psp2_list = []
psp1_list = []
new_list = []
container = []

name = "abc" #data
data = bytearray(name, "utf8")
psp_1 = bytearray(os.urandom(len(name) * 3)) #container
psp_2 = bytearray(os.urandom(int(len(name) * 2.5))) #key

#to binary
to_bit_list(data,name_list)
to_bit_list(psp_2,psp2_list)
to_bit_list(psp_1,psp1_list)

#print
print("Name: ",name_list,sep="\n")
print("Container: ",psp1_list,sep="\n")
print("Key: ",psp2_list,sep="\n")

#key copy for modification
altered = psp2_list.copy()
#influencing key 1's with data
to_altered(psp2_list,altered,name_list)
print("Altered key: ",altered,sep="\n")
#putting altered key to container
to_container(altered,container,psp1_list)
print("Altered container: ",container,sep="\n")
#transmission occurring here
print("~" * 10,"Imaginary transmission:","~" * 10,sep="\n")
#extracting altered key from container
to_container(psp2_list,new_list,container)
print("Altered key(extracted): ",altered,sep="\n")
#retrived_data=[None] * len(altered)
#to_altered(new_list,retrived_data,name_list);

#print(altered)
#print(container)
#print(new_list)
#print(retrived_data)
#print("name:",retrived_data)
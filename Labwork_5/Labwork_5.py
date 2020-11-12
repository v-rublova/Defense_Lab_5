import os
import math

def better_number(key):
    '''
    Preferable digit to be modified.
    '''
    count = 0
    for x in key:
        count+=x.count('1')
    if (count > (len(key)*8)/2): 
        return '1';
    else:
        return '0';

def pack(data):
    '''
    Pack retrieved data into octets.
    '''
    data_copy = data.copy()
    data.clear()
    buf = ""
    for i in range(len(data_copy)):
        if ((i % 8 == 0 and i!=0)):
            data.append(buf)
            buf = ""
        buf += str(data_copy[i])

def to_bit_list(array,name_list):
    for byte in array:
        buf = bin(byte)
        name_list.append(buf[2:].zfill(8))

def index_to_actual(array,index):
    row = math.floor(index / 8)
    column = index % 8
    return array[row][column]

def to_container(altered,container,psp1_list,t=True):
    '''Modifying container with altered key.
        psp1_list - container;
       container - container copy;
       altered - altered key;
    '''
    for i in range(len(altered)):
        b = psp1_list[i]
        a = altered[i]
        container.append(bin(int(b,2) ^ int(a,2))[2:].zfill(8))
    if ((len(container) < len(psp1_list)) and t):
        container.extend(psp1_list[len(container):])

def to_altered(psp2_list,altered,name_list,t=True):
    '''Modifying key with data.
        psp2_list - key;
       altered - key copy;
       name_list - data;
    '''
    #p - preferable digit to be modified with data (0|1)
    p = better_number(psp2_list)
    global_index = 0
    for i in range(len(psp2_list) * 8):
        row = math.floor(i / 8)
        column = i % 8
        b = psp2_list[row][column]
        if psp2_list[row][column] == p and (global_index < len(name_list) * 8):
            if (not t):
                altered.append(int(b) ^ int(name_list[row][column]))
            else:
                altered[row] = (altered[row][:column] + 
                                str(int(index_to_actual(name_list,global_index)) ^ int(b)) + 
                                altered[row][column + 1:])
            global_index+=1
#variables
name_list = []
psp2_list = []
psp1_list = []

new_list = []
container = []
retrived_data = []

name = "message" #data
data = bytearray(name, "utf8")
psp_1 = bytearray(os.urandom(len(data)*3)) #container
psp_2 = bytearray(os.urandom(len(data)*2)) #key

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
#influencing key's 1 or 0 with data
to_altered(psp2_list,altered,name_list)
print("Altered key: ",altered,sep="\n")
#putting altered key into container
to_container(altered,container,psp1_list)
print("Altered container: ",container,sep="\n")
#transmission occurring here
print("~" * 10,"Imaginary transmission:","~" * 10,sep="\n")
#extracting altered key from container
to_container(psp1_list,new_list,container,t=False)
#discarding container's 'tail'
new_list = new_list[:len(psp2_list)]
print("Altered key(extracted): ",new_list,sep="\n")
#extracting data
to_altered(psp2_list,retrived_data,new_list,t=False);
pack(retrived_data);
print("Data(extracted): ",retrived_data,sep="\n")
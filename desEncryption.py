import time
import sys

# Permutation and translation tables for DES
# initial permutation IP
ip = [57, 49, 41, 33, 25, 17, 9,  1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7,
      56, 48, 40, 32, 24, 16, 8,  0,
      58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6 ]

#permuted choice key-1 
pc1 = [56, 48, 40, 32, 24, 16,  8,
       0, 57, 49, 41, 33, 25, 17,
       9,  1, 58, 50, 42, 34, 26,
       18, 10,  2, 59, 51, 43, 35,
       62, 54, 46, 38, 30, 22, 14,
       6, 61, 53, 45, 37, 29, 21,
       13,  5, 60, 52, 44, 36, 28,
       20, 12,  4, 27, 19, 11,  3]

# permuted choice key-2 
pc2 = [13, 16, 10, 23,  0,  4,
       2, 27, 14,  5, 20,  9,
       22, 18, 11,  3, 25,  7,
       15,  6, 26, 19, 12,  1,
       40, 51, 30, 36, 46, 54,
       29, 39, 50, 44, 32, 47,
       43, 48, 38, 55, 33, 52,
       45, 41, 49, 35, 28, 31]

# number left rotations of pc1
left_rotations = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Expansion table for turning 32 bit blocks into 48 bits
expansion_table = [31,  0,  1,  2,  3,  4,
                   3,  4,  5,  6,  7,  8,
                   7,  8,  9, 10, 11, 12,
		   11, 12, 13, 14, 15, 16,
		   15, 16, 17, 18, 19, 20,
		   19, 20, 21, 22, 23, 24,
		   23, 24, 25, 26, 27, 28,
		   27, 28, 29, 30, 31,  0]

# The S-boxes
sbox = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

# 32-bit permutation function P used on the output of the S-boxes
sp = [15, 6, 19, 20, 28, 11,
     27, 16, 0, 14, 22, 25,
     4, 17, 30, 9, 1, 7,
     23,13, 31, 26, 2, 8,
     18, 12, 29, 5, 21, 10,
     3, 24]

# final permutation IP^-1
finalp = [39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25,
          32,  0, 40,  8, 48, 16, 56, 24]

#format the string list into a list of bits
def stringToBinary( inputText):
       #convert string list into a string list with the binary values of the input text
       result = ''.join(f"{ord(i):08b}" for i in inputText)
       pos =0
       output =[0]*(len(inputText) * 8)
       #convert string list into a int list
       for x in result:
          if x=='1':
              output[pos] =1
          else:
              output[pos] =0
          pos +=1
       return  output

#format the hex value into a bit list
def hexToList( inputHex):
       pos =0
       output =[0]*(len(inputHex))
       for x in inputHex:
          if x=='1':
              output[pos] =1
          else:
              output[pos] =0
          pos +=1
       return  output

#convert a bit list into a string
def bitsToString(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        print(byte)
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

#this function permutate the elements of the input block-list according the values of the input table     
def permutate(table, block):
       j=0
       #result must be the same length with the permutation table
       result = [0] * (len(table))
       for i in table:
           result[j] = block[i]
           j+=1
       return result
  
def subKeyGenerator(key, table ):
       #split key into two sectors
       C = key[:28]
       D = key[28:]
       i = 0
       finalKey = []
       print()
       print('==============================================================================================================================================================')
       print('--------------------------------------------------------------------------KEY SCHEDULER-----------------------------------------------------------------------')
       while i < 16:
            j = 0
            while j < table[i]:
                  #shift elements of the L+R sectors by the values of the input table(pop will remove the first element j times, append will add it in the end of the list
                  C.append(C.pop(0))
                  D.append(D.pop(0))
                  j += 1
            print('Round:', i+1, 'Shift:',table[i],'\n','->C:', C,'\n','->D:', D)
            #permutation of the subkey,then append it to a finalKey list
            finalKey.append(permutate(pc2, C + D))
            print('Final key',i+1 ,':',finalKey[i])
            print('==============================================================================================================================================================')
            i += 1
       print()
       return finalKey

#core of DES(ECB)
def desCrypt( block, key):
       start_time = time.time()
       print('------------------------------------------------------------------------INITIALIZATION------------------------------------------------------------------------')
       print()
       print('Input Block')
       printList(inputBlock, 8, 8)
       print()
       print('Key Blcok')
       printList(keyBits, 8, 8)
       #permutate input block with the ip table
       block = permutate(ip, block)
       print()
       print('Permutation Result(ip)')
       printList(block,8,8)
       print()
       #split input block(in half) into two sectors(L+R)
       L = block[:32]
       print('L-in:',L)
       R = block[32:]
       print('R-in:',R)
       print()
       #permutate key with the pc1 table
       key =  permutate(pc1, key)
       print('Permutation Result(pc1)')
       printList(key, 8 , 7)
       print()
       #generate 16 sub-keys
       fKey = subKeyGenerator(key, left_rotations)
       
       i = 0
       print('==============================================================================================================================================================')
       print('==============================================================================================================================================================')
       #starting DES encryption
       while i < 16:
              
              print()
              print('-------------------------------------------------------------------------ROUND',i+1,'-------------------------------------------------------------------------')
              print()
              print('Key')
              printList(fKey[i], 8, 6)
              print()
              #the next L will become the previous R,we will use tempR later for that
              tempR = R[:]
              #permutate R with the e-table table
              R = permutate(expansion_table , R)
              print('Permutation Result(expansion_table)')
              printList(R, 8 ,6)
              #XOR R with the final key i to calculate sBoxes input
              R = list(map(lambda x, y: x ^ y, R, fKey[i]))
              #split sBoxin to 8 boxes
              sBoxin = [R[:6], R[6:12], R[12:18], R[18:24], R[24:30], R[30:36], R[36:42], R[42:]]
              #S-boxes
              j = 0
              index = 0
              sBoxOut = [0]*32
              print()
              print('--------------------------------------------------------------------------S-BOXES-----------------------------------------------------------------------------')
              print('==============================================================================================================================================================')
              while j < 8:
                     print('=====S',j+1,'BOX=====')
                     #calculate ROW
                     row = ( (sBoxin [j][0] << 1 ) + sBoxin [j][5])
                     print('Row:',row)
                     column = ( sBoxin [j][1] << 3 ) + (sBoxin [j][2] <<2 ) + (sBoxin [j][3] << 1 )+ sBoxin [j][4]
                     #calculate COLUMN
                     print('Column:',column)
                     #add ROW,COLUMN to find the sBox value
                     sValue = sbox[j][(row << 4 ) + column]
                     print('Value:',sValue ,'(',format(sValue, "04b"),')')
                     print('=================')
                     #format convert the int sValue to 4bit value,then we fill that value in sBoxOut list
                     for x in format(sValue, "04b") :
                            if x=='1': sBoxOut[index] =1
                            else: sBoxOut[index] =0
                            index += 1
                     j += 1
              print('S-box Final:',sBoxOut)
              print('==============================================================================================================================================================')
              #permutate SBOXES output with a 32bit table
              R = permutate(sp, sBoxOut)
              #XOR R with L
              R = list(map(lambda x, y: x ^ y, L, R))
              #L becomes the previous R
              L = tempR
              print('Lout:',L)
              print('Rout:',R)
              i += 1
              print('==============================================================================================================================================================')
              print()
       #final permutation 
       output = permutate(finalp, R + L)
       print('Permutation Result(finalp)')
       printList(output, 8, 8)
       print('==============================================================================================================================================================')
       print("-> Total time: %s seconds " % (time.time() - start_time))
       print('==============================================================================================================================================================')
       print()
       return output

#with this padding function we fill the blocks with '0's to create 64bit size block,if this is necessary
def pad(data):
    if len(data) != 64 :
           pad_len = 64 - len(data)%64
           data += ([0] * pad_len) 
           return data 
    else: return data

#this function is used to print lists into 2d
def printList(data,rows,cols):
   pos=0
   print('[', end= "")
   for i in range(cols):
          for j in range(rows):
                 if pos == 0:
                      print(data[pos], end="")
                      pos+=1 
                 else:
                      print("",data[pos], end="")
                      pos+=1       
          if pos == len(data): print(']')            
          print("")
          
def main():
       plainText = input('Type a message to decrypt:')
       b = plainText
       #input checking conditions
       while True:
              form = input('Type 1 for Plaintext-Type 2 for Hex:')
              if form == '1':
                     plainText = stringToBinary(plainText)
                     break
              elif form == '2' :
                     plainText = hexToList(bin(int(plainText, 16))[2:].zfill(64))
                     break
              else: print('Invalid number!')
       while True:
              key = input('Type the 64-bit key:',)
              form = input('Type 1 for Plaintext-Type 2 for Hex:')
              if form == '1':
                     keyBits = stringToBinary(key)
              elif form == '2' :
                     keyBits = hexToList(bin(int(key, 16))[2:].zfill(64))
              else: print('Invalid number!')
              if len(keyBits) != 64 :
                     print("Invalid DES key size.Key must be exactly 8 bytes long.Try again...")
              else: break

       #padding input Text
       PlainText = pad(plainText)
       i = 0
       j = 64
       encryptedText = []
       output = []
       sys.stdout = open('EncryptionResult.txt', 'w',encoding="utf-8")

       print('Plaintext:',b)
       print('Key:',key)
       print('==============================================================================================================================================================')
       print()

       while True:
              #first input block will be the first 64bits,if the user input in >64 then will split it into 64bit blocks
              inputBlock = PlainText[i:j]
              encryptedBlock = desCrypt(inputBlock, keyBits)
              output += encryptedBlock
              if j == len(plainText):break
              i = j
              j += 64
              print('========================================================================================')
       print('Final output:',bitsToString(output))
       sys.stdout.close()
       exit()


if __name__ == "__main__":
    main()
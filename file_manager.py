import os

def showMenu(): 
    print("\nPlease choose an option:")
    print("1. Create a file")
    print("2. Delete a file")
    print("3. List files in directory")
    print("4. Exit\n")

print("Welcome to CLI file manager!")
while True:
    showMenu()
    option = int(input("Enter your choice(1-4): "))
    
    if option==1:
        filename = input("Enter file name: ")
        
        if os.path.exists(filename):
            print(f"'{filename}' already exists")
        else:
            with open(filename, "w") as f:
                f.write("")
            print(f"'{filename}' has been created!")
            
    elif option==2:
        filename = input("Enter filename you want to delete: ")
        
        if os.path.exists(filename):
            os.remove(filename)
            print(f"'{filename}' has been removed successfully")
        else:
            print("No such file in the directory\n")
            
    elif option==3 :
        files = os.listdir()
        
        if len(files)==0:
            print("Directory is empty\n")
        else:
            print("folders and files in current directory --> ")
            for f in files:
                print("."+f);
        
    elif option==4 :
        print("Exiting")
        break
    else:
        print("Invalid input")
    
    print("\n==========================================================")
        

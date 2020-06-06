import random

def create_file():
    global el, dim;
    try:
        option = int(input("\nWhat you want to do? \nChoose 1 to Create file\nChoose 2 to Exit "))
    except ValueError:
        print("Wrong input\n")
        create_file()
    if option == 1:
        try:
            dim = int(input("K-D Tree Dimensions : "))
            el = int(input("Number of K-D Tree elements : "))
            max=1000
            min=1
            #max = float(input("Max value of the elements : "))
            #min = float(input("Min value of the elements : "))
        except ValueError:
            print("Wrong input\n")
            create_file()
    print("\nPleae wait while the file is created ...\n")
    try:
     f = open("data.txt", "w+")
     for i in range(el):
      for j in range(dim):
        f.write("{} -".format(round(random.uniform(min, max), 1)))
      f.write("\n")
     f.close()
    except IOError:
     print("Wrong input, can't create the file")
     create_file()
    print("\nDone!\n")

create_file()
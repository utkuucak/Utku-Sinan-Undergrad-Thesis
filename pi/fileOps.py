import sys

file = open(sys.argv[1], "r")
new_file = open ("./hotelCopyfornia.txt", "w")

for line in file:
    print(line)
    new_file.write(line)

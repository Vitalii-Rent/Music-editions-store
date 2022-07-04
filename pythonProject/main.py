import csv


youngest_student = None
min_age = None
with open('MOOC.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        age = int(row["age"])
        if min_age == None or min_age > age:
            youngest_student = row["name"]
            min_age = age
if min_age == None:
    print("The file does not contain any students.")
else:
    print("The youngest student is " + str(youngest_student) + " who is " + str(min_age) + " years old. ")

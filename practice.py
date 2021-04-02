#practice
#stk=[]
#ch='Y'
#while(ch=='Y' or ch=='y'):
#    print("Enter 1 : Push")
 #   print("Enter 2 : Pop")
  #  opt=int(input('enter ur choice:='))
   # if opt==1:
    #    d=int(input("enter book no : "))
     #   stk.append(d)
      #  print(stk)
    #elif opt==2:
     #   if (stk==[]):
      #      print( "Stack empty")
       # else:
        #    p=stk.pop()
         #   print("Deleted element:", p)
          #  print(stk)
    #else:
     #   print('invalid choice')
      #  ch=(input('want to continue?'))

#practice 2
# q=[]
# ch='Y'
# while(ch=='Y' or ch=='y'):
#     print("Enter 1 : Enqueue")
#     print("Enter 2 : Dequeue")
#     opt=int(input('enter ur choice:='))
#     if opt==1:
#         d=int(input("enter book no : "))
#         q.append(d)
#         print(q)
#     elif opt==2:
#         if (q==[]):
#             print( "Queue empty")
#         else:
#             p=q.pop(0)
#             print ("Deleted element:", p)
#             print(q)        
#     else:
#         print('invalid choice')
#         ch=(input('want to continue?'))  
     


#practice3
# no_word = no_lines = no_alpha = 0

# f = open("poem.txt",'r')

# lt = f.readlines()
# no_lines = len(lt)

# for line in lt:  
#     words = line.split()  
#     no_word += len(words)
#     for word in words:
#         for alpha in word:
#             no_alpha += 1

# f.close()

# ch = 'y'
# while (ch == "y" or ch == "Y"):
#     opt = int(input("\n\t0. Exit\n\t1. number of words\n\t2. number of lines\n\t3. number of alphabets\nchoice: "))
#     if opt == 1:
#         print("no_word:", no_word)
#         ch = input("continue?(y/n): ")
#     elif opt == 2:
#         print("no_line: ", no_lines)
#         ch = input("continue?(y/n): ")
#     elif opt == 3:
#         print("no_alpha: ", no_alpha)
#         ch = input("continue?(y/n): ")
#     elif opt == 0:
#         print("exiting")
#         break
#     else:
#         print("invalid entry")
#         ch = input("continue?(y/n): ")
# else:
#     print("exiting")

#practice4
# t_count = count_d = 0
# t_lt = []
# lt_d = []

# f = open("poem.txt",'r')

# lt = f.readlines()

# for line in lt:
#     if line[0] == 't' or line[0] == 'T':
#         t_lt.append(line)
#         t_count += 1

# for line in lt:
#     words = line.split() #st = "mera naam joker"  st.split ==>  ['mera', 'naam', 'joker']
#     if words[-1][-1] == 'd' or words[-1][-1] == 'D':
#         lt_d.append(line)
#         count_d += 1

# f.close()

# ch = 'y'
# while (ch == "y" or ch == "Y"):
#     opt = int(input("\n\t0. Exit\n\t1. t_wala\n\t2. wala_d\nchoice: "))
#     if opt == 1:
#         print("t_count: ", t_count)
#         for i in t_lt:
#             print(i)
#     elif opt == 2:
#         print("count_d: ", count_d)
#         for j in lt_d:
#             print(j)
#     elif opt == 0:
#         print("exiting")
#         break

#practice5
# import mysql.connector
# mydb=mysql.connector.connect(host="localhost",user="root",passwd="root#123",database="school",charset='utf8')
# print(mydb)
# mycursor=mydb.cursor()
# rollno=int(input("Enter the roll number of the student to be deleted: "))
# rl=(rollno,)
# sql="delete from Student where roll_no=%s"
# mycursor.execute(sql,rl)
# print('Record deleted!!!')
# mydb.commit()

#practice6
# import mysql.connector
# from tabulate import tabulate
# mydb=mysql.connector.connect(host="localhost",user="root",passwd="root#123",database="school",charset='utf8')
# print(mydb)
# mycursor=mydb.cursor()
# rollno=int(input("Enter the roll number of the student to be searched: "))
# rl=(rollno,)
# query = "select * from student where roll_no = %s"
# mycursor.execute(query,rl)
# lt = mycursor.fetchall()
# print(tabulate(lt, headers=['roll', 'name', 'class', 'age', 'city'], tablefmt='pretty'))

#practice7
# import mysql.connector
# mydb=mysql.connector.connect(host="localhost",user="root",passwd="root#123",database="school",charset='utf8')
# print(mydb)
# mycursor=mydb.cursor()
# L=[]

# roll_no=int(input("Enter the roll number: "))
# L.append(roll_no)
# name=input("Enter the Name: ")
# L.append(name)
# age=int(input("Enter Age of Student: "))
# L.append(age)
# classy=input("Enter the class: ")
# L.append(classy)
# city=input("Enter city: ")
# L.append(city)

# #stud=(L,)
# query = "insert into student values(%s,%s,%s,%s,%s)"
# mycursor.execute(query,L)
# mydb.commit()

# print("values inserted")

#practice8
#same as practice5

#practice9
#from sympy import *
string = input("Enter string: ")
if string == string[::-1]:
    print("it is palindrome")
else:
    print("not palindrome")

num = int(input("Enter number: "))
#prime = isprime(num)
if prime:
	print("number is prime")
else:
	print("number is not prime")

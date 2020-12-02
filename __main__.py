import mysql.connector as mc
from getpass import getpass
from tabulate import tabulate
#from sys import os

mysql_uname = input("Enter mysql username: ")
mysql_passw = getpass("Enter mysql password: ")
connection = mc.connect(host = 'localhost', user = mysql_uname, password = mysql_passw)
cursor = connection.cursor()

try:
    cursor.execute("create database toucri")
except:
    print()
finally:
    cursor.execute("use toucri")

def tables():
    global cursor
    cursor = connection.cursor()
    outcome_table_query = "create table if not exists outcomes(match_no int not null primary key, team_won varchar(10), team_lost varchar(10))"
    cursor.execute(outcome_table_query)
    cursor.close()
    cursor = connection.cursor()
    try:
        points_table_query = "create table points(ranks int default null, team varchar(10), point int)"
        cursor.execute(points_table_query)
        n = int(input("no. of teams: "))
        for _ in range(n):
            teams = input("Give name of teams: ")
            points_query = "insert into points(team, point) values({},0)".format("'"+teams+"'")
            cursor.execute(points_query)
            connection.commit()
    except:
        print()       

tables()


def per_match():
    match_no = int(input("Match Number: "))
    cursor.execute("create table if not exists {}(team varchar(10), batsman varchar(20), score int, bowler varchar(20), wickets int)".format("matchnum"+str(match_no)))
    team_won = input("Winner name: ")
    team_lost = input("Loser name: ")
    teams = [team_won, team_lost]
    for team in teams:
        for _ in range(2):
            bats = input("Enter batsmans name: ")
            score = int(input("Enter score: "))
            bowls = input("Enter bowlers name: ")
            wick = int(input("Enter wickets: "))
            insert_query = "insert into {0} (team, batsman, score, bowler, wickets) values({1},{2},{3},{4},{5})".format("matchnum"+str(match_no), "'"+team+"'", "'"+bats+"'", score, "'"+bowls+"'", wick)
            cursor.execute(insert_query)
            print("executed")
            connection.commit()
            print("commited")
    outcomes_query = "insert into outcomes(match_no, team_won, team_lost) values({},{},{})".format(match_no, "'"+team_won+"'", "'"+team_lost+"'")
    cursor.execute(outcomes_query)
    connection.commit()
    points_update_query = "update points set point = point + 2 where team = {}".format("'"+team_won+"'")
    cursor.execute(points_update_query)
    connection.commit()


def rank():
    rank_query = "select team, point, @curRank:= @CurRank + 1 as ranks from points p, (select @CurRank:=0) r order by point desc"
    cursor.execute(rank_query)
    points_data = cursor.fetchall()
    points_print = []
    for row in points_data:
        points_print.append(list(row))
    print(tabulate(points_print, headers=['team', 'point', 'rank'], tablefmt="pretty"))


def search(team_to_search):
    global cursor
    search_query = "select match_no from outcomes where team_won = {} or team_lost = {}".format("'"+team_to_search+"'","'"+team_to_search+"'")
    cursor.execute(search_query)
    req_match_no = []       
    for match_code in cursor.fetchall():
        req_match_no.append((list(match_code))[0]) 
    cursor.close()
    cursor = connection.cursor()
    for match in req_match_no:
        cursor.execute("select * from {}".format("matchnum"+str(match)))
        match_data = []
        for i in cursor.fetchall():
            match_data.append(i)
        print(tabulate(match_data, headers = ["team", "batsman", "score", "bowler", "wickets"], tablefmt="pretty")) 


while True:
    try:
        print("==================")
        crud = int(input("Please select:\n\t0. Exit\n\t1. Create\n\t2. Search\n\t3. Points table\nchoice: "))
        if crud == 0:
            connection.close()
            print("So long..!\n==================")
            break
        elif crud == 1:
            per_match()
        elif crud == 2:
            team_to_search = input("Enter team name: ")
            search(team_to_search)
        elif crud == 3:
            rank()
        else:
            print("Invalid choice.")
            print("==================")
    except Exception as e:
        print(e)
        print("Invalid choice.")
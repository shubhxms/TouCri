import mysql.connector as mc
from getpass import getpass
from tabulate import tabulate
#from sys import os

#mysql_uname = input("Enter mysql username: ")
#mysql_passw = getpass.getpass("Enter mysql password: ")
connection = mc.connect(host = 'localhost', user = 'root', password = 'root#123')
cursor = connection.cursor()

try:
    cursor.execute("create database toucri")
    #connection.commit()
except:
    print()
finally:
    cursor.execute("use toucri")

def tables():
    outcome_table_query = "create table outcomes(match_no int not null primary key, team_won varchar(10), team_lost varchar(10))"
    cursor.execute(outcome_table_query)
    points_table_query = "create table points(rank int default null, team varchar(10), points int)"
    cursor.execute(points_table_query)
    teams = eval(input("Give list of teams: "))
    for team in teams:
        points_query = "insert into points(team, points) values({},0)".format(team)
        cursor.execute(points_query)
        connection.commit()


def per_match():
    match_no = int(input("Match Number: "))
    cursor.execute("create table {}(team varchar(10), batsman varchar(20), score int, bowler varchar(20), wickets int)".format(match_no))
    team_won = input("Winner name: ")
    team_lost = input("Loser name: ")
    teams = [team_won, team_lost]
    for team in teams:
        for _ in range(2):
            bats = input("Enter batsmans name: ")
            score = int(input("Enter score: "))
            bowls = input("Enter bowlers name: ")
            wick = int(input("Enter wickets: "))
            insert_query = "insert into {0} values(team, batsman, score, bowler, wickets) values({1},{2},{3},{4},{5})".format(match_no, "'"+team+"'", "'"+bats+"'", score, "'"+bowls+"'", wick)
            cursor.execute(insert_query)
            connection.commit()
    outcomes_query = "insert into outcomes(match_no, team_won, team_lost) values({1},{2},{3})".format(match_no, "'"+team_won+"'", "'"+team_lost+"'")
    cursor.execute(outcomes_query)
    connection.commit()
    points_update_query = "update points set points = points + 2 where team = {}".format(team_won)
    cursor.execute(points_update_query)
    connection.commit()

def rank():
    rank_query = "select team, points, @curRank:= @CurRank as rank from points p, (select @CurRank:=0) r order by points"
    cursor.execute(rank_query)
    points_data = cursor.fetchall()
    points_print = []
    for row in points_data:
        points_print.append(list(row))
    print(tabulate(points_print, headers=['team', 'points', 'rank'], tablefmt="pretty"))



while True:
    try:
        print("==================")
        crud = int(input("Please select:\n\t0. Exit\n\t1. Create\n\t2. Search\n\t3. Update\n\t4. Delete\nchoice: "))
        if crud == 0:
            print("So long..!\n==================")
            break
        elif crud == 1:
            create()
        elif crud == 2:
            team_to_search = input("Enter team name: ")
            search(team_to_search)
        elif crud == 3:
            record_to_update = input("Enter name of book to update: ")
            update(record_to_update)
        elif crud == 4:
            sno_to_delete = input("Enter sno of product to delete: ")
            delete(sno_to_delete)
        else:
            print("Invalid choice.")
            print("==================")
    except:
        print("Invalid choice.")
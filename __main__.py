from os import sys
from getpass import getpass
try:
    from tabulate import tabulate
    import mysql.connector as mc
except ModuleNotFoundError:
    print('Some modules may not be dowloaded!!:')
    print('either mysql.connector')
    print('or tabulate')
    sys.exit()

try:
    mysql_uname = input("Enter mysql username: ")
    mysql_passw = getpass("Enter mysql password: ")
    connection = mc.connect(host = 'localhost', user = mysql_uname, password = mysql_passw)
    cursor = connection.cursor()
except:
    print('Username or Password may be incorrect!\n')
    sys.exit()

print('''
  _____    ___    _   _    ____   ____    ___ 
 |_   _|  / _ \  | | | |  / ___| |  _ \  |_ _|
   | |   | | | | | | | | | |     | |_) |  | | 
   | |   | |_| | | |_| | | |___  |  _ <   | | 
   |_|    \___/   \___/   \____| |_| \_\ |___|
                                              
''')

TEAMS = []

try:
    cursor.execute("create database toucri")
except:
    print()
finally:
    cursor.execute("use toucri")

def tables():
    global cursor
    global TEAMS
    cursor = connection.cursor()
    outcome_table_query = "create table if not exists outcomes(match_no int not null primary key, team_won varchar(10), team_lost varchar(10))"
    cursor.execute(outcome_table_query)
    cursor.close()
    cursor = connection.cursor()
    try:
        points_table_query = "create table points(team varchar(10), point int)"
        cursor.execute(points_table_query)
        n = int(input("no. of teams: "))
        TEAMS = []
        for l in range(n):
            stri = str("Give name of team number"+str(l+1)+": ")
            teams = input(stri)
            TEAMS.append(teams)
            print(TEAMS)
            points_query = "insert into points(team, point) values({},0)".format("'"+teams+"'")
            cursor.execute(points_query)
            connection.commit()
    except:
        fetch_data_query = "select team from points"
        cursor.execute(fetch_data_query)
        data = cursor.fetchall()
        for i in range(len(data)):
            TEAMS.append(data[i][0])
        print(TEAMS)

def drop_db():
    dropping_db_query = "drop database toucri"
    cursor.execute(dropping_db_query)
    connection.commit()
    print('All the data related to the tournamanet has been deleted!! ')
    sys.exit()

tables()

def per_match():
    global TEAMS
    match_no = int(input("Match Number: "))
    try:
        cursor.execute("create table {}(team varchar(10), batsman varchar(20), score int, bowler varchar(20), wickets int)".format("matchnum"+str(match_no)))
        team_won = input("Winner name: ")
        team_lost = input("Loser name: ")
        print(TEAMS)
        while (team_won in TEAMS) and (team_lost in TEAMS):
            teams = [team_won, team_lost]
            for team in teams:
                print(('*-'*5),'Enter data for',team,('-*'*5))
                for i in range(2):
                    str1 = str("Enter batsman number "+str(i+1)+" name: ")
                    bats = input(str1)
                    score = int(input("Enter score: "))
                    str2 = str("Enter bowler number "+str(i+1)+" name: ")
                    bowls = input(str2)
                    wick = int(input("Enter wickets: "))
                    insert_query = "insert into {0} (team, batsman, score, bowler, wickets) values({1},{2},{3},{4},{5})".format("matchnum"+str(match_no), "'"+team+"'", "'"+bats+"'", score, "'"+bowls+"'", wick)
                    cursor.execute(insert_query)
                    connection.commit()
            outcomes_query = "insert into outcomes(match_no, team_won, team_lost) values({},{},{})".format(match_no, "'"+team_won+"'", "'"+team_lost+"'")
            cursor.execute(outcomes_query)
            connection.commit()
            points_update_query = "update points set point = point + 2 where team = {}".format("'"+team_won+"'")
            cursor.execute(points_update_query)
            connection.commit()
            break
        else:
            drop_query = "drop table {}".format("matchnum"+str(match_no))
            cursor.execute(drop_query)
            connection.commit()
            print("wrong team name!!")
            opt = input('try again?(y/n)')
            if opt.lower() == 'y':
                per_match()
            else:
                return
    except:
        print('Something went wrong! May be match details already entered')

def rank():
    rank_query = "select team, point, @curRank:= @CurRank + 1 as ranks from points p, (select @CurRank:=0)  r order by point desc"
    cursor.execute(rank_query)
    points_data = cursor.fetchall()
    points_print = []
    for row in points_data:
        points_print.append(list(row))
    print(tabulate(points_print, headers=['team', 'point', 'rank'], tablefmt="pretty"))

def dlt_dtl(match_numb):
    try:
        cursor.execute("select team_won from outcomes where match_no = {}".format(str(match_numb)))
        dat = cursor.fetchall()
        won_team = dat[0][0]
        tbl_dlt_query = "drop table {}".format("matchnum"+str(match_numb))
        cursor.execute(tbl_dlt_query)
        connection.commit()
        outc_dlt_query = "delete from outcomes where match_no = {}".format(match_numb)
        cursor.execute(outc_dlt_query)
        connection.commit()
        cursor.execute("update points set point = point - 2 where team = {}".format("'"+won_team+"'"))
        connection.commit()
    except:
        print("Something went wrong!")
        return

def updt_match_dtl(match_number):
    try:
        cursor.execute("select team_won, team_lost from outcomes where match_no = {}".format(match_number))
        dat = cursor.fetchall()
        print("Select the team to update: ")
        teams = []
        for i in dat[0]:
            teams.append(i)
        for j in teams:
            print(str(teams.index(j)+1)+'.', j)
        ch = int(input("choice: "))
        cursor.execute("select * from {} where team = '{}'".format("matchnum"+str(match_number), teams[ch - 1]))
        for i in cursor.fetchall():
            print(i)
        choice = int(input("What to update?\n1.Batsman\n2.Bowler\nchoices: "))
        if choice == 1:
            cursor.execute("select batsman, score from {} where team = '{}'".format('matchnum'+str(match_number), teams[ch - 1]))
            for i in cursor.fetchall():
                print(i)
            choose = input("Which batsman? (name): ")
            new_runs = int(input("enter new score for batsman: "))
            try:
                cursor.execute("update {} set score = {} where batsman = '{}'".format("matchnum"+str(match_number), new_runs, choose))
                connection.commit()
                print("updated!")
            except:
                print("Something went wrong :/")
        elif choice == 2:
            cursor.execute("select bowler, wickets from {} where team = '{}'".format('matchnum'+str(match_number), teams[ch - 1]))
            for i in cursor.fetchall():
                print(i)
            choose = input("Which bowler? (name): ")
            new_wicks = int(input("enter new wickets for bowlwer: "))
            try:
                cursor.execute("update {} set wickets = {} where bowler = '{}'".format("matchnum"+str(match_number), new_wicks, choose))
                connection.commit()
                print("updated!")
            except:
                print("something went wrong :/")
        else:
            print("wrong choice. try again.")
    except:
        print("Something went wrong!")
        return

def search(team_to_search):
    global cursor
    print('#'*60)
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
        print('Match Number', match,'won by', match_data[0][0])
        print(tabulate(match_data, headers = ["team", "batsman", "score", "bowler", "wickets"], tablefmt="pretty"))
        print('#'*60)

def whole_tour():
    cursor.execute("select * from outcomes")
    all_data = []
    for k in cursor.fetchall():
        all_data.append(k)
    print(tabulate(all_data, headers= ['Match Number', 'Winning Team', 'Losing Team'], tablefmt="pretty"))


while True:
    try:
        print("==================")
        crud = int(input("Please select:\n\t0. Exit\n\t1. Add match\n\t2. Search\n\t3. Points table\n\t4. Delete match details\n\t5. Update\n\t6. Tournament Summary\n\t7. Delete Tournament and exit\nchoice: "))
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
        elif crud == 4:
            delete = int(input("Enter match number to be deleted: "))
            dlt_dtl(delete)
            print('Match details deleted!')
        elif crud == 5:
            update = int(input("Enter match number to be updated: "))
            updt_match_dtl(update)
        elif crud == 6:
            whole_tour()
        elif crud == 7:
            drop_db()
        else:
            print("Invalid choice.")
            print("==================")
    except:
        print("Something went wrong!!")
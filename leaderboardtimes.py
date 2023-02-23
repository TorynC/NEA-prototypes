import sqlite3

class SQL: #database object 
    def __init__(self,database):
        self.database = database 
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.scores_times = self.cursor.execute("SELECT Username, TutorGroup, Score, Time FROM LoggedIn").fetchall()
        self.times = 0

    def get_high_scores(self): #method to fetch the top 5 scores from the database to be displayed in the leaderboard 
        number = 0
        count = 0
        self.scores_times.sort(key = lambda x:x[2],reverse = True) #sorting tuple using .sort and lambda, tuple fetched from database
        if len(self.scores_times)>=5:
            print("=------------------------------------------------------=")         
            print("Leaderboard (Username, Tutor group, Score, Survival time)") #displays leaderboard of top 5 players 
            for item in self.scores_times[0:5]: 
                count += 1
                print((number+count),item)   
        else:
            print("=------------------------------------------------------=")  #displays leaderboard if the database currently has less than 5 play attempts
            print("Leaderboard (Username, Tutor group, Score, Survival time)")
            for item in self.scores_times[0:len(self.scores_times)]:
                count += 1
                print((number+count),item)
            

    def get_times(self): #method to get the total time from all the attempts of players 
        for time in self.scores_times:
            self.times += int(time[3])
        
    def update_times(self): #method to update the TotalTimes table in database to have the total play time of all attempts from all players 
        data = self.times
        self.cursor.execute("INSERT INTO TotalTimes(Time) VALUES(?)",(data,))
        self.connection.commit() 
        time = self.cursor.execute("SELECT Time FROM ToTalTimes ORDER BY ID DESC LIMIT 1").fetchone()
        id = self.cursor.execute("SELECT AttemptID FROM LoggedIn ORDER BY AttemptID DESC LIMIT 1").fetchone()

        print("")
        print("The game has been played a total of",id[0],"times")
        print("Total playtime from all players:",time[0],"seconds")
        print("=------------------------------------------------------=") 

    def check_empty(self): #defensive programming, method to check that there isn't an empty entry in the score column as it will cause the sorting algorithm to not work 
        self.cursor.execute("DELETE FROM LoggedIn WHERE Score IS NULL") 
        self.connection.commit()

database = SQL("Data.db") #instantiating database object 
database.check_empty() 
database.get_high_scores()
database.get_times() 
database.update_times() #calling database object methods 

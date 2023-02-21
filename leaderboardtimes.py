import sqlite3

class SQL:
    def __init__(self,database):
        self.database = database
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.scores_times = self.cursor.execute("SELECT Username, TutorGroup, Score, Time FROM LoggedIn").fetchall()
        self.times = 0

    def get_high_scores(self):
        number = 0
        count = 0
        self.scores_times.sort(key = lambda x:x[2],reverse = True)
        if len(self.scores_times)>=5:
            print("=------------------------------------------------------=")         
            print("Leaderboard (Username, Tutor group, Score, Survival time)")
            for item in self.scores_times[0:5]:
                count += 1
                print((number+count),item)   
        else:
            print("=------------------------------------------------------=")      
            print("Leaderboard (Username, Tutor group, Score, Survival time)")
            for item in self.scores_times[0:len(self.scores_times)]:
                count += 1
                print((number+count),item)
            

    def get_times(self):
        for time in self.scores_times:
            self.times += int(time[3])
        
    def update_times(self):
        data = self.times
        self.cursor.execute("INSERT INTO TotalTimes(Time) VALUES(?)",(data,))
        self.connection.commit()
        time = self.cursor.execute("SELECT Time FROM ToTalTimes ORDER BY ID DESC LIMIT 1").fetchone()
        id = self.cursor.execute("SELECT AttemptID FROM LoggedIn ORDER BY AttemptID DESC LIMIT 1").fetchone()

        print("")
        print("The game has been played a total of",id[0],"times")
        print("Total playtime from all players:",time[0],"seconds")
        print("=------------------------------------------------------=") 

database = SQL("Data.db")
database.get_high_scores()
database.get_times()
database.update_times()

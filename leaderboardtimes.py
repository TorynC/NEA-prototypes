import sqlite3

class SQL:
    def __init__(self,database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.scores_times = self.cur.execute("SELECT Username, TutorGroup, Score, Time FROM LoggedIn").fetchall()
        self.times = 0

    def get_high_scores(self):
        number = 0
        count = 0
        self.scores_times.sort(key = lambda x:x[2],reverse = True)
        if len(self.scores_times)>=5:
            print("=------------------------------------------------------=")         
            print("Leaderboard (Username, TutorGroup, Score, Survival time)")
            for item in self.scores_times[0:5]:
                count += 1
                print((number+count),item)
            print("=------------------------------------------------------=")     
        else:
            print("=------------------------------------------------------=")      
            print("Leaderboard (Username, TutorGroup, Score, Survival time)")
            for item in self.scores_times[0:len(self.scores_times)]:
                count += 1
                print((number+count),item)
            print("=------------------------------------------------------=")     

    def get_times(self):
        for time in self.scores_times:
            self.times += int(time[3])
        print(self.times)

    def update_times(self):
        data = self.times
        self.cur.execute("INSERT INTO TotalTimes(Time) VALUES(?)",(data,))
        self.conn.commit()

database = SQL("Data.db")
database.get_high_scores()
database.get_times()
database.update_times()
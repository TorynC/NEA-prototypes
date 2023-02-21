import sqlite3

class SQL:
    def __init__(self,database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.scores_times = self.cur.execute("SELECT Username, TutorGroup, Score, Time FROM LoggedIn").fetchall()
        self.times = 0

    def get_high_scores(self):
        self.scores_times.sort(key = lambda x:x[2],reverse = True)
        print("Leaderboard by Username, TutorGroup, Score, Survival time:",(self.scores_times))
    
    '''def get_times(self):
        for time in self.scores_times:
            self.times += int(time[1])
        print(self.times)

    def update_times(self):
        data = self.times
        self.cur.execute("INSERT INTO TotalTimes(Time) VALUES(?)",8)
        self.conn.commit()'''

database = SQL("Data.db")
database.get_high_scores()
#database.get_times()
#database.update_times()
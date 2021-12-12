from tinydb import TinyDB, Query
import operator

class DBHandler():
    """Handles connections to tinydb database. Mainly for minigames
    """

    def __init__(self, user_id, minigame: str = 'cps', db_name: str = 'minigames_db'):
        self.db = TinyDB('hidden/{}.json'.format(db_name))
        self.query = Query()
        
        self.user_id = user_id
        self.minigame = minigame
        self.check_if_user_exists()
        self.check_if_minigame_exists()
        
    
    def get_highscore(self):
        """Returns highscore of current user in current game
        """
        return self.get_user_data()[self.minigame]["highscore"]

    def get_wins(self):
        """Return win counter of current user in current game
        """
        return self.get_user_data()[self.minigame]["wins"]

    def increment_wins(self):
        """Increments the win counter of the current user
        """

        data = self.get_user_data()[self.minigame]
        self.db.update({self.minigame: {'wins': data["wins"] + 1, 'highscore': data["highscore"]}}, self.query.user_id == self.user_id)


    def new_highscore(self, highscore):
        """Sets a new highscore of the current user

        Parameters
        ----------
        highscore : int
            New highscore
        """

        data = self.get_user_data()[self.minigame]
        self.db.update({self.minigame: {'wins': data["wins"], 'highscore': highscore}}, self.query.user_id == self.user_id)

    
    def check_if_user_exists(self):
        """Checks if user exists in TinyDB. If not, user is created
        """

        if len(self.db.search(self.query.user_id == self.user_id)) < 1:
            self.db.insert({'user_id': self.user_id, self.minigame: {'wins': 0, 'highscore': 0}})

    def check_if_minigame_exists(self):
        """Checks if current user already has stats for current minigame
        """
        user = self.db.search(self.query.user_id == self.user_id)[0]
        try:
            test = user[self.minigame]
            return
        except KeyError:
            self.db.update({self.minigame: {'wins': 0, 'highscore': 0}}, self.query.user_id == self.user_id)
        

    def get_leaderboard(self):
        """Returns dict of users and highscores/wins. Sorted descending by value

        Returns
        -------
        dict, dict
            highscores, wins
        """

        users = self.db.all()
        highscores = {}
        wins = {}
        
        for user in users:
            highscores[user['user_id']] = user[self.minigame]['highscore']
            wins[user['user_id']] = user[self.minigame]['wins']

        # Sort dicts by size
        highscores = dict(sorted(highscores.items(), key=operator.itemgetter(1), reverse=True))
        wins = dict(sorted(wins.items(), key=operator.itemgetter(1), reverse=True))

        return highscores, wins


    def get_minigame_list(self):
        """Returns list of minigames that have recorded stats

        Returns
        -------
        list<str>
            List of minigames
        """

        minigames = []
        users = self.db.all()
        for user in users:
            keys = list(user.keys())
            keys.remove('user_id')
            for key in keys:
                if key not in minigames:
                    minigames.append(key)

        return minigames


    def get_user_data(self):
        return self.db.get(self.query.user_id == self.user_id)


    def reset(self):
        self.db.update({self.minigame: {'wins': 0, 'highscore': 0}}, self.query.user_id == self.user_id)
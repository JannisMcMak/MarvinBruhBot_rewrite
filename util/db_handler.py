from tinydb import TinyDB, Query, where

class DBHandler():
    """Handles connections to tinydb database. Mainly for minigames
    """

    def __init__(self, user_id, minigame: str = 'cps', db_name: str = 'minigames_db'):
        self.db = TinyDB('hidden/{}.json'.format(db_name))
        self.query = Query()
        
        self.user_id = user_id
        self.minigame = minigame
        self.check_if_user_exists()
        
    
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


    def get_user_data(self):
        return self.db.get(self.query.user_id == self.user_id)


    def reset(self):
        self.db.update({self.minigame: {'wins': 0, 'highscore': 0}}, self.query.user_id == self.user_id)
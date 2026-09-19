class HighScoreManager:

    def __init__(self, filename):
        self.filename = filename
        self.highscore = 0


    def load(self):

        try:
            with open(self.filename, "r") as file:
                self.highscore = int(file.read())

        except FileNotFoundError:
            self.highscore = 0


    def save(self):

        with open(self.filename, "w") as file:
            file.write(str(self.highscore))


    def update(self, current_score):

        if current_score > self.highscore:
            self.highscore = current_score
            self.save()


    def get_highscore(self):

        return self.highscore
class Game:
    def __init__(self, id, name, files):
        self.id = id
        self.name = name
        self.files = files
        self.is_synchronized = False

    @staticmethod
    def create_from_json(game):
        files = [Game.File(file["name"], file["directory"], file["locations"]) for file in game["files"]]
        return Game(game["id"], game["name"], files)

    class File:
        def __init__(self, name, directory, locations):
            self.name = name
            self.directory = directory
            self.locations = locations
import json

class jsonReader:


    def saveGame(self, data):
        with open("savedata.json", "w") as f:
            json.dump(data,f,indent=4)
            f.close()

    def loadGame(self):
        data = None
        try:
            with open("savedata.json", "r") as f:
                data = json.load(f)
                f.close()
        except FileNotFoundError:
            print('No saved data exists.')
            
        return data
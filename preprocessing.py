
class Preprocessing():

    # Constructor
    def __init__(self, d):
        self.data = d

    def removeAttributes(self, param):
        print("PREPROCESSING/RemoveAttributes: %s" % (param))
        # TODO:
        # Poistetaan datajoukosta turhat attribuutit 
        # (riippuen käyttäjän tekemästä valinnasta)

    def normalizeData(self):
        print("PREPROCESSING/Normalize: %s" % self.data)
        # TODO:
        # Normalisoidaan data

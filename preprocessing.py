
class Preprocessing():

    # Constructor
    def __init__(self, d):
        self.data = d

    def removeAttributes(self, param):
        print("PREPROCESSING/RemoveAttributes: %s" % (param))
        # TODO:
        # Poistetaan datajoukosta turhat attribuutit 
        # (riippuen käyttäjän tekemästä valinnasta)
        #
        # Tätä ei itse asiassa tarvitsekaan (klusteroinnin puolesta) tehdä, 
        # jos antaa klusterointiin parametrina listan ignored_keys=['Att1', 'Att2', 'jne']
        # niin ko. attribuutit jätetään huomioimatta etäisyyksiä laskiessa.

    def normalizeData(self):
        print("PREPROCESSING/Normalize: %s" % self.data)
        # TODO:
        # Normalisoidaan data

    # HUOM: Klusterointi (k-Means) odottaa nyt,
    # että kaikki etäisyyslaskentaan liittyvät
    # attribuutit ovat float-tyyppiä, eli se 
    # olisi hyvä huomioida täällä esikäsittelyssä.
    # (Muunto tehty siis nyt väliaikaisesti 
    # "vasta" klusteroinnin yhteydessä)
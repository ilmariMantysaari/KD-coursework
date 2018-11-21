from collections import OrderedDict

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
        
        #Dictionary kullekin attribuutille
        attributes = {}

        #Luodaan dictionaryt ja alustetaan ne tyhjillä listoilla
        for att in self.data[0]:
            attributes[att] = []

        #Täytetään asiaankuuluvat dictionaryt self.datan arvoilla
        for row in self.data: 
            for att in row:
                attributes[att].append(row[att])

        #Käydään attribuutti-dictionarya läpi attribuutti kerrallaan
        for att in attributes:
            try:
                #Otetaan attribuutin arvojoukon min- ja max-arvot
                minValue = float(min(attributes[att]))
                maxValue = float(max(attributes[att]))

                #Alustetaan tyhjä lista
                normalizedList = []

                #Käydään attribuutin arvoja läpi
                for value in attributes[att]:
                    #Normalisoidaan arvo min-max-normalisoinnilla
                    value =  (float(value) - minValue) / (maxValue - minValue)
                    normalizedList.append(value)

                #Lopuksi korvataan attribuutin arvot normalisoiduilla arvoilla.
                attributes[att] = normalizedList

            #Napataan ValueError, jos muuntaminen floatiksi ei onnistu.
            except ValueError:
                print("Can't be string!")

        #Tässä osassa dictionary-rakenne muutetaan alkuperäiseen OrderedDict-listaan.
        i = 0
        newlist = []
        while i < len(self.data):
            rowdict = {}
            for att in self.data[i]:
                rowdict[att] = attributes[att][i]
            od = OrderedDict(rowdict)
            newlist.append(od)
            i += 1

        return newlist

    # HUOM: Klusterointi (k-Means) odottaa nyt,
    # että kaikki etäisyyslaskentaan liittyvät
    # attribuutit ovat float-tyyppiä, eli se 
    # olisi hyvä huomioida täällä esikäsittelyssä.
    # (Muunto tehty siis nyt väliaikaisesti 
    # "vasta" klusteroinnin yhteydessä)
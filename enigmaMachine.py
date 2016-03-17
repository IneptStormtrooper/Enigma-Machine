"""
This replicates an enigma Machine as used by the germans during ww2.
It can encrypt and decrypt strings with the proper tumblers.
When inputting a string for encryption/decryption it will assume the first n (where n is the number of tumblers)
 characters are used for setting the initial tumbler rotation, as how it was done with german machines
 Does not rely on specific tumblers or settings as they must all be inputted by the user,
  giving more security to the device
"""


# TODO:
# Nothing currently

import enigmaTumbler

class enigmaMachine:

    """
    tumblerList -> a list of enigmaTumblers
    plgBrd -> a dictionary containing letter mappings (eg dict["a"] = "Q")
    either one
    """
    def __init__(self, tmblrList = [], plgBrd = {}):
        self.tumblerList = tmblrList
        self.plugBoard = plgBrd

    def __str__(self):
        i = ""
        for item in self.tumblerList:
            i += str(item)
            i += " "
        return i

    def __doPlugBoard(self, string):
        retString = ""
        for loc, char in enumerate(string):
            try:
                retString += self.plugBoard[char]
            except KeyError:
                retString += string[loc]
        return retString


    # takes in a string to encrypt and returns the encrypted string
    # after the process is finished it resets the tumblers for the next encryption / decryption
    def encrypt(self, encryptString):
        retString = ""
        encryptString = self.__doPlugBoard(encryptString)
        # loop over decryptString and pass each char into tumblers to decrypt it
        for location, char in enumerate(encryptString):
            if location == len(self.tumblerList):# change tumbler settings based on first n letters
                self.setTumblerRotation(retString)
            for tumbler in self.tumblerList:    # loop through tumblers forward
                char = tumbler.getEncryptChar(char)

            char = self.tumblerList[0].flip(char)

            for tumbler in reversed(self.tumblerList):  # loop backward to mimic reflector plate in enigma
                char = tumbler.getEncryptChar(char)

            self.tumblerList[0].increment()     # rotate first tumbler by one
            for count, tumbler in enumerate(self.tumblerList):
                # see if any other tumbler can be incremented based on rotationSetting of previous tumbler
                if (tumbler.rotSetting == tumbler.rotLoc) and count != len(self.tumblerList):
                        self.tumblerList[count].increment()

            retString+=char # combine all decrypted chars into retString
        for tumbler in self.tumblerList:    # resets all the tumblers in the machine to original setting
            tumbler.reset()
        return retString

    # takes in a string to decrypt and returns the decrypted string
    # after the process is finished it resets the tumblers for the next encryption / decryption
    def decrypt(self, decryptString):
        retString = ""
         # loop over decryptString and pass each char into tumblers to decrypt it
        for location, char in enumerate(decryptString):
            if location == 3:
                self.setTumblerRotation(decryptString[:3])
            for tumbler in self.tumblerList:    # loop through tumblers forward
                char = tumbler.getDecryptChar(char)

            char = self.tumblerList[0].flip(char)

            for tumbler in reversed(self.tumblerList):  # loop backward to mimic reflector plate in enigma
                char = tumbler.getDecryptChar(char)

            self.tumblerList[0].increment()     # rotate first tumbler by one
            for count, tumbler in enumerate(self.tumblerList):
                # see if any other tumbler can be incremented based on rotationSetting of previous tumbler
                try:
                    if (tumbler.getRotSetting() == tumbler.getRotLoc()) and count != len(self.tumblerList):
                        self.tumblerList[count].increment()
                except TypeError:
                    if (tumbler.getRotSetting() in tumbler.getRotLoc()) and count != len(self.tumblerList):
                        self.tumblerList[count].increment()

            retString+=char # combine all decrypted chars into retString
        for tumbler in self.tumblerList:    # resets all the tumblers in the machine to original setting
            tumbler.reset()

        retString = self.__doPlugBoard(retString)
        return retString    # return finished string leaving off the first 3 characters which aren't part of message

    # creates and then adds an enigmaTumbler to the list of tumblers the machine uses
    """
    substitutionString -> (string) containing the randomized alphabet the
        Tumbler uses when calculating encryption/decryption chars
    rotationLoc -> a (list of ints) donoting position(s) of where the
        tumbler will rotate the next tumbler in the sequence
    rotationSetting -> (int) starting rotation position of the tumbler
        this value is saved in origSetting to allow tumbler to be reset after each encryption/decryption
    """
    def addTumbler(self, substitutionString, rotationLocation = 0, rotationSetting = 0):
        self.tumblerList.append(enigmaTumbler.enigmaTumbler(substitutionString, rotationLocation, rotationSetting))

    # sets tumbler Rotation of all tumblers to location of char in alphabet
    # uses the first n characters of decrypt/encrypt string using the plaintext chars
    # after this the tumblers will have a different rotation start point so the encryption changed
    def setTumblerRotation(self, charSettings):
        for loc, tumbler in enumerate(self.tumblerList):
            tumbler.setRotSetting(charSettings[loc])

    """
        paramater setting is a string of 2 characters
        they are the in and out settings for the pludboard
        they are added in both directions so doing "al" is equivalent to both "al" and "la"
    """
    def addPlufBoard(self, setting):
        self.plugBoard[setting[0]] = setting[1]
        self.plugBoard[setting[1]] = setting[0]


def main():
    tmb1 = enigmaTumbler.enigmaTumbler("xytrhknpi causwmbqe.fdzolgjv", 10, 0)
    tmb2 = enigmaTumbler.enigmaTumbler("aektp.iyvmcfzqlrnsw odbxhguj", 4, 0)
    tmb3 = enigmaTumbler.enigmaTumbler("uigefkxmoy.dhlcnwptrzbav qjs", 0, 0)

    machine = enigmaMachine([tmb2, tmb3, tmb1], {"l":"a","a":"l"})

    print(machine.encrypt("hello world"))
    print("")
    print(machine.decrypt(machine.encrypt("hello world")))


    #print(machine.encrypt("still testing to see if the machine still works
    # for extra long strings that will cause the tumblers to turn"))
    #print("")
    #print(machine.decrypt("mryfwveica xdzcthmxiemxerbkkzvjtnpikcumjgy
    # bfmxexpyzppucv wtpwkcukzrlfhjqs  zmykbisyclvereeulhdmqzmvnl .l.g"))


if __name__ == "__main__":
    main()
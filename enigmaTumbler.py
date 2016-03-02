"""
Represents a single tumbler in an enigma machine

"""
import string

class enigmaTumbler:

    alphabet = string.ascii_lowercase
    alphabet += " ."
    # this is the default alphabet the tumbler will use when undergoing encryption/decryption
    # if a character is not in this alphabet and is attempted to be encryption/decryption it will fail

    # enigmaTumbler constructor
    """
    substitutionString -> (string) containing the randomized alphabet the Tumbler uses when calculating encryption/decryption chars
    rotationLoc -> a (list of ints) donoting position(s) of where the tumbler will rotate the next tumbler in the sequence
    rotationSetting -> (int) starting rotation position of the tumbler
        this value is saved in origSetting to allow tumbler to be reset after each encryption/decryption
    """
    def __init__(self, substitutionString, rotationLocation = 0, rotationSetting = 0):
        self.subString = substitutionString
        self.rotLoc = rotationLocation
        self.rotSetting = int(rotationSetting)
        self.origSetting = int(rotationSetting)

    def __str__(self):
        return self.subString + "; " + str(self.rotLoc) + "; " + str(self.rotSetting) + "; " + str(self.origSetting)

    # returns encrypted char after it is sent through a single tumbler
    def getEncryptChar(self, char):
        alphLoc = self.alphabet.find(char)  #find location of letter in ascii alphabet
        if alphLoc + self.rotSetting >= len(self.subString):    #
            alphLoc = (alphLoc + self.rotSetting) - len(self.subString)
        else:
            alphLoc+=self.rotSetting
        return self.subString[alphLoc]

    # returns decrypted char after it is sent through a single tumbler
    def getDecryptChar(self, char):
        alphLoc = self.subString.find(char)
        if alphLoc - self.rotSetting < 0:
            alphLoc = len(self.subString) - (self.rotSetting - alphLoc)
        else:
            alphLoc-=self.rotSetting
        return self.alphabet[alphLoc]

    # mimics the reflector plate in an enigma machine
    # if the parameter char is in the first half of the alphabet, add 14 to its position and that is the returned char
    # if the parameter char is in the last half of the alphabet, subtract 14 to its position and that is the returned char
    def flip(self, char):
        if self.alphabet.index(char) < len(self.alphabet)/2:
            return self.alphabet[self.alphabet.index(char)+14]
        else:
            return self.alphabet[self.alphabet.index(char)-14]

    # sets the rotLoc of the tumbler to wherever the given char is in  the standard alphabet
    def setRotLoc(self, char):
        self.rotLoc = enigmaTumbler.alphabet.index(char)

    def setRotSetting(self, char):
        self.rotSetting = enigmaTumbler.alphabet.index(char)

    # returns the location on the tumbler of where it rotates
    def getRotLoc(self):
        return self.rotLoc

    # returns the current rotation setting of tumbler
    def getRotSetting(self):
        return self.rotSetting

    # increases the rotation setting of self by one
    # if this value is equal to length of string, set it to zero
    def increment(self):
        self.rotSetting+=1
        if self.rotSetting == len(self.subString):
            self.rotSetting = 0

    # resets tha rotation setting of the tumbler to what is was when created for use after either encryption/decryption
    def reset(self):
        self.rotSetting = self.origSetting

    def getAlphabet(self):
        return self.alphabet
import requests
import os
import random
import Functions

class functions:
    def __init__(self):
        pass
    def coder(self, str):
        if (len(str) <= 3):
            random_number = ''.join(random.choices('abcdefghijklmnopqrstwxyz', k=3))
            random_number_2 = ''.join(random.choices('abcdefghijklmnopqrstwxyz', k=3))
            str = str.lower()
            str_reverse = str[::-1]
            Encoded = random_number + str_reverse + random_number_2
            return Encoded
        elif (len(str) > 3):
            random_number = ''.join(random.choices('abcdefghijklmnopqrstwxyz', k=3))
            random_number2 = ''.join(random.choices('abcdefghijklmnopqrstwxyz', k=3))
            str = str.lower()
            str_reverse = str[::-1]
            Encoded = random_number + str_reverse + random_number2
            return Encoded


    def decoder(self, str):
        if (len(str) > 3):
            Encoded = str[3:-3]
            Encoded = Encoded[::-1]
            Decoded = Encoded.capitalize()
            return Decoded
        elif (len(str) < 3):
            Encoded = str[3:-3]
            Encoded = Encoded[::-1]
            Decoded = Encoded.capitalize()
            return Decoded

    def Words_Capitalzer(self, Obj, p=''):
        if p != '':
            if type(Obj) == str:
                String2 = Obj.split()
                Final_Print = ''
                for i in range(len(String2)):
                    Final_Print = list(Final_Print)
                    Final_Print.append(String2[i].capitalize())

                Join = ' '.join(Final_Print)

                print(Join)
            elif type(Obj) == list:
                Words = []
                for i in range(len(Obj)):
                    Words.append(Obj[i].capitalize())

            print(Words)
        elif p == '':
            if type(Obj) == str:
                String2 = Obj.split()
                Final_Print = ''
                for i in range(len(String2)):
                    Final_Print = list(Final_Print)
                    Final_Print.append(String2[i].capitalize())

                Join = ' '.join(Final_Print)

                return(Join)
            elif type(Obj) == list:
                Words = []
                for i in range(len(Obj)):
                    Words.append(Obj[i].capitalize())

                return(Words)


    def Words_Upper(self, Obj, p=''):
        if p != '':
            if type(Obj) == str:
                String2 = Obj.split()
                Final_Print = ''
                for i in range(len(String2)):
                    Final_Print = list(Final_Print)
                    Final_Print.append(String2[i].upper())

                Join = ' '.join(Final_Print)

                print(Join)
            elif type(Obj) == list:
                Words = []
                for i in range(len(Obj)):
                    Words.append(Obj[i].upper())

                print(Words)
        elif p == '':
            if type(Obj) == str:
                String2 = Obj.split()
                Final_Print = ''
                for i in range(len(String2)):
                    Final_Print = list(Final_Print)
                    Final_Print.append(String2[i].upper())

                Join = ' '.join(Final_Print)

                return(Join)
            elif type(Obj) == list:
                Words = []
                for i in range(len(Obj)):
                    Words.append(Obj[i].upper())

                return(Words)

    def Words_Lower(self, Obj):
        if type(Obj) == str:
            String2 = Obj.split()
            Final_Print = ''
            for i in range(len(String2)):
                Final_Print = list(Final_Print)
                Final_Print.append(String2[i].lower())
                
            Join = ' '.join(Final_Print)

            return Join
        elif type(Obj) == list:
            Words = []
            for i in range(len(Obj)):
                Words.append(Obj[i].capitalize())

            return Words
        
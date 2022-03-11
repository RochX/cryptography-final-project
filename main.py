#!/usr/bin/python

import random
import csv
import sys
# CLA
# (Dictionary) Database of authorized voters
# First Name, Last Name, SSN, verification

# CTF
# Verification, Canditate, voted


# User "Signs up" generate random verification if valid. Send back encrypted DHE to AES, include signature

# CLA send encrypted list of verification numbers to CTF

# Using their verification numbers, vote with CTF

# CTF publicly prints results


# Virtual Election Booth Project

 # TODO add key exchange to CLA and CTF

class CTF:
    def __init__(self):
        self.candidates = {"Captain Blackbeard": {}, "Miss Fortune": {} }
        self.ids = {}                                                       # Dictionary of validation Ids that have been generated and sent fron CLA
        self.loadTally()

    def vote(self,candidate,id,username):
        if int(id) in CTF.ids:
            for key in self.candidates:
                if str(id) in self.candidates[key].keys():
                    return "You already voted."
            for key in self.candidates:
                if key == candidate:
                    self.candidates[key][id] = username
                    self.saveVoteTally(False)
            return "Congrats! You voted!"
        elif len(CTF.ids) == 0:
            return "Voting period has not begun yet.\n"
        else:
            return "You did not register in time.\n"

    def tally(self):
        print("\nVote Tally\n-----------")
        for key in self.candidates:
            print(key + ": " + str(len(self.candidates[key])))

    def loadTally(self):
        self.candidates = {}
        #read csv, and split on "," the line
        csv_file = csv.reader(open('tally.csv', "r"), delimiter=",")

        #loop through the csv list
        for row in csv_file:
            first = True
            user = False
            key = "name"
            for item in row:
                if first:
                    self.candidates[item] = {}
                    first = False
                    key = item
                else:
                    if not user :
                        idName = item
                        user = True
                    else:
                        self.candidates[key][idName] = item
                        user = False

    # Function to save any CTF updates.
    def saveVoteTally(self,reset):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('tally.csv', "r"), delimiter=",")

        # data rows of csv file 
        rows = []

        if reset:
            rows.append(['Captain Blackbeard'])
            rows.append(['Miss Fortune'])
        else:
            for key in self.candidates:
                candidateData = []
                candidateData.append(key)
                for item in self.candidates[key]:
                    print(item)
                    candidateData.append(item)
                    candidateData.append(self.candidates[key][item])
                rows.append(candidateData)

        # name of csv file 
        filename = "tally.csv"
    
        # writing to csv file 
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 

            # writing the data rows 
            csvwriter.writerows(rows)

# Class meant to represent the CLA and the functions it may need
class CLA:
    def __init__(self):
        self.auth_dict = {}     # Dictionary of Authorized Voter. This uses their SSN as a key, with an array of their first name, last name and validation number 
        self.ids = {}           # Dictionary of validation Ids that have been generated and will be sent to the CTF
        self.loadVoters()       # Intializes data upon start of program.

    # Function to "Register" a user. It checks if they are a valid voter and have not registered yet, then generated a key.
    def validate(self,SSN,first,last):
        if SSN in self.auth_dict:
            if self.auth_dict[SSN][0] == first and self.auth_dict[SSN][1] == last:
                if self.auth_dict[SSN][2] == -1:
                    random.seed(89)
                    idSearch = True
                    while idSearch is True:
                        id = random.randint(0,3000000)
                        if id not in self.ids:
                            self.auth_dict[SSN][2] = id
                            self.ids[id] = True
                            idSearch = False
                    self.saveVoters(False)
                    return "Congrats " + self.auth_dict[SSN][0] + " " + self.auth_dict[SSN][1] + " your verification number is " + str(self.auth_dict[SSN][2]) + "!"
                else:
                    return "You're already registered to vote."
            else:
                return "The SSN and name you entered do not match the database pair."
        else:
            return "The social security number you entered, " + SSN + ", is not authorized to vote."

    # Function to load Voter data from the "voter_auth.csv" file
    def loadVoters(self):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('voter_auth.csv', "r"), delimiter=",")

        #loop through the csv list
        for row in csv_file:
            if row[0] != "SSN":
                self.auth_dict[row[0]] = ['N/A','N/A','N/A',-1]
                self.auth_dict[row[0]][0] = row[1]
                self.auth_dict[row[0]][1] = row[2]
                self.auth_dict[row[0]][2] = int(row[3])
                if int(row[3]) != -1:
                    self.ids[int(row[3])] = True

    # Function to save any CLA updates. One boolean parameter to determine if user data is being reset.
    def saveVoters(self,reset):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('voter_auth.csv', "r"), delimiter=",")

        # field names 
        fields = ['SSN', 'first', 'last', 'id'] 
    
        # data rows of csv file 
        rows = []
        
        if reset == True:
            for item in self.auth_dict:
                rows.append( [item,self.auth_dict[item][0],self.auth_dict[item][1],"-1"] )
                self.auth_dict[item][2] = -1
                self.ids = {}
        else:
            for item in self.auth_dict:
                rows.append( [item,self.auth_dict[item][0],self.auth_dict[item][1],self.auth_dict[item][2]] )

        # name of csv file 
        filename = "voter_auth.csv"
    
        # writing to csv file 
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
        
            # writing the fields 
            csvwriter.writerow(fields) 
        
            # writing the data rows 
            csvwriter.writerows(rows)

    def sendIDs(self,CTF):
        CTF.ids = self.ids
        return "ID list sent\n"


if __name__ == '__main__':
    # First Time Setup at program start
    CLA = CLA()
    CTF = CTF()
    print("Welcome to the Virtual Voting Booth!\n")
    running = True
    
    # Interactable user loop.
    while (running):
        menuChoice = input("Please type the number associated with the action below.\n1. Register to Vote\n2. Vote for a Candidate\n3. Reset Voting Pool\n4. CLA sends the ID list to CTF\n5. CTF Tallies Votes\n6. Quit\n")
        menuChoice = menuChoice.strip()

        if (menuChoice == '1'):
            SSN = input("What is your social security number?\n").strip()
            if len(SSN) == 9:
                first = input("What is your first name?\n").strip()
                last = input("What is your last name?\n").strip()
                print(CLA.validate(SSN,first,last))
            else:
                print(SSN + " is not a valid SSN")
        elif (menuChoice == '2'):
            for key in CTF.candidates.keys():
                print(key)
            voteChoice = input("Please type the name exactly as above that you would like to vote for.\n")
            if voteChoice in CTF.candidates:
                ID = input("Please type your verification ID.\n")
                username = input("Please give an anonymous username to see yourself in the tallyboard.\n")
                print(CTF.vote(voteChoice,int(ID),username))
            else:
                print(voteChoice + " is not on the ballot.\n")
        elif (menuChoice == '3'):
            CLA.saveVoters(True)
            CTF.saveVoteTally(True)
            print("Voting Data Reset\n")
        elif (menuChoice == '4'):
            print(CLA.sendIDs(CTF))
        elif (menuChoice == '5'):
            CTF.tally()
        elif (menuChoice == '6'):
            print("Program Terminating\n")
            running = False
        elif (menuChoice == 'Print CTF ids'):
            print(CTF.ids)
            print(" ")
        elif (menuChoice == 'Print CTF candidates'):
            print(CTF.candidates)
            print(" ")
        elif (menuChoice == 'Print CLA ids'):
            print(CLA.ids)
            print(" ")
        elif (menuChoice == 'Print CLA auth_dict'):
            print(CLA.auth_dict)
            print(" ")
        else:
            print(menuChoice + " is not a viable option. Please select an option from the list.\n")
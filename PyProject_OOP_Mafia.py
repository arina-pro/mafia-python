class Citizen(object):
    """Represents a citizen."""
    def __init__(self, number, karma=0, city='', vote=0, checked=0):
        self.number = number
        self.karma = karma
        self.city = city_name
        self.vote = vote
        self.checked = checked
    karma_type = ['peaceful', 'mafia']

    def __str__(self):
        return 'Citizen #%s [%s]' % (self.number, Citizen.karma_type[self.karma])

class City(object):
    """Represents a city."""
    def __init__(self, name=''):
        self.citizens = []
        self.name = city_name
        mafia_count = 0
        import random
        for i in range(10):
            citizen = Citizen(i+1)
            if mafia_count < 3:
                citizen.karma = random.randint(0, 1)
                if citizen.karma:
                    mafia_count = mafia_count + 1
            citizen.city = self.name
            self.citizens.append(citizen)
        self.mafia = [citizen for citizen in self.citizens if citizen.karma]
                
    def __str__(self):
        city = []
        for citizen in self.citizens:
            city.append(str(citizen))
        return 'Citizens of %s:\n' % (self.name) + '\n'.join(city)

    def city_life(self):
        """Operates mafia, comissar duty and daily voting"""
        #Runs the activity until all mafia or every peaceful citizen is dead
        while len(self.citizens) - len(self.mafia) > 1 and len(self.mafia) != 0:
            print('Nighttime arrived at', self.name,'City.')
            self.kill()
            skip = self.check()
            print('Daytime arrived at', self.name,'City.')
            if skip:
                print('No voting for today!\n')
                continue
            self.vote([i.number for i in self.citizens])
        #Prints the outcome of the game
        if len(self.mafia) == 0:
            print('All the mafia has been eradicated! You fulfilled your duty as a commissar.')
        else:
            self.kill()
            print('The mafia has won. Good luck next time!')

    def check(self):
        """Checks whether a particular citizen is peaceful or a mafiosi"""
        skip = False
        print('Time to check! Available options for checking:\n')
        [print('Citizen #'+str(i.number)) for i in self.citizens if not i.checked]
        print('\nSo far you have checked:')
        [print(i) for i in self.citizens if i.checked]
        vote_user = int(input('\nPlease enter the number of the citizen you want to check.\n'))
        for i in self.citizens:
            if i.number == vote_user:
                print(str(i)+'\n')
                i.checked=True
                if i in self.mafia:
                    print('Congratulations! You have found a mafiosi.')
                    print('Tomorrow trial will be skipped.\n')
                    for j in range(len(self.citizens)):
                        if self.citizens[j].number == i.number:
                            print(self.citizens.pop(j),'has been rightfully executed.\n')
                            self.mafia.remove(i)
                            break
                    skip = True
        return skip

    def kill(self):
        """Randomly 'kills' a peaceful citizen"""
        import random
        killed = False
        while not killed:
            victim_num = random.randrange(len(self.citizens))
            if self.citizens[victim_num] not in self.mafia:
                print(self.citizens.pop(victim_num),'has been killed by mafia tonight.\n')
                killed = True

    def vote(self, vote_range):
        """Imitates the voting for who is the mafia"""
        print('Time to vote! Available options for voting:\n')
        [print('Citizen #'+str(i)) for i in vote_range]
        print('\nSo far you have checked:')
        [print(i) for i in self.citizens if i.checked]
        vote_user = int(input('\nPlease enter the number of the citizen you vote for.\n'))
        import random
        for citizen in self.citizens:
            voted = False
            #User's vote is recorded
            if citizen.number == vote_user:
                citizen.vote = citizen.vote + 1
            #Mafia only votes for a random peaceful citizen
            if citizen.karma:
                while not voted:
                    vote_num = random.choice(vote_range)
                    if citizen.number != vote_num:
                        for votee in self.citizens:
                            if votee.number == vote_num and not votee.karma:
                                votee.vote = votee.vote + 1
                                voted = True
                                break
            #Peaceful citizens randomly vote for those who were not checked
            else:
                while not voted:
                    vote_num = random.choice(vote_range)
                    if citizen.number != vote_num:
                        for votee in self.citizens:
                            if votee.number == vote_num and not votee.checked:
                                votee.vote = votee.vote + 1
                                voted = True
                                break
        #Calculates the maximum vote and gives the outcome (execution)
        self.maxVote()
        
    def maxVote(self):
        """Finds the citizen with the highest vote and executes them"""
        max_vote = -1
        for citizen in self.citizens:
            if max_vote == citizen.vote:
                vote_range_local.append(citizen.number)
            if max_vote < citizen.vote:
                max_vote = citizen.vote
                vote_range_local = [citizen.number]
                global votee
                votee = citizen
        self.clearVotes()
        #Invokes the voting again if more than one citizen has the highest vote
        if len(vote_range_local) > 1:
            print('Multiple citizens have been voted for equally. Re-vote!\n')
            self.vote(vote_range_local)
        #'Justfully' executes the unfortunate peaceful citizen or mafia member
        for i in range(len(self.citizens)):
                if self.citizens[i].number == votee.number:
                    print(self.citizens.pop(i),'has been executed in court today.\n')
                    if votee in self.mafia:
                        self.mafia.remove(votee)
                    break

    def clearVotes(self):
        """Clears the previous voting"""
        for citizen in self.citizens:
            citizen.vote = 0
            
def printCity():
    """Prints the list of citizens and their karma of the current city"""
    print(city_cur)

def game():
    """Let's play the Mafia game!"""
    global city_name
    while True:
        print('Hello! You are a commissar who was transferred to a city corrupted by mafia.\n')
        city_name = str(input('Please enter the name of the city.\n'))
        city_cur = City(city_name)
        city_cur.city_life()
        reply = str(input('Want to play again? Y/N\n'))
        if reply == 'N':
            break
game()

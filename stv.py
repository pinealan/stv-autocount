class election:
    # ncandi: number of running candidates
    # nvote: number of valid votes
    # nseats: number of avaiable seats
    def __init__(self, n, v, s):
        self.ncandi = n
        self.nvotes = v
        self.nseats = s
        self.candidates = []
        self.votes = []

    # candidate names from a list
    def load_candidates(self, names):
        if len(names) == self.ncandi:
            for i in range(self.ncandi):
                self.candidates.append(candidate(names[i], i))
        else:
            raise TypeError('Incorrect number of candidate names')

    # load all the votes from a list/tuple
    def load_votes(self, votes):
        self.votes = [vote(i) for i in votes]  # calls constructor on each vote
        
    # main function that finds the election results
    def run(self):
        round_ = 1  # trailing underscore to avoid clasing with default maths round() function
        nelect = 0  # number of elected candidates
        nelimi = 0  # number of eliminated candidates
        quota = (self.nvotes / (self.nseats + 1)) + 1  # Droop quota

        # initialisation, distribute votes to their first chocies
        for i in self.votes:
            for j in range(self.ncandi):
                if i.rank[j] == 1:
                    self.candidates[j].add(i.weight)
                    self.candidates[j].votes.append(i)

        print ('Quota: ' + str(quota) + '  (E: Elected;  P: Pending;  O: Out)\n')
        self.output('', [i.name for i in self.candidates])
        self.output('Round ' + str(round_) + ':', [i.nvotes for i in self.candidates])

        # begins the stv process, one loop being one round
        while nelect < self.nseats:


            # checks if there enough remaining candidates to fill remaining seats, all passes if just enough
            if self.nseats >= self.ncandi - nelimi:
                for i in self.candidates:
                    if i.status == 'P':
                        i.status = 'E'
                        nelect = nelect + 1
                        print(' ' + i.name + ' elected')
                break

            # finds new candidates with passing quota
            flag = False
            for i in self.candidates:
                if i.status =='P':  # logical error checking
                    if i.nvotes >= quota:
                        i.status = 'PE'
                        nelect = nelect + 1
                        print(' ' + i.name + ' elected')
                        flag = True

            # deals with transfering votes from elected candidates
            if flag == True:
                for i in self.candidates:
                    if i.status =='PE':
                        i.status = 'E'
                        excess = (i.nvotes - quota)/i.nvotes # percentage excess votes
                        self.transfer(i, excess)

            else:

                # if no one met quota, eliminate a candidate
                min_ = self.nvotes
                min_candi = -1
                for i in self.candidates:
                    if i.status == 'P':
                        if i.nvotes < min_:
                            min_ = i.nvotes
                            min_candi = i.candi_no
                self.candidates[min_candi].status = 'O'
                print(' ' + self.candidates[min_candi].name + ' eliminated')
                self.transfer(self.candidates[min_candi], 1)
                nelimi = nelimi + 1
            
            self.output('  state', [i.status for i in self.candidates])
            print()
            round_ = round_ + 1
            self.output('Round ' + str(round_) + ':', [i.nvotes for i in self.candidates])

        self.output('Final:', [i.status for i in self.candidates])

    # transfer votes from one candidate
    def transfer(self, candidate, weight):
        total_trans = [0 for i in range(self.ncandi)]
        for i in candidate.votes:

            # update weight and transfer excess votes
            i.next(weight)
            for j in self.candidates:
                if j.status == 'P' and i.level == i.rank[j.candi_no]:
                    j.votes.append(i)
                    j.add(i.weight)
                    candidate.add(-i.weight)
                    total_trans[j.candi_no] = total_trans[j.candi_no] + i.weight
                    total_trans[candidate.candi_no] = total_trans[candidate.candi_no] - i.weight
        self.output('  trans', total_trans)

    @staticmethod
    def output(title, alist):
        outcome = '{0:<10}'.format(title)
        for i in alist:
            if type(i) == float:
                outcome = outcome + '{0:^10.2f}'.format(i)
            else:
                outcome = outcome + '{0:^10}'.format(i)
        print(outcome)

class vote:
    # rank: rank of candidate preference of this particular ballot
    # ballot_no: vote number (for validation purposes, not sure if this is currently used)
    def __init__(self, r, n = -1):
        self.rank = r
        self.weight = 1
        self.level = 1
        self.ballot_no = n

    def next(self, proportion):
        self.level = self.level + 1
        self.weight = self.weight * proportion


class candidate:
    # nvotes: number of votes
    # state: status of the candidates, 'E' = elected, 'PE' = elected but extra votes not transfered, 'P' = pending, 'O' = out (eliminated)
    def __init__(self, name, n):
        self.name = name
        self.nvotes = 0
        self.status = 'P'
        self.votes = []
        self.candi_no = n

    def add(self, weight):
        self.nvotes = self.nvotes + weight

# By Alan Chan, May 2016
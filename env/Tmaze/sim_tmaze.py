import numpy as np
import sys
from simul import Simulator
from PyPOMDP.pypomdp.parsers import PomdpParser
from collections import Counter
from src.pdfa import PDFA


class RDPState:
    # dataset stored as a *static* (shared) attribute
    Data = None

    # store sets of symbols in traces
    Act = None
    Obs = None
    Rew = None
    Trp = None

    def __init__(self, name, cand=None, a='A', o='a', r='r'):
        self.name = name
        self.a = a
        self.o = o
        self.r = r
        self.parent = cand
        if cand == None:
            # if the state has no parent, create the state q0 with the entire dataset
            self.t = 0
            self.ix = range(self.Data.shape[0])
        else:
            # else extract the indices of traces that are consistent with (a,o)
            ao = f'{a}{o}'
            self.t = cand.t + 1
            self.ix = [i for i in cand.ix if ao in self.Data[i, cand.t]]

        # print(self.ix)
        # self.Data[self.ix, self.t:, :] now contains the traces of the RDP state

    def operatorC11(self):
        # compute the empirical probabilities of each *action*
        ct = Counter([x for elem in self.Act[self.ix, self.t] for x in elem])
        actprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]


        # compute the empirical probabilities of each *observation*
        ct = Counter([x for elem in self.Obs[self.ix, self.t] for x in elem])
        obsprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]


        # compute the empirical probabilities of each *reward*
        ct = Counter([x for elem in self.Rew[self.ix, self.t] for x in elem])
        rewprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]


    def operatorC13(self):
        # compute the empirical probabilities of each *triplet*
        ct = Counter([x for elem in self.Trp[self.ix, self.t] for x in elem])
        trpprob = [(k, v / len(self.ix)) for (k, v) in ct.most_common()]
        return np.array(trpprob)


# incomplete function, intention is to learn an RDP with horizon H
def learnRDP(H,thres):
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    Q_prev = [q0]
    for h in range(H + 1):
        Q_promoted = []
        Q_t = get_candidates(Q_prev, pdfa)
        # promote the most frequent candidate
        # add_transition parameters:
        pdfa.add_transition(Q_t[0].parent, Q_t[0])
        Q_promoted.append(Q_t[0])
        Q_t = remove_candidate(Q_t)  # removing the promoted candidate
        while len(Q_t) > 0:
            for q_promoted in Q_promoted:
                similar = test_distinct(Q_t[0], q_promoted, H, thres)
                if not similar:
                    if q_promoted == Q_promoted[-1]:
                        # promote candidate
                        pdfa.add_transition(Q_t[0].parent, Q_t[0])
                        Q_promoted.append(Q_t[0])
                        break

                else:
                    # merge_routine (have to merge the suffixes as well)
                    # print("merging ", Q_t[0].name, " with ", q_promoted.name)
                    pdfa.add_transition(Q_t[0].parent, q_promoted, True, Q_t[0])
                    # Q_promoted.remove(q_promoted)
                    # Q_promoted.append(q_promoted_new)
                    # print("erge", q_promoted.ix,Q_t[0].ix, q_promoted_new.ix)
                    break

            Q_t = remove_candidate(Q_t)

        # set Q_prev to Q_promoted
        Q_prev = Q_promoted

    return pdfa


# simulate K episodes of Tmaze with horizon H
def simTMaze(filename, K, H):
    # store the episodes in a 2-dimensional matrix D
    # D[k, t] stores a string 'aor' at time t of episode k
    # (a: upper-case letter, o: lower-case letter, r: digit)

    D = np.empty((K, H + 1), dtype=np.dtype('U3'))

    with PomdpParser(filename) as parser:
        sim = Simulator(parser.copy_env())

    # map discrete rewards to integers
    rews = set(sim.R.flat)
    rewmap = {k: v for v, k in enumerate(list(rews))}

    for k in range(K):
        sim.reset()

        # get the observation in the first state
        s, sp, o, r = sim.take_action(0)
        #print(s, 0, sp, o, r)
        D[k, 0] = '{}{}{}'.format(chr(65), chr(97 + o), chr(48 + rewmap[r]))

        # go east H - 1 times
        for i in range(H - 1):
            a = 1
            s, sp, o, r = sim.take_action(a)
            #print(s, a, sp, o, r)
            D[k, i + 1] = '{}{}{}'.format(chr(65 + a), chr(97 + o), chr(48 + rewmap[r]))

        # randomly go up or down and add the dummy observation
        a = 2 + np.random.randint(2)
        s, sp, o, r = sim.take_action(a)
        #print(s, a, sp, o, r)
        dummy = sim.num_observations()
        #D[k, H] = '{}{}{}'.format(chr(65+a), chr(97+dummy), chr(48+rewmap[r]))
        D[k, H] = '{}{}{}'.format(chr(65 + a), chr(97 + dummy), chr(48 + rewmap[r]))

    return D


# Call with "python testtmaze.py Tmaze H K"
# H is the horizon and K is the number of episodes
#   (right now only works with H=2, H=5 or H=10)
def main():
    H = int(sys.argv[2])
    K = int(sys.argv[3])
    RDPState.Data = simTMaze(sys.argv[1] + sys.argv[2] + '.POMDP', K, H)

    RDPState.Act = np.array([[set(RDPState.Data[i][j][0]) for j in range(H + 1)] for i in range(K)])
    RDPState.Obs = np.array([[set(RDPState.Data[i][j][1]) for j in range(H + 1)] for i in range(K)])
    RDPState.Rew = np.array([[set(RDPState.Data[i][j][2]) for j in range(H + 1)] for i in range(K)])
    RDPState.Trp = np.array([[set([RDPState.Data[i][j]]) for j in range(H + 1)] for i in range(K)])

    for j in range(H):
        RDPState.Act[:, H - 1 - j] = [RDPState.Act[i, H - 1 - j].union(RDPState.Act[i, H - j]) for i in range(K)]
        RDPState.Obs[:, H - 1 - j] = [RDPState.Obs[i, H - 1 - j].union(RDPState.Obs[i, H - j]) for i in range(K)]
        RDPState.Rew[:, H - 1 - j] = [RDPState.Rew[i, H - 1 - j].union(RDPState.Rew[i, H - j]) for i in range(K)]
        RDPState.Trp[:, H - 1 - j] = [RDPState.Trp[i, H - 1 - j].union(RDPState.Trp[i, H - j]) for i in range(K)]



    learnRDP(H)

def get_candidates(Q_prev, pdfa):
    Q_t = []
    for q in Q_prev:
        unq, cnt = np.unique(q.Data[q.ix, q.t], axis=0, return_counts=True)
        #sorted in descending order of frequency of aor
        candidates_sorted = unq[np.argsort(-cnt)]
        for i in range(len(candidates_sorted)):
            Q_t.append(
                RDPState(pdfa.get_name(), q, candidates_sorted[i][0], candidates_sorted[i][1], candidates_sorted[i][2]))

    return Q_t


def remove_candidate(Q_t):
    Q_t.pop(0)
    return Q_t


def test_distinct(q1, q2,H, thres):
    if q1.t == H+1:
        return True
    q1_prob = q1.operatorC13()
    q2_prob = q2.operatorC13()
    seq = list(set(q1_prob[:,0])) + list(set(q2_prob[:,0]) - set(q1_prob[:,0]))
    for s in seq:
        p1 = get_probability(s, q1_prob)
        p2 = get_probability(s, q2_prob)
        if np.abs(p1-p2) > thres:
            return False
    return True


def get_probability(aor, q_tr):
    p = np.where(q_tr[:, 0] == aor)[0]
    if len(p) == 0:
        return 0
    return float(q_tr[p[0], 1])

if __name__ == "__main__":
    main()
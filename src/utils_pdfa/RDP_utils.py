from src.utils_pdfa.test import RDPState
import numpy as np


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


def test_distinct(q1, q2, H, thres):
    if q1.t == H + 1:
        return True
    r, o = q1.operatorC11()
    q1_prob = np.concatenate((np.concatenate((r,o),axis=0), q1.operatorC13()), axis=0)
    r, o = q2.operatorC11()
    q2_prob = np.concatenate((np.concatenate((r,o),axis=0), q2.operatorC13()), axis=0)
    seq = list(set(q1_prob[:, 0])) + list(set(q2_prob[:, 0]) - set(q1_prob[:, 0]))
    for s in seq:
        p1 = get_probability(s,q1_prob)
        p2 = get_probability(s,q2_prob)
        if np.abs(p1 - p2) > thres:
            return False
    return True


def get_probability(aor, q_tr):
    p = np.where(q_tr[:, 0] == aor)[0]
    if len(p) == 0:
        return 0
    return float(q_tr[p[0], 1])


def getTrptrp(RDPState):
    Trptrp = []

    for i in range(RDPState.Trp.shape[0]):
        arr = []
        for j in range(RDPState.Trp.shape[1] - 2):
            lo = ((RDPState.Trp[i][j:j + 3]).tolist())
            n = ''
            end = 0
            for l in range(len(lo)):
                if end == 1:
                    n = "P"
                else:
                    n = n + str(list(lo[l])[0])
                if list(lo[l])[0][2] == str(1):
                    end = 1
            arr.append({n})
        lo = ((RDPState.Trp[i][RDPState.Trp.shape[1] - 2:]).tolist())
        n = ''
        for l in range(len(lo)):
            n = n + str(list(lo[l])[0])
        arr.append({n})

        lo = ((RDPState.Trp[i][RDPState.Trp.shape[1] - 1:]).tolist())
        n = ''
        for l in range(len(lo)):
            n = n + str(list(lo[l])[0])
        arr.append({n})
        Trptrp.append(arr)
    return np.array(Trptrp)
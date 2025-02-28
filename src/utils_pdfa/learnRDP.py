from src.utils_pdfa.RDP_utils import *
from src.pdfa import PDFA

def learnRDP(H, thres):
    q0 = RDPState("q0")
    pdfa = PDFA(q0)
    Q_prev = [q0]
    for h in range(H+1):
        print("h: ", h)
        Q_promoted = []
        Q_t= get_candidates(Q_prev, pdfa)
        pdfa.add_transition(Q_t[0].parent, Q_t[0])
        Q_promoted.append(Q_t[0])
        Q_t= remove_candidate(Q_t)  #removing the promoted candidate
        while len(Q_t)>0:
            for q_promoted in Q_promoted:
                similar = test_distinct(Q_t[0],q_promoted,H,thres)
                if not similar:
                    if q_promoted == Q_promoted[-1]:
                        #promote candidate
                        pdfa.add_transition(Q_t[0].parent,  Q_t[0])
                        Q_promoted.append(Q_t[0])
                        break
                else:
                    pdfa.add_transition(Q_t[0].parent, q_promoted, True, Q_t[0])
                    break
            Q_t = remove_candidate(Q_t)
        Q_prev = Q_promoted



    return pdfa

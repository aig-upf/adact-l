from env.Tmaze.generate_tmaze import generate_tmaze
from env.Tmaze.sim_tmaze import RDPState, simTMaze, learnRDP
import numpy as np
from src.utils_pdfa.renderRDP import render
from src.utils_pdfa.plot_plotly import plot_array
import time
import sys
def main():
    # H = 10
    start= int(sys.argv[1])
    end = int(sys.argv[2])
    if sys.argv[3] == "-l":
        log = True
    else:
        log = False

    K = 500
    for i in range (start,end):
        generate_tmaze(1.0, i)
    times=[]
    for H in range(start,end):

        RDPState.Data = simTMaze("env/Tmaze/generated_tmazes/Tmaze"+str(H)+ '.POMDP', K, H)
        RDPState.Act = np.array([[set(RDPState.Data[i][j][0]) for j in range(H + 1)] for i in range(K)])
        RDPState.Obs = np.array([[set(RDPState.Data[i][j][1]) for j in range(H + 1)] for i in range(K)])
        RDPState.Rew = np.array([[set(RDPState.Data[i][j][2]) for j in range(H + 1)] for i in range(K)])
        RDPState.Trp = np.array([[set([RDPState.Data[i][j]]) for j in range(H + 1)] for i in range(K)])

        for j in range(H+1):
            RDPState.Act[:, H - 1 - j] = [RDPState.Act[i, H - 1 - j].union(RDPState.Act[i, H - j]) for i in range(K)]
            RDPState.Obs[:, H - 1 - j] = [RDPState.Obs[i, H - 1 - j].union(RDPState.Obs[i, H - j]) for i in range(K)]
            RDPState.Rew[:, H - 1 - j] = [RDPState.Rew[i, H - 1 - j].union(RDPState.Rew[i, H - j]) for i in range(K)]
            RDPState.Trp[:, H - 1 - j] = [RDPState.Trp[i, H - 1 - j].union(RDPState.Trp[i, H - j]) for i in range(K)]
        avg=[]

        for av in range(10):
            t = time.time()
            RDP = learnRDP(H,0.4)
            avg.append(time.time()-t)
        times.append(np.mean(avg))
        # graph = render(RDP)
        # savefile = "/graphs/" + "Tmaze_H_"+str(H) +"_K_"+ str(K)
        # graph.render("." + savefile)
    plot_array(times, np.arange(start,end), log)



if __name__ == "__main__":
    main()



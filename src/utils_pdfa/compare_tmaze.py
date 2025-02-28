from src.utils_pdfa.test import RDPState, simTMaze
from learnRDP import learnRDP
import numpy as np
from src.utils_pdfa.renderRDP import render
import matplotlib.pyplot as plt


def compare_tmaze():
    # H = 10
    K = 500

    times=[]
    for H in range(5,20):

        RDPState.Data = simTMaze("env/Tmaze/generated_tmazes/Tmaze"+str(H)+ '.POMDP', K, H)
        print(RDPState.Data)
        RDPState.Act = np.array([[set(RDPState.Data[i][j][0]) for j in range(H + 1)] for i in range(K)])
        RDPState.Obs = np.array([[set(RDPState.Data[i][j][1]) for j in range(H + 1)] for i in range(K)])
        RDPState.Rew = np.array([[set(RDPState.Data[i][j][2]) for j in range(H + 1)] for i in range(K)])
        RDPState.Trp = np.array([[set([RDPState.Data[i][j]]) for j in range(H + 1)] for i in range(K)])

        for j in range(H+1):
            RDPState.Act[:, H - 1 - j] = [RDPState.Act[i, H - 1 - j].union(RDPState.Act[i, H - j]) for i in range(K)]
            RDPState.Obs[:, H - 1 - j] = [RDPState.Obs[i, H - 1 - j].union(RDPState.Obs[i, H - j]) for i in range(K)]
            RDPState.Rew[:, H - 1 - j] = [RDPState.Rew[i, H - 1 - j].union(RDPState.Rew[i, H - j]) for i in range(K)]
            RDPState.Trp[:, H - 1 - j] = [RDPState.Trp[i, H - 1 - j].union(RDPState.Trp[i, H - j]) for i in range(K)]
        RDP = learnRDP(H)
        print(RDP.transitions)
        graph = render(RDP)
        savefile = "/graphs/" + "Tmaze_H_"+str(H) +"_K_"+ str(K)
        graph.render("." + savefile)
    plt.plot(times)
    plt.show()



    # img = mpimg.imread("." + savefile+".png")
    # imgplot = plt.imshow(img)
    # plt.show()


if __name__ == "__main__":
    compare_tmaze()
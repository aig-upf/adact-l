

def generate_tmaze(discount, H):
    with open('env/Tmaze/generated_tmazes/Tmaze'+str(H)+'.POMDP', 'w') as f:
        f.write('# Noisy T-maze - length ' + str(H)+'\n' +"\n")
        f.write("discount: "+ str(discount) +"\n")
        f.write("values: reward" +"\n")
        f.write("states: " + str(H*2 + 3) +"\n")
        f.write("actions: "+ str(4) +"\n")
        f.write("observations: "+ str(5) +"\n")
        f.write("start: 1.0 ")
        for i in range(2*H+2):
            f.write(str(0.0)+" ")

        f.write("\n")
        #printing transitions
        f.write("\n"+ "T: 0 : 0 : 1 0.5"+"\n")
        f.write("T: 0 : 0 : 2 0.5" + "\n")
        for i in range((H-1)*2):
            f.write("T: 1 : "+ str(i+1)+" : "+ str(i+3)+ " 1.0"+"\n")

        f.write("T: 2 : "+str(2*H-1)+" : " + str(2*H+1)+" 1.0"+"\n" )
        f.write("T: 2 : " + str(2 * H) + " : " + str(2 * H + 2) + " 1.0" + "\n")

        f.write("T: 3 : " + str(2 * H - 1) + " : " + str(2 * H + 2) + " 1.0" + "\n")
        f.write("T: 3 : " + str(2 * H) + " : " + str(2 * H + 1) + " 1.0" + "\n")

        #printing observations
        f.write("\n"+ "O: 0 : 1 : 0 1.0" +"\n")
        f.write("O: 0 : 2 : 1 1.0" + "\n")

        for i in range((H-2)*2):
            f.write("O: 1 : " + str(i + 3) + " : 2 0.5"+ "\n")
            f.write("O: 1 : " + str(i + 3) + " : 3 0.5" + "\n")

        f.write("O: 1 : "+ str(2*H -1) + " : 4 1.0"+ "\n")
        f.write("O: 1 : "+ str(2*H) + " : 4 1.0"+ "\n")

        f.write("O: 2 : "+ str(2*H +1) + " : 4 1.0"+ "\n")
        f.write("O: 2 : " + str(2 * H + 2) + " : 4 1.0" + "\n")
        f.write("O: 3 : " + str(2 * H + 1) + " : 4 1.0" + "\n")
        f.write("O: 3 : " + str(2 * H + 2) + " : 4 1.0" + "\n")
        #rewards
        f.write("\n"+"R: * : * : " +str(2*H+1) +" : * 4.0"+"\n")
        f.write("R: * : * : " + str(2 * H + 2) + " : * -1.0")

    return 0









if __name__ == "__main__":
    for i in range (5,50):
        generate_tmaze(1.0, i)
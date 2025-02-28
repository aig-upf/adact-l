
import graphviz


hex_list = [ "#fff5f5", "#ffe3e3", "#ffa8a8", "#fa5252"]


def render(pdfa):
    graph = graphviz.Digraph(format="png")
    graph.node("fake", style="invisible")
    graph.attr(rankdir="LR")

    for state in pdfa.states:
        graph.node(state.name) # style='filled',fillcolor=hex_list[get_index]


    graph.edge("fake", pdfa.initial_state.name, style="bold")

    for i in range(len(pdfa.transitions)):
        s= pdfa.transitions[i][0]
        a = pdfa.transitions[i][1]
        o = pdfa.transitions[i][2]
        r = pdfa.transitions[i][3]
        s1 = pdfa.transitions[i][4]
        label = f"{a}"
        label += f", {o}"
        label += f", {r}"
        c = "black"
        graph.edge(
            s,
            s1,
            label=label,
            color=c
        )
    return graph


def replace_c(x):
    s=" ".join(str(y) for y in x)
    s.replace('[', ',')
    s.replace(']','')
    s.replace('\'', '')
    return s


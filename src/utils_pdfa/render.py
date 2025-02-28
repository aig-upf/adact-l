
import graphviz


hex_list = [ "#fff5f5", "#ffe3e3", "#ffa8a8", "#fa5252"]


def render(pdfa, a_dict):
    graph = graphviz.Digraph(format="png")
    graph.node("fake", style="invisible")
    graph.attr(rankdir="LR")

    for state in pdfa.states:
        graph.node(state.name) # style='filled',fillcolor=hex_list[get_index]


    graph.edge("fake", pdfa.initial_state.name, style="bold")
    for s in pdfa.transitions:
        for a in pdfa.transitions[s]:
            for s1 in pdfa.transitions[s][a]:
                label = f"{a}"
                label += f", {replace_c(pdfa.transitions[s][a][s1])}"
                c="black"
                if a in a_dict:
                    c="black"

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


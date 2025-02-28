class PDFA:
    def __init__(self, q0):
        self.initial_state = q0
        self.transitions = []
        self.name_counter = 1
        self.states = []
        self.states.append(q0)

    def get_name(self):
        name = "q" + str(self.name_counter)
        self.name_counter += 1
        return name

    def add_transition(self, q1, q2, merge=False, q3=None):
        if not merge:
            a = q2.a
            o = q2.o
            r = q2.r
            self.transitions.append([q1.name, a, o, r, q2.name])
        else:
            a = q3.a
            o = q3.o
            r = q3.r
            self.transitions.append([q1.name, a, o, r, q2.name])
            q2.ix = list(set(q2.ix)) + list(set(q3.ix) - set(q2.ix))
        if q2 not in self.states:
            self.states.append(q2)
        if q1 not in self.states:
            self.states.append(q1)


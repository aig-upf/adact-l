
import itertools
import numpy as np

class Simulator(object):
    def __init__(self, env):
        """
        Expected attributes in env:
            model_name
            model_spec
            discount
            costs
            values
            states
            actions
            observations
            T
            Z
            R
        """
        for k, v in env.items():
            self.__dict__[k] = v
        
        if self.start is not None:
            self.start = [x / sum(self.start) for x in self.start]
        
        # construct transition matrix
        I = [None] * 4
        L = [self.actions, self.states, self.states, self.observations]
        S = [self.num_actions(), self.num_states(), self.num_states(), self.num_observations()]
        TT = np.zeros((S[0], S[1], S[2]))
        for key, value in self.T.items():
            for i in range(3):
                I[i] = slice(0, S[i]) if key[i] is '*' else L[i].index(str(key[i]))
            TT[I[0], I[1], I[2]] = value
        self.T = TT
        for a, s in itertools.product(range(S[0]), range(S[1])):
            TT[a, s, :] = TT[a, s, :] / sum(TT[a, s, :])
        
        # construct reward matrix
        RR = np.zeros((S[0], S[1], S[2], S[3]))
        for key, value in self.R.items():
            for i in range(4):
                I[i] = slice(0, S[i]) if key[i] is '*' else L[i].index(key[i])
            RR[I[0], I[1], I[2], I[3]] = value
        self.R = RR
        
        # construct observation matrix
        L[2] = self.observations
        S[2] = self.num_observations()
        ZZ = np.zeros((S[0], S[1], S[2]))
        for key, value in self.Z.items():
            for i in range(3):
                I[i] = slice(0, S[i]) if key[i] is '*' else L[i].index(key[i])
            ZZ[I[0], I[1], I[2]] = value
        for a, s in itertools.product(range(S[0]), range(S[1])):
            ZZ[a, s, :] = ZZ[a, s, :] / sum(ZZ[a, s, :])
        self.Z = ZZ
        
        # initialize
        self.reset()
    
    def reset(self):
        if self.init_state is not None:
            state = self.init_state
        elif self.start is not None:
            state = np.random.choice(self.states, p=self.start)
        else:
            state = np.random.choice(self.states)
        self.curr_state = self.states.index(state)

    def num_states(self):
        return len(self.states)

    def num_actions(self):
        return len(self.actions)

    def num_observations(self):
        return len(self.observations)

    def get_legal_actions(self, state):
        """
        Simplest situation is every action is legal, but the actual model class
        may handle it differently according to the specific knowledge domain
        :param state:
        :return: actions selectable at the given state
        """
        return range(self.num_actions())
        
    def sample_next_state(self, s, a):
        return np.random.choice(range(self.num_states()), p=self.T[a, s, :])
        
    def sample_observation(self, a, sp):
        return np.random.choice(range(self.num_observations()), p=self.Z[a, sp, :])

    def simulate_action(self, s, a, debug=False):
        """
        Simulate action a from state s

        s: current state
        a: action taken
        return: next state, observation and reward
        """
        # get new state
        sp = self.sample_next_state(s, a)

        # get new observation
        o = self.sample_observation(a, sp)

        # get new reward
        r = self.R[a, s, sp, o]

        return sp, o, r

    def take_action(self, action):
        """
        Accepts an action and changes the underlying environment state
        
        action: action to take
        return: next state, observation and reward
        """
        s = self.curr_state
        sp, o, r = self.simulate_action(s, action)
        self.curr_state = sp

        return s, sp, o, r

    def print_config(self):
        print("discount:", self.discount)
        print("values:", self.values)
        print("states:", self.states)
        print("actions:", self.actions)
        print("observations:", self.observations)
        print("")
        print("T:", self.T)
        print("")
        print("Z:", self.Z)
        print("")
        print("R:", self.R)
        print("")


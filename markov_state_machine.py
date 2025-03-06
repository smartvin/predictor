from transitions import Machine

class NegotiationStateMachine:
    states = ["initial", "negotiation", "agreement", "breakdown", "deal_signed"]
    transitions = [
        {"trigger": "start_negotiation", "source": "initial", "dest": "negotiation"},
        {"trigger": "reach_agreement", "source": "negotiation", "dest": "agreement"},
        {"trigger": "break_down", "source": "negotiation", "dest": "breakdown"},
        {"trigger": "sign_deal", "source": "agreement", "dest": "deal_signed"},
        {"trigger": "retry_negotiation", "source": "breakdown", "dest": "negotiation"}
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial="initial")

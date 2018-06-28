import json


def ctx_helper(state_from, state_after, receiver_attributes):
    return json.dumps({
        "state_from": state_from,
        "state_after": state_after,
        "receivers": receiver_attributes
    })

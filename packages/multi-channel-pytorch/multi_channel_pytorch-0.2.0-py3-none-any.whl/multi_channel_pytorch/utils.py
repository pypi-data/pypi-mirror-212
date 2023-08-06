def get_bias(state_dict: dict):
    del state_dict['weights']

    return state_dict

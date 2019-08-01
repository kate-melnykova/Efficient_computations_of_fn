from .factorial import factorial
from .compute_pi import compute_pi
from .compute_e import compute_e

function_registry = {
        'factorial': [factorial, 'argument', 'time_limit', 'accuracy'],
        'pi': [compute_pi, 'time_limit', 'accuracy'],
        'e': [compute_e, 'time_limit', 'accuracy']
    }
from celery import shared_task

from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e

function_registry = {
    'factorial': [factorial, 'argument', 'time_limit', 'accuracy'],
    'pi': [compute_pi, 'time_limit', 'accuracy'],
    'e': [compute_e, 'time_limit', 'accuracy']
}


@shared_task
def functio(func_name, arguments, arg_names):
    func = function_registry[func_name][0]
    func(arguments, arg_names)
    return arguments
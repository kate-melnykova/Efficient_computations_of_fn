from celery import shared_task

from sci_funcs.function_registry import function_registry
from sci_funcs.factorial import factorial
from sci_funcs.compute_pi import compute_pi
from sci_funcs.compute_e import compute_e


@shared_task
def args_to_function(arguments, arg_names):
    func_name = arguments['func_name']
    func = function_registry[func_name][0]
    func(arguments, arg_names)
    return arguments
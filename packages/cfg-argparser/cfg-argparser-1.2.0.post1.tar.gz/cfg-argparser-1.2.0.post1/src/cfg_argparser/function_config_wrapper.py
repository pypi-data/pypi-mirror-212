"""A function that can be decorated or wrapped around a file"""
import functools
import inspect
from typing import Callable

from .cfg_dict import CfgDict


def wrap_config(cfg_dict: CfgDict) -> Callable[..., Callable]:
    """Wraps a function with a CfgDict file to make an easy config configuration"""

    def _wrapper(func: Callable) -> Callable:
        # get parameters and defaults
        parameters: dict[str, inspect.Parameter] = dict(inspect.signature(func).parameters)
        save_after = False
        for name, param in parameters.items():
            if name not in cfg_dict:
                if cfg_dict.is_json_serializable(param.default):
                    save_after = True
                    cfg_dict[name] = param.default
        if save_after:
            cfg_dict.save()

        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            new_defaults = dict(zip(parameters.keys(), map(lambda x: x.default, parameters.values())))
            new_defaults.update({k: v for k, v in cfg_dict.items() if k in new_defaults})
            new_defaults.update(kwargs)

            # convert args to kwargs
            default_lst = list(enumerate(new_defaults.items()))
            for idx, arg in enumerate(args):
                default_lst[idx] = (default_lst[idx][0], (default_lst[idx][1][0], arg))
            new_defaults = dict(map(lambda arg: arg[1], default_lst))
            return func(**new_defaults)

        return _wrap

    return _wrapper

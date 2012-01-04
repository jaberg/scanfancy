"""
Interface idea for scan

"""
import theano.tensor as TT
import re


def scan_fancy(**kwargs):
    """
    kwargs can be Variables or functions / lambdas

    functions or lambdas must have only kwargs signatures,
    and those kwargs are matched up with the kwargs of scan_fancy.

    """
    fns = dict([(k, v) for (k, v) in kwargs.items() if callable(v)])
    vars = dict([(k, v) for (k, v) in kwargs.items() if not callable(v)])
    print 'FNS', fns
    print 'VARS', vars

    sequences = []
    non_sequences = []
    outputs_info = []

    for (fn_name, fn) in fns.items():
        n_args = fn.func_code.co_argcount
        arg_names = fn.func_code.co_varnames[:n_args]
        assert len(arg_names) == n_args
        matches = [re.match('(?P<base>.+?)_(?P<tseq>t+)$', aname)
                for aname in arg_names]
        bases = [(m.groups()[0] if m is not None else None)
                for m in matches]
        taps = [(1 - len(m.groups()[1]) if m is not None else None)
                for m in matches]

        for aname, base, tap in zip(arg_names, bases, taps):
            if aname not in kwargs:
                raise TypeError('kwargs in f() and scan must match')
            if tap is None:
                # this argument is to be presented at every step of scan
                non_sequences.append(kwargs[aname])
            elif tap == 0:
                # this argument is to be retrieved from an argument slice
                sequences.append(kwargs[aname])
            elif tap < 0:
                # this argument is an output
                outputs_info
            else:
                assert tap > 0
                raise NotImplementedError('flip loop direction')



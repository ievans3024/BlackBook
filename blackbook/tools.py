from flask import request, session

__author__ = 'ievans3024'


def check_angular_xsrf():
    if request.headers['X-XSRF-TOKEN']:
        if not session.get('XSRF-TOKEN'):
            return False
        elif request.headers['X-XSRF-TOKEN'] == session.get('XSRF-TOKEN'):
            return True
    else:
        return False


def request_accepts(request, *mimetypes):
    best = request.accept_mimetypes.best_match(mimetypes)
    return request.accept_mimetypes[best] and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']


def merge_complex_dicts(*dicts):
    # rightmost dict provided gets priority -> base, extends, extends_extends, etc.
    result = {}
    for d in dicts:
        for k in d.keys():
            if k in result.keys():
                if isinstance(result[k], dict) and isinstance(d[k], dict):
                    result[k] = merge_complex_dicts(result[k], d[k])
                elif isinstance(result[k], list) and isinstance(d[k], list):
                    # TODO: deeper list merging?
                    result[k] += [i for i in d[k] if i not in result[k]]
                elif isinstance(result[k], (str, bool)) and isinstance(d[k], (str, bool)):
                    result[k] = d[k]
                else:
                    raise TypeError(
                        "Unexpected type mismatch: {cls1} and {cls2}".format(
                            cls1=type(result[k]).__name__, cls2=type(d[k]).__name__
                        )
                    )
            else:
                result[k] = d[k]
    return result
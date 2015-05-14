__author__ = 'ievans3024'


def request_accepts(request, *mimetypes):
    best = request.accept_mimetypes.best_match(mimetypes)
    return request.accept_mimetypes[best] and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']
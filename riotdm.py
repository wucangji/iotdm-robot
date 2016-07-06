import iotdm
# import nserver
# import nparser
# import time

application = iotdm.application
container = iotdm.container
contentInstance = iotdm.contentInstance


def connect_to_iotdm(host, user, pw, p):
    return iotdm.connect(host, base="InCSE1", auth=(user, pw), protocol=p)

'''
def new_notification_server(ip, port):
    return nserver.server(ip, int(port))

def read_notifications(n, timeout):
    p = nparser.parse()
    timeout = float(timeout)
    mark = time.time() + timeout
    more = True
    while True:
        now = time.time()
        if now > mark:
            break
        newtimeout = mark - now
        (what, who, data) = n.wait(newtimeout)
        if what == "error":
            return
        if what == "data":
            more = p.process(data)
            if more == False:
                break
        if what == "timeout":
            break
        if more == False:
            break
    return p.body

def close_notification_server(n):
    n.close()
'''


def create_resource(connection, parent, restype, a=None):
    restype = int(restype)
    if a is None:
        x = connection.create(parent, restype)
    else:
        x = connection.create(parent, restype, attr=a)
    if x is None:
        raise AssertionError('Cannot create this resource')
    elif hasattr(x, 'status_code'):
        if x.status_code < 200 or x.status_code > 299:
            raise AssertionError(
                'Cannot create this resource [%d] : %s' %
                (x.status_code, x.text))
    return x

# this might not be necessary now that the library functions can take dicts


def create_subscription(connection, parent, ip, port):
    uri = "http://%s:%d" % (ip, int(port))
    x = connection.create(parent, "subscription", {
        "notificationURI": uri,
        "notificationContentType": "wholeResource"})
    if x is None:
        raise AssertionError('Cannot create this subscription')
    elif hasattr(x, 'status_code'):
        if x.status_code < 200 or x.status_code > 299:
            raise AssertionError('Cannot create subscription [%d] : %s' %
                                 (x.status_code, x.text))
    return x


def retrieve_resource(connection, resid):
    x = connection.retrieve(resid)
    if x is None:
        raise AssertionError('Cannot retrieve this resource')
    elif hasattr(x, 'status_code'):
        if x.status_code < 200 or x.status_code > 299:
            raise AssertionError('Cannot retrieve this resource [%d] : %s' %
                                 (x.status_code, x.text))
    return x


def update_resource(connection, resid, attr):
    x = connection.update(resid, attr)
    if x is None:
        raise AssertionError('Cannot update this resource')
    elif hasattr(x, 'status_code'):
        if x.status_code < 200 or x.status_code > 299:
            raise AssertionError('Cannot update this resource [%d] : %s' %
                                 (x.status_code, x.text))
    return x


def delete_resource(connection, resid):
    x = connection.delete(resid)
    if x is None:
        raise AssertionError('Cannot delete this resource')
    elif hasattr(x, 'status_code'):
        if x.status_code < 200 or x.status_code > 299:
            raise AssertionError('Cannot delete this resource [%d] : %s' %
                                 (x.status_code, x.text))
    return x


def resid(x):
    return iotdm.resid(x)


def text(x):
    return x.text


def status_code(x):
    return x.status_code


def json(x):
    return x.json()


def elapsed(x):
    return x.elapsed.total_seconds()

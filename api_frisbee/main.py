import logging
import urllib3
import uuid
import requests
import datetime
import os

logger = logging.getLogger('api-frisbee.main')

class Frisbee(object):

    def __init__(self,data=None):
        if not data:
            self.id = str(uuid.uuid1())
            self.start_time = datetime.datetime.now().timestamp()
            self.hops = []
        else:
            for k, v in data.items():
                setattr(self, k, v)

    def set_targets(self,targets):
        self.targets = targets

    def keys(self):
        return ["id","targets","start_time","hops"] #,"elapsed_time"]

    def __getitem__(self, key):
        return self.__getattribute__(key)


def setup_logging(logfile=None,level=logging.DEBUG):
    # Disable urllib warnings
    urllib3.disable_warnings()
    # Set a formatter that includes the module name
    formatter = logging.Formatter('%(asctime)s - %(name)20s - %(levelname)10s -  %(funcName)20s() - %(message)s')
    # Init the stream handler
    sthandler = logging.StreamHandler()
    sthandler.setLevel(level)
    sthandler.setFormatter(formatter)
    # Init the root logger (applies to all loggers)
    Rootlogger = logging.getLogger()
    Rootlogger.addHandler(sthandler)
    Rootlogger.setLevel(level)
    # If provided, init a filehandler
    if logfile:
        fhandler = logging.FileHandler(logfile)
        fhandler.setLevel(level)
        fhandler.setFormatter(formatter)
        Rootlogger.addHandler(fhandler)
    # Complete
    logger.info("Logging init")
    return Rootlogger


def start_frisbee(targets):

    frisbee = Frisbee()
    frisbee.set_targets(targets)

    throw_frisbee(frisbee)

    return frisbee

def throw_frisbee(frisbee):

    next_hop = frisbee.targets.pop()

    logger.info(f"I'm going to throw the frisbee: {frisbee.id} to {next_hop}")

    r = requests.post(f"http://{next_hop}/catch",json=dict(frisbee))

    return frisbee

def catch_frisbee(data,request=None):

    frisbee = Frisbee(data)
    hop = {}
    logger.debug(os.uname())
    hop['host'] = os.uname()[1]#.values()#['nodename']

    if request:
        hop['remote'] = request.remote_addr
        logger.info(f"I've caught the frisbee: {frisbee.id} from {request.remote_addr}")
    else:
        logger.info(f"I've caught the frisbee: {frisbee.id}")

    # Work out the times
    now = datetime.datetime.now()
    start = datetime.datetime.fromtimestamp(frisbee.start_time)
    delta = now - start

    # Update a hop object
    hop['received_time'] = now.timestamp()
    hop['elapsed_time'] =delta.total_seconds()

    frisbee.hops.append(hop)


    # If there are targets left, throw again
    if frisbee.targets:
        frisbee = throw_frisbee(frisbee)
        return frisbee
    else:
        # Otherwise finish the game :(
        logger.info(f"I'm the last player of frisbee: {frisbee.id}")

    #logger.debug(dict(frisbee))

    logger.info("######################")
    logger.info("Frisbee report:")
    logger.info(f"ID: {frisbee.id}")
    logger.info(f"TIME: {frisbee.start_time}")

    for i,hop in enumerate(frisbee.hops):
        for key in hop.keys():
            logger.info(f"HOP-{i} {key}: {hop[key]}")

    return frisbee
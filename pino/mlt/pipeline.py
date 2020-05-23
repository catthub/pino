from itertools import combinations
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from typing import Any, Dict, List, Tuple


class Pipeline(object):
    def __init__(self, parent: str, child: str, conn: Connection) -> None:
        self.__parent = parent
        self.__child = child
        self.__conn = conn
        return None

    def __del__(self) -> None:
        self.__conn.close()
        return None

    def send(self, val: Any) -> None:
        self.__conn.send(val)
        return None

    def receive(self) -> Any:
        return self.__conn.recv()

    def poll(self, timeout: float) -> bool:
        return self.__conn.poll(timeout)


class LocalNetwork(object):
    def __init__(self, parent: str, children: List[str],
                 conns: List[Pipeline]) -> None:
        self.__parent = parent
        self.__children = children
        self.__lnet: Dict[str, Pipeline] = dict(zip(children, conns))
        return None

    def send_to(self, child: str, val: Any) -> None:
        self.__lnet[child].send(val)
        return None

    def send_all(self, val: Any) -> None:
        [conn.send(val) for conn in self.__lnet.values()]
        return None

    def receive_from(self, child: str) -> Any:
        return self.__lnet[child].receive()

    def poll_from(self, child: str, timeout: float) -> bool:
        return self.__lnet[child].poll(timeout)


class GlobalNetwork(object):
    def __init__(self, process_ids: List[str]) -> None:
        comb_ids = list(combinations(process_ids, 2))
        pair_procs: List[Tuple[str, str]] = []
        conns: List[Connection] = []
        for comb in comb_ids:
            pair_procs.extend([comb, tuple(reversed(comb))])
            conns.extend(Pipe())
        pipes = [
            Pipeline(pair[0], pair[1], conn)
            for pair, conn in zip(pair_procs, conns)
        ]
        self.__proc_ids = process_ids
        self.__pairs = pair_procs
        self.__net: Dict[Tuple[str, str],
                         Pipeline] = dict(zip(pair_procs, pipes))
        return None

    def get_pipeline_between(self, parent: str, child: str) -> Pipeline:
        return self.__net[(parent, child)]

    def get_local_net(self, parent: str) -> LocalNetwork:
        pairs = [pair for pair in self.__net.keys() if pair[0] == parent]
        pipes = [self.__net[pair] for pair in pairs]
        children = [pair[1] for pair in pairs]
        return LocalNetwork(parent, children, pipes)

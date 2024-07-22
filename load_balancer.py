from consistent_hashing import ConsistentHashMap

class LoadBalancer:
    def __init__(self, N, M, K):
        self.chm = ConsistentHashMap(N, M, K)

    def add_server(self, Sid):
        self.chm.add_server(Sid)

    def remove_server(self, Sid):
        self.chm.remove_server(Sid)

    def route_request(self, Rid):
        return self.chm.map_request(Rid)

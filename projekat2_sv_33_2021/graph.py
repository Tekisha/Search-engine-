    


class Graph:
    def __init__(self):
        self._outgoing = {}
        self._incoming = {}
    

    def insert_edge(self,v,u):
        if v not in self._outgoing:
            self.insert_vertex(v)
        if u not in self._outgoing:
            self.insert_vertex(u)

        self._incoming[v][u] = 1
        self._outgoing[u][v] = 1
    
    def insert_vertex(self,u):
        self._outgoing[u] = {}
        self._incoming[u] = {}

    def degree_vertex(self,u,outgoing = True):
        if outgoing:
            return len(self._outgoing[u])
        else:
            return len(self._incoming[u]) 
    
    def get_neighbours(self,u,outgoing = True):
        if outgoing:
            return self._outgoing[u].keys()
        else:
            return self._incoming[u].keys()
    
    def vertex_count(self):
        return len(self._outgoing)
    
    def edge_count(self):
        total=0
        for v in self._outgoing:
            total += len(self._outgoing[v])
        return total
    


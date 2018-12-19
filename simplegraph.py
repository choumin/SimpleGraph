from itertools import combinations
from itertools import product

class Vertex(dict):
    def __init__(self, index, **args):
        self.index = index
        for key, val in args.items():
            self.__dict__[key] = val
        self.__dict__["in_neighbors"] = set([]) 
        self.__dict__["out_neighbors"] = set([])
        self._neighbors = []

    def get_attributes(self):
        return self.__dict__.keys()

    def set_attribute(self, attr, val):
        self.__dict__[attr] = val

    def neighbors(self):
        return self._neighbors

    def add_neighbor(self, neighbor_type, vertex):
        self._neighbors.append(vertex)
        self.__dict__[neighbor_type].add(vertex)

    def has_neighbor(self, name):
        _n_name = [vertex["name"] for vertex in self._neighbors]
        if name in _n_name:
            return True
        return False
        
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __hash__(self):
        return hash(self.index)

    def degree(self):
        return len(self._neighbors)

    def delete_neighbor(self, name):
        index = -1
        for i in range(len(self._neighbors)):
            if self._neighbors[i]["name"] == name:
                index = i
                break

        if index != -1:
            self._neighbors.pop(index)
        else:
            print("Error! There not exsits a neighbor named: ", name)

        exist = False
        for v in self.__dict__["in_neighbors"]:
            if v["name"] == name:
                vertex = v
                exist = True
            break
        if exist:
            self.__dict__["in_neighbors"].remove(vertex)

        exist = False
        for v in self.__dict__["out_neighbors"]:
            if v["name"] == name:
                vertex = v
                exist = True
        if exist:
            self.__dict__["out_neighbors"].remove(vertex)


class VertexSeq(list):
    def __init__(self):
        self.vertices = []
        self.attributes = {} 
        self.index = 0
        self.name_to_vertex = {}

    def add_vertex(self, **args):
        attributes = self.get_attributes()
        for key in args:
            if key not in attributes:
                self.set_attribute(key, None)
        vertex = Vertex(self.index, **args)
        v_attrs = vertex.get_attributes() 
        
        for attr in attributes:
            if attr not in v_attrs:
                vertex.set_attribute(attr, None)

        self.vertices.append(vertex) 
        self.name_to_vertex[vertex["name"]] = vertex

        self.index += 1

    def get_attributes(self):
        return self.attributes.keys()

    def set_attribute(self, attr, val):
        self.attributes[attr] = val
        for vertex in self.vertices:
            vertex.set_attribute(attr, val)

    def find(self, name):
        if name not in self.name_to_vertex:
            raise(Exception, "vertex not found.")

        return self.name_to_vertex[name]

    def add_neighbor(self, source, target):
        s_vertex = self.find(source)
        t_vertex = self.find(target)
        s_vertex.add_neighbor(neighbor_type = "out_neighbors", vertex = t_vertex)
        t_vertex.add_neighbor(neighbor_type = "in_neighbors", vertex = s_vertex)
        

    def delete_vertices(self, indices):
        vertices = []
        for vertex in self.vertices:
            if vertex.index not in indices:
                vertices.append(vertex)
                
        for index in indices:
            vertex = self.vertices[index]
            try:
                self.name_to_vertex.pop(vertex["name"])
            except:
                import pdb; pdb.set_trace()
            v_neighbors = vertex.neighbors()
            for neigh in v_neighbors:
                neigh.delete_neighbor(vertex["name"])
           
        self.vertices = vertices
        
        for i in range(len(self.vertices)):
            self.vertices[i].index = i

        self.index = len(self.vertices)

    def __setitem__(self, key, val):
        if isinstance(key, str):
            self.set_attribute(key, val)
        else:
            self.vertices[key] = val
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return [vertex[key] for vertex in self.vertices]
        else:
            return self.vertices[key]

    def __iter__(self):
        for elem in self.vertices:
            yield elem

    def __len__(self):
        return len(self.vertices)


class Edge(dict):
    def __init__(self, index, sindex, tindex, sname, tname, **args):
        self.index = index
        self.sindex = sindex
        self.tindex = tindex
        self.sname = sname
        self.tname = tname
        for key, val in args.items():
            self.__dict__[key] = val
        # todo
         
        self.tuple = tuple([sindex, tindex])

    def get_attributes(self):
        return self.__dict__.keys()

    def set_attribute(self, attr, val):
        self.__dict__[attr] = val 

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

class EdgeSeq(list):
    def __init__(self):
        self.edges = []
        self.attributes = {}
        self.index = 0
        self.st_to_edge = {}

    def select(self, _source, _target):
        edge_key = '_'.join([_source, _target])
        if edge_key not in self.st_to_edge:
            raise(Exception, "Edge not found.")

        return [self.st_to_edge[edge_key]] 

    def add_edge(self, sindex, tindex, sname, tname, **args):
        attributes = self.get_attributes()
        for key in args:
            if key not in attributes:
                self.set_attribute(key, None)
        edge = Edge(self.index, sindex, tindex, sname, tname, **args)
        e_attrs = edge.get_attributes() 
        
        for attr in attributes:
            if attr not in e_attrs:
                edge.set_attribute(attr, None)

        self.edges.append(edge)

        self.st_to_edge['_'.join([sname, tname])] = edge

        self.index += 1

    def get_attributes(self):
        return self.attributes.keys()

    def set_attribute(self, attr, val):
        self.attributes[attr] = val
        for edge in self.edges:
            edge.set_attribute(attr, val)

    def __setitem__(self, key, val):
        if isinstance(key, str):
            self.set_attribute(key, val)
        else:
            self.edges[key] = val

    def __getitem__(self, key):
        if isinstance(key, str):
            return [edge[key] for edge in self.edges]
        else:
            return self.edges[key]

    def __iter__(self):
        for elem in self.edges:
            yield elem
    
    def delete_vertices(self, G, indices):
        edges = []
        for edge in self.edges:
            if edge.tuple[0] not in indices and edge.tuple[1] not in indices:
                edges.append(edge)
            else:
                self.st_to_edge.pop('_'.join([edge.sname, edge.tname]))

        self.edges = edges

        for i in range(len(self.edges)):
            edge = self.edges[i]
            edge.index = i
            sindex = G.vs.find(name = edge.sname).index
            tindex = G.vs.find(name = edge.tname).index
            edge.tuple = tuple([sindex, tindex])
            
        self.index = len(self.edges)

    def __len__(self):
        return len(self.edges)

    def get_edge_keys(self):
        return self.st_to_edge.keys()

class Graph():
    def __init__(self):
        self.vs = VertexSeq()
        self.es = EdgeSeq()

    def add_edge(self, source, target, **args):
        if "weight" not in args:
            print("Error: A vertex must have a weight!")
            return
        sindex = self.vs.find(name=source).index
        tindex = self.vs.find(name=target).index
        
        self.es.add_edge(sindex, tindex, source, target, **args)
        self.vs.add_neighbor(source, target) 

    def add_vertex(self, **args):
        if "name" not in args:
            print("Error: A vertex must have a name!") 
            return 
        self.vs.add_vertex(**args)    
    
    def delete_vertices(self, indices):
        self.vs.delete_vertices(indices)
        # todo
        self.es.delete_vertices(self, indices)

    def summary(self):
        s = "The count of vertices is %d, and the count of edges is %d" % \
                (len(self.vs), len(self.es))
        return s

    def size(self):
        return len(self.es)

    def degree(self):
        _degree = {}
        for vertex in self.vs:
            _degree[vertex["name"]] = vertex.degree()
    
        return _degree

    def get_weight(self, u, v, default):
        try:
            edges = self.es.select(u, v)
            return edges[0]["weight"]
        except:
            return default
        
    def get_weight2(self, u, v, default):
        try:
            edges = self.es.select(u, v)
            return 1
        except:
            return default

    def modularity_from_networkx(self, communities):
        m = self.size()
        out_degree = self.degree()
        in_degree = out_degree
        norm = 1.0 / (2 * m)

        def val(u, v):
            w = self.get_weight2(u, v, 0)
            if u == v:
                w *= 2
            return w - in_degree[u] * out_degree[v] * norm
        Q = sum(val(u, v) for c in communities for u, v in product(c, repeat = 2))

        return Q * norm

    def modularity_from_qyj(self, communities):
        Q = 0
        S = 0
        D = 0
        m = self.size() * 2
        vertex_degree = self.degree()
        for community in communities:
            for u, v in combinations(community, 2):
                u_vertex = self.vs.find(name = u)
                if u_vertex.has_neighbor(v):
                    S += 1
                D += vertex_degree[u] * vertex_degree[v]
        Q = 1.0 * (S - D * 1.0 / m) / m

        return Q

    def degree_weighted(self):
        _degree = {}
        for vertex in self.vs:
            _degree[vertex["name"]] = 0
            for neighbor in vertex.neighbors():
                _degree[vertex["name"]] += self.get_weight(vertex["name"], \
                        neighbor["name"], 1)

        return _degree
    
    def modularity_from_zm(self, communities):
        Q = 0
        S = 0
        D = 0
        m = self.size() * 2
        vertex_degree = self.degree_weighted()
        for community in communities:
            for u, v in combinations(community, 2):
                u_vertex = self.vs.find(name = u)
                if u_vertex.has_neighbor(v):
                    S += self.get_weight(u, v, 1) 
                D += vertex_degree[u] * vertex_degree[v]
        Q = 1.0 * (S - D * 1.0 / m) / m

        return Q

    def get_edge_keys(self):
        return self.es.get_edge_keys()

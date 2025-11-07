class Vertex:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x # coordenada del nodo en el eje x
        self.y = y # coordenada del nodo en el eje y
        self.adjacent = {}  # diccionario de nodos adyacentes y sus pesos
    
    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent
    
    def get_id(self):
        return self.id
    
    


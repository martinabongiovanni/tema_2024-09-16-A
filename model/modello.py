
from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        # grafo
        self._grafo = nx.Graph()
        self._stati = []
        self._id_map_stati = {}

    def get_limit_range(self):
        return DAO.get_limit_range()

    def get_all_shapes(self):
        return DAO.get_all_shapes()

    def get_nodes(self):
        return self._grafo.nodes()

    def build_graph(self, lat, lon, shape):
        self._grafo.clear()
        # aggiungo i nodi
        self.fill_id_map_stati(lat, lon, shape)
        self._grafo.add_nodes_from(self._stati)
        # aggiungo gli archi
        for i in range(0, len(self._stati)):
            for j in range(i+1, len(self._stati)):
                if self._stati[j].Neighbors is not None and self._stati[i].id in self._stati[j].Neighbors:
                    peso = self.calcola_peso(self._stati[i].id, self._stati[j].id, lat, lon, shape)
                    self._grafo.add_edge(self._stati[i], self._stati[j], weight=peso)
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def fill_id_map_stati(self, lat, lon, shape):
        self._stati = DAO.get_states_by_input(lat, lon, shape)
        for stato in self._stati:
            self._id_map_stati[stato.id] = stato

    def calcola_peso(self, stato1, stato2, lat, lon, shape):
        durata1 = DAO.get_total_duration(stato1, lat, lon, shape)[0]
        durata2 = DAO.get_total_duration(stato2, lat, lon, shape)[0]
        return durata1 + durata2

    def get_nodelist_by_degree(self):
        lista = []
        for node in self._grafo.nodes():
            degree = self._grafo.degree(node)
            lista.append((str(node), degree))
        return sorted(lista, key=lambda x: x[1], reverse=True)

    def get_edges(self):
        lista = []
        for s1, s2, data in self._grafo.edges(data=True):
            lista.append([str(s1), str(s2), data["weight"]])
        # ordino la lista per pesi crescenti
        lista.sort(key=lambda x: x[2], reverse=True)
        return lista

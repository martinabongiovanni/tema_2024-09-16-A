import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        try:
            limit = self._model.get_limit_range()
            latitude = int(self._view.txt_latitude.value)
            if latitude < int(limit[0][0]) or latitude > int(limit[0][1]):
                self._view.create_alert(f"Attenzione! La latitudine deve essere un valore numerico compreso fra {int(limit[0][0])} e {int(limit[0][1])}.")
                return
            longitude = int(self._view.txt_longitude.value)
            if longitude < int(limit[0][2]) or longitude > int(limit[0][3]):
                self._view.create_alert(f"Attenzione! La longitudine deve essere un valore numerico compreso fra {int(limit[0][2])} e {int(limit[0][3])}.")
                return
            shape = self._view.ddshape.value
            if shape is None:
                self._view.create_alert(f"Attenzione! Selezionare una shape tra quelle in elenco.")
                return
            nNodes, nEdges = self._model.build_graph(latitude, longitude, shape)

            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nNodes}"))
            self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

            self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi di grado maggiore sono:"))
            for tupla in self._model.get_nodelist_by_degree()[0:5]:
                self._view.txt_result1.controls.append(ft.Text(f"{tupla[0]} -> degree: {tupla[1]}"))

            self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono:"))
            for edge in self._model.get_edges()[0:5]:
                self._view.txt_result1.controls.append(ft.Text(f"{edge[0]} <-> {edge[1]} | peso: {edge[2]}"))

        finally:

            self._view.update_page()

    def handle_path(self, e):
        pass

    def fill_ddshape(self):
        shapes = self._model.get_all_shapes()
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))

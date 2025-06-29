import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt, QTimer
from collections import deque
import random

# Ventana principal con el selector de mapas
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector de Mapas")
        self.setGeometry(500, 200, 300, 300)

        # Layout y widgets
        layout = QVBoxLayout()
        self.label = QLabel("Selecciona un mapa:")
        layout.addWidget(self.label)

        # ComboBox para seleccionar métodos de búsqueda
        self.method_selector = QComboBox()
        self.method_selector.addItems(["Evitar ciclos", "No evitar ciclos"])  # Opciones de búsqueda
        layout.addWidget(self.method_selector)

        # ComboBox para seleccionar mapas
        self.map_selector = QComboBox()
        self.map_selector.addItems(["Mapa 1", "Mapa 2", "Mapa 3", "Mapa 4"])  # Nombres de mapas
        layout.addWidget(self.map_selector)

        # Botón para cargar el mapa seleccionado
        self.load_button = QPushButton("Cargar Mapa")
        self.load_button.clicked.connect(self.load_map)
        layout.addWidget(self.load_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_map(self):
        # Obtener el mapa seleccionado y el método de búsqueda
        selected_map = self.map_selector.currentText()
        avoid_cycles = self.method_selector.currentText() == "Evitar ciclos"
        self.maze_window = MazeWindow(selected_map, avoid_cycles)
        self.maze_window.show()

# Ventana del laberinto
class MazeWindow(QMainWindow):
    def __init__(self, map_name, avoid_cycles):
        super().__init__()
        self.setWindowTitle(f"Laberinto - {map_name}")
        self.setGeometry(100, 100, 400, 400)

        # Definir los mapas según la selección
        self.define_maps(map_name)

        # # Posición inicial del ratón
        # self.mouse_pos = [1, 1]
        # # Posición de la meta
        # self.goal_pos = [5, 5]

        # Cargar imagen de KERMIT
        self.mouse_image = QPixmap("kermit.jpg")

        # Cargar imagen de ELMO
        self.elmo_image = QPixmap("elmo.jpg")

        # Cargar imagen de Piggy
        self.piggy_image = QPixmap("pig.jpg")

        self.galleta_image = QPixmap("galleta.jpg")


        # Temporizador para mover la bola roja
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_mouse_step)
        
        # Lista de pasos
        self.path = []
        self.pathPiggy = []
        
        self.current_step = 0


        # Configurar el widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Iniciar la búsqueda y movimiento
        self.start_moving(avoid_cycles)

    def define_maps(self, map_name):
        if map_name == "Mapa 1":
            self.maze = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.mouse_pos = [5, 5]
            self.goal_pos = [1, 5]
            # self.piggy_pos = [4, 3]
            self.piggy_pos = [1, 1]
            self.galleta_pos = [1, 3]
            self.depth = 4
        elif map_name == "Mapa 2":
            self.maze = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.mouse_pos = [5, 1]
            self.goal_pos = [1, 1]
            self.piggy_pos = [1, 5]
            self.depth = 8
        elif map_name == "Mapa 3":
            self.maze = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.mouse_pos = [4, 1]
            self.goal_pos = [4, 5]
            self.piggy_pos = [2, 2]
            self.depth = 4
        elif map_name == "Mapa 4":
            self.maze = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.mouse_pos = [1, 5]
            self.goal_pos = [3, 1]
            self.piggy_pos = [3, 4]
            self.depth = 6

    def start_moving(self, avoid_cycles):
        # Aquí se realiza la búsqueda del camino
        self.path = self.depth_limited_search(tuple(self.mouse_pos), tuple(self.goal_pos), self.depth, avoid_cycles=avoid_cycles)
        self.pathPiggy.append(tuple(self.piggy_pos))

        if self.path:
            self.current_step = 1 #antes era 0 pero ese es su pos actual ahora es su primr paso que sera la meta de la rana
            self.timer.start(1000)  # 1000 ms = 1 segundo

    def depth_limited_search(self, start, goal, depth,avoid_cycles):
        i = 0
        # Implementación de búsqueda limitada por profundidad (DLS) usando una pila (LIFO)
        stack = [(start, [start])]  # Usar stack para DLS
        historial = []
        print(f"Stack:{i} {stack}")
        
        while stack:

            if avoid_cycles:
                i += 1
                (node, path) = stack.pop()  # Extraer el nodo más profundo (LIFO)
                print(f"Stack:{i} {stack}")

                historial.append(node)

                if node == goal:
                    return path
                
                if len(path) <= depth:
                    for fila, columna in reversed([(-1, 0), (0, 1), (1, 0), (0, -1)]):  # Arriba, derecha, abajo, izquierda
                        new_node = (node[0] + fila, node[1] + columna)
                        if self.is_valid_move(new_node) and new_node not in path:
                            stack.append((new_node, path + [new_node]))  # Añadir el nuevo nodo a la pila
                            print(f"Stack:{i} {stack}")
            else:
                i += 1
                (node, path) = stack.pop()  # Extraer el nodo más profundo (LIFO)
                print(f"Stack:{i} {stack}")

                historial.append(node)

                print('camino')
                print(historial)
                
                if node == goal:
                    print('camino')
                    print(historial)
                    return historial
                
                if len(path) <= depth:
                    for fila, columna in reversed([(-1, 0), (0, 1), (1, 0), (0, -1)]):  # Arriba, derecha, abajo, izquierda
                        new_node = (node[0] + fila, node[1] + columna)
                        if self.is_valid_move(new_node):
                            stack.append((new_node, path + [new_node]))  # Añadir el nuevo nodo a la pila
                            print(f"Stack:{i} {stack}")
                else:

                    devuelta = list(reversed(path))
                    if stack:
                        if len(stack[-1][1]) >= 2:
                            nodo_padre_del_siguiente = stack[-1][1][-2]
                        else:
                            nodo_padre_del_siguiente = None  # Manejar el caso de desbordamiento
                    else:
                        # Manejar el caso donde la pila está vacía
                        nodo_padre_del_siguiente = None  # O alguna otra acción adecuad


                    for j in range(len(devuelta)):  # Iterar desde el final hasta el principio
                        if j != 0:
                            if devuelta[j] != nodo_padre_del_siguiente:
                                historial.append(devuelta[j])
                            else:
                                historial.append(devuelta[j])
                                break
                print()

        # Si se ha vaciado la pila y no se ha encontrado la meta, mostrar mensaje
        self.show_message(f"No se ha encontrado la meta dentro del límite de profundidad: {depth}")
        return []

    def distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def is_valid_move(self, pos):
        fila, columna = pos
        # verifica que la columna este dentro del ancho y la fila dentro del largo
        if 0 <= columna < len(self.maze[0]) and 0 <= fila < len(self.maze):
            return self.maze[fila][columna] == 0
        return False

    def move_mouse_step(self):
        # Mover el ratón al siguiente paso en el camino
        print("rana", self.path)
        if self.current_step < len(self.path):
            self.mouse_pos = list(self.path[self.current_step])
            self.current_step += 1
            # self.update()  # Redibuja el laberinto

            # Verifica si ha alcanzado la meta
            if self.mouse_pos == self.goal_pos:
                self.show_message("¡Llegaste a la meta! Kermit encontró a ELMO")  # Muestra el mensaje
                self.timer.stop()  # Detener el temporizador
                print("camino Cerda", self.pathPiggy)

            # Mueve a Piggy (la meta es la rana cuya pos ya no es la incial sino la de su primer paso)
            #self.piggy_pos = self.amplitud(tuple(self.piggy_pos), tuple(self.mouse_pos))
            self.piggy_pos = self.aasterisco(tuple(self.piggy_pos), tuple(self.mouse_pos), tuple(self.galleta_pos))

            self.pathPiggy.append(self.piggy_pos)
            print("camino Cerda", self.pathPiggy)

            self.update()  # Redibuja el laberinto

            if self.piggy_pos == tuple(self.mouse_pos):
                self.show_message("¡Piggy ha atrapado a Kermit!")
                self.timer.stop()  # Detener el temporizador
                print("camino Cerda", self.pathPiggy)
        else:
            self.timer.stop()  # Detener el temporizador si se llegó al final
            print("camino Cerda", self.pathPiggy)

    def paintEvent(self, event):
        # Dibuja el laberinto y el ratón
        qp = QPainter(self)
        cell_size = 50

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    qp.setBrush(QColor(100, 100 , 240))  # Pared (negro)
                else:
                    qp.setBrush(QColor(255, 255, 255))  # Camino (blanco)
                
                qp.drawRect(x * cell_size, y * cell_size, cell_size, cell_size)

        # Dibuja a ELMO
        qp.drawPixmap(self.goal_pos[1] * cell_size, self.goal_pos[0] * cell_size, cell_size, cell_size, self.elmo_image)

        qp.drawPixmap(self.galleta_pos[1] * cell_size, self.galleta_pos[0] * cell_size, cell_size, cell_size, self.galleta_image)

        # Dibuja el ratón usando la imagen
        qp.drawPixmap(self.mouse_pos[1] * cell_size, self.mouse_pos[0] * cell_size, cell_size, cell_size, self.mouse_image)

        #Dibuja pig
        qp.drawPixmap(self.piggy_pos[1] * cell_size, self.piggy_pos[0] * cell_size, cell_size, cell_size, self.piggy_image)

        

    def show_message(self, message):
        # Muestra un mensaje cuando se llega a la meta
        QMessageBox.information(self, "Meta Alcanzada", message)

    def amplitud(self, start, goal):
        i = 0
        # Implementación de búsqueda por amplitud
        queue = deque([(start, [start])])  # Usar una cola para BFS
        print(f"Queue PIGGY: {i} {queue}")

        while queue:
            i += 1
            (node, path) = queue.popleft()  # Extraer el primer nodo (FIFO)
            print(f"Queue PIGGY: {i} {queue}")

            if node == goal:
                # Retornar el siguiente nodo en el camino hacia el objetivo
                if len(path) > 1:  # Asegurarse de que hay un nodo siguiente
                    next_node = path[1]
                    print(f"Objetivo PIGGY encontrado, siguiente nodo a seguir: {next_node}")
                    return next_node
                else:
                    print("El nodo de inicio es el objetivo.")
                    return node  # Si el nodo inicial es el objetivo

            # Expandir nodos adyacentes
            for fila, columna in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Arriba, derecha, abajo, izquierda
                new_node = (node[0] + fila, node[1] + columna)
                if self.is_valid_move(new_node) and new_node not in path:
                    queue.append((new_node, path + [new_node]))  # Añadir el nuevo nodo a la cola
                    print(f"Queue PIGGY: {i} {queue}")

        print("Objetivo PIGGY no encontrado")
        return None  # Si no se encuentra el objetivo
    
    def aasterisco(self, start, goal, cookie):

        dis = self.distancia(start, goal)
        movI = 0
        costoNodo = movI + dis
        i = 0
        # Implementación de búsqueda por amplitud
        queue = deque([([start, [costoNodo, movI, dis]], [start])])  # Usar una cola para BFS
        print(f"Queue PIGGY: {i} {queue}")

        while queue:
            i += 1
            # Ordenar la cola según el costo (costoNodo) y extraer el nodo con menor costo
            queue = deque(sorted(queue, key=lambda x: x[0][1][0]))  # Ordenar por costo
            print(f"Queue PIGGY ORDENADO: {i} {queue}")
            (node, path) = queue.popleft()  # Extraer el nodo con menor costo
            print(f"Queue PIGGY: {i} {queue}")

            if node[0] == goal:
                # Retornar el siguiente nodo en el camino hacia el objetivo
                if len(path) > 1:  # Asegurarse de que hay un nodo siguiente
                    next_node = path[1]
                    print(f"Objetivo PIGGY encontrado, siguiente nodo a seguir: {next_node}")
                    return next_node
                else:
                    print("El nodo de inicio es el objetivo.")
                    return node[0]  # Si el nodo inicial es el objetivo

            # Expandir nodos adyacentes
            for fila, columna in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Arriba, derecha, abajo, izquierda
                new_node = (node[0][0] + fila, node[0][1] + columna)
                if self.is_valid_move(new_node) and new_node not in path:

                    if(cookie in path or cookie in self.pathPiggy):
                        new_costo = (node[1][1] + 0.5) 
                        new_dis =  self.distancia(new_node, goal)
                        new_total = new_costo + new_dis
                        queue.append(([new_node,[new_total,new_costo,new_dis]], path + [new_node]))  # Añadir el nuevo nodo a la cola
                    else:
                        new_costo = (node[1][1] + 1) 
                        new_dis =  self.distancia(new_node, goal)
                        new_total = new_costo + new_dis
                        queue.append(([new_node,[new_total,new_costo,new_dis]], path + [new_node]))  # Añadir el nuevo nodo a la cola
                        
                    print(f"Queue PIGGY: {i} {queue}")

                    if(new_node == cookie):
                        print('Comio Galleta')

        print("Objetivo PIGGY no encontrado")
        return None  # Si no se encuentra el objetivo
    
    
# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
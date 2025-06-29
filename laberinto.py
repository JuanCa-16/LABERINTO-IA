import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer
from collections import deque # Double-Ended-Queue: COLA doblemente terminada, permite agregar y eliminar al inicio y al final 
import random

# Ventana principal con el selector de mapas
class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__() # Llama al constructor de la calse padre (el del parentesis)
        self.setWindowTitle("Selector de Mapas") # Titulo de la Ventana
        self.setGeometry(500, 200, 300, 150)  # Posición (x, y) y tamaño (ancho, alto) de la ventana

        # Layout y widgets
        layout = QVBoxLayout() # Layout vertical que tendra los widgets
        self.etiqueta = QLabel("Selecciona un mapa:") # Crear Etiqueta
        layout.addWidget(self.etiqueta) # Añadir al clayout

        # ComboBox para seleccionar métodos de búsqueda
        self.metodo_seleccionado = QComboBox()
        self.metodo_seleccionado.addItems(["No evitar ciclos", "Evitar ciclos"])  # Opciones de búsqueda
        layout.addWidget(self.metodo_seleccionado)

        # ComboBox para seleccionar mapas
        self.selector_mapa = QComboBox()
        self.selector_mapa.addItems(["Mapa 1", "Mapa 2", "Mapa 3", "Mapa 4"])  # Nombres de mapas
        layout.addWidget(self.selector_mapa)

        # Botón para cargar el mapa seleccionado
        self.boton_carga = QPushButton("Cargar Mapa")
        self.boton_carga.clicked.connect(self.cargar_mapa)  # Conecta el clic del botón con el método del ()
        layout.addWidget(self.boton_carga)

        container = QWidget() # Crear contenedor que contendra al layout
        container.setLayout(layout) # Asigna el layout al contenedor
        self.setCentralWidget(container)# Define el contenedor como el widget central de la ventana

    def cargar_mapa(self):
        # Obtener el mapa seleccionado y el método de búsqueda
        mapa_seleccionado = self.selector_mapa.currentText() # Obtiene el mapa seleccionado en el menu
        evitar_ciclos = self.metodo_seleccionado.currentText() == "Evitar ciclos" # Verifica opcion seleccionada
        self.laberinto_window = LaberintoWindow(mapa_seleccionado, evitar_ciclos) # Crea una nueva ventana LaberintoWindow con el mapa y método seleccionados
        self.laberinto_window.show() # Muestra la nueva ventana LaberintoWindow

# Ventana del laberinto
class LaberintoWindow(QMainWindow):

    def __init__(self, nombre_mapa, evitar_ciclos):

        super().__init__()
        self.setWindowTitle(f"Laberinto - {nombre_mapa}")
        self.setGeometry(100, 100, 400, 400)

        # Definir los mapas según la selección
        self.info_mapas(nombre_mapa) # Llama a la función para definir los parametros de los mapas en función del nombre_mapa seleccionado


        self.paso_a_asterisco = False

        # Cargar imagenes
        self.kermit_img = QPixmap("kermit.jpg")
        self.elmo_img = QPixmap("elmo.jpg")
        self.piggy_img= QPixmap("pig.jpg")
        self.galleta_img = QPixmap("galleta.jpg")

        # Temporizador para mover a Kermit
        self.timer = QTimer() # Crea un temporizador (QTimer) que controlará el movimiento de los elementos
        self.timer.timeout.connect(self.mover_rana) # Conecta el tiempo de espera del temporizador con la función que mueve a la rana
        
        # Lista de pasos
        self.camino = [] # Nodos del camino de Kermit
        self.caminoPiggy = [] # Nodos del camino de Piggy
        self.paso_actual = 0

        # Configurar el widget central
        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        # Iniciar la búsqueda y movimiento
        self.iniciar_movimiento(evitar_ciclos) # Llama a la función que inicia el proceso de búsqued

    def info_mapas(self, nombre_mapa):

        # Mapas de los laberintos 1(obstaculo) 0(camino) y sus variables
        # Matriz 7x7

        if nombre_mapa == "Mapa 1":
            self.mapa_laberinto = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.pos_rana = [5, 5]
            self.pos_meta = [1, 5]
            self.pos_piggy = [1, 1]
            self.pos_galleta = [1, 3]
            self.limite_profundidad = 4
        elif nombre_mapa == "Mapa 2":
            self.mapa_laberinto = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.pos_rana = [5, 1]
            self.pos_meta = [1, 1]
            self.pos_piggy = [1, 5]
            self.pos_galleta = [3, 5]
            self.limite_profundidad = 8
        elif nombre_mapa == "Mapa 3":
            self.mapa_laberinto = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.pos_rana = [2, 3]
            self.pos_meta = [4, 2]
            self.pos_piggy = [2, 1]
            self.pos_galleta = [2, 5]
            self.limite_profundidad = 4 # 4 8 y 15 
        elif nombre_mapa == "Mapa 4":
            self.mapa_laberinto = [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
            self.pos_rana = [1, 5]
            self.pos_meta = [3, 1]
            self.pos_piggy = [3, 4]
            self.pos_galleta = [2, 2]
            self.limite_profundidad = 20

    def busqueda_limitada_profundidad(self, inicio, meta, profundidad, evitar_ciclos):

        # Implementación de búsqueda limitada por profundidad usando una pila (LIFO)
        i = 0
        pila = [(inicio, [inicio])]   # Inicializa la pila con el nodo inicial y su camino hasta ese nodo
        historial = [] # Lista para almacenar el historial de nodos visitados
        
        print(f"-- Pila: {i} {pila}")
        print()
        
        while pila: # Bucle mientras haya nodos en la pila

            if evitar_ciclos:
                i += 1
                print(f"-- Pila: {i} Inicia: {pila}")
                (nodo, path) = pila.pop()  # Extrae el último nodo (el que se expandera) y su camino desde la pila (LIFO)
                print(f"-- Pila: {i} tras expandir:{pila}")
                historial.append(nodo) # Añade el nodo al historial de nodos visitados

                if nodo == meta:
                    print(f">> Camino KERMIT a META: {i} {path}")
                    return path
                
                if len(path) <= profundidad: # Si no ha excedido el límite de profundidad

                    for fila, columna in reversed([(-1, 0), (0, 1), (1, 0), (0, -1)]):  # Arriba, derecha, abajo, izquierda

                        nuevo_nodo = (nodo[0] + fila, nodo[1] + columna)
                        
                        if self.validar_mov(nuevo_nodo) and nuevo_nodo not in path:   # Verifica si el movimiento es válido y no forma un ciclo en el path
                            pila.append((nuevo_nodo, path + [nuevo_nodo]))    # Añade el nuevo nodo y su camino a la pila
                            print(f"-- Pila: {i} hijo expandido: {pila}")

                print(f">> Camino en {i}: {historial}")
                print()
                
            else:

                i += 1
                print(f"-- Pila: {i} Inicia: {pila}")
                (nodo, path) = pila.pop()  # Extrae el último nodo (el que se expandera) y su camino desde la pila (LIFO)
                print(f"-- Pila: {i} tras expandir:{pila}")
                historial.append(nodo)

                if nodo == meta:
                    print(f">> Camino Kermit a META: {i} {path}") #si devuelvo el historial es el de expandido y ahi tendria que descomentar el else para evitar saltos se usa es pa mostrar tdo el recorrido por decirlo asi todo el arbol y no solo la rama correcta
                    return path
                
                if len(path) <= profundidad: # Si no ha excedido el límite de profundidad

                    for fila, columna in reversed([(-1, 0), (0, 1), (1, 0), (0, -1)]):  # Arriba, derecha, abajo, izquierda
                        
                        nuevo_nodo = (nodo[0] + fila, nodo[1] + columna)

                        if self.validar_mov(nuevo_nodo) :  # Verifica si el movimiento es válido

                            if(i >= 2): #desde el segundo mov, es decir despues de expandir la raiz
                                if(nuevo_nodo != path[-2]): #que no se devuelva
                                    pila.append((nuevo_nodo, path + [nuevo_nodo])) # Añade el nuevo nodo y su camino a la pila
                                    print(f"-- Pila: {i} hijo expandido: {pila}")
                            else:
                                pila.append((nuevo_nodo, path + [nuevo_nodo])) # Añade el nuevo nodo y su camino a la pila
                                print(f"-- Pila: {i} hijo expandido: {pila}")
                #else: # Si el camino ha excedido la profundidad

                    # devuelta = list(reversed(path))  # Invierte el camino para volver sobre los pasos

                    # # Para tener el padre del siguiente nodo a expandir
                    # # Ya que es el nodo en comun entre la rama actual y la sigueinte 

                    # if pila:  # Si hay nodos restantes en la pila
                    #     if len(pila[-1][1]) >= 2:  # Si el camino del siguiente nodo a expandir tiene al menos dos nodos (propio y papa)
                    #         nodo_padre_del_siguiente = pila[-1][1][-2] # Obtiene el nodo padre del siguiente nodo
                    #     else:
                    #         nodo_padre_del_siguiente = None  # Si no hay suficiente profundidad, se asigna None
                    # else:
                    #     # Manejar el caso donde la pila está vacía
                    #     nodo_padre_del_siguiente = None  # O alguna otra acción adecuad

                    # # Retrocede sobre el camino
                    # for j in range(len(devuelta)):  # Itera desde el último hasta el primer nodo del camino
                        
                    #     if j != 0:  # Salta el primer nodo (actual)

                    #         if devuelta[j] != nodo_padre_del_siguiente:  # Si el nodo actual no es el padre del siguiente nodo (osea no es el comun entre las ramas)
                    #             historial.append(devuelta[j])  # Añade el nodo al historial
                    #         else:
                    #             historial.append(devuelta[j]) # Añade el nodo y termina el retroceso
                    #             break

                print(f">> Camino en: {i}: {historial}")
                print()

        # Si se ha vaciado la pila y no se ha encontrado la meta, mostrar mensaje
        self.mostrar_mensajes(f"No se ha encontrado la meta dentro del límite de profundidad: {profundidad}")
        return []

    def iniciar_movimiento(self, evitar_ciclos):

        # Aquí se realiza la búsqueda del camino de Kermit
        # Por el metodo de limitada por profundidad
        self.camino = self.busqueda_limitada_profundidad(tuple(self.pos_rana), tuple(self.pos_meta), self.limite_profundidad, evitar_ciclos=evitar_ciclos)
        self.caminoPiggy.append(tuple(self.pos_piggy))


        if self.camino: # Si se ha encontrado un camino para Kermit entonces:
            self.paso_actual = 1 # Antes era 0 pero ese es su pos actual ahora es su primr paso que sera la meta de la rana
            self.timer.start(1000) # Inicia el temporizador para que Kermit se mueva (lo conectamos en __init__) cada 1000 ms (1 segundo)
    
    def mover_rana(self):

        print()

        # Mover el ratón al siguiente paso en el camino
        if self.paso_actual < len(self.camino):
            self.pos_rana = list(self.camino[self.paso_actual])
            self.paso_actual += 1
            self.update()  # Redibuja el laberinto con solo el mov de rana

            # Verifica si ha alcanzado la meta
            if self.pos_rana == self.pos_meta:
                self.mostrar_mensajes("¡Llegaste a la meta! Kermit encontró a ELMO")  # Muestra el mensaje
                self.timer.stop()  # Detener el temporizador
                print("xx Camino Piggy: ", self.caminoPiggy)

            # Si el método aún no ha cambiado a A*, se determina si hay un 40% de probabilidad de cambiar
            if not self.paso_a_asterisco:
                probabilidad = random.random()
                if probabilidad < 0.4:
                    # Cambiar a A* si no se ha cambiado aún
                    self.paso_a_asterisco = True
                    print("Cambiando a A*")

            # MOVER a Piggy (la meta es la rana cuya pos ya no es la incial sino la de su primer paso) 
            # Si ya se ha cambiado a A*, siempre usar A*
            if self.paso_a_asterisco:
                # Usar A* para mover a Piggy
                self.pos_piggy = self.aasterisco(tuple(self.pos_piggy), tuple(self.pos_rana), tuple(self.pos_galleta))
            else:
                # Usar búsqueda por amplitud para mover a Piggy
                self.pos_piggy = self.amplitud(tuple(self.pos_piggy), tuple(self.pos_rana))

            self.caminoPiggy.append(self.pos_piggy)
            print("xx Camino Piggy: ", self.caminoPiggy)

            if self.pos_piggy == tuple(self.pos_galleta):
                self.mostrar_mensajes(" has econtrado la cookie")

            self.update()  # Redibuja el laberinto con el movimiento de ambos

            if self.pos_piggy == tuple(self.pos_rana):
                self.mostrar_mensajes("¡Piggy ha atrapado a Kermit!")
                self.timer.stop()  # Detener el temporizador
                print("xx Camino Piggy: ", self.caminoPiggy)
        else:
            self.timer.stop()  # Detener el temporizador si se llegó al final

    def distancia(self, pos1, pos2):

        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def validar_mov(self, pos):

        fila, columna = pos

        # verifica que la columna este dentro del ancho y la fila dentro del largo
        if 0 <= columna < len(self.mapa_laberinto[0]) and 0 <= fila < len(self.mapa_laberinto):

            return self.mapa_laberinto[fila][columna] == 0
        
        return False

    # Implementación de búsqueda por AMPLITUD
    def amplitud(self, inicio, meta):
        i = 0
        queue = deque([(inicio, [inicio])])  # Usaremos una COLA, FIFO
        print(f"## Cola PIGGY {i}: {queue}")
        print()

        # Bucle que continúa mientras haya nodos en la cola.
        while queue:
            i += 1
            print(f"## Cola PIGGY: {i} Inicia: {queue}")
            (nodo, path) = queue.popleft()  # Extrae el primer nodo de la cola (FIFO) y su camino asociado.
            print(f"## Cola PIGGY: {i} tras Expandir: {queue}")

            if nodo == meta:
                # Retornar el siguiente nodo en el camino hacia el objetivo
                if len(path) > 1:  # Asegurarse de que hay un nodo siguiente
                    next_nodo = path[1]
                    print(f"META PIGGY encontrado, siguiente nodo a seguir: {next_nodo}")
                    return next_nodo
                else:
                    print(f"META PIGGY encontrado, el nodo de inicio es el objetivo: {nodo}")
                    return nodo  # Si el nodo inicial es el objetivo

            # Expande los nodos adyacentes para explorar.

            for fila, columna in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Arriba, derecha, abajo, izquierda

                nuevo_nodo = (nodo[0] + fila, nodo[1] + columna)

                # Verifica si el nuevo nodo es válido y no ha sido visitado en el camino actual.
                if self.validar_mov(nuevo_nodo) and nuevo_nodo not in path:

                    queue.append((nuevo_nodo, path + [nuevo_nodo]))   # Añade el nuevo nodo a la cola con el camino actualizado.
                    print(f"Queue PIGGY: {i} {queue}")
                    print(f"## Cola PIGGY {i}: hijo del expandido: {queue}")

            print()

        print("!! Objetivo PIGGY no encontrado")
        return None  # Si no se encuentra el objetivo
    
    # Implementación de búsqueda por A*
    def aasterisco(self, inicio, meta, cookie):

        dis = self.distancia(inicio, meta) # Distancia manhattan (heuristica) en pos actual
        movI = 0 
        costoNodo = movI + dis
        i = 0
        
        # Usar una cola para implementar A* con el estado del nodo y el camino.
        queue = deque([([inicio, [costoNodo, movI, dis]], [inicio])]) 
        print(f"## Cola PIGGY {i}: {queue}")
        print()
        while queue:
            i += 1
            # Ordenar la cola según el costo (costoNodo) y extraer el nodo con menor costo

            print(f"## Cola PIGGY: {i} Inicia: {queue}")
            queue = deque(sorted(queue, key=lambda x: x[0][1][0]))  # Ordenar por costo
            print(f"## Cola PIGGY Ordenado: {i} {queue}")
            (nodo, path) = queue.popleft()  # Extraer el nodo con menor costo
            print(f"## Cola PIGGY: {i} tras expandir: {queue}")

            # Bucle que continúa mientras haya nodos en la cola.
            if nodo[0] == meta:

                # Retornar el siguiente nodo en el camino hacia el objetivo
                if len(path) > 1:  # Asegurarse de que hay un nodo siguiente
                    next_nodo = path[1]
                    print(f"META PIGGY encontrado, siguiente nodo a seguir: {next_nodo}")
                    return next_nodo
                else:
                    print(f"META PIGGY encontrado, el nodo de inicio es el objetivo: {nodo[0]}")
                    return nodo[0]  # Si el nodo inicial es el objetivo

            # Expandir nodos adyacentes

            for fila, columna in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Arriba, derecha, abajo, izquierda

                nuevo_nodo = (nodo[0][0] + fila, nodo[0][1] + columna)

                # Verifica si el nuevo nodo es válido y no ha sido visitado en el camino actual.
                if self.validar_mov(nuevo_nodo) and nuevo_nodo not in path:

                    # Si la cookie ha sido consumida o está en el camino actual, ajustar el costo.
                    if(cookie in path or cookie in self.caminoPiggy):
                        new_costo = (nodo[1][1] + 0.5) 
                        new_dis =  self.distancia(nuevo_nodo, meta)
                        new_total = new_costo + new_dis
                        queue.append(([nuevo_nodo,[new_total,new_costo,new_dis]], path + [nuevo_nodo]))  # Añadir el nuevo nodo a la cola
                    else:
                        new_costo = (nodo[1][1] + 1) 
                        new_dis =  self.distancia(nuevo_nodo, meta)
                        new_total = new_costo + new_dis
                        queue.append(([nuevo_nodo,[new_total,new_costo,new_dis]], path + [nuevo_nodo]))  # Añadir el nuevo nodo a la cola
                        
                    print(f"## Cola PIGGY: {i} hijo: {queue}")

                    if(nuevo_nodo == cookie):
                        print('^^ Comio Galleta ^^')

            print()

        print("XX Objetivo PIGGY no encontrado")
        return None  # Si no se encuentra el objetivo
    
    def paintEvent(self, event):

        # Dibuja el laberinto y el ratón
        qp = QPainter(self) # Crea un objeto QPainter que permitirá realizar las operaciones de dibujo
        tamano_celda = 50

        # Dibuja el mapa del laberinto
        for y, fila in enumerate(self.mapa_laberinto): # Itera por cada fila del mapa y: indice Fila, fila: valor fila actual([0,1,0...])

            for x, columna in enumerate(fila): # Itera por cada columna de la fila

                if columna == 1: 
                    qp.setBrush(QColor(100, 100 , 240))  # Pared (negro)
                else:
                    qp.setBrush(QColor(255, 255, 255))  # Camino (blanco)
                
                qp.drawRect(x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
                # Dibuja las coordenadas (fila, columna) en cada celda
                qp.setPen(QColor(200, 200, 200))  # Establece el color de la fuente a gris claro
                qp.setFont(QFont('Arial', 6))  # Fuente pequeña para las coordenadas
                # Dibuja el texto de coordenadas en la celda (ajustado al tamaño de la celda)
                # El texto se coloca un poco hacia el centro de la celda, con desplazamiento ajustado
                qp.drawText(x * tamano_celda + 2, y * tamano_celda + 12, f'{y},{x}')

        # Dibuja a Elmo
        qp.drawPixmap(self.pos_meta[1] * tamano_celda, self.pos_meta[0] * tamano_celda, tamano_celda, tamano_celda, self.elmo_img)

        # Dibuja a Galleta
        qp.drawPixmap(self.pos_galleta[1] * tamano_celda, self.pos_galleta[0] * tamano_celda, tamano_celda, tamano_celda, self.galleta_img)

        # Dibuja a Kermit
        qp.drawPixmap(self.pos_rana[1] * tamano_celda, self.pos_rana[0] * tamano_celda, tamano_celda, tamano_celda, self.kermit_img)

        #Dibuja Piggy
        qp.drawPixmap(self.pos_piggy[1] * tamano_celda, self.pos_piggy[0] * tamano_celda, tamano_celda, tamano_celda, self.piggy_img)

    def mostrar_mensajes(self, message):
        # Muestra un mensaje cuando se llega a la meta
        QMessageBox.information(self, "Meta Alcanzada", message)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
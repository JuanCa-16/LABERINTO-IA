# 🐸 IA‑Laberinto‑Kermit

Implementación en **Python + PyQt 6** de un agente en laberinto para la asignatura **Inteligencia Artificial – Universidad del Valle**.  
El objetivo es guiar a **René (Kermit)** mediante **búsqueda limitada por profundidad** hasta su amigo **Elmo**, mientras **Piggy** lo persigue usando **búsqueda en amplitud** y, con probabilidad del 40 %, cambia a **A***.  

El mapa contiene una **galleta**; si Kermit la toma, puede avanzar dos casillas por el costo de una. El juego termina cuando:

1. Kermit llega a Elmo (victoria del jugador).  
2. Piggy alcanza a Kermit (victoria de Piggy).  

---

## 🎮 Reglas resumidas

| Elemento | Algoritmo | Costo de movimiento | Condición especial |
|----------|-----------|---------------------|--------------------|
| **Kermit** | Búsqueda limitada por profundidad (D‑LS) | 1 por paso<br/>½ si tiene galleta | Evita ciclos opcional |
| **Piggy**  | BFS (amplitud); 40 % de prob. de cambiar a **A\*** cada turno | 1 por paso | Se detiene al alcanzar a Kermit |
| **Galleta** | - | Otorga a Kermit movimiento doble al mismo coste | - |

---

## 🏗️ Estructura del proyecto

```
laberinto_kermit/
├── laberinto.py            # Punto de entrada (GUI y lógica completa)
├── kermit.jpg              # Sprite de Kermit
├── elmo.jpg                # Sprite de Elmo
├── pig.jpg                 # Sprite de Piggy
├── galleta.jpg             # Sprite de la galleta
└── README.md
```

---

## ⚙️ Requisitos

```
Python 3.10+
PyQt6
```

Instalación rápida (recomendado dentro de un entorno virtual):

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
.\venv\Scripts\activate     # Windows
pip install PyQt6
```

---

## 🚀 Ejecución

```bash
python laberinto.py
```

Se abrirá una **ventana de selección** donde eliges:

1. Mapa (cuatro laberintos prediseñados).  
2. Estrategia de Kermit (evitar o no ciclos).  

Después pulsa **«Cargar Mapa»** y observa la partida en tiempo real.

---

## 🧠 Algoritmos y heurísticas

| Agente | Estrategia | Detalles |
|--------|-----------|----------|
| **Kermit** | Depth‑Limited Search | Límite de profundidad configurable por mapa. Opción de «Evitar ciclos» filtrando caminos repetidos. |
| **Piggy – BFS** | Búsqueda en amplitud | Cola FIFO. Siempre avanza por el camino más corto conocido al estado actual de Kermit. |
| **Piggy – A\*** | Heurística Manhattan | Cada turno hay 40 % de probabilidad de cambiar de BFS a A\*. La heurística suma: `g(n) = pasos` y `h(n) = distancia de Manhattan`. |
| **Cookie boost** | ‑ | Si Kermit pasa por la galleta, su costo de movimiento se divide a la mitad durante el resto de la partida. Esto se refleja internamente como `+0.5` en la función de coste. |

---

## 📐 Interfaz gráfica

- Desarrollada con **PyQt 6** (`QMainWindow`, `QPainter`, `QTimer`).  
- Tablero fijo 7 × 7, celdas de 50 px.  
- Sprites PNG/JPG para cada personaje y la galleta.  
- Coordenadas de depuración visibles en cada celda.


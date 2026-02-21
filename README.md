# 🍴 Problema de los Filósofos Comensales

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Implementación del problema clásico de sincronización de los **Filósofos Comensales** utilizando el **Algoritmo de Peterson** para exclusión mutua y la **Estrategia del Filósofo Zurdo** para prevención de deadlock.

---

## 📋 Descripción del Problema

Cinco filósofos se sientan alrededor de una mesa circular con un tazón de espagueti. Entre cada par de filósofos hay un tenedor (5 tenedores en total). Los filósofos alternan entre dos actividades:

- 🧠 **PENSAR**: No requiere recursos
- 🍝 **COMER**: Requiere ambos tenedores (izquierdo y derecho)

### 🎯 Desafíos de Sincronización

1. **Exclusión Mutua**: Un tenedor solo puede ser usado por un filósofo a la vez
2. **Deadlock**: Evitar que todos tomen un tenedor y esperen el otro indefinidamente
3. **Starvation**: Garantizar que todos los filósofos eventualmente coman

### 🚫 Restricción del Laboratorio

**NO se permite usar primitivas de sincronización del sistema operativo:**
- ❌ `threading.Lock`
- ❌ `threading.Semaphore`
- ❌ `threading.Condition`
- ✅ Solo `threading.Thread`

La exclusión mutua debe implementarse **manualmente por software**.

---

## 🧩 Solución Implementada

### 1️⃣ Algoritmo de Peterson

Implementación por software de exclusión mutua entre 2 procesos sin primitivas del SO.

**Características:**
- Usa solo 2 variables compartidas: `flag[]` (intenciones) y `turn` (cortesía)
- Garantiza: Exclusión Mutua, Progreso y Espera Limitada
- Cada tenedor es un `PetersonLock` independiente

**Cómo funciona:**
```python
# Entrada a la sección crítica
flag[yo] = True      # 1. Declaro mi intención
turn = otro          # 2. Cedo cortésmente el turno
while flag[otro] and turn == otro:  # 3. Espero si el otro quiere Y es su turno
    pass

# Salida de la sección crítica
flag[yo] = False     # Bajo mi bandera
```

### 2️⃣ Estrategia del Filósofo Zurdo

Previene deadlock rompiendo la espera circular (una de las 4 condiciones de Coffman).

**Implementación:**
- **Filósofos 1-4 (diestros)**: Toman tenedor IZQUIERDO primero, luego DERECHO
- **Filósofo 0 (zurdo)**: Toma tenedor DERECHO primero, luego IZQUIERDO

Al invertir el orden de adquisición de un filósofo, se rompe el ciclo de espera y se **elimina la posibilidad de deadlock**.

---

## 🏗️ Arquitectura del Código

```
📁 Proyecto/
├── 📄 main.py              # Punto de entrada, configuración y presentación
├── 📄 mesa.py              # Orquestación de hilos y recolección de estadísticas
├── 📄 filosofo.py          # Lógica del comportamiento de cada filósofo
├── 📄 peterson_lock.py     # Implementación del Algoritmo de Peterson
│
└── 📚 Documentación/
    ├── README_PRESENTACION.md     # Índice de guías
    ├── GUIA_PRESENTACION.md       # Guía completa para presentar
    ├── CHEAT_SHEET.md             # Consulta rápida
    ├── PETERSON_DETALLADO.md      # Deep dive en Peterson
    ├── JUSTIFICACION_TECNICA.md   # Decisiones de diseño
    └── SCRIPT_PRESENTACION.md     # Script de presentación
```

### Responsabilidades por Módulo

| Módulo | Responsabilidad |
|--------|----------------|
| `main.py` | Configuración (NUM_FILOSOFOS, tiempos) y presentación de resultados |
| `mesa.py` | Crear hilos, gestionar ciclo de vida de simulación, estadísticas |
| `filosofo.py` | Ciclo PENSAR → TOMAR → COMER → SOLTAR, estrategia del zurdo |
| `peterson_lock.py` | Exclusión mutua entre 2 procesos (reemplazo de `threading.Lock`) |

---

## 🚀 Instalación y Ejecución

### Requisitos

- Python 3.8 o superior
- Módulos estándar: `threading`, `time` (incluidos en Python)

### Ejecución

```bash
# Clonar o descargar el repositorio
cd CC3064-Laboratorio1

# Ejecutar la simulación
python main.py
```

### Salida Esperada

```
=== Filósofos Comensales - Peterson Lock + Filósofo Zurdo ===
Filósofos: 5 | Duración: 60s

Filósofo 0 (ZURDO) COMIENDO [tenedores: 0, 1]
Filósofo 2 (DIESTRO) COMIENDO [tenedores: 2, 3]
Filósofo 4 (DIESTRO) COMIENDO [tenedores: 4, 0]
...

--- Finalizando ---

=== RESULTADOS ===
Filósofo 0 (ZURDO): 45 comidas
Filósofo 1 (DIESTRO): 47 comidas
Filósofo 2 (DIESTRO): 43 comidas
Filósofo 3 (DIESTRO): 46 comidas
Filósofo 4 (DIESTRO): 44 comidas

Total: 225 | Promedio: 45.0 | Min: 43 | Max: 47
Sin deadlock
```

---

## ⚙️ Configuración

Modifica las constantes en `main.py`:

```python
NUM_FILOSOFOS = 5           # Número de filósofos/tenedores
DURACION_SIMULACION = 60    # Segundos de simulación
TIEMPO_COMER_BASE = 0.3     # Tiempo base de comer (s)
TIEMPO_PENSAR_BASE = 0.3    # Tiempo base de pensar (s)
```

---

## 🔬 Conceptos Técnicos

### Algoritmo de Peterson

**Propiedades Formales:**
1. ✅ **Exclusión Mutua**: Nunca dos procesos en sección crítica simultáneamente
2. ✅ **Progreso**: Si ninguno está dentro, alguno podrá entrar
3. ✅ **Espera Limitada**: Ningún proceso espera indefinidamente

**Asignación de Roles:**
- Filósofo `i` → Tenedor IZQUIERDO (`tenedor[i]`) → Rol 0 en Peterson
- Filósofo `i` → Tenedor DERECHO (`tenedor[(i+1)%N]`) → Rol 1 en Peterson

Cada tenedor tiene exactamente un proceso 0 y un proceso 1.

### Condiciones de Coffman (Deadlock)

Para que ocurra deadlock se necesitan **las 4 condiciones**:

| Condición | ¿Se Cumple? | Nota |
|-----------|-------------|------|
| 1. Exclusión Mutua | ✅ Sí | Cada tenedor para 1 filósofo |
| 2. Retención y Espera | ✅ Sí | Retienen un tenedor esperando otro |
| 3. No Desalojo | ✅ Sí | No se quitan tenedores por fuerza |
| 4. Espera Circular | ❌ **NO** | **Rota por el filósofo zurdo** |

Como falta una condición, **el deadlock es imposible**.

---

## 📊 Análisis de Resultados

### Métricas de Corrección

1. **Sin Deadlock**: La simulación termina exitosamente en 60 segundos
2. **Sin Starvation**: Todos los filósofos comen > 0 veces
3. **Exclusión Mutua**: Nunca dos filósofos vecinos comen simultáneamente
4. **Fairness**: Ratio Máx/Mín < 2.0 (distribución equitativa)

### Ejemplo de Estadísticas

```
Total de comidas:    225
Duración:           60.02 segundos
Promedio:           45.0 comidas/filósofo
Máximo:             47 comidas
Mínimo:             43 comidas
Ratio Máx/Mín:      1.09 (Equitativo)
```

---

## 🎓 Conceptos de Sistemas Operativos

Este proyecto demuestra:

- **Sincronización de procesos**: Coordinación de hilos concurrentes
- **Exclusión mutua**: Acceso controlado a recursos compartidos
- **Prevención de deadlock**: Romper condiciones de Coffman
- **Algoritmos de sincronización por software**: Peterson, Dekker
- **Concurrencia vs Paralelismo**: GIL de Python permite concurrencia sin paralelismo real
- **Busy-wait vs Blocking**: Trade-offs de eficiencia

---

## 🔍 Preguntas Frecuentes

### ¿Por qué Peterson y no `threading.Lock`?

**R:** La restricción del laboratorio es implementar exclusión mutua manualmente. `Lock` usa instrucciones atómicas del hardware (test-and-set). Peterson logra lo mismo pero **solo con software**, enseñando los fundamentos.

### ¿Puede haber starvation?

**R:** Teóricamente sí, prácticamente no. Peterson garantiza espera limitada entre 2 procesos, y los tiempos aleatorios + scheduling del SO distribuyen oportunidades. Las estadísticas lo confirman.

### ¿Por qué busy-wait en lugar de sleep()?

**R:** Es inherente al algoritmo de Peterson. Si usamos `sleep()` en el while, podemos perder la ventana donde `flag[otro]` cambia, violando la corrección.

### ¿Funciona con N filósofos?

**R:** Sí, con cualquier N ≥ 2. Cada tenedor sigue siendo compartido por exactamente 2 filósofos vecinos, y Peterson aplica correctamente.

---

## 📚 Referencias

- **Peterson, G. L.** (1981). *Myths About the Mutual Exclusion Problem*. Information Processing Letters.
- **Dijkstra, E. W.** (1971). *Hierarchical Ordering of Sequential Processes*. Acta Informatica.
- **Tanenbaum, A. S.** (2014). *Modern Operating Systems* (4th ed.). Pearson.

---

## 👨‍💻 Autor

**Daniel** - CC3064 Sistemas Operativos  
Universidad del Valle de Guatemala - Semestre 7

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para propósitos educativos.

---

## 🙏 Agradecimientos

- A los profesores de Sistemas Operativos por plantear este desafío educativo
- A la comunidad de Python por las herramientas threading
- A Dijkstra, Peterson y Lamport por sus contribuciones seminales a la sincronización

---

**¿Preguntas o sugerencias?** Abre un issue o contacta al autor.

**Nota:** Para guías de presentación detalladas, consulta [README_PRESENTACION.md](README_PRESENTACION.md).
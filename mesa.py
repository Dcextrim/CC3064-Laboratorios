import threading
import time
from peterson_lock import PetersonLock
from filosofo import filosofo


class Mesa:
    
    def __init__(self, num_filosofos, duracion, tiempo_comer, tiempo_pensar):
        self.num_filosofos = num_filosofos
        self.duracion = duracion
        self.tiempo_comer = tiempo_comer
        self.tiempo_pensar = tiempo_pensar
        
        self.tenedores = [PetersonLock(nombre=f"Tenedor-{f}") for f in range(num_filosofos)]
        self.simulacion_activa = [True]
        self.conteo_comidas = [0] * num_filosofos
        self.inicio_simulacion = 0.0
        self.hilos = []
    
    def simulacion_activa_fn(self):
        return self.simulacion_activa[0]
    
    def iniciar(self):
        """Crea e inicia todos los hilos de filósofos"""
        self.inicio_simulacion = time.time()
        
        for i in range(self.num_filosofos):
            hilo = threading.Thread(
                target=filosofo,
                args=(i, self.tenedores, self.simulacion_activa_fn, 
                      self.conteo_comidas, self.inicio_simulacion,
                      self.tiempo_comer, self.tiempo_pensar),
                name=f"Filosofo-{i}",
                daemon=True
            )
            self.hilos.append(hilo)
            hilo.start()
    
    def esperar(self):
        """Espera la duración configurada"""
        try:
            time.sleep(self.duracion)
        except KeyboardInterrupt:
            print("\n[!] Interrupción detectada.")
    
    def detener(self):
        """Detiene la simulación y espera que los hilos terminen"""
        self.simulacion_activa[0] = False
        
        for hilo in self.hilos:
            hilo.join(timeout=10)
    
    def obtener_estadisticas(self):
        """Retorna las estadísticas de la simulación"""
        duracion_real = time.time() - self.inicio_simulacion
        total_comidas = sum(self.conteo_comidas)
        max_comidas = max(self.conteo_comidas)
        min_comidas = min(self.conteo_comidas)
        promedio = total_comidas / self.num_filosofos
        ratio = max_comidas / min_comidas if min_comidas > 0 else 0
        
        return {
            'conteo_comidas': self.conteo_comidas,
            'duracion_real': duracion_real,
            'total_comidas': total_comidas,
            'max_comidas': max_comidas,
            'min_comidas': min_comidas,
            'promedio': promedio,
            'ratio': ratio
        }

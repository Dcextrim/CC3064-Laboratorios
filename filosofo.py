import time

def filosofo(id_fil, tenedores, simulacion_activa_fn, conteo_comidas, inicio_simulacion, 
             tiempo_comer, tiempo_pensar):

    num_filosofos = len(tenedores)
    tenedor_izq = id_fil
    tenedor_der = (id_fil + 1) % num_filosofos

    ROL_EN_IZQUIERDO = 0
    ROL_EN_DERECHO = 1

    es_zurdo = (id_fil == 0)
    tipo = "ZURDO" if es_zurdo else "DIESTRO"

    while simulacion_activa_fn():
        # FASE 1: PENSAR
        time.sleep(tiempo_pensar * (0.5 + (id_fil % 3) * 0.25))

        # FASE 2: TOMAR TENEDORES (orden depende si es zurdo o diestro)
        if es_zurdo:
            tenedores[tenedor_der].acquire(ROL_EN_DERECHO)
            tenedores[tenedor_izq].acquire(ROL_EN_IZQUIERDO)
        else:
            tenedores[tenedor_izq].acquire(ROL_EN_IZQUIERDO)
            tenedores[tenedor_der].acquire(ROL_EN_DERECHO)

        # SECCIÓN CRÍTICA: COMER
        print(f"Filósofo {id_fil} ({tipo}) COMIENDO [tenedores: {tenedor_izq}, {tenedor_der}]")
        time.sleep(tiempo_comer)
        conteo_comidas[id_fil] += 1

        # FASE 3: SOLTAR TENEDORES
        if es_zurdo:
            tenedores[tenedor_izq].release(ROL_EN_IZQUIERDO)
            tenedores[tenedor_der].release(ROL_EN_DERECHO)
        else:
            tenedores[tenedor_der].release(ROL_EN_DERECHO)
            tenedores[tenedor_izq].release(ROL_EN_IZQUIERDO)

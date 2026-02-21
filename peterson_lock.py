class PetersonLock:

    def __init__(self, nombre=""):
        self.flag = [False, False]
        self.turn = 0
        self.nombre = nombre

    def acquire(self, proceso_id):
        otro = 1 - proceso_id
        self.flag[proceso_id] = True
        self.turn = otro
        while self.flag[otro] and self.turn == otro:
            pass

    def release(self, proceso_id):
        self.flag[proceso_id] = False

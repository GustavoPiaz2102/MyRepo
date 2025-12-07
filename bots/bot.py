import pyautogui
from time import sleep, time
import numpy as np
from ultralytics import YOLO
import mss
import cv2
<<<<<<< HEAD
import threading
=======
import threading  # <--- Import necessário
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

class bot:

    def __init__(self):
        print("[INIT] Iniciando bot...")
        self.BallNumber = 30
        self.State = ""
        self.DetectedOnFrame = []
        self.InBattle = False
        self.model = YOLO("best.pt")
<<<<<<< HEAD

        with mss.mss() as temp_sct:
            self.monitor = temp_sct.monitors[1]

        self.running = True
        self.detect_thread = threading.Thread(target=self.ContinuousDetect, daemon=True)
        self.detect_thread.start()

        print("[INIT] Bot iniciado com sucesso!")

# ======================= CORE =======================

    def TryCapture(self):
        print(f"[TryCapture] Estado: {self.State} | Balls: {self.BallNumber} | InBattle: {self.InBattle}")
        start_time = time()

        while True:
=======
        
        # CORREÇÃO AQUI: Não guarde 'self.sct'. 
        # Apenas pegue os dados do monitor e feche.
        with mss.mss() as sct:
            self.monitor = sct.monitors[1]

        self.DetectedOnFrame = []
        
        self.running = True
        self.detect_thread = threading.Thread(target=self.ContinuousDetect, daemon=True)
        self.detect_thread.start()

    def TryCapture(self):
        start_time = time()
        while True:
            # Como DetectedOnFrame é atualizado na thread, podemos apenas ler ele aqui
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
            if self.State == "ReadyToCapture":
                print("[TryCapture] Tentando capturar...")
                if ("CAPTUREBAR" in self.DetectedOnFrame and 
                    "MAGIKARP" in self.DetectedOnFrame and 
                    self.BallNumber > 0 and 
                    self.InBattle):

                    print("[TryCapture] Condições OK → Capturando!")
                    self.KeyPress("up")
                    self.KeyPress("left")
                    self.KeyPress("z")
<<<<<<< HEAD

                    self.BallNumber -= 1
                    self.State = "Waiting"
                    start_time = time()
=======
                    self.BallNumber -= 1
                    self.State = "Waiting"
                    start_time = time() # Reseta timer para o estado Waiting
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

            elif self.BallNumber < 1:
                print("[TryCapture] Sem balls! Saindo...")
                self.KeyPress("right")
                self.KeyPress("down")
                self.KeyPress("z")
                sleep(5)
                return True          

            if self.State == "Waiting":
<<<<<<< HEAD
                elapsed_time = time() - start_time

                if "SUCESSFULCAPTURE" in self.DetectedOnFrame:
                    print("[TryCapture] Captura confirmada!")
                    self.InBattle = False
                    self.State = "Waiting"
                    return True

                if elapsed_time > 10:
                    print("[TryCapture] Timeout → Resetando estado")
                    sleep(5)
                    self.State = "ReadyToCapture"

                sleep(0.1)
=======
                # Lógica de timer corrigida para não travar o loop
                elapsed_time = time() - start_time
                
                if "SUCESSFULCAPTURE" in self.DetectedOnFrame:
                    self.InBattle = False
                    self.State = "Waiting" # Talvez devesse ser outro estado aqui?
                    return True
                
                # Se passou 10 segundos
                if elapsed_time > 10:
                    sleep(5)
                    self.State = "ReadyToCapture"
                
                sleep(0.1) # Pequena pausa para não fritar a CPU neste loop
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
            else:
                print("[TryCapture] Estado inválido → Saindo")
                return False

    def CloseAnouce(self):
        print("[CloseAnouce] Verificando anúncio...")
        if "SKIPANOUCE" in self.DetectedOnFrame:
            print("[CloseAnouce] Anúncio detectado → Fechando")
            self.KeyPress("x")
<<<<<<< HEAD
            self.State = "InWater"
=======
            self.State = "InWater" # Corrigido de SetState para atribuição direta se desejar consistência
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
            return True
        return False

    def TryEntryBattle(self):
<<<<<<< HEAD
        print(f"[TryEntryBattle] Estado: {self.State}")

        while True:
            if self.State == "InWater" and self.BallNumber > 0:
                print("[TryEntryBattle] Tentando iniciar batalha...")
                self.KeyPress("-")
                self.State = "Waiting"
=======
        while True:
            if self.State == "InWater" and self.BallNumber > 0 :
                self.KeyPress("m")
                self.State = "Waiting" # Corrigido erro de sintaxe (era ==)
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
                sleep(5)
            else:
                print("[TryEntryBattle] Condições inválidas")
                return False

            if "STARTBATTLE" in self.DetectedOnFrame and "NMUM" not in self.DetectedOnFrame:
                print("[TryEntryBattle] Batalha iniciada!")
                self.KeyPress("z")
                self.InBattle = True
                sleep(3)
                self.State = "ReadyToCapture"
                return True

            elif "NMUM" in self.DetectedOnFrame:
                print("[TryEntryBattle] Não mordeu")
                self.KeyPress("z")
                self.State = "InWater"
                sleep(1)

    def GoOut(self):
        print("[GoOut] Verificando saída...")
        if "DINGDONG" in self.DetectedOnFrame:
            print("[GoOut] Saída confirmada!")
            for _ in range(5):
                self.KeyPress("z")
                sleep(1)
<<<<<<< HEAD
            self.State = "OUT"
            return True
        return False

# ======================= UTILS =======================

    def KeyPress(self, key):
        print(f"[KeyPress] Pressionando: {key}")
=======
            self.State = "OUT" # Corrigido sintaxe (SetState não é variavel)
            return True
        else:
            return False
    
#======================= Utils ==========================================================

    def KeyPress(self, key):
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
        try:
            sleep(0.25)
            pyautogui.keyDown(key)
            sleep(0.05)
            pyautogui.keyUp(key)
            sleep(0.25)
            return True
        except Exception as e:
            print(f"[KeyPress ERROR] {e}")
            return False

    def SetState(self, str_state):
<<<<<<< HEAD
        print(f"[STATE] Mudando estado → {str_state}")
        self.State = str_state

# ======================= DETECTOR =======================
=======
        self.State = str_state

    # =========================================================================
    # ESTE MÉTODO AGORA RODA EM UMA THREAD SEPARADA
    # =========================================================================
    def ContinuousDetect(self):
            print("Detector iniciado em background...")
            
            # CORREÇÃO AQUI: Inicializa o mss DENTRO da thread
            with mss.mss() as sct:
                while self.running:
                    try:
                        # Usa o 'sct' local desta thread, e não 'self.sct'
                        screenshot = sct.grab(self.monitor)
                        
                        frame = np.array(screenshot)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                        results = self.model(frame, verbose=False)

                        detections = []

                        for r in results:
                            if r.boxes is None:
                                continue

                            for box in r.boxes:
                                cls_id = int(box.cls[0])
                                label = self.model.names[cls_id]
                                detections.append(label)

                        self.DetectedOnFrame = detections
                        
                    except Exception as e:
                        print(f"Erro na thread de detecção: {e}")
                        sleep(1) # Espera um pouco se der erro para não floodar o console
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

    def ContinuousDetect(self):
        print("[Detect] Detector iniciado em background...")

<<<<<<< HEAD
        while self.running:
            try:
                with mss.mss() as sct:
                    while self.running:
                        try:
                            screenshot = sct.grab(self.monitor)
                            frame = np.array(screenshot)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                            results = self.model(frame, verbose=False)
                            detections = []

                            for r in results:
                                if r.boxes is None:
                                    continue

                                for box in r.boxes:
                                    conf = float(box.conf[0])

                                    if conf >= 0.80:
                                        cls_id = int(box.cls[0])
                                        label = self.model.names[cls_id]
                                        detections.append(label)
                                        print(f"[Detect] {label} ({conf*100:.1f}%)", end=" ")

                            if detections:
                                print()

                            self.DetectedOnFrame = detections
                            sleep(0.05)

                        except Exception as inner_e:
                            print(f"[Detect ERROR] Reiniciando captura: {inner_e}")
                            break

            except Exception as e:
                print(f"[Detect CRITICAL] {e}")
                sleep(1)

# ======================= WALK =======================

=======
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
    def AcceptEntry(self):
        print("[AcceptEntry] Tentando entrar...")
        try:
            if self.State == "OUT":
                print("[AcceptEntry] Entrada aceita")
                self.BallNumber = 30

                for _ in range(2):
                    self.KeyPress("up")

                for _ in range(10):
                    self.KeyPress("z")
                    sleep(1)

                self.State = "InEntry"
                return True
            return False
        except Exception as e:
            print(f"[AcceptEntry ERROR] {e}")
            return False

    def WalkToWater(self):
        print(f"[WalkToWater] Estado atual: {self.State}")
        try:
            if self.State == "InEntry":
                print("[WalkToWater] Caminhando até a água...")

                for _ in range(10):
                    self.KeyPress("up")
<<<<<<< HEAD

                for _ in range(6):
                    self.KeyPress("right")

                for _ in range(5):
                    self.KeyPress("up")

=======
                for i in range(6):
                    self.KeyPress("right")
                for i in range(5):
                    self.KeyPress("up")
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355
                self.State = "InWater"
                return True

            return False
        except Exception as e:
            print(f"[WalkToWater ERROR] {e}")
            return False

<<<<<<< HEAD
    def Stop(self):
        print("[STOP] Encerrando bot...")
        self.running = False
        if self.detect_thread.is_alive():
            self.detect_thread.join()
        print("[STOP] Bot finalizado.")

# ======================= MAIN =======================
=======
    # Método para parar a thread limpo se necessário manualmente
    def Stop(self):
        self.running = False
        if self.detect_thread.is_alive():
            self.detect_thread.join()
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

if __name__ == "__main__":
    sleep(5)
    print("[MAIN] Iniciando Bot...")

    PKbot = bot()
    PKbot.SetState("OUT")
<<<<<<< HEAD

    try:
        while True:
            if not PKbot.AcceptEntry(): 
                break

            if not PKbot.WalkToWater(): 
                break

            while True:
                if PKbot.GoOut():
                    break

                if not PKbot.TryEntryBattle():
                    pass

                PKbot.TryCapture()
                PKbot.CloseAnouce()

                sleep(0.1)

    except KeyboardInterrupt:
        print("[MAIN] Parando bot...")
        PKbot.Stop()
=======
    
    try:
        while True:
            # Lógica principal de loop
            if not PKbot.AcceptEntry(): break
            if not PKbot.WalkToWater(): break
            
            # Loop interno de batalha/captura
            while True:
                # Verifica se precisa sair
                if PKbot.GoOut():
                    break # Sai do loop interno e volta pro começo (AcceptEntry provavelmente falhará se já saiu, ajustar lógica conforme necessidade)

                if not PKbot.TryEntryBattle(): 
                    # print("Tentou entrar em battle sem estar na agua ou algo assim")
                    pass
                
                # Tenta capturar se estiver em batalha
                PKbot.TryCapture()
                
                # Checa por avisos para fechar
                PKbot.CloseAnouce()
                
                sleep(0.1) # Evita uso excessivo de CPU no loop principal

    except KeyboardInterrupt:
        print("Parando bot...")
        PKbot.Stop()
>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

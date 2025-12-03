import pyautogui
from time import sleep, time
import numpy as np
from ultralytics import YOLO
import mss
import cv2
import threading  # <--- Import necessário

class bot:

    def __init__(self):
        self.BallNumber = 30
        self.State = ""
        self.DetectedOnFrame = []
        self.InBattle = False
        self.model = YOLO("best.pt")
        
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
            if self.State == "ReadyToCapture":
                if "CAPTUREBAR" in self.DetectedOnFrame and "MAGIKARP" in self.DetectedOnFrame and self.BallNumber > 0 and self.InBattle:
                    #Sequence to try capture
                    self.KeyPress("up")
                    self.KeyPress("left")
                    self.KeyPress("z")
                    self.BallNumber -= 1
                    self.State = "Waiting"
                    start_time = time() # Reseta timer para o estado Waiting

            elif self.BallNumber < 1:
                self.KeyPress("right") 
                self.KeyPress("down")
                self.KeyPress("z")
                sleep(5)     
                return True          

            if self.State == "Waiting":
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
            else:
                return False

    def CloseAnouce(self):
        if "SKIPANOUCE" in self.DetectedOnFrame:
            self.KeyPress("x")
            self.State = "InWater" # Corrigido de SetState para atribuição direta se desejar consistência
            return True
        else:
            return False

    def TryEntryBattle(self):
        while True:
            if self.State == "InWater" and self.BallNumber > 0 :
                self.KeyPress("m")
                self.State = "Waiting" # Corrigido erro de sintaxe (era ==)
                sleep(5)
            else:
                return False
            
            if "STARTBATTLE" in self.DetectedOnFrame and not "NMUM" in self.DetectedOnFrame:
                self.KeyPress("z")
                self.InBattle = True
                sleep(3)
                self.State = "ReadyToCapture"
                return True
            
            elif "NMUM" in self.DetectedOnFrame and not "STARTBATTLE" in self.DetectedOnFrame:
                self.KeyPress("z")
                self.State = "InWater"
                sleep(1)
    
    def GoOut(self):
        if "DINGDONG" in self.DetectedOnFrame:
            for i in range(5):
                self.KeyPress("z")
                sleep(1)
            self.State = "OUT" # Corrigido sintaxe (SetState não é variavel)
            return True
        else:
            return False
    
#======================= Utils ==========================================================

    def KeyPress(self, key):
        try:
            sleep(0.25)
            pyautogui.keyDown(key)
            sleep(0.05)
            pyautogui.keyUp(key)
            sleep(0.25)
            return True
        except:
            return False

    def SetState(self, str_state):
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

#============================ Walk Sequences ============================================

    def AcceptEntry(self):
        try:
            if self.State == "OUT":
                self.BallNumber = 30
                for i in range(2):
                    self.KeyPress("up") 
                for i in range(10):
                    self.KeyPress("z")
                    sleep(1)
                self.State = "InEntry"
                return True
        except Exception as e:
            print(f"[AcceptEntry ERROR] {e}")
            return False

    def WalkToWater(self):
        try:
            if self.State == "InEntry":
                for i in range(10):
                    self.KeyPress("up")
                for i in range(6):
                    self.KeyPress("right")
                for i in range(5):
                    self.KeyPress("up")
                self.State = "InWater"
                return True
            else:
                return False
        except Exception as e:
            print(f"[WalkToWater ERROR] {e}")
            return False

    # Método para parar a thread limpo se necessário manualmente
    def Stop(self):
        self.running = False
        if self.detect_thread.is_alive():
            self.detect_thread.join()

if __name__ == "__main__":
    sleep(5)
    print("Iniciando Bot...")
    PKbot = bot()
    PKbot.SetState("OUT")
    
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
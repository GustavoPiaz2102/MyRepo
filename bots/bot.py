import pyautogui
from time import sleep, time
import numpy as np
from ultralytics import YOLO
import mss
import cv2
import threading

class bot:

    def __init__(self):
        print("[INIT] Iniciando bot...")
        self.BallNumber = 30
        self.State = ""
        self.DetectedOnFrame = []
        self.InBattle = False
        self.model = YOLO("best.pt")

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

                    self.BallNumber -= 1
                    self.State = "Waiting"
                    start_time = time()

            elif self.BallNumber < 1:
                print("[TryCapture] Sem balls! Saindo...")
                self.KeyPress("right")
                self.KeyPress("down")
                self.KeyPress("z")
                sleep(5)
                return True          

            if self.State == "Waiting":
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
            else:
                print("[TryCapture] Estado inválido → Saindo")
                return False

    def CloseAnouce(self):
        print("[CloseAnouce] Verificando anúncio...")
        if "SKIPANOUCE" in self.DetectedOnFrame:
            print("[CloseAnouce] Anúncio detectado → Fechando")
            self.KeyPress("x")
            self.State = "InWater"
            return True
        return False

    def TryEntryBattle(self):
        print(f"[TryEntryBattle] Estado: {self.State}")

        while True:
            if self.State == "InWater" and self.BallNumber > 0:
                print("[TryEntryBattle] Tentando iniciar batalha...")
                self.KeyPress("-")
                self.State = "Waiting"
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
            self.State = "OUT"
            return True
        return False

# ======================= UTILS =======================

    def KeyPress(self, key):
        print(f"[KeyPress] Pressionando: {key}")
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
        print(f"[STATE] Mudando estado → {str_state}")
        self.State = str_state

# ======================= DETECTOR =======================

    def ContinuousDetect(self):
        print("[Detect] Detector iniciado em background...")

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

                for _ in range(6):
                    self.KeyPress("right")

                for _ in range(5):
                    self.KeyPress("up")

                self.State = "InWater"
                return True

            return False
        except Exception as e:
            print(f"[WalkToWater ERROR] {e}")
            return False

    def Stop(self):
        print("[STOP] Encerrando bot...")
        self.running = False
        if self.detect_thread.is_alive():
            self.detect_thread.join()
        print("[STOP] Bot finalizado.")

# ======================= MAIN =======================

if __name__ == "__main__":
    sleep(5)
    print("[MAIN] Iniciando Bot...")

    PKbot = bot()
    PKbot.SetState("OUT")

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

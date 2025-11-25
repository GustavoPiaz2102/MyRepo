import pyautogui
from time import sleep
class bot:

    def __init__(self):
        self.BallNumber = 30
        self.State = ""
        self.DetectedOnFrame = []
        self.InBattle = False
        pass

    def TryCapture(self):
        while True:

            if self.State == "ReadyToCapture":
                if "CAPTUREBAR" in self.DetectedOnFrame and "MAGIKARP" in self.DetectedOnFrame and self.BallNumber > 0 and self.InBattle:
                    #Sequence to try capture
                    self.KeyPress("up")
                    self.KeyPress("left")
                    self.KeyPress("z")
                    self.BallNumber-=1
                    self.State = "Waiting"
            elif self.BallNumber < 1:
                self.KeyPress("right") 
                self.KeyPress("down")
                self.KeyPress("z")
                sleep(5)     
                return True          

            if self.State == "Waiting":
                #Roda um thread durante 10 segundos, timer vai para true caso o tempo seja exedido fica tentando detectar se a captura foi bem sucedida enquanto isso
                timer = False
                while not timer:
                    if "SUCESSFULCAPTURE" in self.DetectedOnFrame:
                        self.InBattle = False
                        self.State = "Waiting"
                        return True
                sleep(5)
                self.State = "ReadyToCapture"
            else:
                return False

    def CloseAnouce(self):
        if "SKIPANOUCE" in self.DetectedOnFrame:
            self.KeyPress("x")
            self.SetState = "InWater"
            return True
        else:
            return False

    def TryEntryBattle(self):
        while True:

            if self.State == "InWater" and self.BallNumber > 0 :
                self.KeyPress("-")
                self.State == "Waiting"
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
                self.SetState = "OUT"
                return True
        else:
            return False
    
#======================= Utils ==========================================================

    def KeyPress(self,key):
        try:
            sleep(0.25)
            pyautogui.keyDown(key)
            sleep(0.05)
            pyautogui.keyUp(key)
            sleep(0.25)
            return True
        except:
            return False

    def SetState(self,str):
        self.State = str

    def ContinuousDetect(self): #Altera a lista de detectados no frame
        pass

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
                    #sleep(0.5)
                for i in range(6):
                    self.KeyPress("right")
                    #sleep(0.5)
                for i in range(5):
                    self.KeyPress("up")
                    #sleep(0.5)
                self.State = "InWater"
                return True
            else:
                return False
        except Exception as e:
            print(f"[WalkToWater ERROR] {e}")
            return False
        


if __name__ == "__main__":
    sleep(5)
    print("Iniciando Bot...")
    PKbot = bot()
    PKbot.SetState("OUT")
    while True:
        if not PKbot.AcceptEntry(): break
        if not PKbot.WalkToWater(): break
        while not PKbot.GoOut():
            if not PKbot.TryEntryBattle(): print("Tentou entrar em battle sem estar na agua")
            if not PKbot.TryCapture(): break




    


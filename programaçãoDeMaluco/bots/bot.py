QntStack = 6
TimeRun = 2.8
TimeInterAction = 0.5
TimeInterButtonDown = 0.001
TimeToSkipHealing = 7.7
import pyautogui as pag
from time import sleep

def GoToPC():
    for i in range(3):
        pag.keyDown('down')
        sleep(TimeInterButtonDown)
        pag.keyUp('down')
        sleep(TimeInterAction)
    pag.keyDown('right')
    sleep(TimeRun)
    pag.keyUp('right')
    for i in range(3):
        pag.keyDown('up')
        sleep(TimeInterButtonDown)
        pag.keyUp('up')
        sleep(TimeInterAction)

def HealPokemon():
    pag.keyDown("up")
    sleep(2)
    pag.keyUp("up")
    sleep(TimeInterAction)
    pag.keyDown("z")
    sleep(TimeToSkipHealing)
    pag.keyUp("z")
    sleep(TimeInterAction)

def OutPC():
    for i in range(9):
        pag.keyDown("down")
        sleep(TimeInterButtonDown)
        pag.keyUp("down")
        sleep(TimeInterAction)
    sleep(2)
    pag.keyDown('down')
    sleep(TimeInterButtonDown)
    pag.keyUp('down')
    sleep(TimeInterAction)
    pag.keyDown('left')
    sleep(TimeRun)
    pag.keyUp('left')
    for i in range(4):
        pag.keyDown('up')
        sleep(TimeInterButtonDown)
        pag.keyUp('up')
        sleep(TimeInterAction)

def Main():
    for i in range(QntStack):
        GoToPC()
        HealPokemon()
        OutPC()

if __name__ == "__main__":
    print("Starting in 5 seconds...")
    sleep(5)
    Main()

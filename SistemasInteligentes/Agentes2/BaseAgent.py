"""
Agente De envio de mensagem em localhost utilizando metadatas para validação
Gustavo Piaz Da Silva - 23200958 
"""

"""
IMPORTS
"""
from spade import agent, behaviour
from spade.message import Message
import asyncio
import os
from time import sleep
from random import randint
#=============================================================

AGTTarget = "AgentePedro@localhost"
MYAGENT = "AgtGustavo@localhost"

def ClearChat():
    os.system("clear" if os.name == 'posix' else 'cls')

class MyAgent(agent.Agent):
<<<<<<< HEAD
    async def setup(self):

        self.ChatHistory = []
        self.add_behaviour(self.SendBehaviour())  
        self.add_behaviour(self.ReceiveBehaviour())
        self.lastReceivedMSG = ""


    class SendBehaviour(behaviour.CyclicBehaviour):
        def ShowHistory(self):
            ClearChat()
            print("Historico de Comunicações")
            for chat in self.agent.ChatHistory:
                if chat is not None:
                    print(chat)
            input("Pressione Enter Para Retornar...")
=======
    async def setup(self):   
        self.lastReceivedMSG = ""
        self.lastPerformativeRCV = "" 
        self.interval = {"Min":0,"Max":0}
        self.lastChooseNumber = 0     
        self.add_behaviour(self.RequestInterval())  
        self.add_behaviour(self.SendBehaviour(period=1))  
        self.add_behaviour(self.ReceiveBehaviour())

    
    class RequestInterval(behaviour.OneShotBehaviour):
        async def run(self):
            msg = Message(to=AGTTarget) 
            msg.body = "qual o intervalo?"
            msg.set_metadata("performative", "request")#intervalo
            if msg.body and msg.body.strip():
                await self.send(msg)
                #print(f"Mensagem enviada: {msg.body}")
                print(f"{MYAGENT} {msg.body}")



    class SendBehaviour(behaviour.PeriodicBehaviour):
        def ChooseCMM(self):
            # ainda não recebeu nada — não tem intervalo
            if self.agent.lastPerformativeRCV == "":
                return True  # não envia ainda

            if self.agent.lastPerformativeRCV == "inform":
                min_val, max_val = self.agent.lastReceivedMSG.split(",")
                self.agent.interval["Min"] = int(min_val.strip())
                self.agent.interval["Max"] = int(max_val.strip())
                self.agent.lastChooseNumber = randint(self.agent.interval["Min"], self.agent.interval["Max"])
                return False

            elif self.agent.lastPerformativeRCV == "inform-done":
                #print("Finalizado!")
                return True

            elif self.agent.lastPerformativeRCV == "failure":
                if self.agent.lastReceivedMSG == "<":
                    self.agent.interval["Max"] = self.agent.lastChooseNumber - 1
                else:
                    self.agent.interval["Min"] = self.agent.lastChooseNumber + 1

                self.agent.lastChooseNumber = randint(self.agent.interval["Min"], self.agent.interval["Max"])
                return False


>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355

        async def run(self):
                
                msg = Message(to=AGTTarget)
                msg.set_metadata("performative", "subscribe")
                if not self.ChooseCMM():
                    msg.body = str(self.agent.lastChooseNumber)
                    if msg.body and msg.body.strip():
                        await self.send(msg)
                        print(f"{MYAGENT} {msg.body}")
                    



    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
<<<<<<< HEAD
            try:
                msg = await self.receive(timeout=10)  # Timeout menor para responsividade
                if msg:
                    received_msg = f"{msg.body}"
                    self.agent.ChatHistory.append(received_msg)
                    self.agent.lastReceivedMSG = received_msg
                    # Pequena pausa assíncrona em vez de sleep bloqueante
=======
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.lastReceivedMSG = msg.body
                self.agent.lastPerformativeRCV = msg.get_metadata("performative")
                for i in range(40):
                    print(" ",end="")
                print(f"{msg.body} {AGTTarget}")


>>>>>>> 024a0e3cf7f5a0257dda90d092fc79413337a355


#=============================================================

if __name__ == "__main__":
    async def main():
        agt = MyAgent(MYAGENT, "senha123")

        try:
            await agt.start(auto_register=True)
            #print("Agente iniciado... Pressione Ctrl+C para encerrar.")
            ClearChat()
            # Manter o agente rodando
            while agt.is_alive():
                await asyncio.sleep(1)
                
        except Exception as e:
            print("Erro ao iniciar agente:", e)
        finally:
            if agt.is_alive():
                await agt.stop()
            print("Agente encerrado.")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEncerrando agente...")
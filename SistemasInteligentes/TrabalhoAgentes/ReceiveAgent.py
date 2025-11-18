
"""


Nome: Pedro Thomas Silveira de Alcantara
Matricula: 23200955
Agente de Recebimento e Validação


"""

# BIBLIOTECAS

from spade import agent, behaviour
from spade.message import Message
from os import system
import asyncio
from random import randint

class MyAgent(agent.Agent):
    async def setup(self):
        self.number = 37
        self.msgToSend = ""
        self.msgRCV = ""
        self.add_behaviour(self.DefineIntervalBehaviour())
        self.add_behaviour(self.ReceiveBehaviour())   
        self.add_behaviour(self.SendBehaviour(period=1))
    class ReceiveBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.msgRCV = msg.body
                print(f"Mensagem recebida: {msg.body}")

    class DefineIntervalBehaviour(behaviour.OneShotBehaviour):
        async def run(self):
            running = True
            while(running):
                msg = await self.receive(timeout=10)
                if msg:
                    running = False
            if msg:
                interval = msg.body.split(",")
                min = int(interval[0])
                max = int(interval[1])
                self.agent.number = randint(min, max)
                print(f"Numero Escolhido no intervalo {min} a {max}: {self.agent.number}")
                msg = ""

    class SendBehaviour(behaviour.PeriodicBehaviour):
        async def run(self):
            
            if not self.agent.msgRCV or self.agent.msgRCV == "":
                return  
                
            try:
                msg_value = int(self.agent.msgRCV)
                
                if msg_value < self.agent.number:
                    self.agent.msgToSend = "maior"
                elif msg_value > self.agent.number:
                    self.agent.msgToSend = "menor"
                else:
                    self.agent.msgToSend = "correto"
                    await self.agent.stop()
                msg = Message(to="AgtGustavo@localhost")
                msg.body = self.agent.msgToSend
                await self.send(msg)
                print(f"Mensagem enviada: {msg.body}")
                
                self.agent.msgRCV = ""
                
            except ValueError:
                print(f"Erro: mensagem recebida não é um número válido: '{self.agent.msgRCV}'")
                self.agent.msgRCV = ""  

async def main():
    agt = MyAgent("AgentePedro@localhost", "senha123")
    try:
        await agt.start(auto_register=True)
    except Exception as e:
        print("Erro ao iniciar agente:", e)
        return

    await asyncio.sleep(1)
    #   system("clear")
    print("Agente iniciado. Pressione CTRL+C para sair.\n")

    try:
        while True:
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        print("Encerrando agente...")
        await agt.stop()

if __name__ == "__main__":
    asyncio.run(main())
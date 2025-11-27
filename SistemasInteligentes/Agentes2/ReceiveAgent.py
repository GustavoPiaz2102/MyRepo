
"""


Nome: Pedro Thomas Silveira de Alcantara
Matricula: 23200955
Agente de Recebimento e Validação Utilizando valores randomicos e metadatas


"""

# BIBLIOTECAS

from spade import agent, behaviour
from spade.message import Message
from os import system
import asyncio
from random import randint
from spade.template import Template

def ThinkNumber():
    val = randint(0,1000)
    intervalmin = randint(0, val)
    intervalmax = randint(val, 1000)
    return val, str(intervalmin) , str(intervalmax)


class MyAgent(agent.Agent):
    async def setup(self):
        templatesubscribe = Template(metadata={"performative": "subscribe"})
        templaterequest = Template(metadata={"performative": "request"})
        self.number,self.intervalmin,self.intervalmax = ThinkNumber()
        self.msgToSend = ""
        self.performativeToSend = ""
        self.add_behaviour(self.Receiverequest(),templaterequest)   
        self.add_behaviour(self.Receivesubscribe(),templatesubscribe)   
        self.add_behaviour(self.SendBehaviour())

    class Receiverequest(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if not msg:
                return
            self.agent.msgToSend = f"O intervalo é ({self.agent.intervalmin},{self.agent.intervalmax})"
            self.agent.performativeToSend = "inform"
    
    class Receivesubscribe(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if not msg:
                return
            ReceivedValue = int(msg.body.split()[-1])
            if ReceivedValue < self.agent.number:
                self.agent.msgToSend = ">"
                self.agent.performativeToSend = "failure"
            elif ReceivedValue > self.agent.number:
                self.agent.msgToSend = "<"
                self.agent.performativeToSend = "failure"
            elif ReceivedValue == self.agent.number:
                self.agent.msgToSend = "Valor Correto"
                self.agent.performativeToSend = "inform-done"

               

    class SendBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            if self.agent.msgToSend == "" or self.agent.performativeToSend == "":
                return
            msg = Message(to="AgtGustavo@localhost")
            msg.body = self.agent.msgToSend
            msg.set_metadata("performative",self.agent.performativeToSend)
            await self.send(msg)
            print(f"Mensagem enviada: {msg.body}")
            
            self.agent.performativeToSend = ""
            self.agent.msgToSend = ""
                

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
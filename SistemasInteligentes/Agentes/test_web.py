import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class DummyPresence:
    def get_contacts(self):
        return {}

class WebOnlyAgent(Agent):
    async def setup(self):
        if self.presence is None:
            self.presence = DummyPresence()
        print(f"🎮 {self.jid.local} iniciado")

class AgenteInteligente(WebOnlyAgent):
    async def setup(self):
        await super().setup()
        self.add_behaviour(self.ComportamentoPrincipal())
        self.add_behaviour(self.ComportamentoSecundario())
        self.add_behaviour(self.Comunicacao())

    class ComportamentoPrincipal(CyclicBehaviour):
        async def run(self):
            print(f"🧠 {self.agent.jid.local}: Processando tarefa principal...")
            await asyncio.sleep(2)

    class ComportamentoSecundario(CyclicBehaviour):
        async def run(self):
            print(f"⚙️  {self.agent.jid.local}: Tarefa secundária...")
            await asyncio.sleep(5)

    class Comunicacao(CyclicBehaviour):
        async def run(self):
            # Envia mensagens para os outros agentes periodicamente
            for agente in self.agent.sistema.agents:
                if agente != self.agent:
                    msg = Message(
                        to=str(agente.jid),
                        body=f"Olá {agente.jid.local}, sou {self.agent.jid.local}!"
                    )
                    await self.send(msg)
                    print(f"📤 {self.agent.jid.local} → {agente.jid.local}: {msg.body}")
            # Espera uma mensagem
            msg = await self.receive(timeout=3)
            if msg:
                print(f"📩 {self.agent.jid.local} recebeu de {msg.sender.local}: {msg.body}")
            await asyncio.sleep(3)


class SistemaAgentes:
    def __init__(self):
        self.agents = []
        self.running = True

    async def iniciar_agentes(self):
        agentes_config = [
            ("cpu@local", AgenteInteligente),
            ("memoria@local", AgenteInteligente),
            ("rede@local", AgenteInteligente),
        ]

        for jid, agent_class in agentes_config:
            agent = agent_class(jid, "nopass")
            agent.sistema = self  # referência para enviar mensagens
            if agent.presence is None:
                agent.presence = DummyPresence()
            await agent.setup()
            self.agents.append(agent)
            print(f"✅ {jid} configurado")

    def iniciar_interface_web(self, port=10000):
        if self.agents:
            self.agents[0].web.start(hostname="127.0.0.1", port=port)
            print(f"🌐 Interface web: http://127.0.0.1:{port}/spade")

    async def executar(self):
        await self.iniciar_agentes()
        self.iniciar_interface_web()
        print("\n🎯 Sistema de agentes em execução! (Ctrl+C para encerrar)\n")

        try:
            while self.running:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            self.parar()

    def parar(self):
        print("\n🛑 Parando sistema...")
        self.running = False
        if self.agents:
            self.agents[0].web.stop()
        print("👋 Sistema encerrado com sucesso!")

async def main():
    sistema = SistemaAgentes()
    await sistema.executar()

if __name__ == "__main__":
    asyncio.run(main())

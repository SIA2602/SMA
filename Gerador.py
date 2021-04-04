import time
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class ReceiverAgent(Agent):
    jaSabeGrau = False
    resolvido = False

    x = random.randint(-1000, 1000)
    a = 0
    while a == 0:
        a = random.randint(-100, 100)
    y = -1 * (a * x)

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                if (ReceiverAgent.jaSabeGrau == False and msg.body == "Grau?"):
                    print("Mensagem recebida: {}".format(msg.body))
                    msg = Message(
                        to="miro30i10@jix.im")  # Instantiate the message
                    msg.set_metadata(
                        "performative",
                        "inform")  # Set the "inform" FIPA performative
                    msg.body = "1grau"  # Set the message content
                    ReceiverAgent.jaSabeGrau = True
                    await self.send(msg)

                elif (ReceiverAgent.jaSabeGrau == True
                      and ReceiverAgent.resolvido == False):
                    print("Valor recebido: {}".format(msg.body))

                    x = float(msg.body)
                    x = float(ReceiverAgent.a * x + ReceiverAgent.y)
                    if (x == 0):
                        ReceiverAgent.resolvido = True

                    msg = Message(
                        to="miro30i10@jix.im")  # Instantiate the message
                    msg.set_metadata(
                        "performative",
                        "inform")  # Set the "inform" FIPA performative

                    msg.body = str(int(x))

                    await self.send(msg)
                    print("Valor enviado: {}".format(msg.body))
                elif (ReceiverAgent.resolvido == True):
                    print("finished")
                    exit()
            else:
                print(
                    "Não foi recebida nenhuma mensagem no intervalo de 5s...")

    async def setup(self):
        print("ReceiverAgent started")
        print("Funcao de 1o grau: ", ReceiverAgent.x)
        print("Funcao: ", ReceiverAgent.a, "x + (", ReceiverAgent.y, ")")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


if __name__ == "__main__":
    receiveragent = ReceiverAgent("acir@jix.im", "Amjengufsc2796")
    future = receiveragent.start()
    future.result()  # wait for receiver agent to be prepared.

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")

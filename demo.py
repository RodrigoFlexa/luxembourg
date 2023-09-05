import traci
import traci.constants as tc
import random
import time

# Função para escolher origem e destino aleatórios
def choose_random_origin_dest():
    edges = traci.edge.getIDList()
    origin = random.choice(edges)
    destination = random.choice(edges)
    while origin == destination:
        destination = random.choice(edges)
    return origin, destination

# Configuração da simulação
sumo_binary = "sumo"  # Caminho para o executável SUMO
sumo_config = "luxembourg.sumocfg"  # Seu arquivo de configuração SUMO

# Inicialização da simulação
traci.start([sumo_binary, "-c", sumo_config])

try:
    while traci.simulation.getMinExpectedNumber() > 0:
        # Escolher origem e destino aleatórios a cada 10 segundos
        if traci.simulation.getTime() % 10 == 0:
            origin, destination = choose_random_origin_dest()
            print(f"Origem: {origin}, Destino: {destination}")

            # Calcular a rota
            traci.route.add("random_route", [origin, destination])
            traci.vehicle.add("random_vehicle", "random_route")

        traci.simulationStep()

except KeyboardInterrupt:
    pass

finally:
    traci.close()

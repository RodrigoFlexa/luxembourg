import traci
import time
import pytz
import datetime
import csv
import random

# Função para obter a data e hora atual formatada
def get_datetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("America/Belem"))
    return currentDT.strftime("%Y-%m-%d %H:%M:%S")
# Função para calcular a velocidade em km/h
def calculate_kmph(m_per_s):
    return round(m_per_s * 3.6, 2)

# Função para adicionar um veículo em uma edge aleatória a cada 5 segundos
spawn_interval = 60
edge_list = ['-34191#5', '--35476#1', '--35283#1','-35161#3']

def create_random_vehicle():
    # Gere um ID aleatório para o veículo
    vehicle_id = f"vehicle_{random.randint(1, 1000)}"
    trip_id = f"trip_{random.randint(1, 1000000)}"

    # Adicione o veículo com o ID gerado e uma rota aleatória do arquivo trips.trips.xml]
    caminho = random.sample(edge_list, 2)
    traci.route.add(trip_id, caminho)

    traci.vehicle.add(vehicle_id, trip_id)

    print(f"Novo veículo criado: {vehicle_id}")

# Inicialize a conexão com o SUMO
traci.start(["sumo-gui", "-c", "luxembourg.sumocfg"])

# Abrir o arquivo CSV para escrita usando um gerenciador de contexto
with open("output.csv", mode='w', newline='') as output_file:
    column_names = ['dateandtime', 'veh_id', 'coord_x', 'coord_y', 'speed_kmph']
    writer = csv.writer(output_file)
    writer.writerow(column_names)  # Escrever o cabeçalho

    while traci.simulation.getMinExpectedNumber() > 0:
        
        create_random_vehicle()

        traci.simulationStep()
        vehicles = traci.vehicle.getIDList()

        for vehicle_id in vehicles:
            x, y = traci.vehicle.getPosition(vehicle_id)
            lon, lat = traci.simulation.convertGeo(x, y)
            speed_mps = traci.vehicle.getSpeed(vehicle_id)
            speed_kmph = calculate_kmph(speed_mps)

            # Escrever os dados no arquivo CSV em tempo real
            data = [get_datetime(), vehicle_id, x, y, speed_kmph]
            writer.writerow(data)

            print("Vehicle:", vehicle_id, "at datetime:", get_datetime())
            print(vehicle_id, ">>> Position: [", round(x), ", ", round(y), "]", \
                  "Speed:", speed_kmph, "km/h |")

        # Verifique se é hora de criar um novo veículo
        if traci.simulation.getTime() % spawn_interval == 0:
            create_random_vehicle()

        # Esperar um segundo (ou ajustar conforme necessário)
        #time.sleep(1)

# Não é necessário fechar o arquivo quando se usa um gerenciador de contexto
traci.close()

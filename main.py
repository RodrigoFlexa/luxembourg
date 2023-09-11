import traci
import time
import pytz
import datetime
import csv
import random

class SumoSimulation:
    def __init__(self, config_file="luxembourg.sumocfg"):
        self.config_file = config_file
        self.spawn_interval = 5
        self.created_vehicles = 0
        self.n_players = 20
        self.players_data = {}
        self.positions = {0: ['-34191#5', '--34168#12', '-34168#11', '--34191#5', '-34652#1', '--34168#11', '-34168#12', '--34168#10', '-34652#0', '--34652#1'],
            1: ['--34937', '-34375#2', '-34375#1', '-34937', '-34375#3', '-34375#0', '-35141#4', '-34770#4', '-34778#5', '-34778#4'],
            2: ['--34253#34', '-34253#35', '--34130', '-34253#34', '-34646', '--34253#33', '--34253#35', '-34253#33', '-34508#1', '--35279#0'],
            3: ['-35062#2', '--35062#3', '-34404', '--35062#2', '-34661', '-35062#1', '-35062#3', '--34661', '-35028#2', '-34898#9'],
            4: ['-34574', '--34253#42', '-34253#41', '--34253#41', '--34574', '-34253#40', '-34244', '-34253#42', '--34253#44', '-34253#43'],
            5:['-35258#0', '--35258#0', '-34513#2', '--35476#1', '-35476#1','-34545', '-34513#1', '-35144#0', '--35476#0', '-35476#0'],
            6: ['--35075#2', '--35075#1', '--35399#2', '-35399#2', '-35075#2', '-35075#3', '--35399#1', '--35399#0', '-35075#1', '-34338#0'],
            7: ['--34698', '-34959#3', '-34698', '-34595', '--35190#1', '--34595', '-35190#1', '--35190#2', '-35190#0', '--34959#3'],
            8: ['--35247', '-35247', '--35312#0', '-34994#1', '-35312#0', '--34830', '-34830', '-35210', '-34507', '--35312#1'],
            9: ['--34771#1', '--34410#0', '-34771#0', '--34771#0', '-34410#0', '-34771#1', '-34790#0', '-35123#2', '--34790#0', '--34625#7'],
            10: ['-35240', '-34435#5', '--34435#4', '-34181#2', '-34435#4', '-34138', '-34181#3', '-34996', '--34435#5', '--34435#3'],
            11: ['-35312#9', '--35312#9', '-34517#0', '--34593#1', '--34517#0', '--34387', '-34158', '-35312#8', '-34387', '-34593#1'],
            12: ['-34884', '--34625#4', '-34625#3', '-34649#4', '-34649#3', '-34604#0', '--34604#0', '-34604#1', '-35330', '-34637'],
            13: ['--34577#2', '-34577#2', '-35130', '--35130', '--35292', '--34686#0', '-34686#0', '-34686#1', '-34926', '-34785'],
            14: ['--34253#2', '-34813#2', '--35070', '--34813#2', '--35322', '-35322', '-34365', '-34253#2', '-35070', '-34523#0'],
            15: ['-34415', '--35451#0', '-35244', '-34820', '-34264#0', '--35451#1', '-35451#1', '-34220', '-35043', '-35188'],
            16: ['--34885', '-34885', '--35282', '--34149', '-34780#1', '-35182#1', '-34259#0', '-34717', '-34544', '--34151'],
            17: ['-35283#0', '--35283#1', '--34832#0', '-34832#0', '--35283#0', '-35283#1', '--34832#1', '-34832#1', '-34783#1', '-34813#5'],
            18: ['--34243#1', '-34243#1', '-35446', '-34243#0', '--35446', '--34243#0', '--34522#5', '-34253#21', '-34522#4', '--34464'], 
            19: ['--34723#0', '-34723#0', '--34503#1', '-34723#1', '-34503#1', '-35387#1', '-34253#17', '--35387#1', '--35387#0', '--34503#0'], 
            20: ['-34293#10', '--35192#2', '--35192#3', '-34273', '--34293#10', '-34226#1', '--34273', '-34226#0', '-34605', '--34328#0'], 
            21: ['-34560', '-35402#1', '-35402#2', '-34998#1', '--34998#1', '--34998#0', '-35402#0', '-35402#3', '-35402#4', '-34833#2'], 
            22: ['-35186', '-34543', '-34917', '--34782#0', '--34917', '--34354#0', '-34671#11', '--34864', '-35109', '--35045'], 
            23: ['-34677#1', '-34677#0', '-34263', '--34217', '-34217', '-34883', '--34883', '--35221#3', '-35221#3', '--34932#3'], 
            24: ['--34372#1', '-34372#0', '-34302#4', '-34372#1', '-35127#6', '-34633#0', '-34291', '--35272', '--34302#4', '-34846#1'], 
            25: ['-34732#0', '--34732#1', '-34431#3', '-34732#1', '-34417#2', '-35128#4', '--34293#5', '--34417#3', '-34417#0', '-34293#4'],
            26: ['-34175#0', '-35469#4', '--35469#5', '--34175#0', '--35469#4', '--34175#1', '-34437', '-35469#3', '-35353', '-35469#5'], 
            27: ['--34585#1', '-35213', '-34585#0', '-35161#3', '-35249#0', '--35161#3', '-34585#1', '--34585#0', '-35161#2', '-35249#1'], 
            28: ['-35308#0', '--35308#0', '-35127#2', '--35213', '-35127#1', '--35308#1', '-35308#1', '-35316', '--35127#2', '--35098#1'],
            29: ['--34857', '-34817', '-34554', '-35157#6', '--35157#6', '-35157#5', '--35157#7', '--35157#5', '-35157#4', '--35157#4'], 
            30: ['-35185#1', '--35185#1', '--35456#5', '-35185#2', '--35042#1', '-35042#1', '-34692', '-35185#0', '-34802'],
            31: ['-34160#1', '-35016', '--34882', '-34160#0', '-34160#4', '-34160#2', '-34160#3'], 
            32: ['-34417#19', '-35417#0', '-35417#2', '-35417#1', '-35471', '--34417#19', '--35323#0', '-34417#18', '--35471', '-35323#0'],
            33: ['--34370#0', '--34481', '-34715#1', '-34370#0', '--35364#0', '--34370#1', '-34370#1', '--34715#1', '-34715#0', '--35382#0'],
            34: ['-34417#19', '--34417#19', '-34417#18', '--35323#0', '-35417#1', '-35417#0', '--34572#1', '-35417#2', '--35038', '-35323#0'],
            35: ['-34873#8', '-34873#7', '-35194#0', '--34873#8', '-35194#2', '-35194#1', '--35164#0', '--34146#0', '--34297#0', '-34297#0'],
            36: ['--35449', '-35449', '-34877#1', '--35433', '-34877#2', '-34877#0', '-35279#4', '--35279#4', '-35433', '-35062#3'], 
            37: ['--34526', '-34253#57', '--34253#57', '-34526', '-34253#56', '--35382#0', '-35382#1', '-35382#0', '--35382#1', '-35441']}

    def get_datetime(self):
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("America/Belem"))
        return currentDT.strftime("%Y-%m-%d %H:%M:%S")

    def calculate_kmph(self, m_per_s):
        return round(m_per_s * 3.6, 2)
        

    def create_random_vehicle(self):
        if self.created_vehicles < self.n_players:
            
            player = self.created_vehicles + 1

            server_start = random.choice(list(self.positions.keys()))
            server_end = random.choice(list(self.positions.keys()))
            
            # Verifica se o servidor é igual ao destino e refaz a seleção
            while server_start == server_end:
                server_end = random.choice(list(self.positions.keys()))

            vehicle_id = f"vehicle_{player}"
            trip_id = f"trip_{player}_0"    

            self.create_route(trip_id, server_start, server_end)
            traci.vehicle.add(vehicle_id, trip_id)
            
            print(f"Novo veículo criado: {vehicle_id}")
            self.created_vehicles = self.created_vehicles + 1

    def create_route(self, trip_id, server_start, server_end):
        start_edge = random.choice(self.positions[server_start])
        end_edge = random.choice(self.positions[server_end])

        while start_edge == end_edge:
            end_edge = random.choice(self.positions[server_end])

        caminho = [start_edge,end_edge]
        
        traci.route.add(trip_id, caminho)
        self.players_data[int(trip_id.split('_')[-2])] = {'server_end':server_end,'start_edge': start_edge,'end_edge':end_edge,'trip_id':trip_id ,'coord': 0, 'flag': 1}


    def record_vehicle_data(self, writer, vehicle_id):
        x, y = traci.vehicle.getPosition(vehicle_id)
        lon, lat = traci.simulation.convertGeo(x, y)
        speed_mps = traci.vehicle.getSpeed(vehicle_id)
        speed_kmph = self.calculate_kmph(speed_mps)

        data = [self.get_datetime(), vehicle_id, x, y, speed_kmph]
        writer.writerow(data)

        # print("Vehicle:", vehicle_id, "at datetime:", self.get_datetime())
        # print(vehicle_id, ">>> Position: [", round(x), ", ", round(y), "]",
        #     "Speed:", speed_kmph, "km/h |")

    def calculate_new_edge(self, vehicle_id):
        player = int(vehicle_id.split("_")[-1])
        print(player, vehicle_id)
        server_end = random.choice(list(self.positions.keys()))
        new_edge = random.choice(self.positions[server_end])
        current_server = self.players_data[player]['server_end']
        
        while current_server == server_end:
            server_end = random.choice(list(self.positions.keys()))

        while new_edge == self.players_data[player]['end_edge']:
            new_edge = random.choice(self.positions[server_end])

        self.players_data[player]['end_edge'] = new_edge
        self.players_data[player]['server_end'] = server_end

        print("O veículo: ",vehicle_id, " foi rerroteado")
        return new_edge
    
    def run_simulation(self):
        traci.start(["sumo-gui", "-c", self.config_file])

        with open("output.csv", mode='w', newline='') as output_file:
            column_names = ['dateandtime', 'veh_id', 'coord_x', 'coord_y', 'speed_kmph']
            writer = csv.writer(output_file)
            writer.writerow(column_names)

            while traci.simulation.getMinExpectedNumber() > 0:
                self.create_random_vehicle()

                traci.simulationStep()
                vehicles = traci.vehicle.getIDList()

                for vehicle_id in vehicles:
                    if vehicle_id != 0 and vehicle_id != '0':
                        self.record_vehicle_data(writer, vehicle_id)

                        arrived = traci.vehicle.getRouteIndex(vehicle_id) == len(traci.vehicle.getRoute(vehicle_id))-1
                    
                        if arrived:
                            # Calcular e definir uma nova rota para o veículo
                            new_edge = self.calculate_new_edge(vehicle_id)
                            traci.vehicle.changeTarget(vehicle_id, new_edge)

                if traci.simulation.getTime() % self.spawn_interval == 0:
                    self.create_random_vehicle()
        traci.close()


if __name__ == "__main__":
    sim = SumoSimulation()
    sim.run_simulation()
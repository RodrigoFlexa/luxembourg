import xml.etree.ElementTree as ET
import math

# Função para calcular a distância entre dois pontos (x1, y1) e (x2, y2)
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Carregar o arquivo .net.xml
net_file = "luxembourg.net.xml"
tree = ET.parse(net_file)
root = tree.getroot()

# Lista de pontos de entrada (x, y)
entry_points = [(1492.1710265251459,7139.450638527051),
	            (2884.310650350817	,6739.898362071253),
	            (8081.8694962413865	,4302.345360684209),
	            (8880.999446399976	,4995.583071687259),
	            (8956.585596129007	,2900.021306697279),
                (9693.765315953002	,4040.9774552639574),
	            (4351.78912476456	,6749.685636194423),
	            (5341.992076640308	,7590.867881071754),
	            (6053.029849687009	,8420.665534330532),
	            (6230.669761522848	,5831.260676609352),
                (6446.489601869776	,6969.5605676062405),
	(6776.31818445836	,7725.019962761551),
                (6785.92811847938	,5631.88518595323),
	            (7000.471389925689	,8517.930215800181),
                (7034.0943249735865	,7203.0999901257455),
	            (7041.881559856411	,6100.76363812387),
                (7019.382565619482	,3541.3401659633964),
	            (7295.687263581378	,7026.132244029082),
	            (7234.1038036357495	,5147.231907959096),
                (7336.778368810832	,5733.291468182579),
                (7477.819084770512	,6206.572780934162),
                (7467.111509346985	,5394.372223624028),
                (7605.93779024086	,8238.779581099749),
                (7551.323836995813	,5914.34841708187),
                (8266.141841106757	,7723.856999381445),
                (8403.357620962488	,6861.515908261761),
                (9639.180501949682	,7772.034544526599),
                (9868.035518714401	,9199.346536568366),
                (10138.663072469237	,9166.881113521755),
                (10433.77439901681	,9612.15468710661),
                (10652.149316757394	,9036.247077666223),
                (1417.465907255828	,10448.740682003088),
                (13063.847855016298	,9224.429118987173),
                (6269.467655669607	,-392.85834977496415),
                (14454.084663019341	,7380.9256480988115),
                (1690.7115968544385	,8623.412708808668),
                (8839.123639357684	,4462.860305545852),
                (10122.09863595455	,-371.97026650141925)]
# Dicionário para armazenar as edges mais próximas para cada ponto
result_dict = {}

# Número de edges mais próximas que você deseja coletar (5 neste caso)
num_closest_edges = 10

# Iterar sobre os pontos de entrada
for point_id, (x, y) in enumerate(entry_points):
    distances = {}

    # Iterar sobre todas as arestas no arquivo .net.xml
    for edge in root.findall(".//edge"):
        edge_id = edge.get("id")
        function = edge.get("function")
        
        # Verificar se a função não é "internal"
        if function != "internal":
            for lane in edge.findall("lane"):
                shape_str = lane.get("shape")
                shape_points = [tuple(map(float, point.split(","))) for point in shape_str.split(" ")]
                for i in range(len(shape_points) - 1):
                    x1, y1 = shape_points[i]
                    x2, y2 = shape_points[i + 1]
                    distance = calculate_distance(x, y, x1, y1)
                    distances[edge_id] = distance

    # Coletar as 5 arestas mais próximas (ou menos se não houver 5)
    closest_edges = sorted(distances, key=distances.get)[:num_closest_edges]

    result_dict[point_id] = closest_edges

# for point_id, closest_edges in result_dict.items():
#     print(f"{point_id}: {closest_edges}")

print(result_dict)
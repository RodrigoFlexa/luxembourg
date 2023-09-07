import time
tempo_i = time.time()

for i in range(300000):
    if i == 100000:
        print("tempo: ", time.time() - tempo_i)
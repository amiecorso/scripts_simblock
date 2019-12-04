


def get_avg_pairwise_delay(filename):
    FILENAME = "output_small.json"

    with open(FILENAME, 'r') as f:
        contents = f.read()

    total_proptime = 0
    numsamples = 0
    aslist = eval(contents)
    for item in aslist:
        if item['kind'] == 'flow-block':
            print(item)
            info = item['content']
            trans_stamp = info['transmission-timestamp']
            recv_stamp = info['reception-timestamp']
            proptime_ms = recv_stamp - trans_stamp
            total_proptime += proptime_ms
            numsamples += 1
    total_proptime /= 1000 # ms to sec
    return round(total_proptime / numsamples, 5)


print(get_avg_pairwise_delay("dummy"))

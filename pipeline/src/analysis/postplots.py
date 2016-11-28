def heatmap_coherence(data, chans, 
                      skip=1, start=0, end=5000):
    currd = data[:, chans][start:end:skip]
    currd = currd.T
    coherearr = []
    for i in range (0, len(cxurrd)):
        temparr = []
        for j in range (0, len(currd)):
            temparr.append(np.mean(
                    signal.coherence(currd[i], currd[j], fs)[1]
                ))
        coherearr.append(temparr)
    data = [
        Heatmap(
            x = chans,
            y = chans,
            z=coherearr
        )
    ]
    iplot(Figure(data = data, layout = layout), filename='labelled-heatmap')
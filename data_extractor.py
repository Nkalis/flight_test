def data_extractor(dataA, dataB):

    import mat4py    
    
    data = mat4py.loadmat("matlab.mat")
    flightdata = data.get('flightdata', {})
    
    data1 = flightdata.get(str(dataA))
    data2 = flightdata.get(str(dataB))
    
    return data1, data2
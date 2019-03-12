def data_extractor():

    import mat4py    
    
    data = mat4py.loadmat("matlab.mat")
    flightdata = data.get('flightdata', {})
    
    return flightdata

m = data_extractor()
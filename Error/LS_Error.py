def ls_error(y, x):
    
    err = 0
    
    if y.shape == x.shape:
        for i in (y - x)**2:
            for j in i:
                err += j
        return err
    else:
        print("Error: Arrays must have the same shapes")

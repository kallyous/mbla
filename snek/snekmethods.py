def treatData(data):
    try: val = int(data)
    except: pass
    else: return val
    try: val = float(data)
    except: pass
    else: return val
    try: val = data.lower().strip()
    except: pass
    else:
        if val == 'true': return True
        if val == 'false': return False
    return data
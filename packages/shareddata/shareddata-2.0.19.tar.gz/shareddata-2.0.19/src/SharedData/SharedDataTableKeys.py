import numpy as np
from numba import njit,prange

class SharedDataTableKeys:
    
    def get_pkeycolumns(database):
        if database == 'MarketData':
            return ['date','symbol']
                
        elif database == 'Portfolios':
            return ['date','portfolio']
        
        elif database == 'Risk':
            return ['date','portfolio','riskfactor']
        
        elif database == 'Relationships':
            return ['date','riskfactor1','riskfactor2']
        
        elif database == 'Positions':
            return ['date','portfolio','symbol']
        
        elif database == 'Orders':
            return ['date','portfolio','symbol','clordid']
                
        elif database == 'Trades':
            return ['date','portfolio','symbol','tradeid']
                
        else:
            raise Exception('Database not implemented!')
                
    ############################## NUMBA JIT FUNCTIONS ##############################

    ############################# CREATE PKEY #############################  
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_marketdata_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['symbol'][start+i])            
            harr[i] = (h1 ^ h2) % n

        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['symbol'] != records[start+i]['symbol']):
                    h = (h + j**2) % n
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!') 
         
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_portfolios_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['portfolio'][start+i])            
            harr[i] = (h1 ^ h2) % n

        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['portfolio'] != records[start+i]['portfolio']):
                    h = (h + j**2) % n
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')                 
            
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_risk_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['portfolio'][start+i])
            h3 = hash(records['riskfactor'][start+i])            
            harr[i] = (h1 ^ h2 ^ h3) % n

        # allocate keys
        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:                 
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['portfolio'] != records[start+i]['portfolio'])\
                    | (records[id]['riskfactor'] != records[start+i]['riskfactor']):
                    h = (h + j**2) % n                    
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')
             
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_relationships_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['riskfactor1'][start+i])
            if records['riskfactor1'][start+i] != records['riskfactor2'][start+i]:
                h3 = hash(records['riskfactor2'][start+i])
                harr[i] = (h1 ^ h2 ^ h3) % n
            else:
                harr[i] = (h1 ^ h2) % n

        # allocate keys
        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:                 
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['riskfactor1'] != records[start+i]['riskfactor1'])\
                    | (records[id]['riskfactor2'] != records[start+i]['riskfactor2']):
                    h = (h + j**2) % n                    
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')
    
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_positions_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['portfolio'][start+i])
            h3 = hash(records['symbol'][start+i])            
            harr[i] = (h1 ^ h2 ^ h3) % n

        # allocate keys
        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:                 
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['portfolio'] != records[start+i]['portfolio'])\
                    | (records[id]['symbol'] != records[start+i]['symbol']):
                    h = (h + j**2) % n                    
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')               

    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_orders_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['portfolio'][start+i])
            h3 = hash(records['symbol'][start+i])
            h4 = hash(records['clordid'][start+i])
            harr[i] = (h1 ^ h2 ^ h3 ^ h4) % n

        # allocate keys
        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:                 
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['portfolio'] != records[start+i]['portfolio'])\
                    | (records[id]['symbol'] != records[start+i]['symbol'])\
                    | (records[id]['clordid'] != records[start+i]['clordid']):
                    h = (h + j**2) % n                    
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')                        
    
    @staticmethod
    @njit(cache=True,parallel=True)
    def create_pkey_trades_jit(records,count,pkey,start):
        n = pkey.size-1
        if start==0:        
            pkey[:] = -1 # reset keys 

        # calculate hash
        nhash = count-start
        harr = np.empty((nhash, ))
        for i in prange(nhash):
            h1 = hash(records['date'][start+i])
            h2 = hash(records['portfolio'][start+i])
            h3 = hash(records['symbol'][start+i])
            h4 = hash(records['tradeid'][start+i])
            harr[i] = (h1 ^ h2 ^ h3 ^ h4) % n

        # allocate keys
        for i in range(nhash):
            h = int(harr[i])
            id = pkey[h]
            if id == -1:                 
                pkey[h] = start+i
            else:
                # check for hash collision
                j = 1
                duplkey = True
                while (records[id]['date'] != records[start+i]['date'])\
                    | (records[id]['portfolio'] != records[start+i]['portfolio'])\
                    | (records[id]['symbol'] != records[start+i]['symbol'])\
                    | (records[id]['tradeid'] != records[start+i]['tradeid']):
                    h = (h + j**2) % n                    
                    if pkey[h] == -1:
                        pkey[h] = start+i
                        duplkey = False
                        break
                    j += 1

                if duplkey:                 
                    raise Exception('error duplicated index!')  

    ############################# GET LOC #############################
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_marketdata_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['symbol'][i])
            h = (h1 ^ h2) % n
            id = pkey[h]
            if id == -1: 
                loc[i] = id # not found
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['symbol'] != keys[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break # not found
                    j += 1
                loc[i] = id
        return loc
    
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_portfolios_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['portfolio'][i])
            h = (h1 ^ h2) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['portfolio'] != keys[i]['portfolio']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
    
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_risk_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['portfolio'][i])
            h3 = hash(keys['riskfactor'][i])
            h = (h1 ^ h2 ^ h3) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['portfolio'] != keys[i]['portfolio'])\
                    | (records[id]['riskfactor'] != keys[i]['riskfactor']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
        
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_relationships_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['riskfactor1'][i])
            h3 = hash(keys['riskfactor2'][i])
            h = (h1 ^ h2 ^ h3) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['riskfactor1'] != keys[i]['riskfactor1'])\
                    | (records[id]['riskfactor2'] != keys[i]['riskfactor2']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
                      
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_positions_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['portfolio'][i])
            h3 = hash(keys['symbol'][i])
            h = (h1 ^ h2 ^ h3) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['portfolio'] != keys[i]['portfolio'])\
                    | (records[id]['symbol'] != keys[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
                        
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_orders_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['portfolio'][i])
            h3 = hash(keys['symbol'][i])
            h4 = hash(keys['clordid'][i])
            h = (h1 ^ h2 ^ h3 ^ h4) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['portfolio'] != keys[i]['portfolio'])\
                    | (records[id]['symbol'] != keys[i]['symbol'])\
                    | (records[id]['clordid'] != keys[i]['clordid']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
    
    @staticmethod
    @njit(cache=True,parallel=True)
    def get_loc_trades_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in prange(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['portfolio'][i])
            h3 = hash(keys['symbol'][i])
            h4 = hash(keys['tradeid'][i])
            h = (h1 ^ h2 ^ h3 ^ h4) % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['portfolio'] != keys[i]['portfolio'])\
                    | (records[id]['symbol'] != keys[i]['symbol'])\
                    | (records[id]['tradeid'] != keys[i]['tradeid']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
                

    ############################## UPSERT ##############################    
    @staticmethod
    @njit(cache=True)
    def upsert_marketdata_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size        
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['symbol'][i])            
            h = (h1 ^ h2) % n
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1            
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['symbol'] != new_records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count                    
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists                    
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
        
    @staticmethod
    @njit(cache=True)
    def upsert_portfolios_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size        
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h = (h1 ^ h2) % n            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1            
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count                    
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists                    
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
      
    @staticmethod
    @njit(cache=True)
    def upsert_risk_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h3 = hash(new_records['riskfactor'][i])                
            h = (h1 ^ h2 ^ h3) % n            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1                
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio'])\
                    | (records[id]['riskfactor'] != new_records[i]['riskfactor']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
    
    @staticmethod
    @njit(cache=True)
    def upsert_relationships_jit(records,count,new_records,pkey):
        n = pkey.size-1
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['riskfactor1'][i])
            if new_records['riskfactor1'][i] != new_records['riskfactor2'][i]:
                h3 = hash(new_records['riskfactor2'][i]) 
                h = (h1 ^ h2 ^ h3) % n
            else:                
                h = (h1 ^ h2) % n
            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['riskfactor1'] != new_records[i]['riskfactor1'])\
                    | (records[id]['riskfactor2'] != new_records[i]['riskfactor2']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid

    @staticmethod
    @njit(cache=True)
    def upsert_positions_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h3 = hash(new_records['symbol'][i])                
            h = (h1 ^ h2 ^ h3) % n
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1                
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio'])\
                    | (records[id]['symbol'] != new_records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
    
    @staticmethod
    @njit(cache=True)
    def upsert_orders_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h3 = hash(new_records['symbol'][i])
            h4 = hash(new_records['clordid'][i])
            h = (h1 ^ h2 ^ h3 ^ h4) % n            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1                
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio'])\
                    | (records[id]['symbol'] != new_records[i]['symbol'])\
                    | (records[id]['clordid'] != new_records[i]['clordid']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid

    @staticmethod
    @njit(cache=True)
    def upsert_trades_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h3 = hash(new_records['symbol'][i])
            h4 = hash(new_records['tradeid'][i])
            h = (h1 ^ h2 ^ h3 ^ h4) % n            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1                
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio'])\
                    | (records[id]['symbol'] != new_records[i]['symbol'])\
                    | (records[id]['tradeid'] != new_records[i]['tradeid']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
    
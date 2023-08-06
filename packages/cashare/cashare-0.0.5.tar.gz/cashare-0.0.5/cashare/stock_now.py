import httpx
from cashare.dname import url1,url2
import pandas as pd
def st_now(token,stock:str):
    if type in['us','hk']:
        url = url1 + '/stock/list/'+type+'/'+ token
        r = httpx.get(url,timeout=40)
        return pd.DataFrame(r.json())
    else:
        return "type输入错误"

if __name__ == '__main__':
    df=st_now(type='us',token='g0ad8f825bad3234af22d39de80f717db93')
    print(df)
    pass




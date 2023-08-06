import httpx
from cashare.dname import url1,url2
import pandas as pd
def stock_list(token,type:str):
    if type in['us','hk']:
        url = url1 + '/stock/list/'+type+'/'+ token
        r = httpx.get(url,timeout=40)
        return pd.DataFrame(r.json())
    else:
        return "type输入错误"

if __name__ == '__main__':
    df=stock_list(type='hk',token='y0ad8f825bad3234ada0ab7ff56e1925372')
    print(df)
    pass




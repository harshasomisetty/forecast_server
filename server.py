import pandas as pd
from pandas.tseries.offsets import *
import numpy as np
from aiohttp import web
from sklearn.linear_model import LinearRegression

routes = web.RouteTableDef()

@routes.post('/')
async def handle_post(request):
    data = await request.json()
    predictions = {}

    for key in data.keys():
        prices = np.array([v for v in data[key].values() if v != None])
        next_date = pd.to_datetime(pd.Series(data[key]).index[-1]) + BDay()
        
        if prices.size <=1:
            predictions[key] = {str(next_date) : None}
        else:
            model = LinearRegression().fit(np.arange(0, prices.size).reshape(-1, 1), prices)
            predictions[key] = {str(next_date): model.predict(np.array([prices.size]).reshape(-1, 1))[0]}
    return web.json_response(predictions)

app = web.Application()
app.add_routes(routes)

#TODO default endpoint handler
#TODO bad json

if __name__ == '__main__':
    web.run_app(app, port=8000)


import pandas as pd
from pandas.tseries.offsets import *
import numpy as np
from aiohttp import web
from sklearn.linear_model import LinearRegression
import dateutil
import logging

logging.basicConfig(level=logging.DEBUG, filename='forecasts.log',
                    format="%(asctime)s:%(levelname)s:%(message)s")

logging.getLogger("aiohttp").setLevel(logging.WARNING)

async def handle_forecast(request):
    data = await request.json()
    print(data)
    if data: 
        predictions = {}

        for key in data.keys():
            try:
                prices = np.array([v for v in data[key].values() if v != None])
            except AttributeError:
                logging.warning("invalid data format: "+ str(data[key]))
                return web.Response(text="Invalid Data Format: "+key)

            try:
                next_date = pd.to_datetime(pd.Series(data[key]).index[-1]) + BDay()
            except dateutil.parser._parser.ParserError:
                logging.warning("invalid string format "+ str(data[key]))
                return web.Response(text="Invalid String Format: "+key)

            if prices.size <=1:
                predictions[key] = {str(next_date) : None}
            else:
                model = LinearRegression().fit(np.arange(0, prices.size).reshape(-1, 1), prices)
                predictions[key] = {str(next_date):
                                    model.predict(np.array([prices.size]).reshape(-1, 1))[0]}
                logging.info(predictions[key])
        return web.json_response(predictions)
    else:
        return web.Response(text="No Post")


app = web.Application()
app.add_routes([web.post('/{tail:.*}', handle_forecast)])
                

#TODO bad json

if __name__ == '__main__':
    web.run_app(app, port=8000)

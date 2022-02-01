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
    try: #makes sure post request contains a payload
        data = await request.json()
    except:
        return web.Response(text="Error: No Data in Post")
    predictions = {}

    for key in data.keys(): #tries to iterate through each equity in payload
        try:
            # ignore all null values
            prices = np.array([v for v in data[key].values() if v != None])
        except AttributeError: # the payload json format is incorrect, so exit
            logging.warning("invalid data format: "+ str(data[key]))
            return web.Response(text="Error Invalid Data Format: "+key)

        if any([i <=0 for i in prices]):
            logging.warning("Negative values are not allowed "+ str(data[key]))
            return web.Response(text="Error Negative values are not allowed: "+key)

        try:
            next_date = pd.to_datetime(pd.Series(data[key]).index[-1]) + BDay()
        except dateutil.parser._parser.ParserError:
            logging.warning("invalid string format "+ str(data[key]))
            return web.Response(text="Error Invalid String Format: "+key)

        if prices.size <=1: # not enough data to make a prediction
            predictions[key] = {str(next_date) : None}
        else: # contruct lin reg model, make 1 step prediction the next result

            # evenly spacing all data points regardless of exact date to make prediction
            model = LinearRegression().fit(np.arange(0, prices.size).reshape(-1, 1), prices)

            # also, making the minimum prediction 0 incase prediction becomes negative
            predictions[key] = {str(next_date):
                                max(0, model.predict(np.array([prices.size]).reshape(-1, 1))[0])}

        logging.info(predictions[key])

    return web.json_response(predictions) # final list of predictions for each equity


app = web.Application()

# all calls get routed to default endpoint function "handle forecast"
app.add_routes([web.post('/{tail:.*}', handle_forecast)])


if __name__ == '__main__':
    web.run_app(app, port=8000)

import pandas as pd
from pandas.tseries.offsets import *
import numpy as np
from aiohttp import web
from sklearn.linear_model import LinearRegression

routes = web.RouteTableDef()


@routes.get('/')
async def handle_main(request):
    text = "Main"
    return web.Response(text=text)

@routes.get('/name/{name}')
async def handle_get(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

@routes.post('/forecast')
async def handle_post(request):
    data = await request.json()
    keys = list(data.keys())
    values = {}

    for key in keys:
        vals = np.array(list(data[key].values()))
        vals = vals[vals != np.array(None)]
        # print(vals)
        model = LinearRegression().fit(np.arange(0, vals.size).reshape(-1, 1), vals)
        values[key] = model.predict(np.array([vals.size]).reshape(-1, 1))[0]
    print(values)
    return web.Response(text="hi")

app = web.Application()
app.add_routes(routes)



if __name__ == '__main__':
    web.run_app(app, port=8080)

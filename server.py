import pandas as pd
from aiohttp import web

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

@routes.post('/post')
async def handle_post(request):
    data = await request.json()
    print(data.keys())
    # print(data.len())
    return web.Response(text="hi")

app = web.Application()
app.add_routes(routes)



if __name__ == '__main__':
    web.run_app(app, port=8080)

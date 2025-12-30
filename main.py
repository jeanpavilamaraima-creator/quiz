from fastapi import FastAPI
from information import information_router
from games import games_router
from starlette.middleware.sessions import SessionMiddleware 
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="mi-secreto-super-seguro")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(information_router, prefix="/info")
app.include_router(games_router)


@app.get("/", include_in_schema=False)
async def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/home")  
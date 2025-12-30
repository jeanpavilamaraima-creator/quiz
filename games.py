import random
from typing import List, Optional
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware 
from countries_data import countries_list 

games_router = APIRouter()



templates = Jinja2Templates(directory="templates")

countries_db_list = countries_list
continents = sorted(list(set(country["continent"] for country in countries_db_list)))

def get_country_by_code(code):
    for c in countries_db_list:
        if c["code"] == code:
            return c
    return None

def get_random_country(continent=None, exclude_codes=[]):
    if continent and continent != "All":
        candidates = [c for c in countries_db_list if c["continent"] == continent]
    else:
        candidates = countries_db_list
    
    available = [c for c in candidates if c["code"] not in exclude_codes]
    
    if not available:
        return None
    return random.choice(available)

@games_router.get("/home", response_class=HTMLResponse)  # Changed to /home to avoid conflict with root
async def home(request: Request):
    request.session.clear()
    return templates.TemplateResponse("home.html", {"request": request, "continents": continents})

@games_router.get("/countries", response_class=HTMLResponse)
async def countries_view(request: Request):
    return RedirectResponse(url="/continent/All", status_code=303)

@games_router.get("/continent/{continent_name}", response_class=HTMLResponse)
async def continent_data(request: Request, continent_name: str):
    if continent_name == "All":
        display = countries_db_list
    else:
        display = [c for c in countries_db_list if c["continent"] == continent_name]
    
    return templates.TemplateResponse("datos_paises.html", {
        "request": request,
        "countries": display,
        "continents": continents,
        "search_term": None
    })

@games_router.post("/check-information", response_class=HTMLResponse)
async def check_info(request: Request, country_name: str = Form(...)):
    search = country_name.strip().lower()
    filtered = [c for c in countries_db_list if search in c["name"].lower()]
    return templates.TemplateResponse("datos_paises.html", {
        "request": request, "countries": filtered, "continents": continents, "search_term": country_name
    })

@games_router.get("/quiz", response_class=HTMLResponse)
async def quiz_global_redirect(request: Request):
    return RedirectResponse(url="/quiz/All", status_code=303)

@games_router.get("/quiz/{continent_name}", response_class=HTMLResponse)
async def quiz_interface(request: Request, continent_name: str):
    session_continent = request.session.get("continent")
    
    if session_continent != continent_name:
        request.session["continent"] = continent_name
        request.session["guessed_codes"] = []
        request.session["attempts"] = 5
        request.session["current_code"] = None
        request.session["message"] = None
        request.session["game_over"] = False

    current_code = request.session.get("current_code")
    
    if not current_code and not request.session.get("game_over"):
        guessed = request.session.get("guessed_codes", [])
        new_country = get_random_country(continent_name, guessed)
        
        if new_country:
            request.session["current_code"] = new_country["code"]
            current_code = new_country["code"]
        else:
            return templates.TemplateResponse("home.html", {
                "request": request, 
                "continents": continents,
                "message": f"¡Felicidades! Completaste todo {continent_name}!"
            })

    country_obj = get_country_by_code(current_code)
    
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "country": country_obj,
        "continent": continent_name,
        "attempts_left": request.session.get("attempts"),
        "message": request.session.get("message"),
        "game_over": request.session.get("game_over", False)
    })

@games_router.post("/quiz/{continent_name}", response_class=HTMLResponse)
async def quiz_process(request: Request, continent_name: str, guess: str = Form(...)):
    current_code = request.session.get("current_code")
    country_obj = get_country_by_code(current_code)
    
    if not country_obj:
        return RedirectResponse(f"/quiz/{continent_name}", status_code=303)

    user_guess = guess.strip().lower()
    correct_name = country_obj["name"].lower()

    if user_guess == correct_name:
        request.session["message"] = f"¡Correcto! Era {country_obj['name']}."
        guessed_list = request.session.get("guessed_codes", [])
        guessed_list.append(current_code)
        request.session["guessed_codes"] = guessed_list
        request.session["current_code"] = None
        if request.session["attempts"] < 5:
            request.session["attempts"] += 1
    else:
        request.session["attempts"] -= 1
        request.session["message"] = "Incorrecto, intenta de nuevo."
        
        if request.session["attempts"] <= 0:
            request.session["game_over"] = True
            request.session["message"] = f"¡Perdiste! Era {country_obj['name']}."

    return RedirectResponse(url=f"/quiz/{continent_name}", status_code=303)

@games_router.post("/quiz", response_class=HTMLResponse)
async def quiz_post_global(request: Request, guess: str = Form(...)):
    return await quiz_process(request, "All", guess)


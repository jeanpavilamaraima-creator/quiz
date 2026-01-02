
from typing import List, Optional
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware 
from countries_data import countries_list 
from continents_facts import continents_facts

information_router = APIRouter()
templates = Jinja2Templates(directory="templates")


countries_db_list = countries_list
continents = sorted(list(set(country["continent"] for country in countries_db_list)))
countries_data = sorted(list(set(countries["name"] for countries in countries_db_list)))





@information_router.get("/continents_data", response_class=HTMLResponse)
async def continents_view(request: Request):
    data = []
    for cont in continents:
        facts = continents_facts.get(cont, {})
        num_countries = len([c for c in countries_db_list if c["continent"] == cont])
        data.append({
            "name": cont,
            "num_countries": num_countries,
            "population": facts.get("population", 0),
            "main_languages": ", ".join(facts.get("main_languages", [])),
            "interesting_facts": "<br>".join(facts.get("interesting_facts", []))  
        })
    return templates.TemplateResponse("datos_continentes.html", {
        "request": request,
        "continents_data": data,
        "continents": continents
    })

@information_router.get("/country/{country_name}", response_class=HTMLResponse)
async def country_detail(request: Request, country_name: str):
    country = next((c for c in countries_db_list if c["name"].lower() == country_name.lower()), None)
    if not country:
        return RedirectResponse("/countries", status_code=303)
    return templates.TemplateResponse("datos_pais.html", {
        "request": request,
        "country": country
    })
    


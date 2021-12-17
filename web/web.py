from fastapi import FastAPI
import uvicorn
import asyncio

from util.db_handler import DBInfoHandler
import config

app = FastAPI()

def error(reason):
    return {"error": reason}

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/{user_id}/stats")
async def user_stats(user_id: int):
    data = DBInfoHandler().get_user_data(user_id)
    if data is None:
        return error("user does not exist")
    return data

@app.get("/{user_id}/stats/{minigame}")
async def user_stats_for_game(user_id: int, minigame: str):
    data = DBInfoHandler().get_user_data(user_id)
    if data is None:
        return error("user does not exist")
    try:
        return data[minigame]
    except KeyError:
        return error("minigame does not exist")


@app.get("/leaderboard")
async def all_leaderboards():
    pass #return {"leaderbaords:" }

@app.get("/leaderboard/list")
async def list_leaderboards():
    return {"minigames": DBInfoHandler().get_minigame_list()}


@app.get("/leaderboard/{minigame}")
async def leaderboard_for_game(minigame: str):
    if minigame not in DBInfoHandler().get_minigame_list():
        return error("minigame does not exist")
    highscores, wins = DBInfoHandler().get_leaderboard(minigame)
    return {"highscores": highscores, "wins": wins}


def run_apiserver():
    uvicorn.run(app=__name__ + ":app", port=config.API_SERVER_PORT, host=config.API_SERVER_HOST, log_level="critical")

def stop_apiserver():
    asyncio.current_task().cancel()

import logging
import re
import rus_extractor
import eng_extractor
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from logger import init_logger, request_headers

init_logger()
logging.getLogger().info("Entities extractor run")
server = FastAPI()

@server.post("/extract")
async def extract(request: Request):
    request_headers.set(dict(request.headers))
    try:
        body = await request.json()
        message = body.get("message")
        if contains_russian(message):
            return JSONResponse(content=rus_extractor.extract_entities(message))
        else:
            return JSONResponse(content=eng_extractor.extract_entities(message))

    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Произошла ошибка при получении обьектов из сообщения")

def contains_russian(text):
    return bool(re.search('[а-яА-Я]', text))
import logging
import rus_extractor
import eng_extractor
import spa_extractor
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from logger import init_logger, request_headers

init_logger()
logging.getLogger().info("Entities extractor run")
server = FastAPI()

SUPPORTED_LANGUAGES = {'ru', 'en', 'es'}

@server.post("/extract")
async def extract(request: Request):
    request_headers.set(dict(request.headers))
    try:
        body = await request.json()
        message = body.get("message")
        lang = body.get("language")

        if not lang:
            raise HTTPException(status_code=400, detail="Field 'language' is required")
        if lang not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported language '{lang}'. Supported: {sorted(SUPPORTED_LANGUAGES)}")

        if lang == 'ru':
            extracted_entities = rus_extractor.extract_entities(message)
        elif lang == 'es':
            extracted_entities = spa_extractor.extract_entities(message)
        else:
            extracted_entities = eng_extractor.extract_entities(message)

        response_content = {"entities": extracted_entities}

        return JSONResponse(content=response_content)

    except HTTPException:
        raise
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {error}")

@server.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
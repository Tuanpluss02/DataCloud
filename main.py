import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from controllers import router as api_router
import uvicorn
import pretty_errors
from utils.custom_response import IResponse
from utils.database_config import MongoManager


def startup_event():
    MongoManager.initialize_collections()

def shutdown_event():
    MongoManager.close_mongo_connection()

app = FastAPI(on_startup=[startup_event], on_shutdown=[shutdown_event])
app.include_router(api_router)

@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=IResponse.init(
        status_code=exc.status_code,
            path=request.url.path,
            message=exc.detail
        )
    )


if __name__ == "__main__":
    pretty_errors.configure(
    separator_character = '*',
    filename_display    = pretty_errors.FILENAME_EXTENDED,
    line_number_first   = True,
    display_link        = True,
    lines_before        = 5,
    lines_after         = 2,
    line_color          = pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
    code_color          = '  ' + pretty_errors.default_config.line_color,
    truncate_code       = True,
    display_locals      = True
)
    uvicorn.run(app, host="0.0.0.0", port=8080)

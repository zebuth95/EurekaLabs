import time

from py_fastapi_logging.middlewares.logging import LoggingMiddleware
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from models.BaseModel import init
from routers.v1.UserRouter import UserRouter
from routers.v1.AuthRouter import AuthRouter
from routers.v1.AlphaRouter import AlphaRouter
from configs.Environment import get_environment_variables
from configs.Limiter import limiter


env = get_environment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    debug=env.DEBUG_MODE
)

# Add Middleware
app.add_middleware(LoggingMiddleware, app_name=env.LOG_DIR)

# Add Routers
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(AlphaRouter)

# Add Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Initialise Data Model Attributes
init()

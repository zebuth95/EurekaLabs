from fastapi import APIRouter, Depends, Request

from adapters.AlphaAdapter import alpa_search
from configs.Auth import oauth2_scheme
from configs.Limiter import limiter
from schemas.AlphaSchema import AlphaOptions

AlphaRouter = APIRouter(prefix="/v1/alpha", tags=["alpha"])


@AlphaRouter.get(
    "/",
)
@limiter.limit("5/minute")
def index(
    request: Request,
    symbol: AlphaOptions,
    token: str = Depends(oauth2_scheme),
):
    return alpa_search(symbol).get()

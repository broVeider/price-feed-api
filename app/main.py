from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from app.common.base import Base
from app.common.crud import get_tokens, sync_tokens
from app.common.schemas import TokenSchema
from app.common.session import engine, get_db


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    create_tables()
    return app


app = start_application()


@app.get("/tokens/", response_model=List[TokenSchema])
def read_users(denom__in: str = '', db: Session = Depends(get_db)):
    return get_tokens(denom__in, db)


@app.on_event("startup")
@repeat_every(seconds=3600)
def sync_tokens_task(db: Session = Depends(get_db)) -> None:
    sync_tokens(db)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI

from . import repository
from db import SessionDep

app = FastAPI()


@app.get("/access/check")
def check_access(tag_uid: str, session: SessionDep):
    maybe_tag = repository.get_tag_by_tag_uid(tag_uid, session)
    is_access_granted = maybe_tag is not None

    access_log = repository.create_access_log(
        tag_uid=tag_uid,
        access_was_granted=is_access_granted,
        personal_information=maybe_tag,
        session=session,
    )

    return access_log

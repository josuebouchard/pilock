from datetime import datetime
from .models import AccessLog, PersonInformation, Tag
from sqlmodel import Session, col, select


def get_tags(session: Session):
    return session.exec(select(Tag)).all()


def get_tag_by_id(id: int, session: Session):
    return session.exec(select(Tag).where(Tag.id == id)).first()


def get_tag_by_tag_uid(tag_uid: str, session: Session):
    tag_uid = tag_uid.strip().upper()
    stmt = select(Tag).where(col(Tag.tag_uid).ilike(tag_uid))
    return session.exec(stmt).first()


def save_tag(tag: Tag, session: Session):
    tracked_tag = session.merge(tag)
    tag.tag_uid = tag.tag_uid.strip().upper()

    session.commit()
    session.refresh(tracked_tag)

    return tracked_tag


def disable_tag(tag_id: int, session: Session):
    tag = session.get(Tag, tag_id)
    session.delete(tag)

    session.commit()


def get_access_logs(
    session: Session,
    from_datetime: datetime | None = None,
    to_datetime: datetime | None = None,
):
    stmt = select(AccessLog).order_by(col(AccessLog.timestamp).desc())
    if from_datetime:
        stmt = stmt.where(AccessLog.timestamp >= from_datetime)
    if to_datetime:
        stmt = stmt.where(AccessLog.timestamp <= to_datetime)

    return session.exec(stmt).all()


def create_access_log(
    tag_uid: str,
    access_was_granted: bool,
    person_information: PersonInformation | None,
    session: Session,
):
    access_log = AccessLog(tag_uid=tag_uid, access_was_granted=access_was_granted)

    if person_information is not None:
        _ = access_log.sqlmodel_update(person_information)

    # {"tag_uid": tag_uid, "access_was_granted": access_was_granted}
    session.add(access_log)
    session.commit()
    session.refresh(access_log)

    return access_log

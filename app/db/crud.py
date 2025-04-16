from sqlalchemy.orm import Session
from app.db.models import UserFact, UserPreference, MessageHistory


def save_user_facts(user_id: int, facts: dict, db: Session):
    for key, value in facts.items():
        existing = db.query(UserFact).filter_by(user_id=user_id, key=key).first()
        if existing:
            existing.value = str(value)
        else:
            new_fact = UserFact(user_id=user_id, key=key, value=str(value))
            db.add(new_fact)
    db.commit()


def save_user_preferences(user_id: int, facts: list, db: Session):
    for fact in facts:
        value = fact["value"]
        sentiment = fact["sentiment"]
        category = fact["category"]

        existing = db.query(UserPreference).filter_by(user_id=user_id, category=category, value=value).first()

        if existing:
            # If the preference already exists, update the sentiment
            existing.sentiment = sentiment
        else:
            new_preference = UserPreference(
                user_id=user_id,
                category=category,
                value=value,
                sentiment=sentiment
            )
            db.add(new_preference)

    db.commit()


def get_user_facts(user_id: int, db: Session):
    facts = db.query(UserFact).filter_by(user_id=user_id).all()
    return {fact.key: fact.value for fact in facts}


def save_message(user_id: int, message: str, is_bot: bool, db: Session):
    new_message = MessageHistory(
        user_id=user_id,
        message=message,
        is_bot=is_bot
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def get_last_bot_message(user_id: int, db: Session) -> str:
    return (
        db.query(MessageHistory)
        .filter_by(user_id=user_id, is_bot=True)
        .order_by(MessageHistory.timestamp.desc())
        .first()
    ).message

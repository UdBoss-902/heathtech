from healthtech import models
from sqlalchemy.orm import Session
from datetime import datetime

def log_action(db: Session, User_id: int, action: str, entity: str, entity_id: int):
    log = models.AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
        User_id=User_id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    
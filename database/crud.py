from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update
from .models import Cat, Mission, Target
from .schemas import CatCreate, MissionCreate


def get_cats(db: Session):
    return db.query(Cat).all()


def create_cat(db: Session, cat: CatCreate):
    db_cat = Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return {"message": f"Cat added  successfully"}


def get_cat_by_id(db: Session, cat_id: int):
    return db.query(Cat).filter(Cat.id == cat_id).first()


def delete_cat(db: Session, cat_id: int):
    try:
        cat = db.query(Cat).filter(Cat.id == cat_id).first()
        if cat:
            db.delete(cat)
            db.commit()
            return {"message": f"Cat {cat_id} deleted  successfully"}
        else:
            return {"error": f"Cat {cat_id} not found"}
    except NoResultFound:
        return {"error": f"Cat {cat_id} not found"}


def update_cat_salary(db: Session, cat_id: int, salary: float):
    stmt = update(Cat).where(Cat.id == cat_id).values(salary=salary)
    result = db.execute(stmt)
    if result.rowcount == 0:
        return None 
    db.commit()
    return {"message": f"Salary updated for cat {cat_id} successfully"}


def get_missions(db: Session):
    return db.query(Mission).all()


def create_mission(db: Session, mission: MissionCreate):
    db_mission = Mission(name=mission.name)
    db.add(db_mission)
    db.commit()
    
    for target in mission.targets:
        db_target = Target(**target.dict(), mission_id=db_mission.id)
        db.add(db_target)
    db.commit()
    db.refresh(db_mission)
    return {"message": f"Mission created  successfully"}


def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    
    if mission and cat and mission.cat_id is None:
        mission.cat_id = cat.id
        cat.status = "on_mission"
        db.commit()
        db.refresh(mission)
        return {"message": f"Cat {cat_id} assigned to {mission_id} mission"}
    return None


def get_mission(db: Session, mission_id: int):
    return db.query(Mission).filter(Mission.id == mission_id).first()


def update_target_notes(db: Session, target_id: int, new_notes: str):
    target = db.query(Target).filter(Target.id == target_id).first()
    if target is None:
        return {"error": "Target not found"}
    if target.mission.complete or target.complete:
        return {"error": "Cannot update notes for completed target or mission"}
    target.notes = new_notes
    db.commit()
    return {"message": "Notes updated successfully"}


def mark_target_complete(db: Session, target_id: int):
    target = db.query(Target).filter(Target.id == target_id).first()
    if target:
        target.complete = True
        db.commit()
        db.refresh(target)
        return {"message": "target completed successfully"}
    return None


def mark_mission_complete(db: Session, mission_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if mission and all(target.complete for target in mission.targets):
        mission.complete = True
        db.commit()
        db.refresh(mission)
        return {"message": "mission completed successfully"}
    return None


def delete_mission(db: Session, mission_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if mission is None:
        return {"error": "Mission not found"}
    if mission.cat_id is not None:
        return {"error": f"Mission is already assigned to a cat and cannot be deleted"}
    db.delete(mission)
    db.commit()
    return {"message": f"Mission {mission_id} deleted successfully"}

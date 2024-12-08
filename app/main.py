from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database.engine import session_factory
from database.crud import (
    get_cats,
    get_cat_by_id,
    create_cat,
    create_mission,
    assign_cat_to_mission,
    update_target_notes,
    mark_target_complete,
    mark_mission_complete,
    delete_cat,
    update_cat_salary,
    delete_mission,
    get_missions,
    get_mission,
)

from database.schemas import CatCreate, MissionCreate
from .utils import validate_breed


app = FastAPI()


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@app.post("/cats/")
def create_new_cat(cat: CatCreate, db: Session = Depends(get_db)):
    if not validate_breed(cat.breed):
        raise HTTPException(status_code=400, detail="Invalid breed")
    return create_cat(db, cat)


@app.get("/cats/")
def read_cats(db: Session = Depends(get_db)):
    return get_cats(db)


@app.put("/cats/{cat_id}/salary/")
def update_cat_salary_route(cat_id: int, salary: float, db: Session = Depends(get_db)):
    result = update_cat_salary(db, cat_id, salary)
    if result is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return result


@app.get("/cats/{cat_id}")
def read_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = get_cat_by_id(db, cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@app.delete("/cats/{cat_id}")
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    result = delete_cat(db, cat_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/missions/")
def get_missions_route(db: Session = Depends(get_db)):
    missions = get_missions(db)
    return missions


@app.post("/missions/")
def create_new_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    return create_mission(db, mission)


@app.delete("/missions/{mission_id}/")
def delete_mission_route(mission_id: int, db: Session = Depends(get_db)):
    result = delete_mission(db, mission_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/missions/{mission_id}/")
def get_mission_route(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@app.post("/missions/{mission_id}/assign/{cat_id}")
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = assign_cat_to_mission(db, mission_id, cat_id)
    if mission is None:
        raise HTTPException(
            status_code=400,
            detail="Mission or Cat not found, or Mission already has a Cat assigned.",
        )
    return mission


@app.post("/targets/{target_id}/notes/")
def update_notes(target_id: int, new_notes: str, db: Session = Depends(get_db)):
    target = update_target_notes(db, target_id, new_notes)
    if target is None:
        raise HTTPException(
            status_code=400, detail="Target is completed or does not exist."
        )
    return target


@app.post("/targets/{target_id}/complete/")
def сomplete_target(target_id: int, db: Session = Depends(get_db)):
    target = mark_target_complete(db, target_id)
    if target is None:
        raise HTTPException(status_code=400, detail="Target does not exist.")
    return target


@app.post("/missions/{mission_id}/complete/")
def complete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = mark_mission_complete(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=400, detail="Mission or targets not completed.")
    return mission

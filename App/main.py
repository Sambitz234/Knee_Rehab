from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging

from .database import Base, engine, DB_PATH
from .routers import exercises, sessions, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Knee Rehab Habit Tracker", version="0.1.0")

app.include_router(exercises.router)
app.include_router(sessions.router)
app.include_router(stats.router)

logger = logging.getLogger("uvicorn")
@app.on_event("startup")
def show_db_path():
    logger.info(f"Using database at: {DB_PATH}")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/ui", response_class=HTMLResponse)
def ui_page():
    return """
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>Knee Rehab Habit Tracker</title>
<link rel="stylesheet" href="/static/styles.css">
</head><body>
<header><h1>Knee Rehab Habit Tracker</h1></header>

<section class="card">
  <h2>Create / Edit Exercise</h2>
  <form id="exerciseForm" onsubmit="return submitExercise(event)">
    <div class="grid">
      <label>Name
        <input id="name" required placeholder="Heel Slides">
      </label>
      <label>Side
        <select id="side">
          <option value="left">left</option>
          <option value="right">right</option>
          <option value="both">both</option>
        </select>
      </label>
      <label>Category
        <select id="category">
          <option value="strength">strength</option>
          <option value="mobility" selected>mobility</option>
          <option value="balance">balance</option>
        </select>
      </label>
      <label>Target sets
        <input id="target_sets" type="number" min="0" value="3">
      </label>
      <label>Target reps
        <input id="target_reps" type="number" min="0" value="12">
      </label>
      <label>Target hold (sec)
        <input id="target_hold_sec" type="number" min="0" value="2">
      </label>
    </div>

    <fieldset class="dow">
      <legend>Days of Week (0=Sun … 6=Sat)</legend>
      <label><input type="checkbox" name="dow" value="0"> Sun</label>
      <label><input type="checkbox" name="dow" value="1"> Mon</label>
      <label><input type="checkbox" name="dow" value="2"> Tue</label>
      <label><input type="checkbox" name="dow" value="3"> Wed</label>
      <label><input type="checkbox" name="dow" value="4"> Thu</label>
      <label><input type="checkbox" name="dow" value="5"> Fri</label>
      <label><input type="checkbox" name="dow" value="6"> Sat</label>
    </fieldset>

    <button id="saveBtn" type="submit">Add Exercise</button>
    <button id="cancelBtn" type="button" class="secondary hidden" onclick="cancelEdit()">Cancel</button>
    <span id="msg" class="msg"></span>
  </form>
</section>

<section class="card">
  <h2>Exercises</h2>
  <table id="exerciseTable">
    <thead>
      <tr>
        <th>ID</th><th>Name</th><th>Side</th><th>Category</th>
        <th>Targets</th><th>Schedule</th><th>Actions</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</section>

<script src="/static/ui.js"></script>
</body></html>
    """

@app.get("/")
def root():
    return {"ok": True, "message": "See /docs for API or /ui for the simple interface"}

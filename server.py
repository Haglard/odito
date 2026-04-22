# ============================================================
# ODITO — Audit Management System
# FastAPI + SQLite + cookie auth
# ============================================================
import os, hashlib, secrets, asyncio, json as jsonlib, io
from datetime import datetime, date
from typing import Optional, List, Any
from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, HTTPException, Cookie, Depends, Request, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ── Config ──────────────────────────────────────────────────
DB_PATH        = os.getenv("ODITO_DB", "odito.db")
ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── Helpers ─────────────────────────────────────────────────
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def now_ts() -> int:
    return int(datetime.utcnow().timestamp())

# ── DB init ─────────────────────────────────────────────────
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT    UNIQUE NOT NULL,
            name          TEXT    NOT NULL,
            password_hash TEXT    NOT NULL,
            role          TEXT    DEFAULT 'operational',
            is_admin      INTEGER DEFAULT 0,
            created_at    INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token      TEXT    PRIMARY KEY,
            user_id    INTEGER NOT NULL,
            created_at INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE TABLE IF NOT EXISTS audit_reports (
            id                        INTEGER PRIMARY KEY AUTOINCREMENT,
            report_ref                TEXT    UNIQUE NOT NULL,
            title                     TEXT    NOT NULL,
            audited_entity            TEXT,
            audit_type                TEXT,
            audit_class               TEXT,
            overall_result            TEXT,
            previous_result           TEXT,
            previous_result_date      TEXT,
            issue_date                TEXT,
            sample_period_from        TEXT,
            sample_period_to          TEXT,
            fieldwork_period_from     TEXT,
            fieldwork_period_to       TEXT,
            exit_meeting_date         TEXT,
            exit_meeting_participants TEXT,
            chief_audit_executive     TEXT,
            audit_team_manager        TEXT,
            audit_team                TEXT,
            background                TEXT,
            status                    TEXT    DEFAULT 'open',
            created_by                INTEGER REFERENCES users(id),
            created_at                INTEGER DEFAULT (strftime('%s','now')),
            updated_at                INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE TABLE IF NOT EXISTS findings (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id     INTEGER NOT NULL REFERENCES audit_reports(id) ON DELETE CASCADE,
            finding_ref  TEXT,
            title        TEXT    NOT NULL,
            priority     INTEGER DEFAULT 3,
            description  TEXT,
            article_ref  TEXT,
            root_cause   TEXT,
            recommendation TEXT,
            status       TEXT    DEFAULT 'open',
            created_at   INTEGER DEFAULT (strftime('%s','now')),
            updated_at   INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE TABLE IF NOT EXISTS corrective_measures (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            finding_id           INTEGER NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
            description          TEXT    NOT NULL,
            action_owner_name    TEXT,
            action_owner_user_id INTEGER REFERENCES users(id),
            deadline             TEXT,
            status               TEXT    DEFAULT 'pending',
            notes                TEXT,
            completion_date      TEXT,
            created_at           INTEGER DEFAULT (strftime('%s','now')),
            updated_at           INTEGER DEFAULT (strftime('%s','now'))
        );
        CREATE TABLE IF NOT EXISTS remediation_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            measure_id  INTEGER NOT NULL REFERENCES corrective_measures(id) ON DELETE CASCADE,
            note        TEXT    NOT NULL,
            author_id   INTEGER REFERENCES users(id),
            created_at  INTEGER DEFAULT (strftime('%s','now'))
        );
        """)
        if ADMIN_EMAIL:
            await db.execute(
                "UPDATE users SET is_admin=1, role='auditor' WHERE email=?",
                (ADMIN_EMAIL,)
            )
        await db.commit()

# ── Lifespan ────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="ODITO", lifespan=lifespan)

# ── Auth helpers ────────────────────────────────────────────
async def get_current_user(vc_token: Optional[str] = Cookie(default=None)):
    if not vc_token:
        return None
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT u.* FROM sessions s JOIN users u ON s.user_id=u.id WHERE s.token=?",
            (vc_token,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

async def require_auth(vc_token: Optional[str] = Cookie(default=None)):
    user = await get_current_user(vc_token)
    if not user:
        raise HTTPException(401, "Non autenticato")
    return user

async def require_auditor(user=Depends(require_auth)):
    if user.get("role") not in ("auditor",) and not user.get("is_admin"):
        raise HTTPException(403, "Richiesto ruolo Auditor")
    return user

async def require_admin(user=Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(403, "Richiesto ruolo Admin")
    return user

# ── Static & pages ──────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

def page(name: str):
    path = os.path.join("static", name)
    with open(path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/", response_class=HTMLResponse)
async def root(): return page("index.html")

@app.get("/login", response_class=HTMLResponse)
async def login_page(): return page("login.html")

@app.get("/register", response_class=HTMLResponse)
async def register_page(): return page("register.html")

@app.get("/audit/new", response_class=HTMLResponse)
async def audit_new_page(): return page("audit-new.html")

@app.get("/audit/{audit_id}", response_class=HTMLResponse)
async def audit_detail_page(audit_id: int): return page("audit-detail.html")

@app.get("/finding/{finding_id}", response_class=HTMLResponse)
async def finding_detail_page(finding_id: int): return page("finding-detail.html")

@app.get("/my-actions", response_class=HTMLResponse)
async def my_actions_page(): return page("my-actions.html")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(): return page("admin.html")

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(): return page("login.html")

# ════════════════════════════════════════════════════════════
# AUTH API
# ════════════════════════════════════════════════════════════
class RegisterReq(BaseModel):
    email: str
    name: str
    password: str

@app.post("/api/auth/register")
async def register(req: RegisterReq):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id FROM users WHERE email=?", (req.email,)) as cur:
            if await cur.fetchone():
                raise HTTPException(400, "Email già registrata")
        await db.execute(
            "INSERT INTO users(email,name,password_hash) VALUES(?,?,?)",
            (req.email.lower().strip(), req.name.strip(), hash_pw(req.password))
        )
        if ADMIN_EMAIL and req.email.lower().strip() == ADMIN_EMAIL.lower():
            await db.execute(
                "UPDATE users SET is_admin=1, role='auditor' WHERE email=?",
                (req.email.lower().strip(),)
            )
        await db.commit()
    return JSONResponse({"ok": True})

class LoginReq(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
async def login(req: LoginReq):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE email=? AND password_hash=?",
            (req.email.lower().strip(), hash_pw(req.password))
        ) as cur:
            user = await cur.fetchone()
        if not user:
            raise HTTPException(401, "Credenziali non valide")
        token = secrets.token_hex(32)
        await db.execute("INSERT INTO sessions(token,user_id) VALUES(?,?)", (token, user["id"]))
        await db.commit()
    resp = JSONResponse({"ok": True})
    resp.set_cookie("vc_token", token, httponly=True, samesite="lax", max_age=86400*30)
    return resp

@app.post("/api/auth/logout")
async def logout(vc_token: Optional[str] = Cookie(default=None)):
    if vc_token:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM sessions WHERE token=?", (vc_token,))
            await db.commit()
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("vc_token")
    return resp

@app.get("/api/auth/me")
async def me(vc_token: Optional[str] = Cookie(default=None)):
    user = await get_current_user(vc_token)
    if not user:
        return JSONResponse({"authenticated": False})
    return JSONResponse({
        "authenticated": True,
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "is_admin": bool(user["is_admin"])
    })

# ════════════════════════════════════════════════════════════
# AUDIT REPORTS API
# ════════════════════════════════════════════════════════════
class AuditReq(BaseModel):
    report_ref: str
    title: str
    audited_entity: Optional[str] = None
    audit_type: Optional[str] = None
    audit_class: Optional[str] = None
    overall_result: Optional[str] = None
    previous_result: Optional[str] = None
    previous_result_date: Optional[str] = None
    issue_date: Optional[str] = None
    sample_period_from: Optional[str] = None
    sample_period_to: Optional[str] = None
    fieldwork_period_from: Optional[str] = None
    fieldwork_period_to: Optional[str] = None
    exit_meeting_date: Optional[str] = None
    exit_meeting_participants: Optional[str] = None
    chief_audit_executive: Optional[str] = None
    audit_team_manager: Optional[str] = None
    audit_team: Optional[str] = None
    background: Optional[str] = None

@app.get("/api/audits")
async def list_audits(user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT a.*, COUNT(f.id) as finding_count
            FROM audit_reports a
            LEFT JOIN findings f ON f.audit_id=a.id
            GROUP BY a.id ORDER BY a.created_at DESC
        """) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/audits")
async def create_audit(req: AuditReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id FROM audit_reports WHERE report_ref=?", (req.report_ref,)) as cur:
            if await cur.fetchone():
                raise HTTPException(400, "Codice report già esistente")
        cur = await db.execute("""
            INSERT INTO audit_reports
                (report_ref,title,audited_entity,audit_type,audit_class,
                 overall_result,previous_result,previous_result_date,issue_date,
                 sample_period_from,sample_period_to,fieldwork_period_from,
                 fieldwork_period_to,exit_meeting_date,exit_meeting_participants,
                 chief_audit_executive,audit_team_manager,audit_team,background,
                 created_by)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (req.report_ref, req.title, req.audited_entity, req.audit_type,
              req.audit_class, req.overall_result, req.previous_result,
              req.previous_result_date, req.issue_date,
              req.sample_period_from, req.sample_period_to,
              req.fieldwork_period_from, req.fieldwork_period_to,
              req.exit_meeting_date, req.exit_meeting_participants,
              req.chief_audit_executive, req.audit_team_manager,
              req.audit_team, req.background, user["id"]))
        await db.commit()
        async with db.execute("SELECT * FROM audit_reports WHERE id=?", (cur.lastrowid,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.get("/api/audits/{audit_id}")
async def get_audit(audit_id: int, user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM audit_reports WHERE id=?", (audit_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(404, "Audit non trovato")
    return JSONResponse(dict(row))

@app.put("/api/audits/{audit_id}")
async def update_audit(audit_id: int, req: AuditReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM audit_reports WHERE report_ref=? AND id!=?",
            (req.report_ref, audit_id)
        ) as cur:
            if await cur.fetchone():
                raise HTTPException(400, "Codice report già esistente")
        await db.execute("""
            UPDATE audit_reports SET
                report_ref=?,title=?,audited_entity=?,audit_type=?,audit_class=?,
                overall_result=?,previous_result=?,previous_result_date=?,issue_date=?,
                sample_period_from=?,sample_period_to=?,fieldwork_period_from=?,
                fieldwork_period_to=?,exit_meeting_date=?,exit_meeting_participants=?,
                chief_audit_executive=?,audit_team_manager=?,audit_team=?,background=?,
                updated_at=strftime('%s','now')
            WHERE id=?
        """, (req.report_ref, req.title, req.audited_entity, req.audit_type,
              req.audit_class, req.overall_result, req.previous_result,
              req.previous_result_date, req.issue_date,
              req.sample_period_from, req.sample_period_to,
              req.fieldwork_period_from, req.fieldwork_period_to,
              req.exit_meeting_date, req.exit_meeting_participants,
              req.chief_audit_executive, req.audit_team_manager,
              req.audit_team, req.background, audit_id))
        await db.commit()
        async with db.execute("SELECT * FROM audit_reports WHERE id=?", (audit_id,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.delete("/api/audits/{audit_id}")
async def delete_audit(audit_id: int, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM audit_reports WHERE id=?", (audit_id,))
        await db.commit()
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
# FINDINGS API
# ════════════════════════════════════════════════════════════
class FindingReq(BaseModel):
    audit_id: int
    finding_ref: Optional[str] = None
    title: str
    priority: int = 3
    description: Optional[str] = None
    article_ref: Optional[str] = None
    root_cause: Optional[str] = None
    recommendation: Optional[str] = None

@app.get("/api/findings")
async def list_findings(audit_id: int = Query(...), user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT f.*,
                   COUNT(m.id) as total_measures_count,
                   SUM(CASE WHEN m.status != 'completed' THEN 1 ELSE 0 END) as open_measures_count,
                   a.report_ref
            FROM findings f
            LEFT JOIN corrective_measures m ON m.finding_id=f.id
            LEFT JOIN audit_reports a ON a.id=f.audit_id
            WHERE f.audit_id=?
            GROUP BY f.id
            ORDER BY f.priority ASC, f.created_at ASC
        """, (audit_id,)) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/findings")
async def create_finding(req: FindingReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("""
            INSERT INTO findings
                (audit_id,finding_ref,title,priority,description,
                 article_ref,root_cause,recommendation)
            VALUES(?,?,?,?,?,?,?,?)
        """, (req.audit_id, req.finding_ref, req.title, req.priority,
              req.description, req.article_ref, req.root_cause, req.recommendation))
        await db.commit()
        async with db.execute("""
            SELECT f.*, a.report_ref FROM findings f
            LEFT JOIN audit_reports a ON a.id=f.audit_id
            WHERE f.id=?
        """, (cur.lastrowid,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.get("/api/findings/{finding_id}")
async def get_finding(finding_id: int, user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT f.*, a.report_ref FROM findings f
            LEFT JOIN audit_reports a ON a.id=f.audit_id
            WHERE f.id=?
        """, (finding_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(404, "Finding non trovato")
    return JSONResponse(dict(row))

@app.put("/api/findings/{finding_id}")
async def update_finding(finding_id: int, req: FindingReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            UPDATE findings SET
                finding_ref=?, title=?, priority=?, description=?,
                article_ref=?, root_cause=?, recommendation=?,
                updated_at=strftime('%s','now')
            WHERE id=?
        """, (req.finding_ref, req.title, req.priority, req.description,
              req.article_ref, req.root_cause, req.recommendation, finding_id))
        await db.commit()
        async with db.execute("""
            SELECT f.*, a.report_ref FROM findings f
            LEFT JOIN audit_reports a ON a.id=f.audit_id
            WHERE f.id=?
        """, (finding_id,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.delete("/api/findings/{finding_id}")
async def delete_finding(finding_id: int, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM findings WHERE id=?", (finding_id,))
        await db.commit()
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
# CORRECTIVE MEASURES API
# ════════════════════════════════════════════════════════════
class MeasureReq(BaseModel):
    finding_id: int
    description: str
    action_owner_name: Optional[str] = None
    action_owner_user_id: Optional[int] = None
    deadline: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None

class MeasureStatusReq(BaseModel):
    status: str

@app.get("/api/measures")
async def list_measures(finding_id: int = Query(...), user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT m.*,
                   u.name as owner_user_name,
                   COUNT(l.id) as log_count,
                   f.finding_ref, f.title as finding_title, f.priority,
                   a.report_ref
            FROM corrective_measures m
            LEFT JOIN users u ON u.id=m.action_owner_user_id
            LEFT JOIN remediation_logs l ON l.measure_id=m.id
            LEFT JOIN findings f ON f.id=m.finding_id
            LEFT JOIN audit_reports a ON a.id=f.audit_id
            WHERE m.finding_id=?
            GROUP BY m.id
            ORDER BY m.deadline ASC NULLS LAST, m.created_at ASC
        """, (finding_id,)) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/measures")
async def create_measure(req: MeasureReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("""
            INSERT INTO corrective_measures
                (finding_id,description,action_owner_name,
                 action_owner_user_id,deadline,status,notes)
            VALUES(?,?,?,?,?,?,?)
        """, (req.finding_id, req.description, req.action_owner_name,
              req.action_owner_user_id, req.deadline, req.status, req.notes))
        await db.commit()
        async with db.execute("""
            SELECT m.*, u.name as owner_user_name, 0 as log_count
            FROM corrective_measures m
            LEFT JOIN users u ON u.id=m.action_owner_user_id
            WHERE m.id=?
        """, (cur.lastrowid,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.put("/api/measures/{measure_id}")
async def update_measure(measure_id: int, req: MeasureReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            UPDATE corrective_measures SET
                description=?, action_owner_name=?,
                action_owner_user_id=?, deadline=?, status=?, notes=?,
                updated_at=strftime('%s','now')
            WHERE id=?
        """, (req.description, req.action_owner_name, req.action_owner_user_id,
              req.deadline, req.status, req.notes, measure_id))
        await db.commit()
        async with db.execute("""
            SELECT m.*, u.name as owner_user_name
            FROM corrective_measures m
            LEFT JOIN users u ON u.id=m.action_owner_user_id
            WHERE m.id=?
        """, (measure_id,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

@app.delete("/api/measures/{measure_id}")
async def delete_measure(measure_id: int, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM corrective_measures WHERE id=?", (measure_id,))
        await db.commit()
    return JSONResponse({"ok": True})

async def _update_measure_status(measure_id: int, status: str, user: dict):
    valid = {"pending", "in_progress", "completed"}
    if status not in valid:
        raise HTTPException(400, "Status non valido")
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM corrective_measures WHERE id=?", (measure_id,)) as cur:
            m = await cur.fetchone()
        if not m:
            raise HTTPException(404, "Misura non trovata")
        # Solo auditor/admin possono aggiornare misure altrui
        if (user.get("role") not in ("auditor",) and not user.get("is_admin")
                and m["action_owner_user_id"] != user["id"]):
            raise HTTPException(403, "Non autorizzato")
        completion = date.today().isoformat() if status == "completed" else None
        await db.execute("""
            UPDATE corrective_measures
            SET status=?, completion_date=?, updated_at=strftime('%s','now')
            WHERE id=?
        """, (status, completion, measure_id))
        # Auto-close finding if all measures completed
        async with db.execute("""
            SELECT COUNT(*) as tot,
                   SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as done
            FROM corrective_measures WHERE finding_id=?
        """, (m["finding_id"],)) as cur2:
            counts = await cur2.fetchone()
        new_finding_status = (
            "closed" if counts["tot"] > 0 and counts["tot"] == counts["done"]
            else "open"
        )
        await db.execute(
            "UPDATE findings SET status=?,updated_at=strftime('%s','now') WHERE id=?",
            (new_finding_status, m["finding_id"])
        )
        await db.commit()
    return JSONResponse({"ok": True, "status": status})

@app.post("/api/measures/{measure_id}/status")
async def update_measure_status_post(measure_id: int, req: MeasureStatusReq, user=Depends(require_auth)):
    return await _update_measure_status(measure_id, req.status, user)

@app.patch("/api/measures/{measure_id}/status")
async def update_measure_status_patch(measure_id: int, req: MeasureStatusReq, user=Depends(require_auth)):
    return await _update_measure_status(measure_id, req.status, user)

# ════════════════════════════════════════════════════════════
# REMEDIATION LOGS API
# ════════════════════════════════════════════════════════════
class LogReq(BaseModel):
    note: str

@app.get("/api/measures/{measure_id}/logs")
async def get_logs(measure_id: int, user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT l.*, u.name as author_name
            FROM remediation_logs l
            LEFT JOIN users u ON u.id=l.author_id
            WHERE l.measure_id=?
            ORDER BY l.created_at ASC
        """, (measure_id,)) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/measures/{measure_id}/logs")
async def add_log(measure_id: int, req: LogReq, user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id FROM corrective_measures WHERE id=?", (measure_id,)) as cur:
            if not await cur.fetchone():
                raise HTTPException(404, "Misura non trovata")
        cur2 = await db.execute(
            "INSERT INTO remediation_logs(measure_id,note,author_id) VALUES(?,?,?)",
            (measure_id, req.note, user["id"])
        )
        await db.commit()
        async with db.execute("""
            SELECT l.*, u.name as author_name FROM remediation_logs l
            LEFT JOIN users u ON u.id=l.author_id WHERE l.id=?
        """, (cur2.lastrowid,)) as c:
            row = await c.fetchone()
    return JSONResponse(dict(row))

# ════════════════════════════════════════════════════════════
# MY ACTIONS (Action Owner view)
# ════════════════════════════════════════════════════════════
@app.get("/api/my-actions")
async def my_actions(user=Depends(require_auth)):
    uid = user["id"]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT m.*,
                   f.title as finding_title, f.priority,
                   f.finding_ref,
                   a.report_ref, a.title as audit_title, a.id as audit_id
            FROM corrective_measures m
            JOIN findings f ON f.id=m.finding_id
            JOIN audit_reports a ON a.id=f.audit_id
            WHERE m.action_owner_user_id=?
            ORDER BY
                CASE m.status WHEN 'completed' THEN 1 ELSE 0 END ASC,
                m.deadline ASC NULLS LAST
        """, (uid,)) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

# ════════════════════════════════════════════════════════════
# DASHBOARD STATS
# ════════════════════════════════════════════════════════════
@app.get("/api/dashboard")
async def dashboard(user=Depends(require_auth)):
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT COUNT(*) as n FROM audit_reports") as c:
            total_audits = (await c.fetchone())["n"]
        async with db.execute("SELECT COUNT(*) as n FROM audit_reports WHERE status='open'") as c:
            open_audits = (await c.fetchone())["n"]
        async with db.execute("SELECT COUNT(*) as n FROM findings WHERE status='open'") as c:
            open_findings = (await c.fetchone())["n"]
        async with db.execute("""
            SELECT COUNT(*) as n FROM corrective_measures
            WHERE status NOT IN ('completed') AND deadline < ?
        """, (today,)) as c:
            overdue = (await c.fetchone())["n"]
        async with db.execute("""
            SELECT COUNT(*) as n FROM corrective_measures WHERE status='completed'
        """) as c:
            completed = (await c.fetchone())["n"]
        async with db.execute("""
            SELECT priority, COUNT(*) as n FROM findings
            WHERE status='open' GROUP BY priority ORDER BY priority
        """) as c:
            by_priority = {r["priority"]: r["n"] for r in await c.fetchall()}
        async with db.execute("""
            SELECT a.*, COUNT(f.id) as finding_count
            FROM audit_reports a
            LEFT JOIN findings f ON f.audit_id=a.id
            GROUP BY a.id ORDER BY a.created_at DESC LIMIT 5
        """) as c:
            recent = [dict(r) for r in await c.fetchall()]
        async with db.execute("""
            SELECT m.*, f.title as description_finding, f.priority,
                   f.finding_ref,
                   a.report_ref, a.title as audit_title,
                   u.name as action_owner_name
            FROM corrective_measures m
            JOIN findings f ON f.id=m.finding_id
            JOIN audit_reports a ON a.id=f.audit_id
            LEFT JOIN users u ON u.id=m.action_owner_user_id
            WHERE m.status NOT IN ('completed') AND m.deadline IS NOT NULL
            ORDER BY m.deadline ASC LIMIT 8
        """) as c:
            deadlines_raw = [dict(r) for r in await c.fetchall()]
    # Enrich deadlines with owner name fallback
    deadlines = []
    for d in deadlines_raw:
        d["action_owner_name"] = d.get("action_owner_name") or d.get("action_owner_name")
        deadlines.append(d)
    return JSONResponse({
        "total_audits": total_audits,
        "open_audits": open_audits,
        "open_findings": open_findings,
        "overdue_measures": overdue,
        "completed_measures": completed,
        "findings_by_priority": by_priority,
        "recent_audits": recent,
        "upcoming_deadlines": deadlines
    })

# ════════════════════════════════════════════════════════════
# ADMIN API
# ════════════════════════════════════════════════════════════
@app.get("/api/admin/users")
async def admin_users(user=Depends(require_admin)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id,email,name,role,is_admin,created_at FROM users ORDER BY created_at"
        ) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.delete("/api/admin/users/{uid}")
async def admin_delete_user(uid: int, user=Depends(require_admin)):
    if uid == user["id"]:
        raise HTTPException(400, "Non puoi eliminare te stesso")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM users WHERE id=?", (uid,))
        await db.commit()
    return JSONResponse({"ok": True})

class SetRoleReq(BaseModel):
    role: str
    is_admin: bool = False

@app.post("/api/admin/users/{uid}/set-role")
@app.patch("/api/admin/users/{uid}/role")
async def admin_set_role(uid: int, req: SetRoleReq, user=Depends(require_admin)):
    if req.role not in ("auditor", "operational", "admin"):
        raise HTTPException(400, "Ruolo non valido")
    is_admin = 1 if (req.role == "admin" or req.is_admin) else 0
    role = "auditor" if req.role == "admin" else req.role
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET role=?, is_admin=? WHERE id=?",
            (role, is_admin, uid)
        )
        await db.commit()
    return JSONResponse({"ok": True})

class SetPwReq(BaseModel):
    password: str

@app.post("/api/admin/users/{uid}/set-password")
@app.patch("/api/admin/users/{uid}/password")
async def admin_set_password(uid: int, req: SetPwReq, user=Depends(require_admin)):
    if len(req.password) < 4:
        raise HTTPException(400, "Password troppo corta")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (hash_pw(req.password), uid)
        )
        await db.commit()
    return JSONResponse({"ok": True})

# ════════════════════════════════════════════════════════════
# USERS LIST (per assegnare action owner)
# ════════════════════════════════════════════════════════════
@app.get("/api/users")
async def list_users(user=Depends(require_auth)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id,name,email,role FROM users ORDER BY name"
        ) as cur:
            rows = await cur.fetchall()
    return JSONResponse([dict(r) for r in rows])

# ════════════════════════════════════════════════════════════
# PDF → AI IMPORT
# ════════════════════════════════════════════════════════════
PDF_PROMPT = """Sei un esperto di report di audit regolatorio. Analizza il testo del report che ti fornisco ed estrai le informazioni strutturate.

Restituisci SOLO un oggetto JSON con questa struttura (usa null per i campi non trovati):

{
  "audit": {
    "report_ref": "codice report es. 2025-NPG-003",
    "title": "titolo completo del report",
    "audited_entity": "nome entità auditata",
    "audit_type": "tipo audit es. Planned Standard Audit",
    "audit_class": "classe audit es. Legal Entity Audit",
    "overall_result": "uno tra: Good, Satisfactory, Unsatisfactory, Poor",
    "previous_result": "giudizio audit precedente",
    "previous_result_date": "YYYY-MM-DD o null",
    "issue_date": "YYYY-MM-DD o null",
    "sample_period_from": "YYYY-MM-DD o null",
    "sample_period_to": "YYYY-MM-DD o null",
    "fieldwork_period_from": "YYYY-MM-DD o null",
    "fieldwork_period_to": "YYYY-MM-DD o null",
    "exit_meeting_date": "YYYY-MM-DD o null",
    "exit_meeting_participants": "stringa con nomi e ruoli",
    "chief_audit_executive": "nome CAE",
    "audit_team_manager": "nome team manager",
    "audit_team": "nomi separati da virgola",
    "background": "testo completo del background/scope/executive summary"
  },
  "findings": [
    {
      "finding_ref": "es. NC-001 o Finding 1",
      "title": "titolo breve della non conformità",
      "priority": 1,
      "description": "descrizione completa della non conformità",
      "article_ref": "riferimento normativo es. DORA Art. 9.4",
      "root_cause": "analisi della causa radice",
      "recommendation": "azione raccomandata"
    }
  ]
}

Per la priorità usa: 1=High/Critical, 2=Relevant/Important, 3=Medium/Moderate, 4=Low/Minor.
Per le date converte qualsiasi formato in YYYY-MM-DD.
Per i findings estrai TUTTE le non conformità, finding, osservazioni presenti nel report.
"""

@app.get("/api/audits/check-openai")
async def check_openai(user=Depends(require_auditor)):
    return JSONResponse({"configured": bool(OPENAI_API_KEY), "model": OPENAI_MODEL})

@app.post("/api/audits/extract-pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    openai_key: Optional[str] = Form(default=None),
    user=Depends(require_auditor)
):
    api_key = openai_key or OPENAI_API_KEY
    if not api_key:
        raise HTTPException(400, "OpenAI API key non configurata. Impostare OPENAI_API_KEY o fornirla nel form.")

    # Leggi PDF ed estrai testo
    content = await file.read()
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n\n"
    except Exception as e:
        raise HTTPException(400, f"Errore lettura PDF: {e}")

    if not text.strip():
        raise HTTPException(400, "Impossibile estrarre testo dal PDF. Il file potrebbe essere scansionato o protetto.")

    # Tronca se troppo lungo (GPT-4o: 128k token ≈ ~500k chars, ma limitiamo a 80k per sicurezza)
    MAX_CHARS = 80000
    truncated = len(text) > MAX_CHARS
    if truncated:
        text = text[:MAX_CHARS] + "\n\n[... documento troncato per dimensioni ...]"

    # Chiama OpenAI
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PDF_PROMPT},
                {"role": "user",   "content": f"Testo del report di audit:\n\n{text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=4096
        )
    except Exception as e:
        raise HTTPException(500, f"Errore OpenAI: {e}")

    try:
        result = jsonlib.loads(response.choices[0].message.content)
    except Exception:
        raise HTTPException(500, "La risposta AI non è JSON valido")

    result["_truncated"] = truncated
    result["_pages"] = len(content) // 2048  # stima pagine
    return JSONResponse(result)


class ImportFinding(BaseModel):
    finding_ref: Optional[str] = None
    title: str
    priority: int = 3
    description: Optional[str] = None
    article_ref: Optional[str] = None
    root_cause: Optional[str] = None
    recommendation: Optional[str] = None

class ImportFullReq(BaseModel):
    audit: AuditReq
    findings: List[ImportFinding] = []

@app.post("/api/audits/import-full")
async def import_full(req: ImportFullReq, user=Depends(require_auditor)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM audit_reports WHERE report_ref=?", (req.audit.report_ref,)
        ) as cur:
            if await cur.fetchone():
                raise HTTPException(400, "Codice report già esistente")
        # Crea audit
        cur = await db.execute("""
            INSERT INTO audit_reports
                (report_ref,title,audited_entity,audit_type,audit_class,
                 overall_result,previous_result,previous_result_date,issue_date,
                 sample_period_from,sample_period_to,fieldwork_period_from,
                 fieldwork_period_to,exit_meeting_date,exit_meeting_participants,
                 chief_audit_executive,audit_team_manager,audit_team,background,
                 created_by)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (req.audit.report_ref, req.audit.title, req.audit.audited_entity,
              req.audit.audit_type, req.audit.audit_class, req.audit.overall_result,
              req.audit.previous_result, req.audit.previous_result_date, req.audit.issue_date,
              req.audit.sample_period_from, req.audit.sample_period_to,
              req.audit.fieldwork_period_from, req.audit.fieldwork_period_to,
              req.audit.exit_meeting_date, req.audit.exit_meeting_participants,
              req.audit.chief_audit_executive, req.audit.audit_team_manager,
              req.audit.audit_team, req.audit.background, user["id"]))
        audit_id = cur.lastrowid
        # Crea findings
        for f in req.findings:
            await db.execute("""
                INSERT INTO findings
                    (audit_id,finding_ref,title,priority,description,
                     article_ref,root_cause,recommendation)
                VALUES(?,?,?,?,?,?,?,?)
            """, (audit_id, f.finding_ref, f.title, f.priority,
                  f.description, f.article_ref, f.root_cause, f.recommendation))
        await db.commit()
    return JSONResponse({"id": audit_id, "findings_created": len(req.findings)})


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)

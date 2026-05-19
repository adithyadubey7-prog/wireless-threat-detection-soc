from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from fastapi import Request

from fastapi import FastAPI

from app.api.routes import router

from app.database.db import (
    insert_scan_history
)

from app.services.background_scanner import (
    start_background_scanner
)

from app.scanner.wifi_scanner import (
    scan_wifi_networks
)

from app.scanner.parser import (
    parse_wifi_output
)

from fastapi import WebSocket

from app.services.websocket_manager import (
    manager
)

from app.detection.detector import (
    run_all_detections
)

from app.detection.scorer import (
    enrich_alerts
)

from app.database.db import (
    initialize_database,
    insert_alert
)

initialize_database()
start_background_scanner()

app = FastAPI(
    title="Wireless Threat Detection SOC"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

app.include_router(router)

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except:

        manager.disconnect(
            websocket
        )

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

@app.get("/scan")
def run_scan():

    raw_output = scan_wifi_networks()

    parsed_networks = parse_wifi_output(
        raw_output
    )

    alerts = run_all_detections(
        parsed_networks
    )

    alerts = enrich_alerts(
        alerts
    )

   

    return {
        "networks_detected": len(
            parsed_networks
        ),
        "alerts_generated": len(alerts),
        "alerts": alerts
    }
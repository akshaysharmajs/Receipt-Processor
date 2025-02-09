from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
from models import Receipt, Points
from uuid import uuid4
from utils import calculate_points
import uvicorn

class CustomJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,  # No extra spaces for indent
            separators=(',', ': ')  # Space after colon for better readability
        ).encode('utf-8')

app = FastAPI()

receipts = {}

@app.post("/receipts/process", response_model=dict, response_class=CustomJSONResponse)
def process_receipt(receipt: Receipt):
    try:
        receipt_id = str(uuid4())
        receipts[receipt_id] = receipt
        return {"id": receipt_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/receipts/{id}/points", response_model=Points, response_class=CustomJSONResponse)
def get_points(id: str):
    if id in receipts:
        points = calculate_points(receipts[id])
        return {"points": points}
    raise HTTPException(status_code=404, detail="Receipt not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

# src/routes/broker_routes.py

from fastapi import APIRouter, HTTPException, Query
from src.services.data_processing import retrieve_and_process_data
from src.services.company_information import companies_data

router = APIRouter()

@router.get("/process")
async def process_data(key: str = Query(...), time: int = Query(...)):
    """
    Process data for a given key and time.
    """
    try:
        results = await retrieve_and_process_data(key, time)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/companies_data")
async def business_data(key: str = Query(...), time: int = Query(...)):
    """
    Process companies data for a given time.
    """
    try:
        results = await companies_data(key, time)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/video")
async def video(time : int = Query(...)):
    """
    Get the video link.
    """
    content = {
        1: "https://www.youtube.com/watch?v=pzRxqx6uXks",
        2: "https://www.youtube.com/watch?v=XcJt1xey84o",
        3: "https://www.youtube.com/watch?v=IGCIX3kLzLw",
    }
    return content[time]
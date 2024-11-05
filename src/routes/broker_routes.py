# src/routes/broker_routes.py

from fastapi import APIRouter, HTTPException, Query
from src.services.data_processing import retrieve_and_process_data
from src.services.changes_company_shares import changes_shares
from src.services.company_information import companies_data

router = APIRouter()

@router.get("/process")
async def process_data(key: str = Query(...), time: int = Query(...)):
    """
    Process data for a given key and time.
    """
    try:
        results = retrieve_and_process_data(key, time)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/companies_shares")
async def business_data(time: int = Query(...)):
    """
    Process companies data for a given time.
    """
    try:
        results = changes_shares(time)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/companies_data")
async def business_data():
    """
    Process companies data for a given time.
    """
    try:
        results = companies_data()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/video")
async def video(time : int = Query(...)):
    """
    Get the video link.
    """
    content = {
        1: "https://www.youtube.com/watch?v=1",
        2: "https://www.youtube.com/watch?v=2",
        3: "https://www.youtube.com/watch?v=3",
    }
    return content[time]
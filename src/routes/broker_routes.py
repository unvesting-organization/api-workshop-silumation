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
        1: '<iframe width="1081" height="556" src="https://www.youtube.com/embed/IGCIX3kLzLw" title="Así se prepara el auténtico Sushi en Japón🇯🇵 | La Capital" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        2: '<iframe width="1081" height="556" src="https://www.youtube.com/embed/XcJt1xey84o" title="La Picaña Rellena | La Capital" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        3: '<iframe width="1081" height="556" src="https://www.youtube.com/embed/pzRxqx6uXks" title="Estrenando mi Nuevo Asador con Picañas | La Capital" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
    }
    return content[time]
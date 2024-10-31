import logging
from fastapi import FastAPI, HTTPException, Request
from database import create_coupon, get_coupon, get_all_coupons, update_coupon_usage_records
from schemas import CouponCreate, CouponRequest, Coupon, ApplyCouponRequest
from typing import List
from operations import apply_coupon, validate_coupon

# Set up the logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CouponAPI")

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response

@app.post("/coupons/", response_model=Coupon)
def create_coupon_route(coupon: CouponCreate):
    coupon_dict = coupon.model_dump()
    coupon_dict["usage_records"] = {
        "global_count": coupon_dict['global_total_repeat_count'],
        "user_usage": {}
    }
    try:
        created_coupon = create_coupon(coupon_dict)
        logger.info(f"Coupon created: {coupon_dict['coupon_code']}")
        return created_coupon
    except Exception as e:
        logger.error(f"Error creating coupon: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coupons/get", response_model=Coupon)
def read_coupon_route(coupon_request: CouponRequest):
    coupon_code = coupon_request.coupon_code
    coupon = get_coupon(coupon_code)
    if coupon is None:
        logger.warning(f"Coupon not found: {coupon_code}")
        raise HTTPException(status_code=404, detail="Coupon not found")
    logger.info(f"Coupon retrieved: {coupon_code}")
    return coupon

@app.get("/coupons/", response_model=List[Coupon])
def get_coupons_route():
    try:
        coupons = get_all_coupons()
        logger.info("Retrieved all coupons.")
        return coupons
    except Exception as e:
        logger.error(f"Error retrieving coupons: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coupons/validate")
def validate_coupon_route(request: ApplyCouponRequest):
    coupon = get_coupon(request.coupon_code)
    
    if not coupon:
        logger.warning(f"Coupon validation failed, not found: {request.coupon_code}")
        raise HTTPException(status_code=404, detail="Coupon not found")

    validate_coupon(coupon, request.user_id)
    logger.info(f"Coupon validated for user {request.user_id}: {request.coupon_code}")
    return {"message": "Coupon is valid for the user."}

@app.post("/coupons/apply", response_model=Coupon)
def apply_coupon_route(apply_coupon_request: ApplyCouponRequest):
    coupon_code = apply_coupon_request.coupon_code
    user_id = apply_coupon_request.user_id

    coupon = get_coupon(coupon_code)
    if coupon is None:
        logger.warning(f"Coupon application failed, not found: {coupon_code}")
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    if validate_coupon(coupon=coupon, user_id=user_id):
        updated_coupon = apply_coupon(coupon, user_id)  
        update_coupon_usage_records(updated_coupon)
        logger.info(f"Coupon applied for user {user_id}: {coupon_code}")
    return updated_coupon

from fastapi import FastAPI, HTTPException
from database import create_coupon, get_coupon, get_all_coupons, update_coupon_usage_records
from schemas import CouponCreate, CouponRequest, Coupon, ApplyCouponRequest
from typing import List
from operations import apply_coupon, validate_coupon

app = FastAPI()

@app.post("/coupons/", response_model=Coupon)
def create_coupon_route(coupon: CouponCreate):
    coupon_dict = coupon.model_dump()
    coupon_dict["usage_records"]= {
        "global_count": coupon_dict['global_total_repeat_count'],
        "user_usage": {}
    }
    try:
        return create_coupon(coupon_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coupons/get", response_model=Coupon)
def read_coupon_route(coupon_request: CouponRequest):
    coupon_code = coupon_request.coupon_code
    coupon = get_coupon(coupon_code)
    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

@app.get("/coupons/", response_model=List[Coupon])
def get_coupons_route():
    try:
        return get_all_coupons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coupons/validate")
def validate_coupon_route(request: ApplyCouponRequest):
    coupon = get_coupon(request.coupon_code)
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    validate_coupon(coupon, request.user_id)

    return {"message": "Coupon is valid for the user."}

@app.post("/coupons/apply", response_model=Coupon)
def apply_coupon_route(apply_coupon_request: ApplyCouponRequest):
    coupon_code = apply_coupon_request.coupon_code
    user_id = apply_coupon_request.user_id

    coupon = get_coupon(coupon_code)
    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if(validate_coupon(coupon=coupon,user_id=user_id)):
        updated_coupon = apply_coupon(coupon, user_id)  
        update_coupon_usage_records(updated_coupon)
    return updated_coupon

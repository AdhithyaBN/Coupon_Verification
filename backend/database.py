from pymongo import MongoClient
import mongomock
from datetime import datetime
from schemas import Coupon
from typing import List


client = mongomock.MongoClient()
db = client["mydatabase"]
collection = db["coupons"]

def create_coupon(coupon):
    if coupon["global_total_repeat_count"]<coupon["user_total_repeat_count"] \
    or coupon["global_total_repeat_count"]<coupon["user_daily_repeat_count"] or \
    coupon["global_total_repeat_count"]<coupon["user_weekly_repeat_count"]:
        raise ValueError("Global total count shouldnt be less than per user count in any form.")
    if coupon["user_total_repeat_count"]<coupon["user_weekly_repeat_count"] or\
    coupon["user_total_repeat_count"]<coupon["user_daily_repeat_count"]:
        raise ValueError("User total repeat count shouldnt be less than user daily and weekly repeat count")
    if coupon["user_weekly_repeat_count"]<coupon["user_daily_repeat_count"]:
        raise ValueError("User weekly repeat count shouldnt be less than user daily repeat count")

    if collection.find_one({"coupon_code": coupon["coupon_code"]}):
        raise ValueError("Coupon code must be unique.")
    
    result = collection.insert_one(coupon)
    coupon["id"] = str(result.inserted_id)
    return coupon

def get_coupon(coupon_code):
    coupon = collection.find_one({"coupon_code": coupon_code})

    return coupon
def get_all_coupons() -> List[Coupon]:
    coupons = list(collection.find())  
    return coupons
def update_coupon_usage_records(coupon:Coupon):
    collection.update_one(
        {"coupon_code": coupon["coupon_code"]}, 
        {"$set": {"usage_records": coupon['usage_records']}}
    )

def update_coupon_usage_in_db(coupon: dict):
    result = collection.update_one(
        {"coupon_code": coupon["coupon_code"]}, 
        {"$set": coupon}  
    )
    if result.modified_count == 0:
        raise ValueError("Coupon update failed; coupon may not exist.")
    return coupon

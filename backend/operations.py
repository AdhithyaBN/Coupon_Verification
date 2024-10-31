from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from schemas import Coupon, UserDay, UserUsage, UserWeek
from database import update_coupon_usage_records, update_coupon_usage_in_db
from fastapi import HTTPException

def get_start_of_week(now: datetime) -> datetime:
    start_of_week = now - timedelta(days=now.weekday() + 1)  
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

def get_start_of_day(now: datetime) -> datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)
def validate_coupon(coupon: dict, user_id: str) -> bool:
    total_usage = coupon['usage_records']['global_count']
    user_usage = coupon['usage_records']['user_usage'].get(user_id)
    reset_flag = False

    if total_usage <= 0:
        raise HTTPException(status_code=400, detail="Global usage expired")

    if user_usage:
        now = datetime.now()

        if user_usage['user_total'] <= 0:
            raise HTTPException(status_code=400, detail="User total usage expired")

        if user_usage['user_week']['count'] <= 0:
            week_start = user_usage['user_week']['week_start']
            if now >= week_start + timedelta(weeks=1):
                user_usage['user_week']['count'] = coupon['user_weekly_repeat_count']
                user_usage['user_week']['week_start'] = get_start_of_week(now)
                reset_flag = True
            else:
                raise HTTPException(status_code=400, detail="User weekly usage expired")

        if user_usage['user_day']['count'] <= 0:
            day_start = user_usage['user_day']['day']
            if now.date() > day_start.date():
                user_usage['user_day']['count'] = coupon['user_daily_repeat_count']
                user_usage['user_day']['day'] = get_start_of_day(now)
                reset_flag = True
            else:
                raise HTTPException(status_code=400, detail="User daily usage expired")

    if reset_flag:
        update_coupon_usage_in_db(coupon)

    return True
    
def apply_coupon(coupon: Dict[str, Any], user_id: str) -> Dict[str, Any]:


    coupon['usage_records']['global_count'] -= 1  

    user_usage = coupon['usage_records']['user_usage'].get(user_id)
    
    if user_usage is None:
        user_usage = {
            "user_total": coupon["user_total_repeat_count"]-1,
            "user_week": {
                "count": coupon["user_weekly_repeat_count"]-1,
                "week_start": get_start_of_week(datetime.now())  
            },
            "user_day": {
                "count": coupon["user_daily_repeat_count"]-1,
                "day": get_start_of_day(datetime.now())  
            }
        }
        coupon['usage_records']['user_usage'][user_id] = user_usage
    else:
        user_usage['user_total'] -= 1
        user_usage['user_week']['count'] -= 1
        user_usage['user_day']['count'] -= 1
        

    return coupon  

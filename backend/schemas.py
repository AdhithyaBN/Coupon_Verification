from pydantic import BaseModel, Field
from typing import Dict, List, Annotated, Optional
from datetime import datetime

class UserWeek(BaseModel):
    count: int
    week_start: Optional[datetime] = None 

class UserDay(BaseModel):
    count: int
    day: Optional[datetime] =None 
class UserUsage(BaseModel):
    user_total: int
    user_week: UserWeek
    user_day: UserDay

class TotalUsage(BaseModel):
    user_usage: Dict[str, UserUsage]  
    global_count: int

class CouponCreate(BaseModel):
    coupon_code: str = Field(..., max_length=50)  
    global_total_repeat_count: Annotated[int, Field(strict=True, gt=0)] = Field(default=1)  
    user_total_repeat_count: Annotated[int, Field(strict=True, gt=0)] = Field(default=1) 
    user_weekly_repeat_count: Annotated[int, Field(strict=True, gt=0)] = Field(default=1) 
    user_daily_repeat_count: Annotated[int, Field(strict=True, gt=0)] = Field(default=1)  

class CouponRequest(BaseModel):
    coupon_code: str 

class Coupon(BaseModel):
    coupon_code: str
    global_total_repeat_count: int
    user_total_repeat_count: int
    user_weekly_repeat_count: int
    user_daily_repeat_count: int
    usage_records: TotalUsage

class ApplyCouponRequest(BaseModel):
    user_id: str
    coupon_code: str

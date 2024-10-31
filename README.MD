Application setup:
run setup.bat to set the environment
run run_app.bat to run the application

use either the postman collection or the curl batch file in the testing folder to check the tests written so far.  




Assumptions
Authentication: 
The user_id provided in each request is assumed to represent an authenticated and authorized user. This API does not handle authentication; it solely relies on the input user_id for tracking usage.

Time Cycle Definitions:
Weekly Cycle: Weeks are defined to start on Sunday at 12:00 AM.
Daily Cycle: Each day starts at 12:00 AM.

Bookkeeping:
The service tracks both weekly and daily limits for each user in addition to the global count for all users. This ensures accurate enforcement of limits and can be scaled based on more time-based limits if needed.


API Endpoints

Create Coupon:
Endpoint: POST /coupons/
Description: Creates a new coupon with specified repeat counts, including global and per-user limits.
Input: Coupon code, global_total_repeat_count, user_total_repeat_count, user_weekly_repeat_count, user_daily_repeat_count.
Validations:
The global_total_repeat_count must not be less than any per-user count.
user_total_repeat_count must be at least as large as both weekly and daily counts.
user_weekly_repeat_count should not be less than user_daily_repeat_count.

Get Coupon Details:
Endpoint: POST /coupons/get
Description: Retrieves the details of a coupon given its coupon code.

Validate Coupon:
Endpoint: POST /coupons/validate
Description: Validates a coupon for a user based on the configured repeat counts.
Input: user_id and coupon_code.
Behavior: Checks global, daily, and weekly limits, rejecting if any limit is exceeded.

Apply Coupon:
Endpoint: POST /coupons/apply
Description: Applies a coupon for a user, reducing repeat counts as applicable.
Input: user_id and coupon_code.
Behavior: Updates counts based on the daily and weekly limits for each user, as well as the global count for all users.


the current test cases check the addition of new coupons, validation of existing coupons, application of coupons.  
All of these for the happy flows, and we ensure that the coupon validity expiry is also verified

given enough time, the next test cases that would be written are to simulate date and week changes to also verify the case where the coupon counts reset.
even with the coupon repeats for day and week repeating, it will expire as required because the total count will keep track of the same.
@echo off
echo ===========================
echo      COUPON API TESTS
echo ===========================

echo.
echo --- Initializing API tests on Port 8080 ---
echo.

REM ---------------------------- Test Case 1: Coupon Creation ----------------------------

echo === Test Case 1.1: Successful Coupon Creation ===
echo curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT50\", \"global_total_repeat_count\": 50, \"user_total_repeat_count\": 20, \"user_weekly_repeat_count\": 10, \"user_daily_repeat_count\": 5 }"
curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT50\", \"global_total_repeat_count\": 50, \"user_total_repeat_count\": 20, \"user_weekly_repeat_count\": 10, \"user_daily_repeat_count\": 5 }"
echo.
echo.

echo === Test Case 1.2: Duplicate Coupon Code Creation ===
echo curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT50\", \"global_total_repeat_count\": 50, \"user_total_repeat_count\": 20, \"user_weekly_repeat_count\": 10, \"user_daily_repeat_count\": 5 }"
curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT50\", \"global_total_repeat_count\": 50, \"user_total_repeat_count\": 20, \"user_weekly_repeat_count\": 10, \"user_daily_repeat_count\": 5 }"
echo.
echo.

REM ---------------------------- Test Case 2: Coupon Validation ----------------------------

echo === Test Case 2.1: Valid Coupon for New User ===
echo curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user789\", \"coupon_code\": \"DISCOUNT50\" }"
curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user789\", \"coupon_code\": \"DISCOUNT50\" }"
echo.
echo.

echo === Test Case 2.2: Valid Coupon for Returning User Under Limit ===
echo curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user789\", \"coupon_code\": \"DISCOUNT50\" }"
curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user789\", \"coupon_code\": \"DISCOUNT50\" }"
echo.
echo.

echo === Test Case 2.3: Nonexistent Coupon Validation ===
echo curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user123\", \"coupon_code\": \"INVALID_CODE\" }"
curl -X POST http://127.0.0.1:8080/coupons/validate -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user123\", \"coupon_code\": \"INVALID_CODE\" }"
echo.
echo.

REM ---------------------------- Test Case 3: Coupon Application ----------------------------

echo === Test Case 3.1: First-time Successful Application for New User ===
echo curl -X POST http://127.0.0.1:8080/coupons/apply -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user456\", \"coupon_code\": \"DISCOUNT50\" }"
curl -X POST http://127.0.0.1:8080/coupons/apply -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user456\", \"coupon_code\": \"DISCOUNT50\" }"
echo.
echo.

echo === Test Case 3.2: Exceeding Daily Limit Application for User ===
echo curl -X POST http://127.0.0.1:8080/coupons/apply -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user456\", \"coupon_code\": \"DISCOUNT50\" }"
curl -X POST http://127.0.0.1:8080/coupons/apply -H "Content-Type: application/json" ^
-d "{ \"user_id\": \"user456\", \"coupon_code\": \"DISCOUNT50\" }"
echo.
echo.

REM ---------------------------- Test Case 4: Fetch Coupons ----------------------------

echo === Test Case 4.1: Retrieve All Coupons ===
echo curl -X GET http://127.0.0.1:8080/coupons/
curl -X GET http://127.0.0.1:8080/coupons/
echo.
echo.

REM ---------------------------- Test Case 5: Invalid Inputs ----------------------------

echo === Negative Test Case: Invalid Input Data (Non-Integer for Repeat Counts) ===
echo curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT10\", \"global_total_repeat_count\": \"INVALID\", \"user_total_repeat_count\": 10, \"user_weekly_repeat_count\": 5, \"user_daily_repeat_count\": 2 }"
curl -X POST http://127.0.0.1:8080/coupons/ -H "Content-Type: application/json" ^
-d "{ \"coupon_code\": \"DISCOUNT10\", \"global_total_repeat_count\": \"INVALID\", \"user_total_repeat_count\": 10, \"user_weekly_repeat_count\": 5, \"user_daily_repeat_count\": 2 }"
echo.
echo.

echo ===========================
echo         TESTS COMPLETE
echo ===========================

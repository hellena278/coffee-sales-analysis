# Databricks notebook source
df = spark.read.csv("/Volumes/workspace/default/coffe_sales/coffee_sales.csv", header=True, inferSchema=True)
df.createOrReplaceTempView("coffee_shop_sales")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from coffee_shop_sales

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS coffee_sales_clean AS
# MAGIC SELECT
# MAGIC     transaction_id,
# MAGIC     CAST(transaction_date AS DATE) AS transaction_date,
# MAGIC     DATE_FORMAT(CAST(transaction_time AS TIMESTAMP), 'HH:mm:ss') AS transaction_time,
# MAGIC     transaction_qty,
# MAGIC     store_id,
# MAGIC     store_location,
# MAGIC     product_id,
# MAGIC     CAST(unit_price AS DECIMAL(10,2)) AS unit_price,
# MAGIC     product_category,
# MAGIC     product_type,
# MAGIC     product_detail
# MAGIC FROM coffee_shop_sales
# MAGIC WHERE transaction_id IS NOT NULL
# MAGIC     AND transaction_date IS NOT NULL
# MAGIC     AND transaction_time IS NOT NULL
# MAGIC     AND transaction_qty IS NOT NULL
# MAGIC     AND store_id IS NOT NULL
# MAGIC     AND store_location IS NOT NULL
# MAGIC     AND product_id IS NOT NULL
# MAGIC     AND unit_price IS NOT NULL
# MAGIC     AND product_category IS NOT NULL
# MAGIC     AND product_type IS NOT NULL
# MAGIC     AND product_detail IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM coffee_sales_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE transactions AS 
# MAGIC SELECT
# MAGIC transaction_id,
# MAGIC transaction_date,
# MAGIC transaction_time,
# MAGIC transaction_qty,
# MAGIC store_id,
# MAGIC product_id
# MAGIC FROM coffee_sales_clean
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from transactions

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE products AS
# MAGIC SELECT
# MAGIC product_id,
# MAGIC product_category,
# MAGIC product_type,
# MAGIC product_detail,
# MAGIC unit_price
# MAGIC FROM coffee_sales_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM product

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE stores AS
# MAGIC SELECT
# MAGIC store_id,
# MAGIC store_location
# MAGIC FROM coffee_sales_clean
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM stores

# COMMAND ----------

# MAGIC %sql
# MAGIC -- MAVEN ROASTER SALES TRENDED OVERTIME
# MAGIC SELECT 
# MAGIC  t.product_id,
# MAGIC  p.product_category,
# MAGIC  p.product_detail,
# MAGIC  t.transaction_date,
# MAGIC  SUM(t.transaction_qty * p.unit_price) AS total_revenue
# MAGIC FROM transactions t
# MAGIC JOIN products p ON t.product_id = p.product_id
# MAGIC GROUP BY t.transaction_date, t.product_id, p.product_category ,p.product_detail
# MAGIC ORDER BY t.transaction_date ASC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- WHICH DAYS OF THE WEEK TENDS TO BE BUSIEST, WHY?
# MAGIC
# MAGIC SELECT 
# MAGIC     DAYOFWEEK(transaction_date) AS day_number,
# MAGIC     DATE_FORMAT(transaction_date, 'EEEE') AS day_of_week,
# MAGIC     store_id,
# MAGIC     COUNT(transaction_id) AS total_transactions,
# MAGIC     SUM(transaction_qty) AS total_items_sold,
# MAGIC     ROUND(SUM(transaction_qty * unit_price), 2) AS total_revenue
# MAGIC FROM coffee_sales_clean
# MAGIC GROUP BY day_number, day_of_week,store_id 
# MAGIC ORDER BY day_number ASC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- WHAT TIME OF THE DAY TEND TO BE MOST POPULAR
# MAGIC
# MAGIC SELECT 
# MAGIC     UPPER (store_location) AS store_location,
# MAGIC     HOUR(transaction_time) AS hour_of_day,
# MAGIC     CASE 
# MAGIC         WHEN HOUR(transaction_time) BETWEEN 6 AND 11 THEN 'AM'
# MAGIC         WHEN HOUR(transaction_time) BETWEEN 12 AND 14 THEN 'PM'
# MAGIC         WHEN HOUR(transaction_time) BETWEEN 15 AND 17 THEN 'PM'
# MAGIC         WHEN HOUR(transaction_time) BETWEEN 18 AND 21 THEN 'PM'
# MAGIC         ELSE 'AM'
# MAGIC     END AS time_of_day,
# MAGIC     COUNT(transaction_id) AS total_transactions
# MAGIC FROM coffee_sales_clean
# MAGIC GROUP BY store_location, hour_of_day, time_of_day
# MAGIC ORDER BY store_location, hour_of_day ASC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- WHICH PRODUCTS SOLD MOST, WHICH DRIVE MOST REVENUE FOR BUSINESS
# MAGIC SELECT
# MAGIC  product_id,
# MAGIC  UPPER(product_category) AS product_category,
# MAGIC SUM(transaction_qty) as total_items_sold,
# MAGIC ROUND(SUM(transaction_qty * unit_price),2) as total_revenue
# MAGIC FROM coffee_sales_clean
# MAGIC GROUP BY product_id, product_category
# MAGIC ORDER BY total_revenue DESC
# MAGIC
# MAGIC
# MAGIC
# Databricks notebook source
spark.sql("select current_user()").display()
spark.sql("select continent, * from kaninipro.dev.sales_customers").display()
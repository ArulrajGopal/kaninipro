# Databricks notebook source
# MAGIC %md
# MAGIC #data preparation

# COMMAND ----------

data = [
    (1, "Bhagavatharku nakkal adhigam athanal inimel money pechu channel illa nakkal pechu channel"),
    (2,"தங்களுக்கும் தங்களது குழுவினருக்கும் மிக்க நன்றி🙏🙏🙏"),
    (3,"Very informative discussion"),
    (4,"Vishnu you paying tax??? Your income is 12lak plus???"),
    (5,"Sir if Reliance is bad they why dont you sell ur Reliance (ur father baught) and buy world best stock( ITC).."),
    (6,"Book profit on Monday sit on the cash wait for 21000 nifty"),
    (7,"The one thing i learnt from this channel is he is still in 90s so every stock he says I buyed it at lowest price . But he forgets that most of his audience where childrens during that time 😂 . And he also says look future but his investments and thought are of past ."),
    (8,"Idfc first  bank results would have been added as he was discussing it for long time and now left it out"),
    (9,"Indus bank consider from RS1200,, but anand now said 52weeks low.. what a interpretation"),
    (10,"Again again he is blaberring on Rupee depreciation. Contra views, some times good some times very bad on dollar depreciation 😂")

]

cols = ["id", "comment"]
youtube_comment_df = spark.createDataFrame(data, cols)
youtube_comment_df.write.mode("overwrite").format("delta").saveAsTable("youtube_comment_tbl")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from youtube_comment_tbl

# COMMAND ----------

# MAGIC %md
# MAGIC #classify, translate and fix grammar

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table youtube_cleansed_tbl as
# MAGIC with cte as(
# MAGIC   select 
# MAGIC   `comment`,
# MAGIC   ai_classify(`comment`, ARRAY("English","Tamil")) as language,
# MAGIC   case 
# MAGIC     when ai_classify(`comment`, ARRAY("English","Tamil")) = 'Tamil' then ai_translate(`comment`, 'en') 
# MAGIC     else `comment`
# MAGIC   end as translated_en
# MAGIC from 
# MAGIC   youtube_comment_tbl
# MAGIC )
# MAGIC select *, ai_fix_grammar(translated_en) as `clean_comment` from cte

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from youtube_cleansed_tbl

# COMMAND ----------

# MAGIC %md
# MAGIC #summarize, analyze sentiment and gen

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC   clean_comment,
# MAGIC   ai_analyze_sentiment(clean_comment) as sentiment,
# MAGIC   ai_summarize(clean_comment, 8) as summary,
# MAGIC   ai_gen(concat(clean_comment, ' <- This is a YouTube comment. Give a polite reply in 5 to 7 words.')) as author_reply
# MAGIC from youtube_cleansed_tbl

# COMMAND ----------

# MAGIC %md
# MAGIC #extract and mask

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC   clean_comment,
# MAGIC   ai_mask(clean_comment, ARRAY('Price'))  AS price_masked,
# MAGIC   ai_extract(clean_comment, ARRAY('name')) AS name_extracted
# MAGIC from youtube_cleansed_tbl

# COMMAND ----------




# COMMAND ----------


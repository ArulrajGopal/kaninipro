-- Databricks notebook source
-- MAGIC %md
-- MAGIC #classify, translate and fix grammar

-- COMMAND ----------

create or replace table youtube_cleansed_tbl as
with cte as(
  select 
  `comment`,
  ai_classify(`comment`, ARRAY("English","Tamil")) as language,
  case 
    when ai_classify(`comment`, ARRAY("English","Tamil")) = 'Tamil' then ai_translate(`comment`, 'en') 
    else `comment`
  end as translated_en
from 
  youtube_comment_tbl
)
select *, ai_fix_grammar(translated_en) as `clean_comment` from cte

-- COMMAND ----------

select * from youtube_cleansed_tbl

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #summarize, analyze sentiment and gen

-- COMMAND ----------

select 
  clean_comment,
  ai_analyze_sentiment(clean_comment) as sentiment,
  ai_summarize(clean_comment, 8) as summary,
  ai_gen(concat(clean_comment, ' <- This is a YouTube comment. Give a polite reply in 5 to 7 words.')) as author_reply
from youtube_cleansed_tbl

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #extract and mask

-- COMMAND ----------

select 
  clean_comment,
  ai_mask(clean_comment, ARRAY('Price'))  AS price_masked,
  ai_extract(clean_comment, ARRAY('name')) AS name_extracted
from youtube_cleansed_tbl

-- COMMAND ----------


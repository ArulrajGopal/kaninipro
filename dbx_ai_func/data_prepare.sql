-- Databricks notebook source
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

-- COMMAND ----------

select * from youtube_comment_tbl
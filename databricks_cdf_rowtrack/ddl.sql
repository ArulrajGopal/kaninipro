	-- enabling change data feed while creating table
	CREATE TABLE people_cdf (id INT, name STRING, age INT, Indicator String)
	  TBLPROPERTIES (delta.enableChangeDataFeed = true)
	  
	-- enabling change data feed after creating table
	ALTER TABLE people_cdf
	  SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
	  
	  
	-- enabling row level tracking while creating table
	CREATE TABLE people_cdf (id INT, name STRING, age INT, Indicator String)
	  TBLPROPERTIES (delta.enableRowTracking = true)
	
	-- enabling row level tracking after creating table
	ALTER TABLE people_cdf
	  SET TBLPROPERTIES (delta.enableRowTracking = true)

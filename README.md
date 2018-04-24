# mysqlpgsql
A database migration tool for MySQL and PostgreSQL

FOR COMMAND LINE:__
  python3 mysql2pgsql.py <mysql-dump-file>__
  python3 pgsql2mysql.py <pgsql-dump-file>__
  
  -- when we run the command , corresponding commands will be generated in the terminal
  
FOR GUI APP:
	cd GuiApp/
	sudo apt-get install python3-tk  //installation of tkinter module
	python3 app.py
	
	-- we will PgSQL or MySQL using Radio buttons
	-- dump file will be browse with the Browse button
	-- Clicking Convert button will displayed the corresponding commands in the textarea below.
	-- the sql commands in textbox can be saved using Save As button.

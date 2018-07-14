# Logs Analysis Project

Source code for Logs Analysis project.

## How to run the application?

1) Install [Git](https://git-scm.com/downloads)

2) Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
Don't start VirtualBox as Vagrant will be used to start it.

3) Install [Vagrant](https://www.vagrantup.com/)

4) Download [VM Configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
Extract the above file into local directory.

5) Setup and start your VM
Change directory to the VM configuration directory using GitBash, and run the command ```bash vagrant up``` to install and start VM.
You need to run this command every time you restart your machine to start your VM.

6) Login to VM
Use the command ```bash vagrant ssh```

7) Download the data
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

8) Load the data into PostgreSQL
Copy the file newsdata.sql to /vagrant directory.
Change the directory to the vagrant directory ```bash cd /vagrant``` and use the command ```bash psql -d news -f newsdata.sql```

9) Download the source code
Use git to clone or download the source code from https://github.com/bharasheh/portfolio-site.git

10) Run the application using the command
```bash python logs-analysis.py```

## Expected Output

==========================================================
What are the most popular three articles of all time?
==========================================================
Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views


==========================================================
Who are the most popular article authors of all time?
==========================================================
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views


==========================================================
On which days did more than 1% of requests lead to errors?
==========================================================
July 17, 2016 - 2.3%
vagrant@vagrant:/vagrant/logs-analysis$

## Code Design
The start function in the code is ```python main()``` where it will start the different parts of the analysis code.

The code is using ```python psycopg2``` to connect to PostgreSQL.

The reusable function ```python print_sql_result``` is to print the output of the SQL statements for all analysis functions. This function receives the db_conn which is the database connection, sql statement that generates the analysis report, and line_suffix to be added at the end of each line.

The function ```python print_articles_by_popularity``` is to find the articles by popularity. It can be used to find the most or the less popular articles. You can show any required number of articles or all of them.

The function ```python print_authors_by_popularity``` is to find the authors by popularity. It can be used to find the most or the less popular authors. You can show any required number of authors or all of them.

The function ```python print_days_with_errors``` is using sub-query to find how many requests with and without errors everyday, then the parent query will calculate the percentage of the daily errors, and show only the days with errors more than the error_threshold.

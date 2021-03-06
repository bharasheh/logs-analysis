#!/usr/bin/env python3
#
# Reporting tool that prints out reports (in plain text) using data in
# the database which has browsing history for articles web site.

import psycopg2

DBNAME = "news"


def print_sql_result(db_conn, sql, line_suffix):
    """This function print the result of the SQL using the DB connection.
    The SQL should have at least two columns in the 'select' statement.
    Each row will be printed in a separate line, and 'line_suffix'
    will be printed at the end."""
    cursor = db_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print("{} - {}{}".format(row[0], row[1], line_suffix))


def print_articles_by_popularity(db_conn, order, num_of_articles):
    """Order and print articles by popularity.
    Use 'order=desc' for most popular or 'order=asc' for less popular.
    num_of_articles is number of articles to show or use 'ALL'
    to show all articles."""
    sql = """SELECT articles.title, count(log.id) AS num
             FROM log, articles
             WHERE lower(log.path) = '/article/'||articles.slug
             GROUP BY articles.title
             ORDER BY num {}
             LIMIT {};"""
    sql = sql.format(order, str(num_of_articles))
    print_sql_result(db_conn, sql, " views")


def print_authors_by_popularity(db_conn, order, num_of_authors):
    """Order and print authors by popularity.
    Use 'order=desc' for most popular or 'order=asc' for less popular.
    num_of_authors is number of authors to show or use 'ALL'
    to show all authors."""
    sql = """SELECT authors.name, count(log.id) AS num
             FROM log, articles, authors
             WHERE lower(log.path) = '/article/'||articles.slug
             AND articles.author = authors.id
             GROUP BY authors.name
             ORDER BY num {}
             LIMIT {};"""
    sql = sql.format(order, str(num_of_authors))
    print_sql_result(db_conn, sql, " views")


def print_days_with_errors(db_conn, error_threshold):
    """Print the days that have percentage of requests with errors
    more than error_threshold."""
    sql = """SELECT log_date,
             round(
               cast(error_count as decimal)
               / (error_count + passed_count)
               * 100, 1) AS error_percentage
             FROM (
             SELECT to_char(time, 'FMMonth DD, YYYY') AS log_date,
             sum(
             case
               when status < '400' then 1
               else 0
               end
               ) as passed_count,
             sum(
             case
               when status >= '400' then 1
               else 0
               end) as error_count
             FROM log
             GROUP BY log_date) AS log_by_date
             WHERE round(
               cast(error_count as decimal)
               / (error_count + passed_count)
               * 100, 1) > {};"""
    sql = sql.format(str(error_threshold))
    print_sql_result(db_conn, sql, "%")


def main():
    """Start the Logs Analysis tool."""
    conn = psycopg2.connect(database=DBNAME)

    print("\n\n==========================================================")
    print("What are the most popular three articles of all time?")
    print("==========================================================")
    print_articles_by_popularity(conn, "desc", 3)

    print("\n\n==========================================================")
    print("Who are the most popular article authors of all time?")
    print("==========================================================")
    print_authors_by_popularity(conn, "desc", "ALL")

    print("\n\n==========================================================")
    print("On which days did more than 1% of requests lead to errors?")
    print("==========================================================")
    print_days_with_errors(conn, 1)

    conn.close()


if __name__ == '__main__':
    main()

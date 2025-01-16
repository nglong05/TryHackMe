## Terminology and Types
XSS is a vulnerability that allows an attacker to inject malicious scripts into a web page viewed by another user. Consequently, they bypass the Same-Origin Policy (SOP); SOP is a security mechanism implemented in modern web browsers to prevent a malicious script on one web page from obtaining access to sensitive data on another page. SOP defines origin based on the protocol, hostname, and port. Consequently, a malicious ad cannot access data or manipulate the page or its functionality on another origin, such as an online shop or bank page. XSS dodges SOP as it is executing from the same origin.
### JavaScript for XSS

Basic knowledge of JavaScript is pivotal for understanding XSS exploits and adapting them to your needs. Knowing that XSS is a client-side attack that takes place on the target’s web browser, we should try our attacks on a browser similar to that of the target. It is worth noting that different browsers process certain code snippets differently. In other words, one exploit code might work against Google Chrome but not against Mozilla Firefox or Safari.

Suppose you want to experiment with some JavaScript code in your browser. In that case, you need to open the Console found under Web Developer Tools on Firefox, Developer Tools on Google Chrome, and Web Inspector on Safari. Alternatively, use the respective shortcuts:

-    On Firefox, press Ctrl + Shift + K
-    On Google Chrome, press Ctrl + Shift + J
-    On Safari, press Command + Option + J

A web browser with the Console tab ready.

Let’s review and try some essential JavaScript functions:

-    Alert: You can use the alert() function to display a JavaScript alert in a web browser. Try alert(1) or alert('XSS') (or alert("XSS")) to display an alert box with the number 1 or the text XSS.
-    Console log: Similarly, you can display a value in the browser’s JavaScript console using console.log(). Try the following two examples in the console log: console.log(1) and console.log("test text") to display a number or a text string.
-    Encoding: The JavaScript function btoa("string") encodes a string of binary data to create a base64-encoded ASCII string. This is useful to remove white space and special characters or encode other alphabets. The reverse function is atob("base64_string").

Furthermore, you can experiment with displaying values, such as the document.cookie by using alert(document.cookie) for example.
### 
Types of XSS

-    Reflected XSS: This attack relies on the user-controlled input reflected to the user. For instance, if you search for a particular term and the resulting page displays the term you searched for (reflected), the attacker would try to embed a malicious script within the search term.
-    Stored XSS: This attack relies on the user input stored in the website’s database. For example, if users can write product reviews that are saved in a database (stored) and being displayed to other users, the attacker would try to insert a malicious script in their review so that it gets executed in the browsers of other users.
-    DOM-based XSS: This attack exploits vulnerabilities within the Document Object Model (DOM) to manipulate existing page elements without needing to be reflected or stored on the server. This vulnerability is the least common among the three.

![alt text](image-25.png)
## Causes and Implications

Cross-site scripting (XSS) is a web security vulnerability that allows an attacker to inject malicious scripts into a web page viewed by other users. As a result, the unsuspecting users end up running the unauthorized script in their browsers, although the website they are visiting is trusted to be benign. Therefore, XSS can be a severe threat because it exploits users’ trust in a site.
What Makes XSS Possible

There are many reasons why XSS vulnerabilities are still found in web apps. Below, we list a few of them.

**Insufficient input validation and sanitization**

Web applications accept user data, e.g., via forms, and use this data in the dynamic generation of HTML pages. Consequently, malicious scripts can be embedded as part of the legitimate input and will eventually be executed by the browser unless adequately sanitized.

**Lack of output encoding**

The user can use various characters to alter how a web browser processes and displays a web page. For the HTML part, it is critical to properly encode characters such as <, >, ", ', and & into their respective HTML encoding. For JavaScript, special attention should be given to escape ', ", and \\. Failing to encode user-supplied data correctly is a leading cause of XSS vulnerabilities.

**Improper use of security headers**

Various security headers can help mitigate XSS vulnerabilities. For example, Content Security Policy (CSP) mitigates XSS risks by defining which sources are trusted for executable scripts. A misconfigured CSP, such as overly permissive policies or the improper use of unsafe-inline or unsafe-eval directives, can make it easier for the attacker to execute their XSS payloads.

**Framework and language vulnerabilities**

Some older web frameworks did not provide security mechanisms against XSS; others have unpatched XSS vulnerabilities. Modern web frameworks automatically escape XSS by design and promptly patch any discovered vulnerability.

**Third-party libraries**

Integrating third-party libraries in a web application can introduce XSS vulnerabilities; even if the core web application is not vulnerable.

### Implications of XSS

There are many implications of XSS. Below, we list a few of them.

**Session hijacking**

As XSS can be used to steal session cookies, attackers can take over the session and impersonate the victim if successful.

**Phishing and credential theft**

Leveraging XSS, attackers can present a fake login prompt to the user. In one recent case, the browser’s page was partially hidden by a dialogue box requesting users to connect to their cryptocurrency wallet.

**Social engineering**

Using XSS, an attacker can create a legitimate-looking pop-up or alert within a trusted website. This can trick users into clicking malicious links or visiting malicious websites.

**Content manipulation and defacement**

In addition to phishing and social engineering, an attacker might use XSS to change the website for other purposes, such as inflicting damage on the company’s reputation.

**Data exfiltration**

XSS can access and exfiltrate any information displayed on the user’s browser. This includes sensitive information such as personal data and financial information.

**Malware installation**

A sophisticated attacker can use XSS to spread malware. In particular, it can deliver drive-by download attacks on the vulnerable website.

![alt text](image-26.png)

## Reflected XSS

Reflected XSS is a type of XSS vulnerability where a malicious script is reflected to the user’s browser, often via a **crafted URL** or form submission. Consider a search query containing `<script>alert(document.cookie)</script>;` many users wouldn’t be suspicious about such a URL, even if they look at it up close. If processed by a vulnerable web application, it will be executed within the context of the user’s browser.

In this innocuous example, it displays the cookie in an alert box. Obviously, an attacker wants to achieve more than just displaying the cookie as an alert to the user. However, for such an attack to be possible, we need a vulnerable application.

### Vulnerable Web Application

One simple reflected XSS vulnerability is when the user searches for some term, and the search string is included verbatim in the results page. This simple scenario provides an easy target for the attacker to exploit.

Although discovering such vulnerabilities is not always easy, fixing them is straightforward. User input such as `<script>alert('XSS')</script>` should be santized or HTML-encoded to `&lt;script&gt;alert('XSS')&lt;/script&gt;.`

In the following subsections, we provide examples of vulnerable code in the following languages and frameworks:

-    PHP
-    JavaScript (Node.js)
-    Python (Flask)
-    C# (ASP.NET)

**PHP**

Vulnerable code
```php
<?php
$search_query = $_GET['q'];
echo "<p>You searched for: $search_query</p>";
?>
```
`$_GET` is a PHP array containing values from the URL query string. Furthermore, `$_GET['q']` refers to the query string parameter `q`. For example, in `http://shop.thm/search.php?q=table`, `$_GET['q']` has the value table.

As you might have guessed, the vulnerability is caused by the search value displayed on the result page without sanitization. Therefore, an attacker can add a malicious script to the URL, knowing it would be executed. For example, as a proof of concept, the following URL can be tested: `http://shop.thm/search.php?q=<script>alert(document.cookie)</script>` and if the site is vulnerable, an alert box will appear displaying the user’s cookie.

Fixed code
```php
<?php
$search_query = $_GET['q'];
$escaped_search_query = htmlspecialchars($search_query);
echo "<p>You searched for: $escaped_search_query</p>";
?>
```
The PHP function `htmlspecialchars()` converts special characters to HTML entities. The characters `<`, `>`, `&`, `"`, `'` are replaced by default to prevent scripts in the input from executing. You can read its documentation [here](https://www.php.net/htmlspecialchars). 

### JavaScript (Node.js)

Vulnerable code
```js
const express = require('express');
const app = express();

app.get('/search', function(req, res) {
    var searchTerm = req.query.q;
    res.send('You searched for: ' + searchTerm);
});

app.listen(80);
```
If you are unfamiliar with Node.js, the code snippet above uses `Express`, a popular web application framework for Node.js. The `req.query.q` will extract the value of `q`. For example, in `http://shop.thm/search?q=table`, `req.query.q` has the value table. Finally, the response is generated by appending the search term provided by the user to “You searched for:”.

Because the value is taken from the user and inserted in the response HTML without sanitization or escaping, it is easy to append a malicious query. As a proof of concept, we can test the following URL: `http://shop.thm/search?q=<script>alert(document.cookie)</script>`, and if the site is vulnerable, an alert box will appear displaying the user’s cookie.

Fixed code
```js
const express = require('express');
const sanitizeHtml = require('sanitize-html');

const app = express();

app.get('/search', function(req, res) {
    const searchTerm = req.query.q;
    const sanitizedSearchTerm = sanitizeHtml(searchTerm);
    res.send('You searched for: ' + sanitizedSearchTerm);
});

app.listen(80);
```
The solution is achieved by using the sanitizeHtml() from the sanitize-html library. This function removes unsafe elements and attributes. This includes removing script tags, among other elements that could be used for malicious purposes.

Another approach would be by using the `escapeHtml()` function instead of the `sanitizeHtml()` function. As the name indicates, the `escapeHtml()` function aims to escape characters such as `<`, `>`, `&`, `"`, and `'`.
### Python (Flask)

Vulnerable code

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/search")
def home():
    query = request.args.get("q")
    return f"You searched for: {query}!"

if __name__ == "__main__":
    app.run(debug=True)
```
If you are unfamiliar with Flask, `request.args.get()` is used to access query string parameters from the request URL. In fact, `request.args` contains all the query string parameters in a dictionary-like object. For example, in `http://shop.thm/search?q=table`, `request.args.get("q")` has the value table.

Because the value is taken from the user and inserted in the response HTML without sanitization or escaping, it is easy to append a malicious query. As a proof of concept, we can test the following URL: `http://shop.thm/search?q=<script>alert(document.cookie)</script>`, and if the site is vulnerable, an alert box will appear displaying the user’s cookie.

Fixed code
```python
from flask import Flask, request
from html import escape

app = Flask(__name__)

@app.route("/search")
def home():
    query = request.args.get("q")
    escaped_query = escape(query)
    return f"You searched for: {escaped_query}!"

if __name__ == "__main__":
    app.run(debug=True)
```
The main change is that the user input is now escaped using the `escape()` function from the html module. Note that the `html.escape()` function in Flask is actually an alias for `markupsafe.escape()`. They both come from the `Werkzeug` library and serve the same purpose: escaping unsafe characters in strings. This function converts characters like `<`, `>`, `"`, `'` to HTML escaped entities, disarming any malicious code the user has inserted.
### ASP.NET

Vulnerable code

```C#
public void Page_Load(object sender, EventArgs e)
{
    var userInput = Request.QueryString["q"];
    Response.Write("User Input: " + userInput);
}
```
If you are unfamiliar with ASP.NET and C#, the code above uses `Request.QueryString`, which returns a collection of associated string keys and values. In the example above, we are interested in the value associated with the key q, and we save it in the variable userInput. Finally, the response is created by appending the userInput to another string.

Fixed code
```C#
using System.Web;

public void Page_Load(object sender, EventArgs e)
{
    var userInput = Request.QueryString["q"];
    var encodedInput = HttpUtility.HtmlEncode(userInput);
    Response.Write("User Input: " + encodedInput);
}
```
Again, the solution lies in encoding the user input into HTML-safe strings. ASP.NET C# provides the `HttpUtility.HtmlEncode()` method, which converts various characters, such as `<`, `>`, and `&`, into their respective HTML entity encoding.

![alt text](image-27.png)

## Vulnerable Web Application 1

The attached VM runs a vulnerable version of copyparty. The discovered reflected XSS vulnerability has the ID CVE-2023-38501, and its exploit is published here.

copyparty is file server software. Prior to version 1.8.7, the application contains a reflected cross-site scripting via URL-parameter `?k304=...` and `?setck=...`. The worst-case outcome of this is being able to move or delete existing files on the server, or upload new files, using the account of the person who clicks the malicious link. It is recommended to change the passwords of one's copyparty accounts, unless one have inspected one's logs and found no trace of attacks. Version 1.8.7 contains a patch for the issue. 

**Description**

Copyparty is a portable file server. Versions prior to 1.8.6 are subject to a reflected cross-site scripting (XSS) Attack. 

Vulnerability that exists in the web interface of the application could allow an attacker to execute malicious javascript code by tricking users into accessing a malicious link.

**POC**

https://localhost:3923/?k304=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3Dalert(1)%3E

`?k304=y <img src=copyparty onerror=alert(1)>`

## Stored XSS

Stored XSS, or Persistent XSS, is a web application security vulnerability that occurs when the application stores user-supplied input and later embeds it in web pages served to other users without proper sanitization or escaping. Examples include web forum posts, product reviews, user comments, and other data stores. In other words, stored XSS takes place when user input is saved in a data store and later included in the web pages served to other users without adequate escaping.

Stored XSS begins with an attacker injecting a malicious script in an input field of a vulnerable web application. The vulnerability might lie in how the web application processes the data in the comment box, forum post, or profile information section. When other users access this stored content, the injected malicious script executes within their browsers. The script can perform a wide range of actions, from stealing session cookies to performing actions on behalf of the user without their consent.

### Vulnerable Web Application

There are many reasons for a web application to be vulnerable to stored XSS. Some of the best practices to prevent stored XSS vulnerabilities are:

-    Validate and sanitize input: Define clear rules and enforce strict validation on all user-supplied data. For instance, only alphanumeric characters can be used in a username, and only integers can be allowed in age fields.
-    Use output escaping: When displaying user-supplied input within an HTML context, encode all HTML-specific characters, such as <, >, and &.
-    Apply context-specific encoding: For instance, within a JavaScript context, we must use JavaScript encoding whenever we insert data within a JavaScript code. On the other hand, data placed in URLs must use relevant URL-encoding techniques, like percent-encoding. The purpose is to ensure that URLs remain valid while preventing script injection.
-     Practice defence in depth: Don’t rely on a single layer of defence; use server-side validation instead of solely relying on client-side validation.

### PHP
Vulnerable Code

The code below has multiple vulnerabilities. It does two things:

-    Read a comment from the user and save it in the $comment variable.
-    Adds the $comment to the column comment in the table comments in a database.
-    Later, it iterates over all the rows in the column comment and displays them on screen.

```php
// Storing user comment
$comment = $_POST['comment'];
mysqli_query($conn, "INSERT INTO comments (comment) VALUES ('$comment')");

// Displaying user comment
$result = mysqli_query($conn, "SELECT comment FROM comments");
while ($row = mysqli_fetch_assoc($result)) {
    echo $row['comment'];
}
```
Fixed Code
```php
// Storing user comment
$comment = mysqli_real_escape_string($conn, $_POST['comment']);
mysqli_query($conn, "INSERT INTO comments (comment) VALUES ('$comment')");

// Displaying user comment
$result = mysqli_query($conn, "SELECT comment FROM comments");
while ($row = mysqli_fetch_assoc($result)) {
    $sanitizedComment = htmlspecialchars($row['comment']);
    echo $sanitizedComment;
}
```
Before displaying every comment on the screen, we pass it through the `htmlspecialchars()` function to ensure all special characters are converted to HTML entities. Consequently, any attempts for stored XSS won’t make it to the end user’s browser.

This is outside the scope of this room; however, if you are curious about the SQL injection vulnerability, this is alleviated using the `mysqli_real_escape_string()`. This function escapes special characters in the input string so it can safely be used in an SQL statement.

### JavaScript (Node.js)
Vulnerable Code

The following JavaScript code reads a comment received from a user that was saved in a database table. We assume the comments array has been populated from the database. Discover what makes it vulnerable to stored XSS and how to solve it.
```js
app.get('/comments', (req, res) => {
  let html = '<ul>';
  for (const comment of comments) {
    html += `<li>${comment}</li>`;
  }
  html += '</ul>';
  res.send(html);
});
```
The main issue in the code above is that it reads the user’s input saved in comment (from the comments array) and is displayed as part of the HTML code. Consequently, when another user views this user’s comment as HTML, the browser will execute any scripts injected into it.

Fixed Code
```js
const sanitizeHtml = require('sanitize-html');

app.get('/comments', (req, res) => {
  let html = '<ul>';
  for (const comment of comments) {
    const sanitizedComment = sanitizeHtml(comment);
    html += `<li>${sanitizedComment}</li>`;
  }
  html += '</ul>';
  res.send(html);
});
```
Part of the solution is sanitizing the HTML before displaying it to the user. We can remove HTML elements outside the allowlist using the `sanitizeHTML()` function. In general, we expect to allow basic text formatting such as bold and italic (`<b>` and `<i>`), but we would remove potentially dangerous or unsafe elements such as `<script>` and `<onload>`. 

### Python (Flask)
Vulnerable Code

```py
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

@app.route('/comment', methods=['POST'])
def add_comment():
    comment_content = request.form['comment']
    comment = Comment(content=comment_content)
    db.session.add(comment)
    db.session.commit()
    return 'Comment added!'

@app.route('/comments')
def show_comments():
    comments = Comment.query.all()
    return render_template_string(''.join(['<div>' + c.content + '</div>' for c in comments]))
```
The first issue is that the `comment_content` is set to the user’s form submission retrieved from `request.form['comment']` without sanitization. This in itself lays the ground for stored XSS and SQL injection. Furthermore, when a user wants to view the comments, they are displayed without escaping, another perfect recipe for stored XSS.

Fixed Code
```py
from flask import Flask, request, render_template_string, escape
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

@app.route('/comment', methods=['POST'])
def add_comment():
    comment_content = request.form['comment']
    comment = Comment(content=comment_content)
    db.session.add(comment)
    db.session.commit()
    return 'Comment added!'

@app.route('/comments')
def show_comments():
    comments = Comment.query.all()
    sanitized_comments = [escape(c.content) for c in comments]
    return render_template_string(''.join(['<div>' + comment + '</div>' for comment in sanitized_comments]))
```
We used the `escape()` function to ensure that any special characters in the user-submitted comment are replaced with HTML entities. As you would expect, the characters `&`, `<`, `>`, `'`, and `"` are converted to HTML entities (`&amp;`, `&lt;`, `&gt;`, `&#39;`, and `&quot;`). We made two changes:

Although the user-submitted input `request.form['comment']` is saved verbatim, the content of each saved comment c goes through the `escape()` function before it is sent to the user’s browser to be displayed as HTML.

### C# (ASP.NET)
Vulnerable Code

The following C# code has multiple vulnerabilities. Take a quick look at the code below and think about what needs to be changed.
```C#
public void SaveComment(string userComment)
{
    var command = new SqlCommand("INSERT INTO Comments (Comment) VALUES ('" + userComment + "')", connection);
    // Execute the command
}

public void DisplayComments()
{
    var reader = new SqlCommand("SELECT Comment FROM Comments", connection).ExecuteReader();
    while (reader.Read())
    {
        Response.Write(reader["Comment"].ToString());
    }
    // Execute the command
}
```
One of the vulnerabilities we observe in the code above is stored XSS. The system stores whatever comment the user inputs without any changes and later displays it to other users. Another vulnerability outside the scope of this room is SQL injection.

Fixed Code
```c#
using System.Web;

public void SaveComment(string userComment)
{
    var command = new SqlCommand("INSERT INTO Comments (Comment) VALUES (@comment)", connection);
    command.Parameters.AddWithValue("@comment", userComment);
}

public void DisplayComments()
{
    var reader = new SqlCommand("SELECT Comment FROM Comments", connection).ExecuteReader();
    while (reader.Read())
    {
        var comment = reader["Comment"].ToString();
        var sanitizedComment = HttpUtility.HtmlEncode(comment);
        Response.Write(sanitizedComment);
    }
    reader.Close();
}
```
With a few changes, the code’s security has improved. Stored-XSS is fixed by using the `HttpUtility.HtmlEncode()` method before displaying the userComment as part of a web page. If you are curious, the SQL injection vulnerability is fixed by using parametrized SQL queries with values passed separately instead of building the SQL query via string concatenation. This can be achieved using the Parameters.`AddWithValue()` method in the `SqlCommand` objects.

![alt text](image-28.png)

### Vulnerable Web Application 2

The attached VM runs the vulnerable project Hospital Management System. The project was uploaded a few years ago and was never updated since then. It is fully functional. Unfortunately, a stored XSS vulnerability was discovered and tagged as `CVE-2021-38757` and an exploit was published, but the application has not been patched till the time of writing.

To exploit the vulnerability, the attacker only needs to click on “Contact”, and fill in the name, email, phone number, and submit the payload in the message field. Something simple such as `<script>alert("Simple XSS")</script>` would still work.

Any message sent via the Contact page appears to the Receptionist when they log in. To log in as the Receptionist via the corresponding tab, use the following credentials:

-    Username: admin
-    Password: admin123

The vulnerability lies in the `contact.php`. Although the code works well, it is not secure. As we can see in the listing below, the user’s submitted message is saved unsanitized in the database table.

```php
<?php 
$con=mysqli_connect("localhost","root","","myhmsdb");
if(isset($_POST['btnSubmit']))
{
	$name = $_POST['txtName'];
	$email = $_POST['txtEmail'];
	$contact = $_POST['txtPhone'];
	$message = $_POST['txtMsg'];

	$query="insert into contact(name,email,contact,message) values('$name','$email','$contact','$message');";
	$result = mysqli_query($con,$query);
	
	if($result)
    {
    	echo '<script type="text/javascript">'; 
		echo 'alert("Message sent successfully!");'; 
		echo 'window.location.href = "contact.html";';
		echo '</script>';
    }
}
```

![alt text](image-29.png)

## DOM-Based XSS
The DOM is a programming interface representing a web document as a tree. The DOM makes it possible to programmatically access and manipulate the different parts of a website using JavaScript. Let’s consider a practical example.

Consider the HTML code of example.com in the screenshot below (as fetched on the first of February 2024). We opened the Web Developer Tools using the Firefox web browser and checked the Inspector tab.

![alt text](image-30.png)

A web browser with the Inspector tab displaying an example website.

The DOM tree shown above is like the following list with sublists.

    document
        <!DOCTYPE html>
        html
            head
                title
                meta
                meta
                meta
                style
            body
                div
                    h1
                    p
                    p
                        a

The tree starts with the document node and branches into DOCTYPE and html. The html node branches into head and body. The head has the title, a few meta tags, and a style. In this simple example, the body has a single div that branches into one h1 and two p. This is a concise page. More practical pages would have tens or hundreds of branches.

We can view the DOM tree using the web browser’s built-in Web Developer’s Tools. For example, press Ctrl + Shift + I on Firefox and check the Inspector tab.

Alternatively, we can access the JavaScript console, as mentioned in Task 2. Using JavaScript, you can manipulate the DOM tree. For example, you can create a new element using `document.createElement()` and add a child to any element using `element.append()`. Here is an example from MDN documentation.
```js
let div = document.createElement("div");
let p = document.createElement("p");
div.append(p);

console.log(div.childNodes); // NodeList [ <p> ]
```
In the example code above, we created two elements, `div` and `p`. Then, we appended the latter element to the div element.

**Vulnerable Web Applications**

DOM-based XSS vulnerabilities take place within the browser. They don’t need to go to the server and return to the client’s web browser. In other words, the attacker will try to exploit this situation by injecting a malicious script, for example, into the URL, and it will be executed on the client’s side without any role for the server in this. We will present an elementary and minimal static site without relying on the back-end code to demonstrate this concept.

Vulnerable “Static” Site
```html
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Page</title>
</head>
<body>
    <div id="greeting"></div>
    <script>
        const name = new URLSearchParams(window.location.search).get('name');
        document.write("Hello, " + name);
    </script>
</body>
</html>
```
The page above expects the user to provide their name after ?name=. In the screenshot below:

-    The user has entered Web Tester after ?name in the URL.
-    The greeting worked as expected and displayed “Hello, Web Tester”.
-    Finally, the DOM structure on the right is left intact; the `<body>` has three direct children.

A web browser with the Inspector tab displaying the original DOM structure of an example static site.

The user might try to inject a malicious script. In the screenshot below, we see the following:

-    The user added `<script>alert("XSS")</script>` instead of only Web Tester as their name.
-    The script was executed, and an alert dialogue box was displayed.
-    Most importantly, we can see how the DOM tree got a new element. `<body>` has four children now.

A web browser with the Inspector tab displaying the manipulated DOM structure of an example static site.

This basic example illustrates a couple of things:

-    The server has no direct role in DOM-based vulnerabilities. In this demonstration, everything took place on the client’s browser without using a back end.
-    The DOM was insecurely modified using document.write().

**Fixed “Static” Site**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Secure Page</title>
</head>
<body>
    <div id="greeting"></div>
    <script>
        const name = new URLSearchParams(window.location.search).get('name');
        // Escape the user input to prevent XSS attacks
        const escapedName = encodeURIComponent(name);
        document.getElementById("greeting").textContent = "Hello, " + escapedName;
    </script>
</body>
</html>
```
One way to fix this page is by avoiding adding user input directly with `document.write()`. Instead, we first escaped the user input using `encodeURIComponent()` and then added it to textContent.

The previous attempt does not work now. We can see that:

-    The user has added JavaScript as part of their input.
-    The JavaScript code is displayed as encoded characters and presents no threat in the current context.
-    The DOM structure is no longer affected when the user attempts to add code as part of their submitted name.

![alt text](image-31.png)

## Context and Evasion
### Context

The injected payload will most likely find its way within one of the following:

-    Between HTML tags
-    Within HTML tags
-    Inside JavaScript

When XSS happens between HTML tags, the attacker can run `<script>alert(document.cookie)</script>`.

However, when the injection is within an HTML tag, we need to end the HTML tag to give the script a turn to load. Consequently, we might adapt our payload to `><script>alert(document.cookie)</script>` or `"><script>alert(document.cookie)</script>` or something similar that would fit in the context.

We might need to terminate the script to run the injected one if we can inject our XSS within an existing JavaScript. For instance, we can start with `</script>` to end the script and continue from there. If your code is within a JavaScript string, you can close the string with `'`, complete the command with a semicolon, execute your command, and comment out the rest of the line with `//`. You can try something like this `';alert(document.cookie)//`.

This example should give you some ideas to escape the context you start from. Generally speaking, being aware of the context where your XXS payload is executing is very important for the successful execution of the payload.

### Evasion

Various repositories can be consulted to build your custom XSS payload. This gives you plenty of room for experimentation. One such list is the XSS Payload List.

However, sometimes, there are filters blocking XSS payloads. If there is a limitation based on the payload length, then Tiny XSS Payloads can be a great starting point to bypass length restrictions.

If XSS payloads are blocked based on specific blocklists, there are various tricks for evasion. For instance, a horizontal tab, a new line, or a carriage return can break up the payload and evade the detection engines.

-    Horizontal tab (TAB) is 9 in hexadecimal representation
-    New line (LF) is A in hexadecimal representation
-    Carriage return (CR) is D in hexadecimal representation

Consequently, based on the XSS Filter Evasion Cheat Sheet, we can break up the payload. `<IMG SRC="javascript:alert('XSS');">` in various ways:

`<IMG SRC="jav&#x09;ascript:alert('XSS');">`

`<IMG SRC="jav&#x0A;ascript:alert('XSS');">`

`<IMG SRC="jav&#x0D;ascript:alert('XSS');">`

![alt text](image-32.png)

# T2A2 API WEBSERVER

<br>

## R1 - Identification of the problem you are trying to solve by building this particular app.

With the book review/management application the main purpose is so the user can keep track and review all types of written content that they have read. The main problem that the app is attempting to solve is for users to have access to an app that will track all different types of written content not just one or two types, while also being able to keep track and share reviews for this content.

<br>

## R2 - Why is it a problem that needs solving?

The idea for this application came from looking at other apps such as 'Good Reads' and 'My Anime List'. Both of these applications are used to keep track and review what users have read. However 'Good Reads' is focused and presented to the public as an application to review "standard" books such as novels, short stories etc. , while 'My Anime List' only keeps track of manga and anime reviews. The idea for this app is to merge and expand on the two, to create one platform that users can use instead of having to sign up and use multiple applications.

This would be marketed for anyone who reads any type of content. This means that people who don't enjoy reading for leisure but need to find reviews on thesis', essays or research papers that they would need for an assignment or to reference in their own paper would have reviews and descriptions. By having an application that provides reviews, ratings and descriptions for content such as these would be extremely useful for many people. This means that all this information and reviews can be kept on one application instead of having to find reviews in multiple places. 
 
Users would be able to search the type of content they wish such as manga, books, articles, research papers etc. This makes it a diverse platform for all types of people from leisure readers to students completing an assignment. With these ideas implemented, it will help solve the problem of multiple application usage and aid the user in organisation for their book reviews and management all in one application.  

<br>

## R3- Why have you chosen this database system?

The database I have chosen to use is a relational database using PostgreSQL for database creation and manipulation. PostgreSQL is one of the most popular RDBMSs and includes many useful features to aid in the creation and management of a database. It supports common database primitives, numerous network-related types, geometric types and monetary types. Its stability and ability to work with large amounts of data and traffic for applications without jeopardising the applications performance or data integrity make it a practical choice for this applciation. 

One of the main reasons for choosing PostgreSQL is its support of writing database functions using the primary lanaguages that will be used and implemented in the API webserver, which includes SQL and Python. PostgreSQL has great support with database primitives such as numeric, Boolean and string which are used to build the application. Its support for JSON also makes it a viable choice for working with the relational data in the system since JSON will be implemented when building and creating this application. Having the ability to define my own types and transmitting the data for the web application will aid in the development of my database and structuring the data. 

Authentication, access control and secuirty are important for any application. PostgreSQL has a robust system to be able to appropriately and effciently handle these aspects. These authentication and authorization functionalities are crucial when dealing with user's personal data. PostgreSQL offers authentication methods, role-based access control, encryption and access permissions. These are all aspects that are crucial in providing a safe environment for your user's data by aiding in building a secure and safe application. 

One of the other features that PostgreSQL provides in the ability to define inheritance relationships between tables and add comments. Table inheritance allows for more manageable indexes and speeds up searches in the database. Changes are then easier to make as only the parent table will need to be changed for a cascade effect on the other tables instead of having to do in individually. These smaller indexes allow for easier reading and organisation, making a valuable feature for managing and organising the database. The ability to be able to add comments on database objects aid in organisation and management of data in the application by adding these comments to tables, databases and other database objects. 

PostgreSQL's use of arrays allows for efficient data organization by organizing related data into one single column. This is used to represent a collection of chosen values which simplifies the data model. Compact storage, index support, flexibility, readability and array functions are also other traits that arrays in PostgreSQL offer. Various array functions allow for dynamic operations on the arrays. With multiple array data types that work efficently with ORMs, this allows for easy mapping of array data between the application code and database. 

Its large list of features, reliablitly, performance and community support makes it a suitable choice for creating and building this application. The wide community support promotes a welcoming and well documented platform for PostgreSQL which provides further benfits to using this system. Due to it's popularity in the community, regualr updates and bug fixes further make it a viable choice for this application. 

<b><u>What are the drawbacks compared to others?</b></u>

The drawback of using PostgreSQL is that it can be complex for beginners, due to its expansive and advanced features list. With lack of knowledge of the system, it can impact performace due to the learning curve and making sure the database is organised to maximise performance. It must also be installed since it isn't directly installed on hosting platforms. Further installation of external resources is another drawback since there are common tools that are unavailable on PostgreSQL that are on other DBMSs. 

One of the main drawbacks is its lack of support for horizontal scaling. As the workload increases in the database it can become difficult to spread that workload across multiple machines in order to improve performance. Its lack of features for NoSQL impact its ability to work with application that require these features.  

When working with large amount of data, it requires heavy memory usage to cache data and execute queries efficiently. This also impacts performance if the system isn't allocated enough storage. Performance can also be impacted through low reading speeds which are caused by the scale of the application. Large loading operations also affect performance as it lacks built-in compression capabilities. 

While PostgreSQL offers a wide range of features, its drawbacks in NoSQL features and various performance aspects impacts makes it less suitable for certain applications that require these attributes to build and manage an application. 

<br>

## R4 - Identify and discuss the key functionalities and benefits of an ORM

Object-relational mapping (ORM) aids in simplifying and abstracting complexities when interacting with a relational database. By mapping attributes or properties of objects in the column of database tables, it enables developers to work with the data in an object-oriented manner. By providing CRUD API and a simplified data-model, it provides an easier learning curve for interacting with a database, compared to learning SQL syntax to communicate and manipulate data. ORMs act as bridging between two different paradigms making a popular programming technique. Some popular ORM systems are SQLAlchemy and Django.

One of the main key functionalities and benefits of an ORM is its ability to allow developers to write in their preferred programming language instead of SQL to manipulate data and schemas in a database. A developer can use a programming language that they work well with to work on a database instead of using SQL, providing flexibility and speed for developers. The ability to speed up production is due to not having to write multiple syntax from different languages to manage and manipulate data in the database. This subtracts dealing with low-level database operations and SQL queries by interacting directly with an object in the database instead of through SQL. 

ORMs are able to generate and execute SQL queries to perform database operations, joining and sorting. Features for validation and transformation of data before it is in the database provides organisation and maintenance of the database, since this is important information that needs to be stored. Schema management is another function that some ORMs provide. This generates or updates the schema if there are changes to the object model. This aids in management of the database. 

Other popular ORM tools are active record pattern and data mapper pattern. The active record pattern tool is used to map any data within the structure of objects in the code. It is able to manage data through using classes and structures. This offers multiple benefits such as simplifying a database, database abstraction, association and database schema management, testing and debugging. The data mapper pattern also contributes in maintaining code and providing flexibility and efficiency in database operations. 

<br>

## R5 - Document all endpoint of your API

### <u><b>Auth controller endpoints:</u></b>

<br>

### Route: ('/register', methods=['POST'])

	- HTTP request verb: POST
	- Allows someone to create a new account by providing their first name, last name, email and password.
	- No authentication is needed
	- Required data: User data is put in the request JSON (first name, last name, email, password)
	
Returns:

	- Serialized user object upon successful registration with HTTP status code 201 
	- Error message with HTTP status code 409 (Conflict) if email is already in use
	- Error message with HTTP status code 409 (Conflict) if any required fields are missing.

<br>

### Route: ('/login', methods=['POST'])

	- HTTP request verb: POST
	- Allows users to log in to their account by providing email and password
	- No authentication is needed
	- Required data: User login data in the request JSON (email, password)
	
Returns:

	- User email, JWT access token, and admin status when login is successful with HTTP status code 200 (OK).
	- Error message with HTTP status code 401 (Unauthorized) if  email or password provided is invalid.

<br>
<br>

### <u><b>Review controller endpoints:</u></b>

### Route: ('/reviews', methods=['GET])

	- HTTP request verb: GET
	- Retrieves list of all reviews from the database and return as JSON
	- No authentication required
	- No data is required
	
Returns:

	- List of all reviews as JSON objects with HTTP status code 200 (OK)

<br>

### Route: ('reviews/int:id, methods=['GET'])

	- HTTP request verb: PET
	- Retrieves one review from the database based on provided ID, and returns as JSON
	- No authentication required
	- Required data: ID (int) of review needed to retrieve

Returns:

	- Review data as a JSON object with HTTP status code 200 (OK) if review found
	- Error message as a JSON object with HTTP status code 404 (Not Found), if review ID not found

<br>

### Route: ('/reviews', methods=['POST'])

	- HTTP request verb: POST
	- Creates new review by extracting review data from the request JSON and adds to database
	- Requires valid JWT token from a user
	- Required data: Review data in request JSON required (content_id, rating and comment)

Returns:

	- The created review as a JSON object with HTTP status code 201 (Created) if review is successfully created.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if content_id doesn't exist.
	- Error message as a JSON object with HTTP status code 400 (Bad Request) if request JSON is missing the required content_id.

<br>

### Route: ('reviews/int:id, methods=['DELETE'])

	- HTTP request verb: DELETE
	- Only allows authorized users (the owners of review) to delete a review based on its ID.
	- Requires valid JWT token from a user
	- Required data: ID (int) of review needed to delete
	
Returns:

	- Success message as a JSON object with HTTP status code 200 (OK) if review is found and successfully deleted.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if review with the specified ID does not exist.
	- Error message as a JSON object with HTTP status code 403 (Forbidden) if user making the request is not the creator of the review.

<br>

### Route: ('reviews/int:id, methods=['PUT', 'PATCH'])

	- HTTP request verb: PUT, PATCH
	- Allows authorized users (the owners of the review) to update the rating or comment of their review based on its ID.
	- Requires a valid JWT token from a user
	- Required data: ID (int) of review to be updated
	
Returns:

	- Updated review as a JSON object with HTTP status code 200 (OK) if review is found and successfully updated.
	- Error message as a JSON object with HTTP status code 403 (Forbidden) if current user is not the owner of the review.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if review with the specified ID does not exist.

<br>
<br>

### <u><b>Content controller endpoints:</u></b>

### Route: ('/content', method=['GET'])

	- HTTP request verb: GET
	- Retrieves list of all content from the database and returns it as JSON
	- No authentication required
	- No required data
	
Returns: 

	- List of all content  as JSON objects with HTTP status code 200 (OK).

<br>

### Route: ('content/<int:id>', method=['GET'])

	- HTTP request verb: GET
	- Retrieves a single piece of content from the database based on the provided ID and returns it as JSON.
	- No authentication required
	- Required data: ID (int) of content needed to retrieve
	
Returns:

	- Content data as a JSON object with HTTP status code 200 (OK) if content is found.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if content is not found.

<br>

### Route: ('/content', methods=['POST'])

	- HTTP request verb: POST
	- Creates new content by extracting content data from the request JSON and adding it to the database.
	- Requires a valid JWT token from admin
	- Required data: Content data in the request JSON (title, genre, description, published, publisher, category_id, author_id)
	
Returns:

	- Created content as a JSON object with HTTP status code 201 (Created) if current user is an admin and the content is successfully created.
	- Error message as a JSON object with HTTP status code 403 (Forbidden) if current user is not an admin.
	- Error message as a JSON object with HTTP status code 400 (Bad Request) if the request JSON is missing required fields or contains invalid category or author IDs.
	
<br>    

### Route: ('content/<int:id>', methods=['DELETE'])

	- HTTP request verb: DELETE
	- Allows admins to delete a content item from the database based on the provided ID.
	- Requires a valid JWT token from admin
	- Required data: ID (int)  of the content item to be deleted.

Returns:

	- A success message as a JSON object with HTTP status code 200 (OK) if content item is found and successfully deleted.
	- Error message as a JSON object with HTTP status code 403 (Forbidden) if current user is not an admin.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if content item with the specified ID does not exist.

<br>
	
### Route:('content/<int:id>', methods=['PUT', 'PATCH'])

	- HTTP request verb: PUT, PATCH
	- Allows admins to update a content item based on its ID. The content can be partially updated by providing only the fields to be changed in the request JSON.
	- Requires a valid JWT token from admin
	- Required data: ID (int)  of the content item to be updated.
	
Returns:

		- Updated content as a JSON object with HTTP status code 200 (OK) if content item is found and successfully updated.
		- error message as a JSON object with HTTP status code 403 (Forbidden) if current user is not an admin.
		- Error message as a JSON object with HTTP status code 404 (Not Found) if content item with the specified ID does not exist.
		- Error message as a JSON object with HTTP status code 400 (Bad Request) if provided category or author IDs are invalid.

<br>
<br>

### <b><u>Category controller endpoints:</u></b>

### Route: ('/category', method=['GET'])

	- HTTP request verb: GET
	- Retrieves a list of all categories from the database and returns it as JSON.
	- No authentication is required
	- No required data

Returns:

	- List of all categories as JSON objects with HTTP status code 200 (OK).
	
<br>    

### Route: ('/category/<int:id>', method=['GET'])

	- HTTP request verb: GET
	- Retrieves a single category from the database based on the provided ID and returns it as JSON.
	- No authentication is required
	- Required data: ID (int) of the category to retrieve.

Returns:

	- Category data as a JSON object with HTTP status code 200 (OK) if category is found
	- Error message as a JSON object with HTTP status code 404 (Not Found) if  category is not found.

<br>

### Route: ('/category', methods=['POST'])

	- HTTP request verb: POST
	- Creates a new category by extracting the category data from the request JSON and adding it to the database.
	- Requires a valid JWT token from admin
	- Required data: Category data in the request JSON.

Returns:

	- Dictionary containing the details of the newly created category if successful.
	
Raises:

	- 403 Forbidden: If the user making the request is not an admin, an error message is returned.

<br>

### Route: ('/category/<int:id>', methods=['DELETE'])

	- HTTP request verb: DELETE
	- Allows admins to delete a category from the database based on the provided ID.
	- Requires a valid JWT token from admin
	- Required data: ID (int) of the category to be deleted.
	
Returns:

		○ Dictionary containing result of the operation:
			- If category is successfully deleted, it returns a message confirming the deletion.
			- If  category with  given ID does not exist, it returns an error message with status 404.
			
Raises:

	- 403 Forbidden: If the user making the request is not an admin, an error message is returned
	
<br>

### Route: ('/category/<int:id>', methods=['PUT', 'PATCH'])

	- HTTP request verb: PUT, PATCH
	- Allows admins to update a category's information in the database based on the provided ID.
	- Requires a valid JWT token from admin
	- Required data: ID (int) of the category to be updated.
	
Returns: 

	- Dictionary containing updated information of the category if successful.
	
Raises:

	- 403 Forbidden: If the user making the request is not an admin, an error message is returned.
	- 404 Not Found: If the category with the given ID does not exist, an error message is returned.
	
<br>
<br>

### <b><u>Author controller endpoints:</u></b>

### Route: ('/author', method=['GET'])

	- HTTP request verb: GET
	- Retrieves list of all authors from the database and returns it as JSON.
	- No authentication is required
	- No required data

Returns:

	-  List of all authors as JSON objects with HTTP status code 200 (OK).

<br>

### Route: ('/author/<int:id>', method=['GET'])

	- HTTP request verb: GET
	- Retrieves a single author from the database based on the provided ID and returns it as JSON.
	- No authentication is required
	- Required data: ID (int)  of the author to retrieve.

Returns:

	- Author data as a JSON object with HTTP status code 200 (OK) if author is found.
	- Error message as a JSON object with HTTP status code 404 (Not Found) if author is not found.

<br>

### Route: ('/author', methods=['POST'])

	- HTTP request verb: POST
	- Creates a new author by extracting the author data from the request JSON and adding it to the database
	- Requires a valid JWT token from admin
	- Required data: Author data in the request JSON.

Returns: 

	- Dictionary containing the details of the newly created author if successful.
	
Raises:

	- 403 Forbidden: If the user making the request is not an admin, an error message is returned

<br>

### Route: ('/author/<int:id>', methods=['DELETE'])

	- HTTP request verb: DELETE
	- Allows admins to delete an author from the database based on the provided ID.
	- Requires a valid JWT token from admin
	- Required data: ID (int) of the author to be deleted.

Returns:

	○ A dictionary containing the result of the operation:
		-  If author is successfully deleted, it returns a message confirming the deletion.
		-  If author with the given ID does not exist, it returns an error message with status 404.

Raises:

	- 403 Forbidden: If the user making the request is not an admin, an error message is returned.

<br>

### Route: ('/author/<int:id>', methods=['PUT', 'PATCH'])

	- HTTP request verb: PUT, PATCH
	- Allows admins to update an author's information in the database based on the provided ID.
	- Requires a valid JWT token from admin
	- Required data: ID (int) of the author to be updated.
	
Returns: 

	- Dictionary containing the updated information of the author if successful.
	
Raises:

	- 403 Forbidden: If user making the request is not an admin, error message is returned.
	- 404 Not Found: If author with the given ID does not exist, error message is returned.

<br>
<br>

## R6 - An ERD for your app
![ERD](/docs/ERD.png)

<br>
<br>

## R7 - Detail any third party services that your app will use

The main third party services that are used/needed to build the application are bcrypt, JWT, Psycopg, Marshmallow and SQLAlchemy. Each where used extensively in the development process in order to create a functional API application and work with the database.

### bcrypt

Bcrypt is a cryptographic hashing algorithm used for hashing passwords and other personal/sensitive data. It is popular for storing passwords in databases securely as it uses multiple security features in order to prevent and avoid cyber attacks such as brute-force attacks.

<u>KEY FEATURES:</u>

Bcrypts key features include its adaptive work factor, salting and modularity. It allows for an adjustable work factor which determines the number of iterations the algorithm will perform when hashing a password. When computational power increases, the cost factor can be increased which will slow the hashing process and make it more resource-intensive. This aids in combating brute-force attacks. Salting is adding random data into the password before hashing, preventing repeats of passwords from producing the same hash. This aids in combating rainbow table attacks. Bcrypt is modular and allows for parameters to be adjusted such as the cost factor and salt length. This ensure it can adapt to any secuirty requirement changes made in the future making it flexible. These key features make bcrypt a popular choice for defence against password attacks.

<u>ADVANTAGES:</u>

Security

	- As computational power increases, Bcrypt is still able to remain secure through its adjustable cost factor. This makes it brute-force attacks significantly slower.
	- If multiple passwords are the same they will have different hashing which makes precomputed rainbow table impractical if an attack occurs.
	
Use and Implementation:

	- Widley used and available in multiple programming languages and libraries, which make it easier for developers when securing passwords in applications.

<u>WEAKNESSES:</u>

	- Performance can be impacted by it adaptive work factor as it can be slower than other hash functions if there is a high volume of password hashing requests.
	- Fixed hash lengths can also become a limitation if the system specifies a hash length. 
	
<u>PROCESS:</u>

1. Generates a random salt which is usually 128 bits long
2. Adds the randomly generated salt to the password creating the 'salted password'
3. Blowfish cipher is used by bcrypt to expand salted password into an initial key schedule
4. Multiple rounds of encryption is performed to create final hash. Number of rounds is determines by cost factor.
After specified rounds, final hash is produced (192 bits). Value is represented in a base64-encoded string. Hash will include cost factor, salt and final password.

<br>

### JWT

A JWT (JSON Web Token) is used for authentication and authorization in web applications and APIs. It securely transmits information between parties as a JSON object. They are digitally signed and typically encrypted to ensure integrity.

<u>KEY FEATURES:</u>

JWT key features are authentication, authorization, it is self-contained and stateless and uses JSON format. JWTs are represented as JSON objects which consist of a header, payload and signature. JWTs are stateless, meaning the server does not need to store session data. All the required information is contained within the JWT itself. With all necessary information embedded in the JWT, there is no need for additional database lookups, reducing latency and easier scaling. Its main feature is its authentication and authorization abilities. A user will log in and receive a JWT, which is sent with requests to prove user identity. This can also mediate what users have access to through the JWT.


<u>ADVANTAGES:</u>

Stateless

	- Servers don’t need to maintain session data. This makes them scalable and suitable for distributed systems.

Efficiency and compact

	- The format of JWTs is compact which makes them more efficient when being transmitted over a network. They store in the client-side storage such as cookies.

  Security

	- Since they are digital token that require a user to sign in, they ensure data integrity and can also be encrypted which adds another layer of security.


<u>WEAKNESS:</u>

	- Token size can increase if multiple custom claims are include, potentially increasing the size of HTTP headers and impacting performace.
	- JWTs can not be revoked once they have been issued to a user since they are stateless. To handle any revocations a time expiration on the token should be used.
	- Its important to avoid storing any personal or sensitive information in JWTs since they are not encrypted by default. 
	

<u>JWT STRUCTURE:</u>
Consists of three parts - Header, Payload, Signature

Header

	- Contains metadata about type of token and signing algorithm used.

Payload

	- Contains claims or statements about the user and other data. Can be either standard claims to custom claims that are specific to application.

Signature

	- Is created by hashing the header and payload with a secret key which are using the algorithm specified in the headers.


<u>TOKEN CREATION:</u>

Whenever a user logs in or a server needs to generate a JWT, it will construct the header and payload. Then, it calculates the signature by hashing the concatenated header and payload with a secret key. The final JWT is the concatenation of the base64-encoded header, payload, and signature.


<u>TOKEN VERIFICATION:</u>

 To verify a received JWT, the server first decodes the base64-encoded segments to retrieve the header and payload. It then recalculates the signature using the same algorithm and secret key. If the recalculated signature matches the one in the JWT, the token is considered valid.

<br>

### Psycopg

Psycopg is a Python library that provides a PostgreSQL adapter for connecting to and working with PostgreSQL databases. It is used to communicate and interact with Python applications that use PostgreSQL databases.

<u>KEY FEATURES:</u>

Psycopg's main feature is its ability to work as an adapter for PostgreSQL to communicate between Python applications and PostgreSQL databases. The thread safety feature allows multiple threads to be  able to use the same connection without conflicts occurring. Python objects and data types are handled as it automatically converts them to and from PostgreSQL data types. Parameterized queries are supported and they prevent SQL injection attacks while also improving performance by reusing query plans.


<u>ADVANTAGES:</u>

	- Large list of PostgreSQL features for support, which includes advanced data types. 
	- Fast and efficient implementation in C, which supports high-performing applications.
	- Error handling is also included as it raises exceptions during connection or query execution in order to handle errors.
	

<u>WEAKNESSES:</u>

	- It is only designed for PostgreSQL databases, which doesn't make it suitable for other DBMS.
	- Some expense issues for establishing database connections. 

<br>

### Marshmallow:

Marshmallow is used in web applications and APIs as it validates input data and makes it into a format which is suitable for storage or transmission. It converts data types to and from native data types making it a popular and powerful Python library.

<u>KEY FEATURES:</u>

Main features and advantages include serialization, deserialization, validation, nested schemas and integration with web frameworks. Serialization allows for defining serialization schemas which specifies how data structures should be converted into JSON format. Through deserialization it allows for specifying incoming data such as JSON and how it should convert into native Python data types. Validation is used to define rules and constraints for fields in the schema. This allows for errors to be raised if data doesn't meet specified criteria. Nested schemas allow for serialized and deserialized nested data structures while integration with frameworks such as Flask allow for easier building of web applications and APIs.


<u>WEAKNESSES:</u>

Marshmallow may include a learning curve for some, especially when it comes to complex data structures.

<br>

### SQLAlchemy

SQLAlchemy is a Python SQL toolkit and ORM. It is used to interact with a relational database using Python.

<u>KEY FEATURES:</u>

The main features and advantages of SQLAlchemy are it SQL expression language which provides a way to interact with a database using SQL expressions to perform CRUD operations. The ORM component allows for mapping of Python classes to the database tables. It works well with multiple database engines such as PostgreSQL which was used in this application. This provides flexibility for switching between database engine without changing application code. It allows for committing or rollback changes to a database and optimises database quires. 

<u>WEAKNESSES:</u>

	- Similar to Marshmallow can it can require a learning curve, especially with the ORM component.

<br>
<br>

Other important packages that where installed to enable the app to run are blinker, click, Jinja2, python dotenv and Wrkzeug.

Blinker: Allows communication between different parts of the application. 

Click: Package that creates command-line interface (CLIs) with easy-to-use syntax

Jinja2: Template engine that is used to generate dynamic content in web apps.

Python dotenv: Loads environment variablles from a .env file into the application's environment.

Wrkzeug: Used for Web Server Gateway Interface applications to handle HTTP requests and responses in Flask.

<br>
<br>

## R8 - Describe your projects models in terms of the relationships they have with each other

Each of the entities have been given their own models file where relationships have been establish in order to create a functional and organised database with proper relations and connections to entities. The relationships created for the models in the application allow navigation and retrieval od data from the database in order to display content, reviews, author, categories and user information efficiently and correctly. Through the structured data it allows for relevant recommendations of written content, content that can be grouped by category or author and user interaction to create reviews and rate written content.

<br>

<u>USER MODEL</u>

The 'User' model represents users that using the web application. A person must be a user with an account to be able to view, edit, change, add or delete data to the database. Users are restricted on some aspects such as editing author or category as only the admin is authorised to do so.

The attributes that are present in the user model are `id`, `first_name`, `last_name`, `year_born`, `email`, `password`, and `is_admin`. For 'is_admin', this is set to False as a default when a user first created their account.

<br>

The associations that are in the 'User' model are:

#### One-to-Many (User to Review): 

	- One user can write multiple reviews, while each review is associated with only one user. This is defined by the `reviews` relationship in the `User` model using `back_populates='user'`.

#### One-to-Many (User to Content):

	-  One user can create multiple content items, while each content item is associated with only one user. This is established through the `content` relationship in the `User` model with `back_populates='author'`.

<br>

<u>REVIEW MODEL</u>

The 'Review' model represents reviews that users have made for specific content items in the web application. A user can create, delete, edit and view reviews. A user can only edit or delete a review that they have made, not other user reviews which is mediated through user authorisation.

The attributes for the review model are  `id`, `rating`, `comment`, and `created`. 

<br>

The associations that are in the 'Review' model are:

#### Many-to-One (Review to User): 

	- Each review is written by one user, and one user can write multiple reviews. This relationship is defined using the `user_id` field in the `Review` model as a foreign key referencing the `id` field in the `User` model.
	
#### Many-to-One (Review to Content): 

	- Each review is associated with one piece of content, and each piece of content can have multiple reviews. This relationship is established using the `content_id` field in the `Review` model as a foreign key referencing the `id` field in the `Content` model.

<br>

<u>CONTENT MODEL</u>

The `Content` model represents different pieces of written content (e.g., Novels, Manga, Research Essay) created by authors

The attributes for the 'Content' model are `id`, `title`, `genre`, `description`, `published`, and `publisher`. 

<br>

The associations that are in the 'Content' model are:

#### One-to-Many (Content to Review): 

	- One content item can have multiple reviews, and each review is associated with only one content item. This is established through the `reviews` relationship in the `Content` model with `back_populates='content'`.

#### Many-to-One (Content to Author): 

	- Each content item is created by one author, and each author can create multiple content items. This relationship is defined using the `author_id` field in the `Content` model as a foreign key referencing the `id` field in the `Author` model.

#### Many-to-One (Content to Category): 

	- Each content item belongs to one category, and each category can have multiple content items. This relationship is established using the `category_id` field in the `Content` model as a foreign key referencing the `id` field in the `Category` model.

<br>

<u>CATEGORY MODEL</u>

The `Category` model represents different categories to which multiple pieces of content can belong. 

The attributes for the 'Category' model are `id` and `category`. 

<br>

The associations that are in the 'Category' model are:

#### One-to-Many (Category to Content): 

	- One category can have multiple pieces of content associated with it, and each content item is associated with only one category. This relationship is defined through the `content` relationship in the `Category` model with `back_populates='category'`.

<br>

<u>AUTHOR MODEL</u>

The `Author` model represents authors who create content items (e.g., books, movies, articles).

The attributes for the 'Author' model are `id` and `author`. 

<br>

The associations that are in the 'Author' model are:

#### One-to-Many (Author to Content):

	- One author can have multiple pieces of content, and each  pieces of content is associated with only one author. This relationship is defined through the `content` relationship in the `Author` model with `back_populates='author'`.

<br>

<u>ASSOCIATIONS</u>
- When accessing the `reviews` attribute of a `User` object, it can retrieve all the reviews written by one user.

- Through the `content` attribute of a `User` object, you can access all the content items created by that user.

- For `Content` objects, you can access their associated `reviews`, `author`, and `category`.

- The `Author` model, you can retrieve all the content items created by a specific author.

<br>

<u>CASCADE DELETES:</u>

Cascade deletes have been added to ensure normalisation of the database. If a piece of content is deleted then all related reviews will also be deleted to ensure that reviews with no related content are not sitting in the database. This applies to users as well. If a user is deleted then all reviews that they have created will be deleted too.

<br>
<br>

## R9 - Discuss the database relations to be implemented in your application

To make sure the database is normalised, creation of clear relationships between tables and no overlap of table names has been made. Ensuring that each table has a clear primary key and necessary foreign keys has been implemented. Enforcing 'characteristics' to the required aspects in the columns also ensures that the data is stored in an organised manner to ensure that the database runs smoothly.

<br>

<u><ul><b>DATABASE RELATIONSHIPS</u></ul></b>

For the author and category entities they have a mandatory relationship with the content as they must be included when creating and editing any content. This provides a organised database where a user can search for a category or author and get any related content. The review and content entities don't have a mandatory relationship since it is the users choice as to whether they want to write a review or not, since you can't review or rate something if you haven't read the content. If the user is creating a review and they don't wish to leave a comment about the content then only the rating is NOT NULL, instead of having both NOT NULL and making the user write a comment. Only users can create a review, so someone must create an account to make a review of any content. 

### One-to-Many Relationships:

<u>User and Review</u>

	- Each user can have many reviews. So for any of the content, they are able to write a review. This means that if they wish they can create one review or many reviews. They all write there own reviews.

<u>Content and Review</u>

	- Each piece of content can receive multiple reviews from multiple users. Each piece of content can have multiple reviews, but each review can be associated with only one piece of content. This is because you can't have one review relate to multiple pieces of content since the content is not the same.

<u>Content and Category</u>

	- Multiple pieces of content can belong in the same category. This makes it easier when searching for written content.

<u>Content and Author</u>

    - One author can publish multiple pieces of content. If a user likes an author then they look up all written content that they have written. 

<br>
<br>

## R10 - Describe the way tasks are allocated and tracked in your project

LINK: https://trello.com/b/bfUtFTrv/api-webserver-project

Task are tracked in an online app called Trello. To start the process I broke down the assignment into the README documentation and code and design requirements then creating a 'to do' list for each. Other list include a 'In Progress' and 'Done'. This allows me to keep track of all tasks that needed to be completed. 

In the README list, the requirements are all put on separate cards with their own headings to identify want the task is. Each card then has a description of what the task entails and the criteria for that requirement is included too. This is to make sure that everything that is needed for the requirement is within the card. This allows for an organised break down of the requirements and everything that need to be done for that one task. They are also given labels to clarify if they are for the README documentation or the code requirements. 

Other labels for the cards include whether this task has criteria that need to be meet or is a card that I have included to aid in my personal organisation. This include editing cards, what I want done or need to do in regards to that list that aren't included in the assessment break down or criteria.

This process is also done for the code requirement list to ensure that all criteria is meet for the project and I'm including everything that I need do to for my application. Each card also includes dates of when I want that card to be completed. I broke this down and did it each week. I did this so I could see my progress and what has been completed at the end of each week. This aided in allocating what I wanted to complete in the next week and to keep on top of building and managing the application. 

<b>WEEK ONE</b>
![WEEK 1 SS](/docs/Screenshot%202023-07-13%20at%206.49.50%20pm.png)
- This was the end of week one with everything that has been completed, what was in progress and tasks that still needed to be completed.

<b>WEEK TWO</b>
![WEEK 2 SS](/docs/Screenshot%202023-07-22%20at%201.33.35%20pm.png)
- This was the end of week two with everything that has been completed, what was in progress and tasks that still needed to be completed.

<b>WEEK THREE</b>
![WEEK 3 SS](/docs/Screenshot%202023-07-27%20at%201.17.41%20pm.png)

-  This was the end of Week 3 with everything completed and ready for submission

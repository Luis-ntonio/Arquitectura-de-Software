# Database Setup Instructions

This README provides short instructions on how to create the database tables using the `optional.sql` file.

## Prerequisites

* A running PostgreSQL or MySQL database server.
* A SQL client tool (e.g., `psql`, `mysql`, pgAdmin, MySQL Workbench).

## Steps

1.  **Connect to your database server** using your SQL client.

2.  **Create the database (if it doesn't exist):**

    * **PostgreSQL:** `CREATE DATABASE your_database_name;`
    * **MySQL:** `CREATE DATABASE your_database_name;`

    Replace `your_database_name` with your desired database name.

3.  **Select the database:**

    * **PostgreSQL:** `\c your_database_name`
    * **MySQL:** `USE your_database_name;`

4.  **Execute the `optional.sql` script:**

    * **Using command line:**
        * **PostgreSQL:** `psql -U your_username -d your_database_name -f optional.sql`
        * **MySQL:** `mysql -u your_username -p your_database_name < optional.sql`
    * **Using a GUI client:** Open `optional.sql` in a query window and execute it.

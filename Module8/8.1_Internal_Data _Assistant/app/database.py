import sqlite3
from pathlib import Path

#SQLite is a free and open-source relational database engine written in the C programming language. 
# It is not a standalone application; 
# rather, it is a library that software developers embed in their applications. 
# Store database file inside the project folder.

DB_PATH = Path("internal_company_data.db")



def create_demo_database():
    # Connect to SQLite database.
    # If the file does not exist, SQLite creates it.
    connection = sqlite3.connect(DB_PATH)

    # Create cursor to execute SQL commands.
    cursor = connection.cursor()

    # Create a safe demo sales table.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales_orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            region TEXT,
            product TEXT,
            order_amount REAL,
            order_status TEXT,
            email TEXT,
            username TEXT,
            password TEXT
        )
        """
    )

    # Clear old demo data so repeated runs remain consistent.
    cursor.execute("DELETE FROM sales_orders")

    # Insert sample internal business data.
    cursor.executemany(
    """
    INSERT INTO sales_orders
    (
        order_id,
        customer_name,
        region,
        product,
        order_amount,
        order_status,
        email,
        username,
        password
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    [
        (
            1,
            "ABC Retail",
            "South",
            "Analytics Platform",
            12000,
            "Completed",
            "contact@abcretail.com",
            "abcretail_admin",
            "abc123"
        ),

        (
            2,
            "Nova Foods",
            "North",
            "CRM Suite",
            8500,
            "Pending",
            "support@novafoods.com",
            "nova_ops",
            "nova123"
        ),

        (
            3,
            "Green Energy Ltd",
            "West",
            "Analytics Platform",
            15000,
            "Completed",
            "admin@greenenergy.com",
            "green_admin",
            "green123"
        ),

        (
            4,
            "Metro Logistics",
            "East",
            "Inventory AI",
            6400,
            "Completed",
            "ops@metrologistics.com",
            "metro_ops",
            "metro123"
        ),

        (
            5,
            "Blue Finance",
            "South",
            "CRM Suite",
            11000,
            "Cancelled",
            "finance@bluefinance.com",
            "blue_fin",
            "blue123"
        ),

        (
            6,
            "HealthFirst",
            "North",
            "Inventory AI",
            9300,
            "Completed",
            "admin@healthfirst.com",
            "health_admin",
            "health123"
        ),

        (
            7,
            "Sky Retail",
            "East",
            "Analytics Platform",
            7200,
            "Pending",
            "sales@skyretail.com",
            "sky_sales",
            "sky123"
        ),

        (
            8,
            "Quantum Telecom",
            "West",
            "CRM Suite",
            21000,
            "Completed",
            "admin@quantumtel.com",
            "quantum_admin",
            "quantum123"
        ),

        (
            9,
            "Urban Fashion",
            "South",
            "Inventory AI",
            4800,
            "Completed",
            "support@urbanfashion.com",
            "urban_support",
            "urban123"
        ),

        (
            10,
            "NextGen Labs",
            "North",
            "Analytics Platform",
            17800,
            "Pending",
            "labs@nextgen.com",
            "nextgen_labs",
            "next123"
        ),

        (
            11,
            "Prime Logistics",
            "East",
            "CRM Suite",
            9900,
            "Completed",
            "contact@primelogistics.com",
            "prime_admin",
            "prime123"
        ),

        (
            12,
            "DigitalCore",
            "West",
            "Inventory AI",
            13500,
            "Completed",
            "admin@digitalcore.com",
            "digital_admin",
            "digital123"
        ),

        (
            13,
            "Bright Health",
            "South",
            "Analytics Platform",
            8200,
            "Cancelled",
            "support@brighthealth.com",
            "bright_support",
            "bright123"
        ),

        (
            14,
            "Future Mobility",
            "North",
            "CRM Suite",
            16500,
            "Completed",
            "mobility@futuremobility.com",
            "future_mobility",
            "future123"
        ),

        (
            15,
            "SmartBuild",
            "East",
            "Inventory AI",
            14300,
            "Pending",
            "admin@smartbuild.com",
            "smart_admin",
            "smart123"
        ),
    ],
)

    # Save database changes.
    connection.commit()

    # Close database connection.
    connection.close()


def run_read_only_query(sql_query: str):
    # Open database connection.
    connection = sqlite3.connect(DB_PATH)

    # Return rows as dictionaries instead of tuples.
    connection.row_factory = sqlite3.Row

    # Create cursor.
    cursor = connection.cursor()

    # Execute read-only SQL query.
    cursor.execute(sql_query)

    # Fetch all rows from query result.
    rows = cursor.fetchall()

    # Convert rows into list of dictionaries.
    results = [dict(row) for row in rows]

    # Close connection.
    connection.close()

    # Return query results.
    return results
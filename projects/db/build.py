import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    if database.exists():
        database.unlink()

    with duckdb.connect(database) as _con:

    ### Members Table
    # Stores loyalty members' names, contact details, joining dates and points balances.


        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                mobile VARCHAR NOT NULL,
                email VARCHAR,
                join_date DATE NOT NULL,
                points_balance INTEGER NOT NULL CHECK (points_balance >= 0)
            )
        """)

    ### Products Table
    # Stores menu items, categories, prices, costs and availability.


        _con.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR NOT NULL
                    CHECK (category IN ('coffee', 'tea', 'food', 'other')),
                price DECIMAL(10,2) NOT NULL,
                cost DECIMAL(10,2) NOT NULL,
                available_today BOOLEAN NOT NULL,
                CHECK (price >= cost)
            )
        """)

    ### Options Table
    # Stores the add-ons customers can choose, along with their prices and costs.
        _con.execute("""
            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0)
            )
        """)

    ### Orders Table

        _con.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                ordered_at TIMESTAMP NOT NULL,
                member_id INTEGER,
                channel VARCHAR NOT NULL
                    CHECK (channel IN ('counter', 'app')),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)

     ### Order Lines Table
        # Stores the products purchased in each order.

        _con.execute("""
            CREATE TABLE order_lines (
                line_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

    ### Line Options Table
        # Stores the add-ons selected for each order line.

        _con.execute("""
           CREATE TABLE line_options (
                line_id INTEGER NOT NULL,
                option_id INTEGER NOT NULL,
                price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0),
                PRIMARY KEY (line_id, option_id),
                FOREIGN KEY (line_id) REFERENCES order_lines(line_id),
                FOREIGN KEY (option_id) REFERENCES options(option_id)
            )
        """)

    ### Payments Table
        # Stores payments made for each order, including split payments.

        _con.execute("""
            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                method VARCHAR NOT NULL
                    CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

        data_folder = mo.notebook_dir() / "data"

        for table_name in [
            "members",
            "products",
            "options",
            "orders",
            "order_lines",
            "line_options",
            "payments"
        ]:
            csv_file = data_folder / f"{table_name}.csv"

            _con.execute(
                f"INSERT INTO {table_name} "
                f"SELECT * FROM read_csv_auto(?)",
                [str(csv_file)]
            )

        # Create a view showing product sales

        _con.execute("""
            CREATE VIEW product_sales AS
            SELECT
                p.product_id,
                p.name,
                SUM(ol.quantity) AS units_sold,
                SUM(ol.quantity * ol.unit_price) AS revenue
            FROM products p
            JOIN order_lines ol
                ON p.product_id = ol.product_id
            GROUP BY p.product_id, p.name
        """)
     

    return database, duckdb


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS total_members FROM members")
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'members' AS table_name, COUNT(*) AS total_rows FROM members
        UNION ALL
        SELECT 'products', COUNT(*) FROM products
        UNION ALL
        SELECT 'options', COUNT(*) FROM options
        UNION ALL
        SELECT 'orders', COUNT(*) FROM orders
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM order_lines
        UNION ALL
        SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL
        SELECT 'payments', COUNT(*) FROM payments
    """)

    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(ask):
    ask("SHOW TABLES")
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data was generated using `make_data.py` and saved as seven CSV files in the `data` folder.

    I generated 50 loyalty members, 25 products, 10 options, 1,200 orders, 2,377 order lines, 2,064 line options and 1,515 payments.

    The data covers the 12-month period ending November 1, 2026. I used a fixed random seed of 6301 so the same data is generated each time.

    I intentionally made the payment totals for Orders 1 and 2 incorrect by adding $1.00 to each. I will check for these differences using SQL in Part B.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data
    """)
    return


@app.cell
def _(mo):
    import polars as pl

    orders_data = pl.read_csv(
        mo.notebook_dir() / "data" / "orders.csv",
        try_parse_dates=True
    )

    hourly_orders = (
        orders_data
        .with_columns(
            pl.col("ordered_at").dt.hour().alias("hour")
        )
        .group_by("hour")
        .agg(pl.len().alias("number_of_orders"))
        .sort("hour")
    )

    hourly_orders
    return (hourly_orders,)


@app.cell
def _(hourly_orders, mo):
    import altair as alt

    chart = (
        alt.Chart(hourly_orders)
        .mark_bar(color="steelblue", size=35)
        .encode(
            x=alt.X(
                "hour:O",
                title="Hour of the Day",
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=15,
                    titleFontSize=18
                )
            ),
            y=alt.Y(
                "number_of_orders:Q",
                title="Number of Orders",
                axis=alt.Axis(
                    labelFontSize=15,
                    titleFontSize=18
                ),
                scale=alt.Scale(domainMin=0)
            ),
            tooltip=["hour", "number_of_orders"]
        )
        .properties(
            title=alt.TitleParams(
                text="Babson Bean Café: Orders by Hour",
                fontSize=22,
                anchor="middle"
            ),
            width=700,
            height=400
        )
        .configure_view(stroke=None)
    )

    mo.ui.altair_chart(chart)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Initially, my data showed orders spread almost evenly throughout the day, which did not seem realistic for a campus café. I changed the order generation in make_data.py to make mornings and lunchtime busier. The updated chart now shows the highest number of orders around 9 AM and another busy period between 12 PM and 1 PM, with fewer orders later in the afternoon. This seems more realistic for a café serving students.## Summary

    By adjusting the order generation logic to weight morning and lunchtime hours more heavily, the synthetic data now reflects realistic café traffic patterns. This makes the dashboard more useful for identifying true peak hours, which could help with staffing decisions or inventory planning in a real-world scenario.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'members' AS table_name, COUNT(*) AS total_rows FROM members
        UNION ALL
        SELECT 'products', COUNT(*) FROM products
        UNION ALL
        SELECT 'options', COUNT(*) FROM options
        UNION ALL
        SELECT 'orders', COUNT(*) FROM orders
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM order_lines
        UNION ALL
        SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL
        SELECT 'payments', COUNT(*) FROM payments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 5: A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO products
                (product_id, name, category, price, cost, available_today)
                VALUES (999, 'Test Latte', 'coffee', 2.00, 5.00, TRUE)
            """)
    except Exception as e:
        print("Database refused the row:")
        print(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 6: Answers You Already Knew
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I generated the data using make_data.py, so I already know the answers to these three questions before running the SQL queries.

    How many loyalty members are there? I expect 50 because my script generated 50 members.

    How many products are on the menu? I expect 25 because I included 25 menu items.

    How many orders were generated? I expect 1,200 because my script created 1,200 orders.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'Members' AS question, COUNT(*) AS actual FROM members
        UNION ALL
        SELECT 'Products', COUNT(*) FROM products
        UNION ALL
        SELECT 'Orders', COUNT(*) FROM orders
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 7: A View
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT *
        FROM product_sales
        ORDER BY revenue DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I created a view called product_sales to track how many units of each product were sold and the revenue generated, excluding add-ons. Espresso had the highest product revenue at $1,268.76, followed by Brownie at $1,242.15. The café can use this view regularly to see which products are generating the most sales without rewriting the SQL query.
    """)
    return


if __name__ == "__main__":
    app.run()

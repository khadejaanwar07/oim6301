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
    # 1. The Tables
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

    
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

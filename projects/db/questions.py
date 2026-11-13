import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return


@app.cell
def _():
    from datetime import date

    as_of = date(2026, 11, 1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B: Babson Bean Café

    ## 1. Business Questions

    ## 2. How I Know These Numbers Are Right

    ## 3. Working With the Agent

    ## 4. Reading It Back

    Prediction: Question 2

    I chose Question 2, which calculates revenue, cost and margin by product category using the PRODUCTS, ORDER_LINES and LINE_OPTIONS tables.

    I have 2,405 order lines and 2,122 line options. I predict the joins will produce around 3,500 rows before grouping. I'm using a LEFT JOIN because some order lines have multiple add-ons while others have none. This means every order line will appear at least once, and lines with multiple add-ons will appear more than once.

    I'll compare my prediction with the actual number of rows and explain any difference.

    ## 5. Going Further

    ## 6. Time Spent
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

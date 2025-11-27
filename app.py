from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from ads_mcp.tools.search import search  # reuses your existing search tool

app = FastAPI()


def _base_html(content: str) -> str:
    """Wraps inner content with a simple, pleasant layout + styles."""
    return f"""
    <html>
      <head>
        <title>Google Ads MCP UI</title>
        <style>
          body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f5f5fb;
            margin: 0;
            padding: 0;
          }}
          .page {{
            max-width: 900px;
            margin: 40px auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            padding: 24px 32px 32px;
          }}
          h1 {{
            margin-top: 0;
            font-size: 28px;
          }}
          p.helper {{
            color: #555;
            margin-top: 4px;
          }}
          form {{
            margin-top: 16px;
            display: grid;
            grid-template-columns: 180px 1fr;
            grid-row-gap: 10px;
            grid-column-gap: 12px;
            align-items: center;
          }}
          label {{
            font-weight: 600;
            font-size: 14px;
          }}
          input[type="text"],
          input[type="number"] {{
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 14px;
          }}
          .full-row {{
            grid-column: 1 / -1;
          }}
          button {{
            margin-top: 16px;
            grid-column: 1 / -1;
            justify-self: flex-start;
            padding: 8px 18px;
            border-radius: 999px;
            border: none;
            background: #1a73e8;
            color: white;
            font-weight: 600;
            cursor: pointer;
          }}
          button:hover {{
            background: #155ec0;
          }}
          .results {{
            margin-top: 24px;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
          }}
          th, td {{
            border: 1px solid #eee;
            padding: 6px 8px;
            text-align: left;
          }}
          th {{
            background: #fafafa;
          }}
          .error {{
            margin-top: 16px;
            padding: 10px 12px;
            border-radius: 6px;
            background: #fde4e4;
            color: #8b1a1a;
            font-size: 13px;
          }}
          .back-link {{
            display: inline-block;
            margin-bottom: 12px;
            text-decoration: none;
            color: #1a73e8;
            font-size: 14px;
          }}
        </style>
      </head>
      <body>
        <div class="page">
          {content}
        </div>
      </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    inner = """
      <h1>Google Ads Search</h1>
      <p class="helper">
        Enter a Google Ads customer ID and choose a simple query to test the MCP server.
      </p>
      <form method="post" action="/search">
        <label>Customer ID (no dashes):</label>
        <input type="text" name="customer_id" placeholder="1234567890" />

        <label>Resource:</label>
        <input type="text" name="resource" value="campaign" />

        <label>Fields (comma separated):</label>
        <input type="text" name="fields" value="campaign.id,campaign.name" />

        <label>Limit:</label>
        <input type="number" name="limit" value="10" min="1" max="1000" />

        <div class="full-row">
          <small>
            Tip: start with a small customer and a low limit (e.g. 10) so responses stay fast.
          </small>
        </div>

        <button type="submit">Run search</button>
      </form>
    """
    return _base_html(inner)


@app.post("/search", response_class=HTMLResponse)
def run_search(
    customer_id: str = Form(...),
    resource: str = Form(...),
    fields: str = Form(...),
    limit: str = Form("10"),
):
    try:
        fields_list = [f.strip() for f in fields.split(",") if f.strip()]

        results = search(
            customer_id=customer_id,
            fields=fields_list,
            resource=resource,
            conditions=[],
            orderings=[],
            limit=limit,
        )

        if results:
            # Build a simple table from the first row's keys.
            columns = list(results[0].keys())
            header_html = "".join(f"<th>{col}</th>" for col in columns)
            rows_html = ""
            for row in results:
                cells = "".join(f"<td>{row.get(col, '')}</td>" for col in columns)
                rows_html += f"<tr>{cells}</tr>"

            results_html = f"""
              <div class="results">
                <h2>Results ({len(results)} rows)</h2>
                <table>
                  <thead><tr>{header_html}</tr></thead>
                  <tbody>{rows_html}</tbody>
                </table>
              </div>
            """
        else:
            results_html = """
              <div class="results">
                <h2>No results</h2>
                <p>No rows were returned for this query. Try a different customer ID or resource.</p>
              </div>
            """

        inner = f"""
          <a href="/" class="back-link">&larr; Back</a>
          <h1>Google Ads Search</h1>
          {results_html}
        """
        return _base_html(inner)

    except Exception as exc:
        inner = f"""
          <a href="/" class="back-link">&larr; Back</a>
          <h1>Google Ads Search</h1>
          <div class="error">
            <strong>Error while running search:</strong><br/>
            {type(exc).__name__}: {str(exc)}
          </div>
        """
        return _base_html(inner)
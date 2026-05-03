#!/usr/bin/env python3
"""
Weekly SEO Email Report — Rose Medical Pavilion
================================================
Pulls data from Google Search Console, GA4, and (optionally) a SERP API,
then formats a clean HTML email and sends it via Gmail SMTP.

Cron example (every Monday at 7 AM):
    0 7 * * 1 /usr/bin/python3 /path/to/seo_report.py

Environment variables required:
    GOOGLE_SERVICE_ACCOUNT_JSON   Path to a single service account JSON that
                                  has been granted access to both GSC and GA4
                                  (or set separate paths; see CREDS_ vars below)
    GSC_PROPERTY                  https://rosemedicalpavilion.com
    GA4_PROPERTY_ID               properties/534869539
    SMTP_USER                     Gmail address (e.g. you@gmail.com)
    SMTP_PASS                     Gmail App Password (not your login password)

Optional — competitor SERP data (choose one provider):
    SERPAPI_KEY                   Key from serpapi.com  (free tier: 100 searches/mo)
    DATAFORSEO_LOGIN              DataForSEO login email
    DATAFORSEO_PASSWORD           DataForSEO API password

    If neither key is set the Competitor Snapshot section will display a
    placeholder table instructing you to add one.

Recipients:
    REPORT_TO   Comma-separated email list (defaults to benjaminsher@gmail.com)
"""

import os
import sys
import json
import smtplib
import traceback
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------------------------------------------------------------------
# Configuration — override via env vars or edit defaults here
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

# Credential file: single shared SA or two separate ones
_SA_JSON = os.environ.get(
    "GOOGLE_SERVICE_ACCOUNT_JSON",
    os.path.join(SCRIPT_DIR, "../credentials/ga4-service-account.json")
)
GSC_CREDS_PATH = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", _SA_JSON)
GA4_CREDS_PATH = os.environ.get("GA4_SERVICE_ACCOUNT_JSON", _SA_JSON)

GSC_PROPERTY   = os.environ.get("GSC_PROPERTY", "https://rosemedicalpavilion.com")
GA4_PROPERTY   = os.environ.get("GA4_PROPERTY_ID", "properties/534869539")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

REPORT_TO = [
    a.strip()
    for a in os.environ.get("REPORT_TO", "benjaminsher@gmail.com").split(",")
    if a.strip()
]

SERPAPI_KEY         = os.environ.get("SERPAPI_KEY", "")
DATAFORSEO_LOGIN    = os.environ.get("DATAFORSEO_LOGIN", "")
DATAFORSEO_PASSWORD = os.environ.get("DATAFORSEO_PASSWORD", "")

# Key terms to track for competitor snapshot
COMPETITOR_KEYWORDS = [
    "pediatric neurologist phoenix",
    "pediatric epilepsy phoenix",
    "child neurologist phoenix az",
    "pediatric neurology scottsdale",
    "children's neurologist arizona",
    "pediatric headache specialist phoenix",
    "adhd specialist children phoenix az",
    "epilepsy doctor children phoenix",
]

# Competitors to watch for in results (domain fragments, lowercase)
COMPETITOR_DOMAINS = [
    "rosemedicalpavilion.com",
    "phoenixchildrens.org",
    "bannerhealth.com",
    "dignityhealth.org",
    "honorhealth.com",
    "azbrainandspine.com",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_section(name, fn):
    """Run fn(); on exception return an error HTML block instead of crashing."""
    try:
        return fn()
    except Exception:
        tb = traceback.format_exc()
        return f"""
        <div class="section error">
          <h2>{name}</h2>
          <p class="err">This section could not be loaded. Error details:</p>
          <pre>{tb}</pre>
        </div>"""


def _pct(val):
    return f"{float(val) * 100:.1f}%"


def _pos(val):
    return f"{float(val):.1f}"


def _num(val):
    return f"{int(round(float(val))):,}"


# ---------------------------------------------------------------------------
# 1. Google Search Console
# ---------------------------------------------------------------------------

def _gsc_service():
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_file(
        GSC_CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    return build("searchconsole", "v1", credentials=creds)


def _gsc_query(service, start, end, dimensions, row_limit=10):
    body = {
        "startDate": str(start),
        "endDate":   str(end),
        "dimensions": dimensions,
        "rowLimit":   row_limit,
        "orderBy":    [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
    result = service.searchanalytics().query(
        siteUrl=GSC_PROPERTY, body=body
    ).execute()
    return result.get("rows", [])


def fetch_gsc():
    """Return (current_rows_query, prior_rows_query, current_rows_page,
               prior_rows_page, current_totals, prior_totals)."""
    service = _gsc_service()

    # GSC has ~3-day data lag
    end_cur   = date.today() - timedelta(days=3)
    start_cur = end_cur - timedelta(days=6)        # 7-day window
    end_pri   = start_cur - timedelta(days=1)
    start_pri = end_pri - timedelta(days=6)        # prior 7-day window

    # Top 10 queries — current period
    q_cur  = _gsc_query(service, start_cur, end_cur, ["query"], 10)
    # Top 10 queries — prior period (same queries, so we can compare)
    # We pull top 500 for the prior period and match by key later
    q_pri_all = _gsc_query(service, start_pri, end_pri, ["query"], 500)
    q_pri_map = {r["keys"][0]: r for r in q_pri_all}

    # Top 10 pages — current period
    p_cur = _gsc_query(service, start_cur, end_cur, ["page"], 10)
    p_pri_all = _gsc_query(service, start_pri, end_pri, ["page"], 500)
    p_pri_map = {r["keys"][0]: r for r in p_pri_all}

    # Site-wide totals (no dimension filter, rowLimit=1 still returns aggregate)
    def site_totals(start, end):
        body = {
            "startDate": str(start),
            "endDate":   str(end),
            "dimensions": [],   # no breakdown → site aggregate
            "rowLimit":   1,
        }
        rows = service.searchanalytics().query(
            siteUrl=GSC_PROPERTY, body=body
        ).execute().get("rows", [])
        if rows:
            r = rows[0]
            return {
                "clicks":      r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "ctr":         r.get("ctr", 0),
                "position":    r.get("position", 0),
            }
        return {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}

    cur_totals = site_totals(start_cur, end_cur)
    pri_totals = site_totals(start_pri, end_pri)

    return (
        q_cur, q_pri_map,
        p_cur, p_pri_map,
        cur_totals, pri_totals,
        start_cur, end_cur,
        start_pri, end_pri,
    )


# ---------------------------------------------------------------------------
# 2. GA4
# ---------------------------------------------------------------------------

def fetch_ga4():
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest, OrderBy,
    )
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        GA4_CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    end   = date.today()
    start = end - timedelta(days=6)  # 7-day window

    def run(dimensions, metrics, order_metric=None, limit=25):
        order_bys = []
        if order_metric:
            order_bys = [OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name=order_metric),
                desc=True,
            )]
        req = RunReportRequest(
            property=GA4_PROPERTY,
            date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            order_bys=order_bys,
            limit=limit,
        )
        return client.run_report(req)

    # Sessions by source / medium
    sources = run(
        dimensions=["sessionSourceMedium"],
        metrics=["sessions"],
        order_metric="sessions",
        limit=20,
    )

    # Overview — sessions, users, new users
    overview = run(
        dimensions=[],
        metrics=["sessions", "totalUsers", "newUsers", "bounceRate",
                 "averageSessionDuration"],
    )

    return sources, overview, start, end


# ---------------------------------------------------------------------------
# 3. Competitor Snapshot via SerpAPI or DataForSEO
# ---------------------------------------------------------------------------

def _rank_via_serpapi(keyword):
    """Return list of (position, domain) using SerpAPI. Max 10 results."""
    import urllib.request
    import urllib.parse
    params = urllib.parse.urlencode({
        "q":      keyword,
        "location": "Phoenix, Arizona, United States",
        "hl":    "en",
        "gl":    "us",
        "api_key": SERPAPI_KEY,
        "num":   10,
    })
    url = f"https://serpapi.com/search.json?{params}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read())
    results = []
    for item in data.get("organic_results", []):
        link = item.get("link", "")
        pos  = item.get("position", 99)
        domain = link.split("/")[2] if "//" in link else link
        results.append((pos, domain.replace("www.", "")))
    return results


def _rank_via_dataforseo(keyword):
    """Return list of (position, domain) using DataForSEO Live SERP endpoint."""
    import urllib.request
    import base64
    creds_b64 = base64.b64encode(
        f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}".encode()
    ).decode()
    payload = json.dumps([{
        "keyword":       keyword,
        "location_name": "Phoenix,Arizona,United States",
        "language_code": "en",
        "depth":         10,
        "se_type":       "organic",
    }]).encode()
    req = urllib.request.Request(
        "https://api.dataforseo.com/v3/serp/google/organic/live/regular",
        data=payload,
        headers={
            "Authorization": f"Basic {creds_b64}",
            "Content-Type":  "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())
    results = []
    tasks = data.get("tasks", [])
    if tasks:
        items = (
            tasks[0]
            .get("result", [{}])[0]
            .get("items", [])
        )
        for item in items:
            if item.get("type") == "organic":
                domain = item.get("domain", "").replace("www.", "")
                pos    = item.get("rank_absolute", 99)
                results.append((pos, domain))
    return results


def fetch_competitor_rankings():
    """
    Returns list of dicts:
      { keyword, our_rank, results: [(pos, domain), ...] }

    Uses SerpAPI if SERPAPI_KEY is set, DataForSEO if those creds are set,
    otherwise returns placeholder data.
    """
    rows = []
    use_serpapi    = bool(SERPAPI_KEY)
    use_dataforseo = bool(DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD)

    for kw in COMPETITOR_KEYWORDS:
        try:
            if use_serpapi:
                results = _rank_via_serpapi(kw)
            elif use_dataforseo:
                results = _rank_via_dataforseo(kw)
            else:
                results = []  # placeholder mode

            our_rank = "—"
            for pos, domain in results:
                if "rosemedicalpavilion.com" in domain:
                    our_rank = pos
                    break

            rows.append({
                "keyword":  kw,
                "our_rank": our_rank,
                "results":  results[:5],  # top 5 for display
                "live":     use_serpapi or use_dataforseo,
            })
        except Exception as exc:
            rows.append({
                "keyword":  kw,
                "our_rank": "error",
                "results":  [],
                "live":     False,
                "error":    str(exc),
            })

    return rows


# ---------------------------------------------------------------------------
# 4. HTML Report Builder
# ---------------------------------------------------------------------------

CSS = """
<style>
  body { font-family: Arial, Helvetica, sans-serif; background: #f4f6f8;
         margin: 0; padding: 20px; color: #333; }
  .wrapper { max-width: 780px; margin: auto; background: #fff;
             border-radius: 8px; overflow: hidden;
             box-shadow: 0 2px 8px rgba(0,0,0,.12); }
  .header  { background: #1a3d6e; color: #fff; padding: 24px 32px; }
  .header h1 { margin: 0 0 4px; font-size: 22px; }
  .header p  { margin: 0; font-size: 13px; opacity: .8; }
  .section   { padding: 24px 32px; border-bottom: 1px solid #e8ecf0; }
  .section:last-child { border-bottom: none; }
  .section h2 { margin: 0 0 16px; font-size: 17px; color: #1a3d6e;
                border-left: 4px solid #2b7de9; padding-left: 10px; }
  table  { width: 100%; border-collapse: collapse; font-size: 13px; }
  th     { background: #f0f4f9; text-align: left; padding: 8px 10px;
           border-bottom: 2px solid #d0d8e4; white-space: nowrap; }
  td     { padding: 7px 10px; border-bottom: 1px solid #eef0f3;
           vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  .up    { color: #1a8a3a; font-weight: bold; }
  .down  { color: #c0392b; font-weight: bold; }
  .flat  { color: #888; }
  .kpi-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }
  .kpi  { flex: 1; min-width: 130px; background: #f0f4f9;
          border-radius: 6px; padding: 14px 16px; }
  .kpi .label { font-size: 11px; text-transform: uppercase;
                letter-spacing: .05em; color: #666; }
  .kpi .value { font-size: 24px; font-weight: bold; color: #1a3d6e;
                margin: 4px 0 2px; }
  .kpi .delta { font-size: 12px; }
  .badge-1  { background: #fff3cd; color: #7d5a00;
              border-radius: 12px; padding: 2px 8px; font-size: 11px; }
  .badge-top { background: #d4edda; color: #155724;
               border-radius: 12px; padding: 2px 8px; font-size: 11px; }
  .err  { color: #c0392b; }
  pre   { background: #f7f7f7; padding: 10px; border-radius: 4px;
          font-size: 11px; overflow-x: auto; white-space: pre-wrap; }
  .placeholder { background: #fff8e1; border: 1px dashed #f0ad4e;
                 border-radius: 6px; padding: 14px 16px; font-size: 13px; }
  .footer { background: #f0f4f9; padding: 14px 32px; font-size: 11px;
            color: #888; text-align: center; }
</style>
"""


def _delta_html(cur, pri, higher_is_better=True, fmt=None):
    """Return coloured delta string."""
    if pri == 0:
        return '<span class="flat">—</span>'
    diff = cur - pri
    if fmt == "pct":
        label = f"{diff * 100:+.1f}pp"
    elif fmt == "pos":
        # position: lower is better, so flip sign for colour
        label = f"{diff:+.1f}"
        higher_is_better = False  # already accounted for below
        # For position, lower number = better, so diff<0 is good
        is_good = diff < 0 if not higher_is_better else diff > 0
        cls = "up" if is_good else ("down" if diff != 0 else "flat")
        return f'<span class="{cls}">{label}</span>'
    else:
        pct = (diff / pri) * 100
        label = f"{diff:+,.0f} ({pct:+.1f}%)"
    is_good = diff > 0 if higher_is_better else diff < 0
    cls = "up" if is_good else ("down" if diff != 0 else "flat")
    return f'<span class="{cls}">{label}</span>'


def build_traffic_summary(cur, pri, start_cur, end_cur, start_pri, end_pri):
    def kpi(label, c_val, p_val, higher_is_better=True, fmt=None):
        if fmt == "pct":
            display = _pct(c_val)
        elif fmt == "pos":
            display = _pos(c_val)
        else:
            display = _num(c_val)
        delta = _delta_html(float(c_val), float(p_val), higher_is_better, fmt)
        return f"""
        <div class="kpi">
          <div class="label">{label}</div>
          <div class="value">{display}</div>
          <div class="delta">vs prior week: {delta}</div>
        </div>"""

    kpis = (
        kpi("Clicks",         cur["clicks"],      pri["clicks"])
        + kpi("Impressions",  cur["impressions"],  pri["impressions"])
        + kpi("Avg CTR",      cur["ctr"],          pri["ctr"],          fmt="pct")
        + kpi("Avg Position", cur["position"],     pri["position"],
              higher_is_better=False, fmt="pos")
    )
    return f"""
    <div class="section">
      <h2>Traffic Summary
        <span style="font-size:12px;font-weight:normal;color:#666;margin-left:8px;">
          {start_cur} to {end_cur} vs {start_pri} to {end_pri}
        </span>
      </h2>
      <div class="kpi-grid">{kpis}</div>
    </div>"""


def build_top_queries(q_cur, q_pri_map):
    rows_html = ""
    for r in q_cur:
        kw       = r["keys"][0]
        clicks   = r.get("clicks", 0)
        impr     = r.get("impressions", 0)
        ctr      = r.get("ctr", 0)
        pos      = r.get("position", 0)
        pri      = q_pri_map.get(kw, {})
        d_clicks = _delta_html(clicks, pri.get("clicks", 0))
        d_pos    = _delta_html(pos, pri.get("position", 0),
                               higher_is_better=False, fmt="pos")
        rows_html += f"""
        <tr>
          <td>{kw}</td>
          <td>{_num(clicks)}</td>
          <td>{d_clicks}</td>
          <td>{_num(impr)}</td>
          <td>{_pct(ctr)}</td>
          <td>{_pos(pos)} {d_pos}</td>
        </tr>"""
    return f"""
    <div class="section">
      <h2>Top 10 Queries by Clicks</h2>
      <table>
        <thead><tr>
          <th>Query</th><th>Clicks</th><th>vs Prior</th>
          <th>Impressions</th><th>CTR</th><th>Avg Position</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_top_pages(p_cur, p_pri_map):
    rows_html = ""
    for r in p_cur:
        page     = r["keys"][0].replace(GSC_PROPERTY, "")
        clicks   = r.get("clicks", 0)
        impr     = r.get("impressions", 0)
        ctr      = r.get("ctr", 0)
        pos      = r.get("position", 0)
        pri      = p_pri_map.get(r["keys"][0], {})
        d_clicks = _delta_html(clicks, pri.get("clicks", 0))
        d_pos    = _delta_html(pos, pri.get("position", 0),
                               higher_is_better=False, fmt="pos")
        display_page = page if len(page) < 55 else page[:52] + "…"
        rows_html += f"""
        <tr>
          <td title="{page}"><code style="font-size:11px">{display_page}</code></td>
          <td>{_num(clicks)}</td>
          <td>{d_clicks}</td>
          <td>{_num(impr)}</td>
          <td>{_pct(ctr)}</td>
          <td>{_pos(pos)} {d_pos}</td>
        </tr>"""
    return f"""
    <div class="section">
      <h2>Top 10 Pages by Clicks</h2>
      <table>
        <thead><tr>
          <th>Page</th><th>Clicks</th><th>vs Prior</th>
          <th>Impressions</th><th>CTR</th><th>Avg Position</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_traffic_sources(sources, overview, start, end):
    # overview totals
    ov_html = ""
    if overview.rows:
        r = overview.rows[0]
        mv = lambda i: r.metric_values[i].value
        ov_html = f"""
        <div class="kpi-grid" style="margin-bottom:20px">
          <div class="kpi"><div class="label">Sessions</div>
            <div class="value">{_num(mv(0))}</div></div>
          <div class="kpi"><div class="label">Total Users</div>
            <div class="value">{_num(mv(1))}</div></div>
          <div class="kpi"><div class="label">New Users</div>
            <div class="value">{_num(mv(2))}</div></div>
          <div class="kpi"><div class="label">Bounce Rate</div>
            <div class="value">{float(mv(3))*100:.1f}%</div></div>
          <div class="kpi"><div class="label">Avg Session</div>
            <div class="value">{float(mv(4)):.0f}s</div></div>
        </div>"""

    total_sessions = sum(
        int(row.metric_values[0].value) for row in sources.rows
    ) or 1
    rows_html = ""
    for row in sources.rows:
        src  = row.dimension_values[0].value
        sess = int(row.metric_values[0].value)
        pct  = sess / total_sessions * 100
        bar  = f'<div style="background:#2b7de9;height:6px;border-radius:3px;width:{min(pct,100):.0f}%;margin-top:4px"></div>'
        rows_html += f"""
        <tr>
          <td>{src}</td>
          <td>{_num(sess)}</td>
          <td>{pct:.1f}%{bar}</td>
        </tr>"""

    return f"""
    <div class="section">
      <h2>Traffic Sources
        <span style="font-size:12px;font-weight:normal;color:#666;margin-left:8px;">
          GA4 · {start} to {end}
        </span>
      </h2>
      {ov_html}
      <table>
        <thead><tr><th>Source / Medium</th><th>Sessions</th><th>Share</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_competitor_snapshot(comp_rows):
    has_live = any(r.get("live") for r in comp_rows)

    if not has_live:
        return f"""
    <div class="section">
      <h2>Competitor Snapshot</h2>
      <div class="placeholder">
        <strong>No SERP API key configured.</strong><br>
        To enable live competitor rankings, set one of these environment variables
        and re-run the script:<br><br>
        <code>SERPAPI_KEY=your_key_here</code> — free tier at
        <a href="https://serpapi.com">serpapi.com</a> (100 searches/month)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&mdash; or &mdash;<br>
        <code>DATAFORSEO_LOGIN=your@email.com</code> +
        <code>DATAFORSEO_PASSWORD=your_pass</code> — pay-per-use at
        <a href="https://dataforseo.com">dataforseo.com</a>
        (~$0.002 per keyword check)<br><br>
        Keywords that will be tracked once configured:
        <ul style="margin:8px 0 0">
          {''.join(f"<li>{kw}</li>" for kw in COMPETITOR_KEYWORDS)}
        </ul>
      </div>
    </div>"""

    rows_html = ""
    for r in comp_rows:
        kw       = r["keyword"]
        our_rank = r["our_rank"]
        rank_cls = ""
        if isinstance(our_rank, int):
            if our_rank <= 3:
                rank_cls = "badge-top"
            elif our_rank <= 10:
                rank_cls = "badge-1"

        rank_display = (
            f'<span class="{rank_cls}">{our_rank}</span>'
            if rank_cls else str(our_rank)
        )

        top5 = r.get("results", [])
        top5_html = ", ".join(
            f"<strong>{d}</strong>" if "rosemedicalpavilion" in d else d
            for _, d in top5[:5]
        ) if top5 else "—"

        error_html = (
            f'<br><small class="err">{r["error"]}</small>'
            if r.get("error") else ""
        )
        rows_html += f"""
        <tr>
          <td>{kw}</td>
          <td style="text-align:center">{rank_display}{error_html}</td>
          <td style="font-size:11px;color:#555">{top5_html}</td>
        </tr>"""

    return f"""
    <div class="section">
      <h2>Competitor Snapshot</h2>
      <table>
        <thead><tr>
          <th>Keyword</th>
          <th style="text-align:center">Our Rank</th>
          <th>Top Results</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_html_report(sections_html, report_date):
    body = "".join(sections_html)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SEO Report — Rose Medical Pavilion — {report_date}</title>
  {CSS}
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>SEO Weekly Report — Rose Medical Pavilion</h1>
      <p>rosemedicalpavilion.com &nbsp;|&nbsp; Generated {report_date}</p>
    </div>
    {body}
    <div class="footer">
      Automated report generated by seo_report.py &nbsp;&bull;&nbsp;
      Data sources: Google Search Console, GA4{", SerpAPI" if SERPAPI_KEY else ""}
      {", DataForSEO" if DATAFORSEO_LOGIN else ""}
    </div>
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 5. Send email
# ---------------------------------------------------------------------------

def send_email(html_body, report_date):
    if not SMTP_USER or not SMTP_PASS:
        print("[WARN] SMTP_USER or SMTP_PASS not set — printing report to stdout.")
        print(html_body)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"SEO Report — Rose Medical Pavilion — {report_date}"
    msg["From"]    = SMTP_USER
    msg["To"]      = ", ".join(REPORT_TO)

    # Plain-text fallback
    plain = (
        f"SEO Weekly Report for rosemedicalpavilion.com\n"
        f"Generated {report_date}\n\n"
        f"View this email in an HTML-capable client for the full report."
    )
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, REPORT_TO, msg.as_string())

    print(f"[OK] Email sent to {', '.join(REPORT_TO)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    report_date = date.today().isoformat()
    print(f"[seo_report.py] Starting run for {report_date}")

    sections = []

    # --- Section 1 + 2 + 3: GSC traffic summary, top queries, top pages ----
    def gsc_sections():
        (q_cur, q_pri_map, p_cur, p_pri_map,
         cur_totals, pri_totals,
         start_cur, end_cur,
         start_pri, end_pri) = fetch_gsc()

        print(f"  GSC: {int(cur_totals['clicks'])} clicks, "
              f"{int(cur_totals['impressions'])} impressions this week")

        return (
            build_traffic_summary(cur_totals, pri_totals,
                                  start_cur, end_cur, start_pri, end_pri)
            + build_top_queries(q_cur, q_pri_map)
            + build_top_pages(p_cur, p_pri_map)
        )

    sections.append(_safe_section("Traffic Summary / GSC", gsc_sections))

    # --- Section 4: GA4 traffic sources ------------------------------------
    def ga4_section():
        sources, overview, start, end = fetch_ga4()
        print(f"  GA4: {len(sources.rows)} source/medium rows")
        return build_traffic_sources(sources, overview, start, end)

    sections.append(_safe_section("Traffic Sources (GA4)", ga4_section))

    # --- Section 5: Competitor snapshot ------------------------------------
    def comp_section():
        rows = fetch_competitor_rankings()
        live_count = sum(1 for r in rows if r.get("live"))
        print(f"  Competitors: {live_count}/{len(rows)} keywords with live SERP data")
        return build_competitor_snapshot(rows)

    sections.append(_safe_section("Competitor Snapshot", comp_section))

    # --- Build & send ------------------------------------------------------
    html = build_html_report(sections, report_date)
    send_email(html, report_date)
    print("[seo_report.py] Done.")


if __name__ == "__main__":
    main()

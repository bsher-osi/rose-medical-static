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

# GA4 service account
_SA_JSON = os.environ.get(
    "GOOGLE_SERVICE_ACCOUNT_JSON",
    os.path.join(SCRIPT_DIR, "../credentials/ga4-service-account.json")
)
GA4_CREDS_PATH = os.environ.get("GA4_SERVICE_ACCOUNT_JSON", _SA_JSON)

# GSC OAuth2 refresh token (owner account — required for Search Console access)
GSC_TOKEN_PATH    = os.path.join(SCRIPT_DIR, "../credentials/gsc_token.json")
GSC_CLIENT_ID     = os.environ.get("GSC_CLIENT_ID", "")
GSC_CLIENT_SECRET = os.environ.get("GSC_CLIENT_SECRET", "")
GSC_REFRESH_TOKEN = os.environ.get("GSC_REFRESH_TOKEN", "")

GSC_PROPERTY   = os.environ.get("GSC_PROPERTY", "sc-domain:rosemedicalpavilion.com")
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
    "pediatric neurology phoenix az",
    "child neurologist phoenix",
    "pediatric epilepsy specialist phoenix",
    "pediatric headache doctor phoenix",
    "adhd specialist children phoenix",
    "pediatric neurology scottsdale",
    "children's neurologist arizona",
    "pediatric neurologist near me phoenix",
    "rose medical pavilion phoenix",
]

# Competitors to watch for in results (domain fragments, lowercase)
COMPETITOR_DOMAINS = [
    "rosemedicalpavilion.com",
    "phoenixchildrens.org",
    "bannerhealth.com",
    "dignityhealth.org",
    "honorhealth.com",
    "azbrainandspine.com",
    "childrenshospital.org",
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
    from google.oauth2.credentials import Credentials

    # Prefer env vars, fall back to saved token file
    client_id     = GSC_CLIENT_ID
    client_secret = GSC_CLIENT_SECRET
    refresh_token = GSC_REFRESH_TOKEN

    if not (client_id and client_secret and refresh_token):
        if os.path.exists(GSC_TOKEN_PATH):
            with open(GSC_TOKEN_PATH) as f:
                tok = json.load(f)
            client_id     = tok.get("client_id", "")
            client_secret = tok.get("client_secret", "")
            refresh_token = tok.get("refresh_token", "")

    if not (client_id and client_secret and refresh_token):
        raise RuntimeError(
            "GSC OAuth credentials not found. Run seo/agents/gsc_auth_setup.py first."
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
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

def _ga4_creds():
    """Return GA4 credentials — OAuth token preferred, SA fallback."""
    from google.oauth2.credentials import Credentials as OAuthCreds
    from google.oauth2.service_account import Credentials as SACreds

    # Try OAuth token first (same token used for GSC)
    client_id     = GSC_CLIENT_ID
    client_secret = GSC_CLIENT_SECRET
    refresh_token = GSC_REFRESH_TOKEN
    if not (client_id and client_secret and refresh_token) and os.path.exists(GSC_TOKEN_PATH):
        with open(GSC_TOKEN_PATH) as f:
            tok = json.load(f)
        client_id     = tok.get("client_id", "")
        client_secret = tok.get("client_secret", "")
        refresh_token = tok.get("refresh_token", "")

    if client_id and client_secret and refresh_token:
        return OAuthCreds(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/analytics.readonly"],
        )

    # Fall back to service account
    return SACreds.from_service_account_file(
        GA4_CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )


def fetch_ga4():
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest, OrderBy,
    )

    client = BetaAnalyticsDataClient(credentials=_ga4_creds())

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

    # Sessions by source / medium (with new users per channel)
    sources = run(
        dimensions=["sessionSourceMedium"],
        metrics=["sessions", "newUsers"],
        order_metric="sessions",
        limit=20,
    )

    # Overview — sessions, users, new users, pageviews, bounce, avg duration
    overview = run(
        dimensions=[],
        metrics=["sessions", "totalUsers", "newUsers", "screenPageViews",
                 "bounceRate", "averageSessionDuration"],
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


def fetch_keyword_rankings_gsc(keywords, days=28):
    """
    Pull our own positions for specific keywords from GSC (free, no SERP API).
    Returns dict: { keyword_lower: {clicks, impressions, position, position_prior} }
    Uses a 28-day window for better coverage of low-volume keywords.
    """
    service   = _gsc_service()
    end_cur   = date.today() - timedelta(days=3)
    start_cur = end_cur - timedelta(days=days - 1)
    end_pri   = start_cur - timedelta(days=1)
    start_pri = end_pri - timedelta(days=days - 1)

    def pull(start, end, limit=5000):
        body = {
            "startDate":  str(start),
            "endDate":    str(end),
            "dimensions": ["query"],
            "rowLimit":   limit,
        }
        return {
            r["keys"][0].lower(): r
            for r in service.searchanalytics().query(
                siteUrl=GSC_PROPERTY, body=body
            ).execute().get("rows", [])
        }

    cur_map = pull(start_cur, end_cur)
    pri_map = pull(start_pri, end_pri)

    result = {}
    for kw in keywords:
        k = kw.lower()
        cur = cur_map.get(k, {})
        pri = pri_map.get(k, {})
        result[k] = {
            "clicks":         int(cur.get("clicks", 0)),
            "impressions":    int(cur.get("impressions", 0)),
            "position":       cur.get("position", 0),
            "position_prior": pri.get("position", 0),
        }
    return result


def fetch_competitor_rankings():
    """
    Returns list of dicts with our GSC rankings for each tracked keyword.
    If a SERP API key is configured, also fetches competitor positions.
    """
    use_serpapi    = bool(SERPAPI_KEY)
    use_dataforseo = bool(DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD)

    # Always pull our own positions from GSC
    try:
        gsc_data = fetch_keyword_rankings_gsc(COMPETITOR_KEYWORDS)
    except Exception as e:
        gsc_data = {}
        print(f"  [WARN] GSC keyword pull failed: {e}")

    rows = []
    for kw in COMPETITOR_KEYWORDS:
        k    = kw.lower()
        gsc  = gsc_data.get(k, {})
        pos  = gsc.get("position", 0)
        pos_p = gsc.get("position_prior", 0)

        our_rank = round(pos, 1) if pos > 0 else "—"
        ww = "—"
        if pos > 0 and pos_p > 0:
            delta = pos - pos_p
            if abs(delta) >= 0.5:
                ww = f"{delta:+.1f}"
                # green if improved (lower number), red if dropped
            else:
                ww = "="

        try:
            if use_serpapi:
                serp = _rank_via_serpapi(kw)
            elif use_dataforseo:
                serp = _rank_via_dataforseo(kw)
            else:
                serp = []
        except Exception as exc:
            serp = []

        rows.append({
            "keyword":     kw,
            "our_rank":    our_rank,
            "ww":          ww,
            "clicks":      gsc.get("clicks", 0),
            "impressions": gsc.get("impressions", 0),
            "results":     serp[:5],
            "live":        True,  # always live via GSC
        })

    return rows


# ---------------------------------------------------------------------------
# 4. HTML Report Builder
# ---------------------------------------------------------------------------

GOLD   = "#c9a84c"
DARK   = "#141414"
CARD   = "#1e1e1e"
CARD2  = "#252525"
BORDER = "#2e2e2e"
MUTED  = "#888"
WHITE  = "#f0f0f0"

CSS = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  body {{ font-family: 'Inter', Arial, sans-serif; background: {DARK};
         margin: 0; padding: 24px 12px; color: {WHITE}; }}
  .wrapper {{ max-width: 760px; margin: auto; background: {CARD};
              border-radius: 10px; overflow: hidden;
              border: 1px solid {BORDER}; }}
  .header  {{ padding: 28px 32px 22px; border-bottom: 1px solid {BORDER}; }}
  .header .eyebrow {{ font-size: 11px; font-weight: 600; letter-spacing: .12em;
                      text-transform: uppercase; color: {GOLD}; margin-bottom: 6px; }}
  .header h1 {{ margin: 0 0 4px; font-size: 26px; font-weight: 700; color: #fff; }}
  .header .sub {{ font-size: 13px; color: {MUTED}; margin: 0; }}
  .section   {{ padding: 22px 32px; border-bottom: 1px solid {BORDER}; }}
  .section:last-child {{ border-bottom: none; }}
  .section h2 {{ margin: 0 0 14px; font-size: 11px; font-weight: 600;
                 letter-spacing: .1em; text-transform: uppercase; color: {GOLD}; }}
  .opp-note {{ font-size: 12px; color: {MUTED}; margin: -8px 0 14px; }}
  table  {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th     {{ text-align: left; padding: 7px 10px; font-size: 11px;
            font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
            color: {MUTED}; border-bottom: 1px solid {BORDER}; white-space: nowrap; }}
  td     {{ padding: 8px 10px; border-bottom: 1px solid {BORDER};
            vertical-align: middle; color: {WHITE}; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,.03); }}
  a  {{ color: {GOLD}; text-decoration: none; }}
  .up   {{ color: #4caf7d; font-weight: 600; }}
  .down {{ color: #e05c5c; font-weight: 600; }}
  .flat {{ color: {MUTED}; }}
  .nodata {{ color: {MUTED}; font-style: italic; }}
  .kpi-grid {{ display: flex; gap: 10px; flex-wrap: wrap; }}
  .kpi  {{ flex: 1; min-width: 120px; background: {CARD2};
           border: 1px solid {BORDER}; border-radius: 8px; padding: 14px 16px; }}
  .kpi .label {{ font-size: 10px; font-weight: 600; text-transform: uppercase;
                 letter-spacing: .1em; color: {MUTED}; }}
  .kpi .value {{ font-size: 28px; font-weight: 700; color: {GOLD};
                 margin: 6px 0 2px; line-height: 1; }}
  .kpi .delta {{ font-size: 11px; color: {MUTED}; }}
  .comp-summary {{ font-size: 12px; color: {MUTED}; margin-bottom: 14px; }}
  .comp-summary b {{ color: {WHITE}; }}
  .badge-t3  {{ background: #2a4a2e; color: #4caf7d;
                border-radius: 10px; padding: 1px 7px; font-size: 11px; }}
  .badge-t10 {{ background: #3a3a1e; color: {GOLD};
                border-radius: 10px; padding: 1px 7px; font-size: 11px; }}
  .err  {{ color: #e05c5c; }}
  pre   {{ background: #111; padding: 10px; border-radius: 4px;
           font-size: 11px; overflow-x: auto; white-space: pre-wrap;
           color: #aaa; border: 1px solid {BORDER}; }}
  .placeholder {{ background: #1e1a10; border: 1px dashed #5a4a20;
                  border-radius: 6px; padding: 14px 16px; font-size: 13px;
                  color: #b89a4a; }}
  .footer {{ padding: 14px 32px; font-size: 11px; color: {MUTED};
             text-align: center; border-top: 1px solid {BORDER}; }}
</style>
"""


def _delta_html(cur, pri, higher_is_better=True, fmt=None):
    if pri == 0:
        return '<span class="flat">-</span>'
    diff = cur - pri
    if fmt == "pct":
        label = f"{diff * 100:+.1f}pp"
    elif fmt == "pos":
        label = f"{diff:+.1f}"
        is_good = diff < 0  # lower position = better
        cls = "up" if is_good else ("down" if diff != 0 else "flat")
        return f'<span class="{cls}">{label}</span>'
    else:
        pct = (diff / pri) * 100
        label = f"{diff:+,.0f} ({pct:+.1f}%)"
    is_good = diff > 0 if higher_is_better else diff < 0
    cls = "up" if is_good else ("down" if diff != 0 else "flat")
    return f'<span class="{cls}">{label}</span>'


def _kpi_box(label, value, sub="-"):
    return f"""
    <div class="kpi">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
      <div class="delta">{sub}</div>
    </div>"""


def build_ga4_section(overview, start, end):
    # metrics order: sessions(0), totalUsers(1), newUsers(2), screenPageViews(3),
    #                bounceRate(4), averageSessionDuration(5)
    if not overview.rows:
        sessions = new_users = pageviews = bounce = avg_fmt = "N/A"
    else:
        r  = overview.rows[0]
        mv = lambda i: r.metric_values[i].value
        sessions  = _num(mv(0))
        new_users = _num(mv(2))
        pageviews = _num(mv(3))
        bounce    = f"{float(mv(4))*100:.0f}%"
        avg_secs  = float(mv(5))
        avg_fmt   = f"{int(avg_secs//60):02d}:{int(avg_secs%60):02d} avg"

    kpis = (
        _kpi_box("Sessions",    sessions,  "-")
        + _kpi_box("New Users", new_users, "-")
        + _kpi_box("Page Views", pageviews, "-")
        + _kpi_box("Bounce Rate", bounce,   avg_fmt)
    )
    return f"""
    <div class="section">
      <h2>Traffic (GA4 7-Day)</h2>
      <div class="kpi-grid">{kpis}</div>
    </div>"""


def build_gsc_kpis(cur, pri):
    def fmt_val(v, fn):
        return fn(v) if float(v) > 0 else "0"

    def kpi_delta(label, c_val, p_val, higher_is_better=True, fmt=None):
        if fmt == "pct":
            display = _pct(c_val) if float(c_val) > 0 else "N/A"
        elif fmt == "pos":
            display = _pos(c_val) if float(c_val) > 0 else "N/A"
        else:
            display = _num(c_val)
        delta = _delta_html(float(c_val), float(p_val), higher_is_better, fmt)
        return _kpi_box(label, display, f"vs prior week: {delta}")

    kpis = (
        kpi_delta("Clicks",       cur["clicks"],      pri["clicks"])
        + kpi_delta("Impressions", cur["impressions"], pri["impressions"])
        + kpi_delta("CTR",         cur["ctr"],         pri["ctr"],         fmt="pct")
        + kpi_delta("Avg Position", cur["position"],   pri["position"],
                    higher_is_better=False, fmt="pos")
    )
    return f"""
    <div class="section">
      <h2>Search Visibility (GSC 7-Day)</h2>
      <div class="kpi-grid">{kpis}</div>
    </div>"""


def build_competitive_position(comp_rows):
    """Keyword table with Pos, W/W, Competitors Ahead, Clicks, Impressions."""
    has_live = any(r.get("live") for r in comp_rows)

    # Tally summary counts
    t3 = t10 = t20 = no_data = 0
    for r in comp_rows:
        rk = r.get("our_rank")
        if rk == "—" or rk == "error" or rk == 0:
            no_data += 1
        elif isinstance(rk, (int, float)):
            if rk <= 3:   t3 += 1
            if rk <= 10:  t10 += 1
            if rk <= 20:  t20 += 1
        else:
            no_data += 1

    summary = (
        f'Competitors Ahead = other sites ranking above you. '
        f'Top 3: <b>{t3}</b> &nbsp; Top 10: <b>{t10}</b> '
        f'&nbsp; Top 20: <b>{t20}</b> &nbsp; No data: <b>{no_data}</b>'
    )

    rows_html = ""
    for r in comp_rows:
        kw      = r["keyword"]
        rk      = r.get("our_rank", "—")
        ww      = r.get("ww", "—")      # week-over-week position delta
        clicks  = r.get("clicks", "")
        impr    = r.get("impressions", "")

        # Competitors ahead = estimated results ranked above us
        ahead = "—"
        if isinstance(rk, (int, float)) and rk > 0:
            ahead = str(max(0, int(rk) - 1))

        if isinstance(rk, (int, float)) and rk > 0:
            rk_display = f"{rk:.1f}"
            if rk <= 3:
                pos_html = f'<span class="badge-t3">{rk_display}</span>'
            elif rk <= 10:
                pos_html = f'<span class="badge-t10">{rk_display}</span>'
            else:
                pos_html = rk_display
        elif has_live:
            pos_html = f'<span class="nodata">No data</span>'
        else:
            pos_html = f'<span class="nodata">No data</span>'

        err = f'<br><small class="err">{r["error"]}</small>' if r.get("error") else ""
        rows_html += f"""
        <tr>
          <td style="color:#ccc">{kw}</td>
          <td style="text-align:center">{pos_html}{err}</td>
          <td style="text-align:center;color:#888">{ww}</td>
          <td style="text-align:center;color:#888">{ahead}</td>
          <td style="text-align:center;color:#888">{_num(clicks) if clicks else "—"}</td>
          <td style="text-align:center;color:#888">{_num(impr) if impr else "—"}</td>
        </tr>"""

    # Only show SERP API note if no live data at all and no GSC positions either
    has_any_pos = any(isinstance(r.get("our_rank"), float) for r in comp_rows)
    if not has_live and not has_any_pos:
        placeholder = """
        <div class="placeholder" style="margin-top:12px">
          Positions sourced from GSC (28-day avg). Add <code>SERPAPI_KEY</code>
          to also show competitor rankings.
        </div>"""
    else:
        placeholder = ""

    return f"""
    <div class="section">
      <h2>Competitive Position</h2>
      <div class="comp-summary">{summary}</div>
      <table>
        <thead><tr>
          <th>Keyword</th>
          <th style="text-align:center">Pos</th>
          <th style="text-align:center">W/W</th>
          <th style="text-align:center">Competitors Ahead</th>
          <th style="text-align:center">Clicks</th>
          <th style="text-align:center">Impr</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
      {placeholder}
    </div>"""


def build_seo_opportunities(q_cur):
    """Queries ranking top 20 with CTR < 4% — title/meta quick wins."""
    opps = [
        r for r in q_cur
        if 0 < float(r.get("position", 99)) <= 20
        and float(r.get("ctr", 0)) < 0.04
        and int(r.get("impressions", 0)) > 0
    ]
    if not opps:
        return ""

    rows_html = ""
    for r in opps:
        rows_html += f"""
        <tr>
          <td style="color:#ccc">{r["keys"][0]}</td>
          <td style="text-align:center">{_num(r.get("impressions",0))}</td>
          <td style="text-align:center">{_pct(r.get("ctr",0))}</td>
          <td style="text-align:center">{_pos(r.get("position",0))}</td>
        </tr>"""

    return f"""
    <div class="section">
      <h2>SEO Opportunities</h2>
      <div class="opp-note">Ranking top 20 but CTR under 4% — better title/meta could double clicks.</div>
      <table>
        <thead><tr>
          <th>Query</th>
          <th style="text-align:center">Impressions</th>
          <th style="text-align:center">CTR</th>
          <th style="text-align:center">Position</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def _strip_domain(url):
    """Return just the path portion of a URL."""
    import re
    path = re.sub(r'^https?://[^/]+', '', url) or "/"
    return path

def build_top_pages_ga4(p_cur, sources):
    """Top pages from GSC by clicks."""
    rows_html = ""
    for r in p_cur:
        full_url = r["keys"][0]
        page     = _strip_domain(full_url)
        clicks   = r.get("clicks", 0)
        impr     = r.get("impressions", 0)
        pos      = r.get("position", 0)
        display  = page if len(page) < 55 else page[:52] + "…"
        rows_html += f"""
        <tr>
          <td><a href="{full_url}" title="{page}">{display}</a></td>
          <td style="text-align:center">{_num(clicks)}</td>
          <td style="text-align:center">{_num(impr)}</td>
          <td style="text-align:center">{_pos(pos)}</td>
        </tr>"""

    return f"""
    <div class="section">
      <h2>Top Pages</h2>
      <table>
        <thead><tr>
          <th>Page</th>
          <th style="text-align:center">Clicks</th>
          <th style="text-align:center">Impressions</th>
          <th style="text-align:center">Avg Position</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_traffic_sources(sources, overview, start, end):
    rows_html = ""
    for row in sources.rows:
        src_med = row.dimension_values[0].value
        parts   = src_med.split(" / ", 1)
        src     = parts[0]
        med     = parts[1] if len(parts) > 1 else ""
        sess    = int(row.metric_values[0].value)
        new_u   = int(row.metric_values[1].value) if len(row.metric_values) > 1 else ""
        rows_html += f"""
        <tr>
          <td style="color:#ccc;font-weight:600">{src}</td>
          <td style="color:#888">{med}</td>
          <td style="text-align:center">{_num(sess)}</td>
          <td style="text-align:center">{_num(new_u) if new_u != "" else "—"}</td>
        </tr>"""

    return f"""
    <div class="section">
      <h2>Traffic Sources</h2>
      <table>
        <thead><tr>
          <th>Source</th><th>Medium</th>
          <th style="text-align:center">Sessions</th>
          <th style="text-align:center">New Users</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>"""


def build_html_report(sections_html, report_date, start_date, end_date):
    from datetime import date as _date
    day_name = _date.today().strftime("%A").upper()
    start_fmt = start_date.strftime("%-d %b") if hasattr(start_date, "strftime") else str(start_date)
    end_fmt   = end_date.strftime("%-d %b") if hasattr(end_date, "strftime") else str(end_date)
    full_date = _date.today().strftime("%A, %B %-d, %Y")
    body = "".join(s for s in sections_html if s)
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
      <div class="eyebrow">Rose Medical Pavilion &middot; {day_name}</div>
      <h1>SEO Performance Report</h1>
      <p class="sub">{start_fmt} &ndash; {end_fmt} &nbsp;&middot;&nbsp; {full_date}</p>
    </div>
    {body}
    <div class="footer">
      Automated report &nbsp;&bull;&nbsp; Google Search Console + GA4
      {" &bull; SerpAPI" if SERPAPI_KEY else ""}
      {" &bull; DataForSEO" if DATAFORSEO_LOGIN else ""}
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
    msg["Subject"] = f"SEO Daily Report — Rose Medical Pavilion — {report_date}"
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
    today       = date.today()
    report_date = today.isoformat()
    print(f"[seo_report.py] Starting run for {report_date}")

    sections   = []
    start_date = today - timedelta(days=6)
    end_date   = today

    # --- GA4: traffic KPIs (top of report) ---------------------------------
    sources = overview = ga4_start = ga4_end = None
    try:
        sources, overview, ga4_start, ga4_end = fetch_ga4()
        print(f"  GA4: {len(sources.rows)} source/medium rows")
        sections.append(build_ga4_section(overview, ga4_start, ga4_end))
    except Exception as e:
        sections.append(f'<div class="section"><h2>Traffic (GA4 7-Day)</h2><p class="err">GA4 data unavailable: {e}</p></div>')

    # --- GSC: search visibility KPIs + competitive position ----------------
    q_cur_cache = []
    p_cur_cache = []
    def gsc_sections():
        (q_cur, q_pri_map, p_cur, p_pri_map,
         cur_totals, pri_totals,
         start_cur, end_cur,
         start_pri, end_pri) = fetch_gsc()
        print(f"  GSC: {int(cur_totals['clicks'])} clicks, "
              f"{int(cur_totals['impressions'])} impressions this week")
        q_cur_cache.extend(q_cur)
        p_cur_cache.extend(p_cur)
        return (
            build_gsc_kpis(cur_totals, pri_totals)
            + build_competitive_position(fetch_competitor_rankings())
            + build_seo_opportunities(q_cur)
            + build_top_pages_ga4(p_cur, sources)
        )

    sections.append(_safe_section("GSC + Competitive", gsc_sections))

    # --- Traffic sources ---------------------------------------------------
    if sources is not None:
        try:
            sections.append(build_traffic_sources(sources, overview, ga4_start, ga4_end))
        except Exception:
            pass

    # --- Build & send ------------------------------------------------------
    html = build_html_report(sections, report_date, start_date, end_date)
    send_email(html, report_date)
    print("[seo_report.py] Done.")


if __name__ == "__main__":
    main()

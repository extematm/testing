"""Fetch recent GitHub commits, summarize with Ollama, and save as PDF."""

import os
import re
import textwrap
from datetime import datetime, timedelta, timezone

import requests

#from reportlab.lib.pagesizes import A4
#from reportlab.pdfgen import canvas

# -------------------------
# CONFIG
# -------------------------

GITHUB_REPO = "extematm/weekly-summary"
OLLAMA_MODEL = "qwen:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"
REPORTS_DIR = "reports"


# -------------------------
# HELPER FUNCTIONS
# -------------------------


def get_last_week_commits(repo):
    """Fetch commits from the last week for a given GitHub repo."""
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {"since": one_week_ago.isoformat() + "Z"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    commits = response.json()
    norway_offset = timedelta(hours=1)
    commit_messages = []
    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        dt_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        dt_norway = dt_utc + norway_offset
        human_date = dt_norway.strftime("%Y-%m-%d %H:%M:%S")
        message = commit["commit"]["message"]
        commit_messages.append(f"- {human_date}: {message}")
    return "\n".join(commit_messages) if commit_messages else "No commits in the last week."


def summarize_commits(commit_text):
    """Summarize commit messages using Ollama."""
    prompt = f"Please answer ONLY in English. Make the summary very structured.\n{commit_text}"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    if "response" not in data:
        raise ValueError(f"Unexpected Ollama response: {data}")
    return data["response"]


def draw_footer(c, width, margin, page_num):
    """Draw page footer."""
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width // 2, margin // 2, f"Page {page_num}")


def check_page_break(c, y, margin, height, width, page_num):
    """Handle automatic page breaks."""
    if y < margin + 40:
        draw_footer(c, width, margin, page_num)
        c.showPage()
        page_num += 1
        y = height - margin
        c.setFont("Helvetica", 12)
    return y, page_num


def draw_wrapped_text(c, text, y, margin, width, height, page_num, max_line_width):
    """Draw wrapped text with automatic pagination."""
    for line in text.splitlines():
        for wrapped in textwrap.wrap(line, width=max_line_width):
            c.drawString(margin, y, wrapped)
            y -= 16
            y, page_num = check_page_break(c, y, margin, height, width, page_num)
    return y, page_num


def save_summary_pdf(summary_text, raw_commits, filename_hint="summary"):
    """Save the summary as a PDF report."""
    safe_hint = re.sub(r"[^a-zA-Z0-9]+", "_", filename_hint)[:20]
    now = datetime.now()
    date_str = now.strftime("%Y%m%d_%H%M%S")
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    filename = os.path.join(reports_dir, f"{date_str}_{safe_hint}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 40
    max_line_width = int((width - 2 * margin) // 7)
    y = height - margin
    page_num = 1

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width // 2, y, "Weekly Project Summary Report")
    y -= 30
    c.setFont("Helvetica", 11)
    generated_time = now.strftime("%Y-%m-%d %H:%M:%S")
    c.drawCentredString(width // 2, y, f"Generated: {generated_time}")
    y -= 20
    c.line(margin, y, width - margin, y)
    y -= 30

    # Summary section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Summary:")
    y -= 22
    c.setFont("Helvetica", 12)
    y, page_num = draw_wrapped_text(
    c,
    summary_text,
    y,
    margin,
    width,
    height,
    page_num,
    max_line_width,
    )

    y -= 10

    if y < margin + 60:
        y, page_num = check_page_break(c, y, margin, height, width, page_num)

    # Raw commits section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Raw Commits:")
    y -= 22
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.line(margin, y + 10, width - margin, y + 10)
    y -= 10
    c.setFont("Helvetica", 12)
    y, page_num = draw_wrapped_text(
    c,
    raw_commits,
    y,
    margin,
    width,
    height,
    page_num,
    max_line_width,
    )
    draw_footer(c, width, margin, page_num)
    c.save()
    print(f"PDF report saved as: {filename}")


# -------------------------
# MAIN
# -------------------------


def main():
    """Main function."""
    print(f"Fetching last week's commits from {GITHUB_REPO}...\n")
    raw_commits = get_last_week_commits(GITHUB_REPO)
    print("Raw commit activity:\n", raw_commits, "\n")
    print("----------------------------------------------\n")
    summary = raw_commits if raw_commits == "No commits in the last week." else summarize_commits(raw_commits)
    print("Commit Summary:\n", summary)
    save_summary_pdf(summary, raw_commits)


if __name__ == "__main__":
    main()

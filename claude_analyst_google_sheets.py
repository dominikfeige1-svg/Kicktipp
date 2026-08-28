#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KICKTIPP ANALYST v4.0 - Mit Google Sheets Integration
Claude analysiert automatisch und schreibt direkt in dein Google Sheet!
"""

import json
import os
from datetime import datetime
import anthropic
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import gspread

print("\n" + "="*70)
print("🤖 KICKTIPP ANALYST v4.0 - Google Sheets Integration")
print("="*70 + "\n")

# ===== CLAUDE API =====
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ===== GOOGLE SHEETS SETUP =====
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Von dir!
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_JSON")  # Service Account JSON

try:
    if GOOGLE_CREDENTIALS:
        # Parse Service Account JSON
        creds_dict = json.loads(GOOGLE_CREDENTIALS)
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        print("✅ Google Sheets verbunden!\n")
    else:
        sheet = None
        print("⚠️  Google Sheets nicht konfiguriert (optional)\n")
except Exception as e:
    print(f"⚠️  Google Sheets Fehler: {e}\n")
    sheet = None

# ===== SPIELE FÜR MORGEN PRÜFEN =====
from datetime import datetime, timedelta

today = datetime.now()
tomorrow = today + timedelta(days=1)

print(f"📅 Prüfe auf Spiele für: {tomorrow.date()}\n")

# Später: echte API für Spielplan
# Für jetzt: Demo
matches_to_analyze = []

if tomorrow.date() == datetime(2026, 8, 29).date():
    matches_to_analyze = [
        {
            'team1': 'Borussia Dortmund',
            'team2': 'Hamburger SV',
            'date': '2026-08-29',
            'time': '18:30',
            'competition': 'Bundesliga ST1'
        }
    ]

if not matches_to_analyze:
    print("✅ Keine Spiele morgen - Script beendet.\n")
    exit(0)

print(f"📋 Analysiere {len(matches_to_analyze)} Spiele...\n")

# ===== GOOGLE SHEETS HEADER =====
if sheet:
    sheet.clear()
    header = [
        ["🤖 KICKTIPP ANALYZER", f"Generiert: {datetime.now().strftime('%d.%m.%Y %H:%M')}"],
        [],
        ["Team 1", "Team 2", "Tipp", "Konfidenz %", "Begründung 1", "Begründung 2", "Begründung 3", "Begründung 4", "Begründung 5", "Quellen"]
    ]
    sheet.append_rows(header)

# ===== ANALYSEN =====
analysis_results = []

for match in matches_to_analyze:
    team1 = match['team1']
    team2 = match['team2']
    
    print(f"🔍 Analysiere: {team1} vs {team2}")
    
    prompt = f"""Du bist ein professioneller Bundesliga-Analyst für Kicktipp.

Analysiere: **{team1} vs {team2}**
Datum: {match['date']} um {match['time']}

NUTZE DIESE QUELLEN (Hierarchie):
- TIER 1: Oddspedia, Flashscore (Quoten)
- TIER 2: Understat, WhoScored (xG, Form)
- TIER 3: LigaInsider, Transfermarkt (Verletzungen, H2H)
- TIER 4: Opta, Goal.com (Taktik)

DEINE ANTWORT (genau dieses Format - KEINE anderen Worte!):
{{
    "tipp": "X:Y",
    "confidence": XX,
    "reason_1": "Konkrete Begründung mit Quelle (z.B. Quote 1.50)",
    "reason_2": "Konkrete Begründung mit Quelle (z.B. xG 2.8 vs 1.2)",
    "reason_3": "Konkrete Begründung mit Quelle (z.B. 5 Ausfälle)",
    "reason_4": "Konkrete Begründung mit Quelle (z.B. H2H 3:1)",
    "reason_5": "Konkrete Begründung mit Quelle (z.B. Form W-W-W)",
    "sources": "Oddspedia, Understat, LigaInsider, Transfermarkt"
}}"""
    
    # ===== CLAUDE ANALYSIEREN =====
    response = claude_client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        tools=[{"type": "builtin_tool", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    analysis_text = ""
    for block in response.content:
        if hasattr(block, 'text'):
            analysis_text = block.text
    
    # ===== JSON PARSEN =====
    try:
        import re
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            analysis = {
                'tipp': '1:1',
                'confidence': 50,
                'reason_1': 'Analyse fehler',
                'reason_2': '',
                'reason_3': '',
                'reason_4': '',
                'reason_5': '',
                'sources': 'N/A'
            }
    except:
        analysis = {
            'tipp': '1:1',
            'confidence': 50,
            'reason_1': 'JSON-Fehler',
            'reason_2': '',
            'reason_3': '',
            'reason_4': '',
            'reason_5': '',
            'sources': 'N/A'
        }
    
    analysis_results.append({
        'team1': team1,
        'team2': team2,
        **analysis
    })
    
    print(f"   ✅ {team1} vs {team2}: {analysis['tipp']} ({analysis['confidence']}%)\n")

# ===== IN GOOGLE SHEETS SCHREIBEN =====
if sheet and analysis_results:
    print("📝 Schreibe in Google Sheets...\n")
    for analysis in analysis_results:
        row = [
            analysis['team1'],
            analysis['team2'],
            analysis['tipp'],
            analysis['confidence'],
            analysis.get('reason_1', ''),
            analysis.get('reason_2', ''),
            analysis.get('reason_3', ''),
            analysis.get('reason_4', ''),
            analysis.get('reason_5', ''),
            analysis.get('sources', '')
        ]
        sheet.append_row(row)
    print("✅ Google Sheets aktualisiert!\n")

# ===== SPEICHERN ALS JSON (FÜR MAKE.COM) =====
output_json = {
    'generated_at': datetime.now().isoformat(),
    'for_date': str(tomorrow.date()),
    'tipps': analysis_results
}

os.makedirs('output', exist_ok=True)
with open('output/tipps.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, indent=2, ensure_ascii=False)

print("="*70)
print("✅ ANALYSIS COMPLETE!")
print("="*70)
print(f"""
✅ Google Sheets: Tipps mit Begründung geschrieben
✅ JSON: Für Make.com bereit
✅ Make.com: Wird Kicktipp füllen

Du siehst die Tipps auf dem Handy:
  └─ Google Sheets App → Dein Sheet
  └─ Aktuell, mit Begründung, jederzeit verfügbar!
""")

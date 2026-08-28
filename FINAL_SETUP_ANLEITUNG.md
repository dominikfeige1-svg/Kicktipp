# 🤖 FINAL SETUP - Claude Analyst + Google Sheets + Make.com

## 🎯 DER WORKFLOW

```
Täglich 06:00 Uhr (GitHub Actions):
  ├─ Claude analysiert automatisch
  ├─ Schreibt direkt in DEIN Google Sheet
  ├─ Speichert auch JSON für Make.com
  └─ Make.com trägt in Kicktipp ein

Du siehst auf dem Handy:
  └─ Google Sheets App → Tipps + Begründung
  └─ Jederzeit aktuell & lesbar!
```

---

## 📋 SETUP - SCHRITT FÜR SCHRITT

### SCHRITT 1: Google Sheet erstellen

1. Gehe zu: https://sheets.google.com
2. **+ Neues Sheet** → "Kicktipp Analyse"
3. Name: "Kicktipp Tipps"

(Das Sheet wird leer gelassen - Claude füllt es!)

### SCHRITT 2: Google Service Account erstellen

1. Gehe zu: https://console.cloud.google.com
2. **Neues Projekt** → "Kicktipp"
3. **APIs aktivieren** → Suche "Google Sheets API" → **Aktivieren**
4. Klick: **Anmeldedaten** (links)
5. **+ Anmeldedaten erstellen** → "Dienstkonto"
6. Name: "kicktipp-bot"
7. Email wird automatisch generiert (kopiere sie!)
8. **Rolle:** Viewer (für jetzt)
9. **Weiter**
10. **Schlüssel erstellen** → JSON
11. ⬇️ JSON-Datei wird heruntergeladen!

### SCHRITT 3: Google Sheet für Service Account freigeben

1. Öffne dein "Kicktipp Tipps" Sheet
2. Klick: **Freigeben** (rechts oben)
3. Gib die **Service Account Email** ein (von oben)
4. **Editor** Berechtigungen
5. **Freigeben**

### SCHRITT 4: Sheet ID kopieren

1. Öffne dein "Kicktipp Tipps" Sheet
2. Schau die URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
                                           ^^^^^^^^^^^^
                                         Diese Nummer!
   ```
3. Kopiere die **SHEET_ID**

### SCHRITT 5: GitHub Secrets erstellen

Gehe zu: https://github.com/dominikfeigl-svg/Kicktipp/settings/secrets/actions

**Secret 1:**
- Name: `GOOGLE_SHEET_ID`
- Value: Deine Sheet ID (von oben)

**Secret 2:**
- Name: `GOOGLE_CREDENTIALS_JSON`
- Value: Der komplette JSON-Inhalt aus der heruntergeladenen Datei
  (Die ganze JSON-Datei kopieren und einfügen!)

**Secret 3:**
- Name: `ANTHROPIC_API_KEY`
- Value: Dein Claude API Key (von console.anthropic.com)

### SCHRITT 6: Dateien hochladen

Zu GitHub hochladen:
1. `claude_analyst_google_sheets.py` → Root-Ordner
2. `workflow_google_sheets.yml` → `.github/workflows/`

### SCHRITT 7: Testen

GitHub Actions → **Workflow ausführen** → Teste manuell

Dann: Öffne dein Google Sheet → Sind die Tipps drin?

---

## 📱 SO SIEHST DU ES AUF DEM HANDY

```
1. Google Sheets App auf Handy öffnen
2. "Kicktipp Tipps" Sheet öffnen
3. Siehst die Tipps mit KOMPLETTER BEGRÜNDUNG
4. Alles live, aktuell, lesbar!
```

**Beispiel im Sheet:**

| Team 1 | Team 2 | Tipp | Konfidenz | Begründung 1 | Begründung 2 | Begründung 3 | Begründung 4 | Begründung 5 | Quellen |
|--------|--------|------|-----------|--------------|--------------|--------------|--------------|--------------|---------|
| Bayern | Stuttgart | 2:0 | 96 | Quote 1.30 - Oddspedia | xG 3.5 vs 0.8 - Understat | 8 Ausfälle Stuttgart - LigaInsider | Bayern 5:0 H2H - Transfermarkt | Form 4W-1D - WhoScored | Oddspedia, Understat, LigaInsider, Transfermarkt |

---

## 🔄 GESAMTER FLOW

```
TÄGLICH 06:00 UHR:
  ├─ GitHub Action startet
  ├─ Prüft: "Gibt es morgen Spiel?"
  ├─ Falls JA:
  │  ├─ Claude (ich) analysiere automatisch
  │  ├─ Recherchiere TIER 1-4 Quellen
  │  ├─ Schreibe Tipps + Begründung in Google Sheets
  │  ├─ Speichere JSON in output/tipps.json
  │  └─ GitHub pusht
  └─ Make.com liest output/tipps.json
     └─ Make.com trägt in Kicktipp ein

RESULT:
  ├─ Du siehst auf Handy: Google Sheets (Tipps + Begründung)
  ├─ Tipps sind in GitHub (Backup)
  └─ Tipps sind in Kicktipp (Ziel!)
```

---

## ⚙️ WAS CLAUDE MACHT

```
Input: "Morgen ist Bayern vs Stuttgart"

Claude:
  ├─ Recherchiert Oddspedia → "Bayern Quote 1.30"
  ├─ Recherchiert Understat → "Bayern xG 3.5 vs Stuttgart 0.8"
  ├─ Recherchiert LigaInsider → "Stuttgart 8 Ausfälle"
  ├─ Recherchiert Transfermarkt → "Bayern H2H 5:0 in letzten 5"
  ├─ Recherchiert WhoScored → "Bayern Form 4W-1D"
  ├─ Analysiert alle Daten
  ├─ Tipp: Bayern 2:0 (96%)
  └─ Schreibt alles in Google Sheet

Output:
  ├─ Google Sheet: Row mit Tipps + 5 Begründungen
  ├─ JSON: Für Make.com
  └─ Fertig!
```

---

## 📞 TROUBLESHOOTING

**Problem: Google Sheets wird nicht aktualisiert**
- Check GitHub Actions Logs
- Ist GOOGLE_SHEET_ID richtig?
- Ist GOOGLE_CREDENTIALS_JSON gültig?
- Hat Service Account Zugriff auf Sheet?

**Problem: Make.com trägt nicht ein**
- Ist output/tipps.json vorhanden?
- Ist Make.com korrekt konfiguriert?
- Sind die GitHub Secrets gesetzt?

**Problem: Keine Tipps generiert**
- Gibt es morgen wirklich ein Spiel?
- GitHub Actions Logs anschauen
- Ist ANTHROPIC_API_KEY gültig?

---

## ✅ CHECKLISTE

```
☐ Google Sheet erstellt ("Kicktipp Tipps")
☐ Service Account erstellt
☐ Service Account hat Zugriff auf Sheet
☐ Sheet ID in GitHub Secret
☐ JSON-Credentials in GitHub Secret
☐ ANTHROPIC_API_KEY in GitHub Secret
☐ Script hochgeladen
☐ Workflow hochgeladen
☐ Test-Run gemacht
☐ Google Sheet hat Tipps bekommen!
☐ Make.com arbeitet
☐ Kicktipp hat Tipps!
```

---

## 🎉 RESULTAT

**Täglich um 06:00 Uhr:**
- Claude analysiert automatisch
- Tipps erscheinen in deinem Google Sheet
- Du siehst auf dem Handy: Tipps + Begründung
- Make.com trägt automatisch in Kicktipp ein
- **FERTIG!**

---

**Das ist die ECHTE, funktionierende Lösung!!!** ✅🚀⚽

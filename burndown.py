#!/usr/bin/env python3
"""
Burndown chart del proyecto CARE — Unsa-ips-grupo
Consulta el GitHub Project (Projects v2) vía API GraphQL, obtiene los
Estimates (Story Points) por Sprint y Status, y genera burndown.png.

Requiere:
  - Variable de entorno PROJECT_TOKEN (token con scopes: repo, read:project)
  - pip install requests matplotlib

Se ejecuta desde GitHub Actions (ver burndown.yml) o localmente.
"""

import os
import sys
from datetime import date, datetime

import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ============ CONFIGURACIÓN ============
ORG = "Unsa-ips-grupo"
PROJECT_NUMBER = 8

# Calendario de sprints (inicio, fin) — alineado al plan del equipo
SPRINTS = {
    "Sprint 1": (date(2026, 5, 25), date(2026, 6, 5)),
    "Sprint 2": (date(2026, 6, 8), date(2026, 6, 19)),
    "Sprint 3": (date(2026, 6, 22), date(2026, 7, 3)),
    "Sprint 4": (date(2026, 7, 6), date(2026, 7, 13)),
}
OUTPUT = "burndown.png"
# =======================================

TOKEN = os.environ.get("PROJECT_TOKEN")
if not TOKEN:
    sys.exit("ERROR: falta la variable de entorno PROJECT_TOKEN")

QUERY = """
query($org: String!, $number: Int!, $cursor: String) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          fieldValues(first: 20) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldIterationValue {
                title
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_items():
    """Descarga todos los items del Project con sus campos."""
    items, cursor = [], None
    while True:
        resp = requests.post(
            "https://api.github.com/graphql",
            json={"query": QUERY, "variables": {"org": ORG, "number": PROJECT_NUMBER, "cursor": cursor}},
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data:
            sys.exit(f"ERROR GraphQL: {data['errors']}")
        page = data["data"]["organization"]["projectV2"]["items"]
        items.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return items
        cursor = page["pageInfo"]["endCursor"]


def parse_item(node):
    """Extrae (sprint, estimate, status) de un item; tolera campos faltantes."""
    sprint = status = None
    estimate = 0
    for fv in node["fieldValues"]["nodes"]:
        fname = (fv.get("field") or {}).get("name", "")
        t = fv["__typename"]
        if t == "ProjectV2ItemFieldNumberValue" and fname.lower() == "estimate":
            estimate = fv.get("number") or 0
        elif t == "ProjectV2ItemFieldSingleSelectValue":
            if fname.lower() == "status":
                status = fv.get("name")
            elif "sprint" in fname.lower():
                sprint = fv.get("name")
        elif t == "ProjectV2ItemFieldIterationValue" and "sprint" in fname.lower():
            sprint = fv.get("title")
    return sprint, estimate, status


def normalize_sprint(raw):
    """'SPRINT 1' / 'sprint 1' / 'Sprint 1' -> 'Sprint 1'."""
    if not raw:
        return None
    digits = "".join(c for c in raw if c.isdigit())
    return f"Sprint {digits}" if digits else None


def main():
    print(f"Consultando Project #{PROJECT_NUMBER} de {ORG}...")
    items = fetch_items()

    total_sp = 0
    sp_by_sprint = {s: 0 for s in SPRINTS}
    done_by_sprint = {s: 0 for s in SPRINTS}

    for node in items:
        sprint_raw, est, status = parse_item(node)
        sprint = normalize_sprint(sprint_raw)
        if sprint not in SPRINTS or not est:
            continue
        total_sp += est
        sp_by_sprint[sprint] += est
        if status and status.strip().lower() == "done":
            done_by_sprint[sprint] += est

    print(f"Total SP: {total_sp}")
    for s in SPRINTS:
        print(f"  {s}: {sp_by_sprint[s]} SP planificados / {done_by_sprint[s]} completados")

    if total_sp == 0:
        sys.exit("ERROR: no se encontraron Estimates. Revisar nombres de campos (Estimate/Sprint/Status).")

    # ---- Construcción de las curvas ----
    today = date.today()
    start = list(SPRINTS.values())[0][0]
    end = list(SPRINTS.values())[-1][1]

    # Línea ideal: de total_sp a 0 entre inicio y fin del proyecto
    ideal_x = [start, end]
    ideal_y = [total_sp, 0]

    # Línea real: baja lo completado a lo largo de cada sprint (hasta hoy)
    real_x, real_y = [start], [total_sp]
    remaining = total_sp
    for s, (s_ini, s_fin) in SPRINTS.items():
        if today < s_ini:
            break
        done = done_by_sprint[s]
        point_date = min(s_fin, today)
        remaining -= done
        real_x.append(point_date)
        real_y.append(remaining)
        if today <= s_fin:
            break

    # ---- Gráfico ----
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=140)
    ax.plot(ideal_x, ideal_y, "--", color="#8a8f98", label="Ideal", linewidth=1.6)
    ax.plot(real_x, real_y, "-o", color="#1f7a6a", label="Real", linewidth=2.2, markersize=5)

    # Sombrear los sprints
    palette = ["#eef3f8", "#e8f2ee", "#fdf3e7", "#f5ecf7"]
    for i, (s, (s_ini, s_fin)) in enumerate(SPRINTS.items()):
        ax.axvspan(s_ini, s_fin, color=palette[i % 4], zorder=0)
        ax.text(s_ini, total_sp * 1.03, s, fontsize=8, color="#555")

    ax.set_title(f"Burndown — Proyecto CARE · {total_sp} Story Points · generado {today.strftime('%d/%m/%Y')}",
                 fontsize=11)
    ax.set_ylabel("Story Points restantes")
    ax.set_ylim(0, total_sp * 1.1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT)
    print(f"OK: {OUTPUT} generado.")


if __name__ == "__main__":
    main()

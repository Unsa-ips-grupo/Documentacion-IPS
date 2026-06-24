# Documentación IPS — CARE + care_fe

> **Curso:** Ingeniería y Procesos de Software  
> **Universidad:** UNSA · Escuela Profesional de Ingeniería de Sistemas  
> **Período:** Abril — Julio 2026 · Semestre 2026-A  
> **Docente:** Prof. Robert Arisaca

---

## Equipo — Grupo A1

| Rol | Integrante |
|-----|-----------|
| Líder Sprint 0 | Johan Vilca Flores |
| Líder Sprint 1 | Gustavo Alonso Yunque Quispe |
| Development Team | Henry Alex Navarro Quispe |
| Development Team | Franco Jesus Cahua Soto |
| Development Team | Alberth Edwar Riveros Vilca |

---

## 1. Producto de Software Seleccionado: CARE + care_fe

Hemos seleccionado **CARE** (Coronasafe Analysis Response Engine) como producto para el desarrollo del curso. Cumple con todos los criterios exigidos:

- **Dominio:** Sistema de Información Hospitalaria (HIS + EMR + EHR). Nació durante la pandemia COVID-19 para gestionar la red de UCIs de India. Opera en **11 estados** y beneficia a más de **186 millones de personas**.
- **Licencia:** MIT — completamente open-source bajo la organización [ohcnetwork](https://github.com/ohcnetwork).
- **Certificación:** Bien Público Digital (DPG) — reconocido por la Digital Public Goods Alliance (UNICEF, ONU, Noruega).
- **Complejidad:** Arquitectura dividida en dos repositorios con más de 40 módulos integrados, sistema de plugins, soporte FHIR y TeleICU.
- **Stack:** Python 3.11 + Django + DRF (backend) · React 18 + TypeScript 5 + Vite (frontend) · PostgreSQL · Redis + Celery · Docker Compose.
- **Repositorios fork:**
  - Backend → [Unsa-ips-grupo/care](https://github.com/Unsa-ips-grupo/care)
  - Frontend → [Unsa-ips-grupo/care_fe](https://github.com/Unsa-ips-grupo/care_fe)

### Repositorios upstream (originales)

| Repo | URL | Stars | Forks |
|------|-----|-------|-------|
| `ohcnetwork/care` (backend) | https://github.com/ohcnetwork/care | 375+ | 598+ |
| `ohcnetwork/care_fe` (frontend) | https://github.com/ohcnetwork/care_fe | 611+ | 1094+ |

---

## 2. Cronograma General (Sprints de 15 días)

| Sprint | Período | Objetivo | Estado |
|--------|---------|----------|--------|
| **Sprint 0** (Hito 1) | Hasta 13 de Mayo | Plan, selección de producto, roles, repositorio organizacional y GitHub Pages | Concluido |
| **Sprint 1** | 14 de Mayo — 27 de Mayo | Setup técnico: levantar CARE + care_fe en local con Docker, analizar módulos y documentar en Wiki | Concluido |
| **Sprint 2** (Hito 2) | 28 de Mayo — 10 de Junio | Pipeline CI/CD funcionando en GitHub Actions (lint, tests, build Docker) | Concluido |
| **Sprint 3** | 11 de Junio — 24 de Junio | Mejora funcional sobre un módulo de care_fe y despliegue a staging | En progreso |
| **Sprint 4** (Hito 3) | 25 de Junio — 13 de Julio | Entrega final: artículo IEEE, demo en vivo y documentación completa · **100% del trabajo final** | Pendiente |

---

## 3. Stack Tecnológico

### Backend — `ohcnetwork/care`

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| Python | 3.11+ | Lenguaje principal |
| Django + DRF | 4.x / 3.x | Framework web y API REST |
| PostgreSQL | 14+ | Base de datos relacional |
| Redis + Celery | Redis 7 | Cola de tareas asíncronas |
| Docker Compose | v2 | Orquestación local (`make up`) |

### Frontend — `ohcnetwork/care_fe`

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| React | 18+ | Librería UI (SPA) |
| TypeScript | 5.x | Tipado estático |
| Vite + Tailwind CSS | Vite 5 / Tailwind 3 | Build y estilos |
| Playwright | — | Tests E2E |

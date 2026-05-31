# Health Monitor AI

# Despre Proiect

Realizat pentru monitorizarea stării de sănătate, folosind date provenite de la un smartwatch și tehnici AI.

Aplicația analizează date precum:
  - ritmul cardiac
  - somnul
  - nivelul de stres
  - numărul de pași

și oferă recomandări privind starea de sănătate a utilizatorului, folosind tehnici de procesare și analiză a datelor.

---
# Funcționalități
- REST API pentru preluarea datelor biometrice
- Analiza ritmului cardiac
- Analiza somnului
- Calcularea unui health score
- Validarea datelor de intrare
- Normalizarea valorilor biometrice
- Salvarea istoricului datelor

---
# Tehnologii folosite

## Backend
- Python
- Flask

## Alte librării
- JSON
- Requests
- OpenAI API (planificat)

---
# Licență

Proiect realizat în scop educațional.
---
#Fluxul aplicației
1. Utilizatorul introduce date biometrice provenite de la smartwatch.
2. Datele sunt validate și normalizate.
3. Sistemul analizează ritmul cardiac, somnul și activitatea fizică.
4. Se calculează un Health Score.
5. Datele sunt salvate pentru analiză ulterioară.
6. Dashboard-ul afișează rezultatele și recomandările.
---
## Arhitectura Proiectului

```text
health-monitor-ai/
│
├── backend/
│   ├── api.py
│   ├── analysis.py
│   └── storage.py
│
├── frontend/
│   └── app.py
│
├── ai-agent/
│
├── data/
│   └── health_data.json
│
└── README.md
```
---
#Istalare
- clonează repository-ul:
   - git clone
- instalează dependențele
   - pip install -r requirements.txt
- pornește aplicația
   - python backend/api.py
- pentru dashboard
   - streamlit run frontend/app.py
---
#Exemplu de utilizare
##Exemplu input
{
  "heart_rate": 75,
  "sleep_hours": 7.5,
  "steps": 8500
}

##Exemplu Output

{
  "health_score": 84,
  "health_status": "good"
}
---
# Business Intelligence Features

- Monitorizarea ritmului cardiac
- Analiza calității somnului
- Monitorizarea activității fizice
- Calcularea unui Health Score
- Vizualizarea indicatorilor de sănătate
- Analiza tendințelor în timp
- Recomandări pentru îmbunătățirea stilului de viață
---
# Contributors
- [ungureanuIrinuca](https://github.com/ungureanuIrinuca)
- [Deny0511](https://github.com/Deny0511)
- [elenasotoc5](https://github.com/elenasotoc5)
- [andreimihnea05](https://github.com/andreimihnea05)
---

# Counterfactual Inflation Analysis:
## What If Ukraine Had Been Part of the Euro Area?
### Quantitative Methods in Finance — Final Project
**Hanane LARBI — Master 2 Finance, Technology & Data**
**Université Paris 1 Panthéon-Sorbonne (2025–2026)**

---

## Project Objective

This project studies a counterfactual macroeconomic question:

> What would Ukraine's inflation trajectory have looked like if Ukraine had been a member of the Euro Area?

The analysis combines economic reasoning on monetary sovereignty and Optimal Currency Area (OCA) theory with econometric methods studied during the course. The objective is to construct a plausible counterfactual inflation path for Ukraine under hypothetical Euro Area membership and compare it with observed inflation dynamics.

---

## Economic Motivation

Ukraine experienced several major inflationary and exchange-rate crises during the sample period:
- the 2008–2009 global financial crisis,
- the 2014–2015 Crimea annexation and Donbas conflict,
- the 2022 full-scale Russian invasion.

These crises were associated with large hryvnia depreciations and strong inflation spikes. The project investigates whether Euro Area membership — through imported ECB credibility and the absence of exchange-rate devaluations — could have reduced inflation volatility. At the same time, the analysis also considers the potential costs of losing monetary sovereignty during asymmetric geopolitical shocks.

---

## Methodological Framework

### 1. Preliminary Monetary Regime Analysis (Part A)

A chronological analysis of Ukraine's exchange-rate and monetary regimes between 2000 and 2025:
- de facto dollar pegs (2000–2008, 2010–2014),
- major devaluation episodes (2008-09, 2014-15, 2022),
- capital controls,
- transition toward inflation targeting (2016),
- wartime exchange-rate stabilization (2022–2023).

This section is used to construct regime-dependent treatment intensity weights in the counterfactual analysis. The key finding: Ukraine had genuine monetary sovereignty only during the devaluation episodes and the post-2016 inflation targeting period — not during the peg periods.

### 2. PCA Common Inflation Factor

A Principal Component Analysis (PCA) is applied to a panel of 11 Euro Area countries to extract a common inflation factor. The first principal component explains **84.7%** of EA inflation variance, validating the Ciccarelli-Mojon (2010) hypothesis that a single European factor drives most cross-country inflation co-movement. The EA cross-sectional mean serves as the baseline counterfactual.

### 3. Structural VAR (Blanchard-Quah Identification)

The core econometric framework is a trivariate Structural VAR including:
- Brent crude oil prices (external energy shock),
- Ukrainian industrial production growth (real activity),
- Ukrainian year-on-year inflation.

The Blanchard-Quah (1989) long-run restriction identifies:
- **oil shocks** — external, remain under EA membership,
- **supply shocks** — idiosyncratic to Ukraine (geopolitics, agriculture), remain under EA membership,
- **demand/monetary shocks** — replaced by EA demand shocks under the counterfactual.

The same trivariate SVAR is estimated for the Euro Area to extract EA structural demand shocks.

### 4. Regime-Weighted Counterfactual

The treatment effect varies across periods depending on Ukraine's degree of monetary sovereignty (from Part A):
- **weaker treatment** during exchange-rate peg periods (Ukraine already had no independent monetary policy),
- **stronger treatment** during devaluation and floating-rate periods (full monetary autonomy exercised).

The counterfactual resimulates Ukraine's VAR dynamics replacing inflation equation residuals with a weighted blend of EA demand residuals.

---

## Key Results

| Period | Actual inflation | Counterfactual | Gap |
|---|---|---|---|
| USD peg I (2006–2008) | ~10% | ~11% | ≈ 0pp |
| GFC 2008–09 | ~7% | ~9% | small |
| USD peg II (2010–2013) | ~10% | ~11% | ≈ 0pp |
| Crimea/Donbas 2014–15 | ~26% | ~20% | +6pp |
| Inflation targeting 2016–21 | ~9% | ~10% | small |
| Full-scale invasion 2022 | ~28% | ~20% | +8pp |

The counterfactual shows that monetary sovereignty was most costly during the 2014-15 and 2022 crises. During peg periods, the gap is near zero — Ukraine already had limited de facto monetary sovereignty.

---

## Data Sources

| Variable | Source | Period |
|---|---|---|
| EA HICP inflation (AT, BE, DE, ES, FI, FR, GR, IE, IT, NL, PT) | ECB Data Portal | 2000–2025 |
| Ukraine CPI (month-on-month index) | State Statistics Service of Ukraine (SSSU) | 2005–2025 |
| UAH/USD exchange rate | Stooq | 2005–2025 |
| Brent crude oil price (USD/bbl) | FRED — series DCOILBRENTEU | 2005–2025 |
| ECB deposit facility rate | FRED — series ECBDFR | 2005–2025 |
| Euro Area industrial production YoY | FRED — series EA19PRINTO01GYSAM | 2005–2023 |
| Ukraine industry value added growth | World Bank API — NV.IND.TOTL.KD.ZG (annual, interpolated to monthly) | 2005–2024 |

**Note on data harmonisation:** The ECB series are provided as year-on-year percentage changes. The Ukrainian CPI is provided as a month-on-month index (base = previous month). Conversion to year-on-year rates uses a 12-month rolling product of monthly indices, implemented in `src/01_data_preparation.py`.

---

## Repository Structure

```
Part A_Preliminary Analysis/
    Chronological Analysis.md        ← NBU regime chronology 2000–2025

ukraine_counterfactual/
    Notebooks/
        Analysis_part_final.ipynb    ← Baseline: PCA + Ciccarelli-Mojon
        External_Data_final.ipynb    ← External data download and validation
        SVAR_BQ.ipynb                ← Trivariate SVAR Blanchard-Quah counterfactual
    data/
        raw/                         ← Original ECB HICP panel + Ukraine CPI
        data_processed/              ← Transformed panel, baseline and SVAR results
        data_external/               ← UAH/USD, Brent, ECB rate, EA IP, Ukraine IP
    src/
        01_data_preparation.py       ← MoM → YoY conversion, panel construction

outputs/
    fig1_raw_series.png              ← Ukraine vs EA inflation with regime shading
    fig2_pca_diagnostics.png         ← PCA scree plot and loadings
    fig3_counterfactual_baseline.png ← Baseline counterfactual (EA mean)
    fig4_external_data.png           ← External data overview
    fig5_irf_blanchard_quah.png      ← Cumulative IRFs (Blanchard-Quah)
    fig6_counterfactual_svar.png     ← Final SVAR counterfactual
```

## How to Replicate

Run in order:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Data preparation
python ukraine_counterfactual/src/01_data_preparation.py

# 3. Run notebooks in order
#    Analysis_part_final.ipynb → External_Data_final.ipynb → SVAR_BQ.ipynb
```

All external data is downloaded programmatically inside the notebooks (FRED CSV API, World Bank API, Stooq). The UAH/USD file (`uahusd_m.csv`) was manually downloaded from Stooq and is provided in `data/data_external/`.

---

## References

- Mundell (1961) — A theory of optimum currency areas
- Blanchard & Quah (1989) — Dynamic effects of aggregate demand and supply disturbances
- Giavazzi & Pagano (1988) — The advantage of tying one's hands
- Calvo & Reinhart (2002) — Fear of floating
- Ciccarelli & Mojon (2010) — Global inflation
- Bayoumi & Eichengreen (1993) — Shocking aspects of European monetary integration
- De Grauwe (2012) — The governance of a fragile eurozone
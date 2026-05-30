# TAM/SAM/SOM Market Sizing Methodology

Market sizing serves as the foundational calculation for operational planning, sales capacity structuring, and outbound targets (e.g., headcount budgeting, lead volumes, and revenue expectations). This methodology maps standard bottom-up and top-down sizing calculations.

---

## 🦅 The Sizing Triad Definitions

*   **TAM (Total Addressable Market)**: The theoretical maximum global revenue potential if **100%** of the addressable market bought your product. Ignores geographical, language, or ICP constraints.
*   **SAM (Serviceable Addressable Market)**: The subset of TAM that you can realistically serve with your current product features, language support, geographical footprint, and technology integrations.
*   **SOM (Serviceable Obtainable Market)**: The subset of SAM that you can realistically capture within the next **12 to 36 months** given current team headcount, capital constraints, and brand equity. This is the core operational number that drives outbound planning.

---

## 📊 Sizing Calculation Frameworks

### 1. Top-Down Sizing (Macro-Analysis)
Uses third-party industry reports (Gartner, IDC, Statista) to estimate overall market sizes, then applies percentage filters:

$$\text{SAM} = \text{TAM} \times \% \text{ Geography Atte.} \times \% \text{ Segment Atte.} \times \% \text{ Tech Stack Comp.}$$

*Rule*: Top-down calculations frequently overestimate market sizes. Use primarily as a sanity check against bottom-up results.

### 2. Bottom-Up Sizing (Micro-Analysis - High Authority)
Uses primary data sources (LinkedIn Sales Navigator queries, database lists, government business registries) to build an active, countable database of target entities:

$$\text{SAM (Bottom-Up)} = \text{Count of Target Entities inside ICP} \times \text{ACV (Annual Contract Value)}$$

---

## ⚖️ The 3 SOM Penetration Scenarios

For the 12-to-36-month horizon, apply three distinct penetration percentages to the bottom-up SAM to establish operational expectations:

| Scenario | SAM Penetration | Underlying Operational Logic |
| :--- | :--- | :--- |
| **Conservative** | **0.5% – 1.0%** | Outreach relies solely on cold outbound channels. Brand awareness is near-zero. No channel partnership support. |
| **Realistic** | **1.0% – 3.0%** | Cold outbound supported by basic inbound content marketing, paid retargeting, and 1-2 active channel partner relationships. |
| **Aggressive** | **3.0% – 7.0%** | High-velocity outbound, established brand leadership, mature partner ecosystem, and high inbound referral loops. |

---

## ⚙️ Outbound Capacity Planning Linking

Market sizing must dictate daily operational capacity, not just live as an abstract slide. Translate the **Realistic SOM** target into daily sales activities:

$$\text{Required SQLs / Month} = \frac{\text{Annual Closed Deals Target}}{\text{Opportunity Close Rate \%}} \div 12$$

$$\text{Required Outbound Contacts / Month} = \frac{\text{Required SQLs / Month}}{\text{SQL Response to Meeting Rate \%}}$$

*Example Capacity Calibration*:
*   **Target SOM**: \$1M ARR
*   **ACV**: \$20,000 (Requires 50 Closed Deals/Year)
*   **Close Rate**: 20% (Requires 250 SQLs/Year $\approx$ 21 SQLs/Month)
*   **Meeting Rate**: 2% (Requires 1,050 prospecting target contacts reached per month)
*   **SDR Quota**: 350 contacts/SDR/month $\implies$ **Requires 3 full-time SDRs**.

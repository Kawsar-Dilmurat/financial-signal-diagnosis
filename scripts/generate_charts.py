import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'

df = pd.read_csv('/mnt/user-data/uploads/financial_statements_cleaned.csv')

NAVY = "#1a3a5c"
ORANGE = "#e07b39"
BLUE_GRAD = ["#c9dcea", "#8fb8d6", "#4a7fa8", "#1a3a5c"]
RED = "#c0392b"
GREY = "#b0bec5"

OUT = "/home/claude/finance-report/assets"

# ---------- 1. Profit Margin Ranking ----------
pm = pd.read_csv('/mnt/user-data/uploads/Profit_Margin_Ranking_data.csv')
pm = pm.sort_values('Avg. Net Profit Margin', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
colors = [ORANGE if v < 0 else NAVY for v in pm['Avg. Net Profit Margin']]
bars = ax.barh(pm['Company'], pm['Avg. Net Profit Margin'], color=colors, height=0.6)
for bar, val in zip(bars, pm['Avg. Net Profit Margin']):
    x = val + (0.5 if val >= 0 else -0.5)
    ha = 'left' if val >= 0 else 'right'
    ax.text(x, bar.get_y() + bar.get_height()/2, f"{val:.2f}", va='center', ha=ha, fontsize=13)
ax.set_title("Average Profit Margin Ranking (2009-2022)", fontsize=17, pad=15)
ax.set_xlabel("Avg. Net Profit Margin (%)", fontsize=13)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=11)
ax.axvline(0, color='#888', linewidth=0.8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/01-profit-margin-ranking.png", facecolor='white')
plt.close()
print("1 done")

# ---------- 2. Growth vs Margin ----------
gm = pd.read_csv('/mnt/user-data/uploads/Growth_vs_Margin_data.csv')
fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
sizes = gm['Avg. Market Cap(in B USD)'] / gm['Avg. Market Cap(in B USD)'].max() * 3000 + 200
colors_map = {'AAPL':'#4a7fa8','AMZN':'#c0392b','NVDA':'#5a9367','MCD':'#5aa39e','AIG':'#e0a039','PCG':'#d4b23c','SHLDQ':'#9b6b9e'}
for _, row in gm.iterrows():
    c = colors_map.get(row['Company'], '#888')
    ax.scatter(row['Avg. Revenue YoY Growth %'], row['Avg. Net Profit Margin'],
               s=row['Avg. Market Cap(in B USD)']/gm['Avg. Market Cap(in B USD)'].max()*3000+150,
               color=c, alpha=0.85, edgecolors='white', linewidth=1, zorder=3)
    ax.annotate(row['Company'], (row['Avg. Revenue YoY Growth %'], row['Avg. Net Profit Margin']),
                xytext=(0, -22), textcoords='offset points', ha='center', fontsize=13, fontweight='bold')
ax.axvline(0, color='#ccc', linewidth=1, zorder=1)
ax.set_title("Revenue Growth vs. Profit Margin", fontsize=17, pad=15)
ax.set_xlabel("Avg. Revenue YoY Growth %", fontsize=13)
ax.set_ylabel("Avg. Net Profit Margin", fontsize=13)
ax.tick_params(labelsize=12)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/02-growth-vs-margin.png", facecolor='white')
plt.close()
print("2 done")

# ---------- 3. Revenue Growth Index ----------
rg = pd.read_csv('/mnt/user-data/uploads/Revenue_Growth_Index_data.csv')
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
colors_map3 = {'AAPL':'#4a7fa8','AIG':'#e0a039','AMZN':'#c0392b','MCD':'#5aa39e','NVDA':'#5a9367','PCG':'#d4b23c','SHLDQ':'#9b6b9e'}
for company, group in rg.groupby('Company'):
    group = group.sort_values('Year')
    ax.plot(group['Year'], group['Revenue Index (Base=100)'], label=company, color=colors_map3[company], linewidth=2.2)
    last = group.iloc[-1]
    ax.annotate(company, (last['Year'], last['Revenue Index (Base=100)']),
                xytext=(6, 0), textcoords='offset points', va='center', fontsize=12, fontweight='bold', color=colors_map3[company])
ax.set_title("Revenue Growth Index (Base = 100)", fontsize=17, pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Revenue Index (Base=100)", fontsize=13)
ax.tick_params(labelsize=11)
ax.set_xlim(2008, 2024)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/03-revenue-growth-index.png", facecolor='white')
plt.close()
print("3 done")

print("ALL DONE")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT = "/home/claude/finance-report/assets"
df = pd.read_csv('/mnt/user-data/uploads/financial_statements_cleaned.csv')

POS = "#e07b39"
NEG = "#4a7fa8"

def equity_ni_panel(company, ax_ni, ax_eq, title):
    d = df[df['Company'] == company].sort_values('Year')
    colors_ni = [NEG if v < 0 else POS for v in d['Net Income']]
    colors_eq = [NEG if v < 0 else POS for v in d['Share Holder Equity']]
    ax_ni.bar(d['Year'], d['Net Income'], color=colors_ni, width=0.7)
    ax_ni.set_title(title, fontsize=16)
    ax_ni.set_ylabel("Net Income", fontsize=12)
    ax_ni.axhline(0, color='#888', linewidth=0.8)
    ax_ni.tick_params(labelsize=10)
    for s in ['top','right']: ax_ni.spines[s].set_visible(False)

    ax_eq.bar(d['Year'], d['Share Holder Equity'], color=colors_eq, width=0.7)
    ax_eq.set_ylabel("Shareholder Equity", fontsize=12)
    ax_eq.axhline(0, color='#888', linewidth=0.8)
    ax_eq.tick_params(labelsize=10)
    ax_eq.set_xlabel("Year", fontsize=12)
    for s in ['top','right']: ax_eq.spines[s].set_visible(False)

# ---------- 05. MCD vs Sears equity (side by side) ----------
fig, axes = plt.subplots(2, 2, figsize=(13, 7), dpi=150, sharex='col')
equity_ni_panel('MCD', axes[0,0], axes[1,0], "MCD")
equity_ni_panel('SHLDQ', axes[0,1], axes[1,1], "SHLDQ")
plt.tight_layout()
plt.savefig(f"{OUT}/05-mcd-sears-equity.png", facecolor='white')
plt.close()
print("5 done")

# ---------- 06. Sears three-line index ----------
s = df[df['Company'] == 'SHLDQ'].sort_values('Year').copy()
s['Gross_Margin_%'] = s['Gross Profit'] / s['Revenue'] * 100
for col, label in [('Revenue','Revenue_Index'), ('Gross_Margin_%','Gross_Margin_Index'), ('Current Ratio','Current_Ratio_Index')]:
    base = s[col].iloc[0]
    s[label] = s[col] / base * 100

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
lines = [('Revenue_Index', '#c0392b', 'Revenue'), ('Gross_Margin_Index', '#e0a039', 'Gross Margin'), ('Current_Ratio_Index', '#4a7fa8', 'Current Ratio')]
offsets = {'Revenue': -18, 'Gross Margin': 14, 'Current Ratio': -4}
for col, color, label in lines:
    ax.plot(s['Year'], s[col], color=color, linewidth=2.4, label=label)
    last = s.iloc[-1]
    ax.annotate(f"{label}\n{last[col]:.1f}", (last['Year'], last[col]), xytext=(8, offsets[label]),
                textcoords='offset points', fontsize=12, fontweight='bold', color=color, va='center')
ax.set_title("Sears: Three Metrics Declining Together (2009=100)", fontsize=16, pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Index (2009=100)", fontsize=13)
ax.tick_params(labelsize=11)
ax.set_xlim(2008, 2021)
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/06-sears-three-line-index.png", facecolor='white')
plt.close()
print("6 done")

# ---------- 08. AIG EBITDA, Net Income, CFO ----------
a = df[df['Company'] == 'AIG'].sort_values('Year')
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
series = [('EBITDA', '#c0392b'), ('Net Income', '#e0a039'), ('Cash Flow from Operating', '#5a9367')]
offsets2 = {'EBITDA': 10, 'Net Income': -14, 'Cash Flow from Operating': 10}
for col, color in series:
    ax.plot(a['Year'], a[col], color=color, linewidth=2.4, label=col)
    last = a.iloc[-1]
    ax.annotate(f"{col}\n{last[col]:,.0f}", (last['Year'], last[col]), xytext=(8, offsets2[col]),
                textcoords='offset points', fontsize=11.5, fontweight='bold', color=color, va='center')
ax.axhline(0, color='#ccc', linewidth=1)
ax.set_title("AIG: EBITDA, Net Income & Operating Cash Flow", fontsize=16, pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Value ($M)", fontsize=13)
ax.tick_params(labelsize=11)
ax.set_xlim(2008, 2025)
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/08-aig-ebitda-vs-net-income.png", facecolor='white')
plt.close()
print("8 done")

# ---------- 09 & 10. Implied Shares vs Equity ----------
def shares_equity_chart(company, title, filename):
    d = df[df['Company'] == company].sort_values('Year').copy()
    d['Implied_Shares'] = d['Net Income'] / d['Earning Per Share']
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), dpi=150, sharex=True)
    ax1.plot(d['Year'], d['Share Holder Equity'], color='#e07b39', linewidth=2.4)
    ax1.axhline(0, color='#ccc', linewidth=1)
    ax1.set_ylabel("Avg. Share\nHolder Equity", fontsize=12)
    ax1.tick_params(labelsize=11)
    ax1.set_title(title, fontsize=16, pad=12)
    for s_ in ['top','right']: ax1.spines[s_].set_visible(False)

    ax2.plot(d['Year'], d['Implied_Shares'], color='#7d5a9e', linewidth=2.4)
    ax2.set_ylabel("Implied Shares\nOutstanding (M)", fontsize=12)
    ax2.set_xlabel("Year", fontsize=13)
    ax2.tick_params(labelsize=11)
    for s_ in ['top','right']: ax2.spines[s_].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{OUT}/{filename}", facecolor='white')
    plt.close()

shares_equity_chart('MCD', "McDonald's: Buybacks Track the Equity Decline", "09-mcd-shares-vs-equity.png")
print("9 done")
shares_equity_chart('SHLDQ', "Sears: Equity Collapsed, Share Count Didn't", "10-sears-shares-vs-equity.png")
print("10 done")

print("ALL DONE")

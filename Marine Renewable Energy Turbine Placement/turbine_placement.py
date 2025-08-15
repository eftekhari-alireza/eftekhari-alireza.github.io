import random
import time
import numpy as np
from datetime import datetime
import sys
from IPython.display import clear_output, display
from ipyleaflet import Map, basemaps, CircleMarker, LayersControl
from ipywidgets import VBox, HBox, Button, Dropdown, HTML, Textarea

# Device specifications and constants
device_specs = {
    'wind':  {'cost': 3e6, 'mw': 4, 'color': 'blue',  'name': 'Wind Turbine'},
    'wave':  {'cost': 2e6, 'mw': 1, 'color': 'green', 'name': 'Wave Converter'},
    'tidal': {'cost': 4e6, 'mw': 2, 'color': 'red',   'name': 'Tidal Turbine'}
}
DEFAULT_BUDGET = 30e6
MAX_DEVICES   = 10

# Typing effect
def print_slow(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

# Calculate energy output
def calculate_annual_output(dev_type, quality):
    capacity_factors = {'wind': 0.40, 'wave': 0.30, 'tidal': 0.35}
    hours = 8760
    mw = device_specs[dev_type]['mw']
    return mw * hours * capacity_factors[dev_type] * quality

# Quality label
def get_quality_description(q):
    if q > 1.2:   return "🌟 Exceptional"
    if q > 1.0:   return "⚡ Excellent"
    if q > 0.8:   return "✓ Good"
    if q > 0.6:   return "~ Moderate"
    return "△ Marginal"

# Ordinal helper for rankings
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

class MarineMapGame:
    def __init__(self, student_name):
        self.name    = student_name
        self.budget  = DEFAULT_BUDGET
        self.placed  = []
        self.counter = 0

        # Map widget\
        self.map = Map(
            center=(53.2, -8.0), zoom=6,
            basemap=basemaps.CartoDB.Positron,
            layout={'height': '400px'}
        )
        self.map.add_control(LayersControl())

        self.device_dd  = Dropdown(options=list(device_specs.keys()), description='Device:')
        self.finish_btn = Button(description='Finish', button_style='success')
        self.status     = HTML()
        self.log_area   = Textarea(value='', layout={'width':'100%','height':'250px'}, disabled=True)

        self.finish_btn.on_click(self._finish)
        self.map.on_interaction(self._on_click)

    def start(self):
        self._update_status()
        display(VBox([
            HBox([self.device_dd, self.finish_btn]),
            self.status,
            self.map,
            self.log_area
        ]))

    def _log_slow(self, text, delay=0.02):
        for ch in text:
            self.log_area.value += ch
            time.sleep(delay)
        self.log_area.value += "\n"

    def _on_click(self, **kwargs):
        if kwargs.get('type') != 'click': return
        lat, lon = kwargs['coordinates']
        if len(self.placed) >= MAX_DEVICES:
            self._update_status('Max placed!')
            return
        dev  = self.device_dd.value
        spec = device_specs[dev]
        if self.budget < spec['cost']:
            self._update_status('Insufficient funds!')
            return

        marker = CircleMarker(location=(lat, lon), radius=8, color=spec['color'], fill=True)
        self.map.add_layer(marker)

        self.counter += 1
        # Simulated quality
        if dev == 'wind':
            base = 1.25 if lon < -9.5 else (1.0 if lon < -8.5 else 0.7)
        elif dev == 'wave':
            base = 1.3  if lon < -10 else (1.1 if lon < -9 else 0.5)
        else:
            base = 1.3 if (54.3 < lat < 54.5 and -5.6 < lon < -5.4) else 0.6
        quality = base * random.uniform(0.9, 1.1)

        self.placed.append({
            'id': self.counter,
            'type': dev,
            'lat': lat,
            'lon': lon,
            'mw': spec['mw'],
            'cost': spec['cost'],
            'quality': quality
        })
        self.budget -= spec['cost']
        self._update_status()

    def _update_status(self, warn=None):
        text = f"Budget: €{self.budget/1e6:.1f}M | Devices: {len(self.placed)}/{MAX_DEVICES}"
        if warn:
            text += f" (<span style='color:red'>{warn}</span>)"
        self.status.value = text

    def _finish(self, _btn):
        clear_output(wait=True)
        display(VBox([
            HBox([self.device_dd, self.finish_btn]),
            self.status,
            self.map,
            self.log_area
        ]))
        self.log_area.value = ''

        # Intro & Summary
        self._log_slow(f"\n🏁 Deployment complete, {self.name}! Analyzing your strategy...", 0.05)
        time.sleep(1)

        spent = DEFAULT_BUDGET - self.budget
        for d in self.placed:
            d['annual_mwh'] = calculate_annual_output(d['type'], d['quality'])
        total_mw  = sum(d['mw'] for d in self.placed)
        total_mwh = sum(d['annual_mwh'] for d in self.placed)
        counts    = {t: sum(1 for d in self.placed if d['type']==t) for t in device_specs}

        self._log_slow(f"\n{self.name}'s Strategic Deployment Summary:", 0.04)
        self._log_slow(f"• Budget used: €{spent/1e6:.1f}M of €30M", 0.03)
        self._log_slow(f"• Devices: {len(self.placed)} (Wind: {counts['wind']}, Wave: {counts['wave']}, Tidal: {counts['tidal']})", 0.03)
        self._log_slow(f"• Capacity: {total_mw} MW", 0.03)
        self._log_slow(f"• Annual output: {total_mwh:,.0f} MWh", 0.03)

        # Environmental impact
        self._log_slow("\n🌍 ENVIRONMENTAL IMPACT:", 0.04)
        co2   = total_mwh * 0.45
        homes = int(total_mwh / 4.2)
        self._log_slow(f"• CO₂ savings: {co2:,.0f} tons/yr", 0.03)
        self._log_slow(f"• Homes powered: {homes:,}", 0.03)
        self._log_slow(f"• Trees eq.: {int(co2*45):,}", 0.03)

        # Location analysis (all turbines)
        self._log_slow("\n📍 LOCATION ANALYSIS:", 0.04)
        sorted_devs = sorted(self.placed, key=lambda x: x['annual_mwh'], reverse=True)
        for i, d in enumerate(sorted_devs, 1):
            rank = ordinal(i)
            desc = get_quality_description(d['quality'])
            self._log_slow(
                f"{rank}: {device_specs[d['type']]['name']} #{d['id']} @ "
                f"{d['lat']:.2f}N,{abs(d['lon']):.2f}W | {desc} | {d['annual_mwh']:,.0f} MWh",
                0.02
            )

        # Real-world regional potentials
        self._log_slow("\n🗺️ REGIONAL RESOURCE POTENTIAL:", 0.04)
        self._log_slow(
            "Offshore wind: High potential on the Atlantic west and southwest coasts (e.g. Donegal Bay, Cork/Kerry); "
            "lower in the Irish Sea (east coast).", 0.03
        )  # Based on SEAI Wind Atlas ([seai.ie](https://www.seai.ie/renewable-energy/wind-energy/wind-atlas-map?utm_source=chatgpt.com))
        self._log_slow(
            "Wave energy: Highest along the Atlantic west coast (Mizen Head to Achill), "
            "minimal on east and south coasts.", 0.03
        )  # Based on Marine Renewable Energy Atlas ([atlas.marine.ie](https://atlas.marine.ie/OceanEnergy.html?utm_source=chatgpt.com))
        self._log_slow(
            "Tidal energy: Strong currents in Shannon Estuary (up to 2.3 m/s) "
            "and Strangford Lough; weaker tidal streams in open Atlantic and Irish Sea.", 0.03
        )  # Based on ScienceDirect study ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0960148121017742?utm_source=chatgpt.com))

        # Strategic insights
        self._log_slow("\n🎯 STRATEGIC INSIGHTS:", 0.04)
        if any(d['type']=='wind' and d['quality']>1.1 for d in self.placed):
            self._log_slow("✓ You harnessed strong Atlantic winds!", 0.03)
        else:
            self._log_slow("💡 Consider moving turbines further west or southwest for better wind.", 0.03)
        if any(d['type']=='wave' and d['quality']>1.2 for d in self.placed):
            self._log_slow("✓ You picked high-energy wave sites!", 0.03)
        else:
            self._log_slow("💡 Try placing wave converters along the Mizen Head–Achill stretch.", 0.03)
        if any(d['type']=='tidal' and d['quality']>1.15 for d in self.placed):
            self._log_slow("✓ You captured strong tidal currents!", 0.03)
        else:
            self._log_slow("💡 Targets like Shannon Estuary & Strangford Lough have highest tide."), 0.03

        # Efficiency rating
        efficiency = (total_mwh / spent) * 1e6
        self._log_slow(f"\n💰 EFFICIENCY RATING: {efficiency:.1f} MWh/€1M", 0.04)
        if efficiency > 500:
            self._log_slow("🌟 Outstanding efficiency!", 0.03)
        elif efficiency > 400:
            self._log_slow("👍 Solid strategy!", 0.03)
        else:
            self._log_slow("🔍 Opportunities exist to optimize placements based on real regional data.", 0.03)

# Runner
def run_marine_game():
    clear_output()
    print("\n" + "="*80)
    print_slow("🌊 MARINE ENERGY STRATEGIC DEPLOYMENT CHALLENGE 🌊", 0.05)
    print("="*80)
    print_slow("\nWelcome, future energy strategists!", 0.04)
    print_slow("You have €30M to deploy marine renewables around Ireland.", 0.03)
    print_slow("But you won't know output until after placements!", 0.03)
    print("\n" + "-"*80)
    name = input("\nEnter your codename, Strategist: ") or "Strategist"
    print_slow(f"\nReady, {name}? Let's plan!", 0.04)
    print("\nYour arsenal:")
    for k,v in device_specs.items():
        print(f"- {v['name']}: €{int(v['cost']/1e6)}M | {v['mw']}MW")
    print("\n" + "-"*80)
    input("\nPress Enter to launch the strategic map...")
    game = MarineMapGame(name)
    game.start()

if __name__ == '__main__':
    run_marine_game()

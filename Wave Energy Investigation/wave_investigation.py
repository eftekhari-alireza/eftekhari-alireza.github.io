import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import time
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime

answer = None
score = 0


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def create_power_plot(months, wave_heights, wave_periods, wave_power_kW, avg_wave_height,
                      avg_wave_period, avg_power, annual_energy_MWh, homes_powered, location_name):
    """Create and save a colorful wave power plot for the location"""
    # Create colorful power plot
    plt.figure(figsize=(12, 8))

    # Create subplot for wave power
    plt.subplot(2, 1, 1)

    # Ocean-themed colormap from deep blue to aqua to yellow
    colors = ["#08519c", "#3182bd", "#6baed6", "#9ecae1",
              "#c6dbef", "#deebf7", "#fee391", "#fec44f"]
    cmap = LinearSegmentedColormap.from_list("ocean_colors", colors)

    # Plot with colorful bars
    bars = plt.bar(range(1, 13), wave_power_kW, color=cmap(np.linspace(0, 1, 12)))
    plt.xticks(range(1, 13), labels=months, rotation=45)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{height:.0f}', ha='center', va='bottom', fontsize=9)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylabel('Wave Power (kW/m)', fontsize=12)
    plt.title(f'Wave Power Output at {location_name} (kW per meter of wave crest)', fontsize=14)

    # Create subplot for wave heights and periods
    plt.subplot(2, 1, 2)

    # Plot wave heights and periods
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    # Wave heights as bars
    bars1 = ax1.bar(range(1, 13), wave_heights, alpha=0.7, color='steelblue', label='Wave Height')
    # Wave periods as line
    line1 = ax2.plot(range(1, 13), wave_periods, 'o-', color='darkgreen', linewidth=2,
                     markersize=8, label='Wave Period')

    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(months, rotation=45)
    ax1.set_ylabel('Significant Wave Height (m)', fontsize=12, color='steelblue')
    ax2.set_ylabel('Average Wave Period (s)', fontsize=12, color='darkgreen')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax2.tick_params(axis='y', labelcolor='darkgreen')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Add legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Wave Climate Parameters', fontsize=12)

    # Add information box
    info_text = (
        f"🌊 Average wave height: {avg_wave_height:.1f} m\n"
        f"⏱️ Average wave period: {avg_wave_period:.1f} s\n"
        f"⚡ Average power: {avg_power:.1f} kW/m\n"
        f"🔋 Annual energy: {annual_energy_MWh:.1f} MWh\n"
        f"🏠 Can power: {homes_powered} homes"
    )

    plt.figtext(0.15, 0.02, info_text, bbox=dict(facecolor='lightblue', alpha=0.8), fontsize=10)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_wave_power_analysis.png"
    plt.savefig(output_file)
    plt.close()

    return output_file

def create_seasonal_analysis(months, wave_heights, wave_periods, location_name):
    """Create a seasonal wave climate analysis chart"""
    plt.figure(figsize=(10, 6))

    # Define seasons for wave energy (storm season vs calm season)
    seasons = {
        'Winter Storm': ['December', 'January', 'February'],
        'Spring Transition': ['March', 'April', 'May'],
        'Summer Calm': ['June', 'July', 'August'],
        'Autumn Build-up': ['September', 'October', 'November']
    }

    # Calculate seasonal averages for both height and period
    seasonal_avg_height = {}
    seasonal_avg_period = {}

    for season, season_months in seasons.items():
        # Get indices of months belonging to this season
        season_heights = []
        season_periods = []
        for i, month in enumerate(months):
            if month in season_months:
                season_heights.append(wave_heights[i])
                season_periods.append(wave_periods[i])

        # Calculate averages
        if season_heights:
            seasonal_avg_height[season] = sum(season_heights) / len(season_heights)
            seasonal_avg_period[season] = sum(season_periods) / len(season_periods)
        else:
            seasonal_avg_height[season] = 0
            seasonal_avg_period[season] = 0

    # Calculate wave power for each season (simplified: P ∝ H²T)
    seasonal_power = {}
    for season in seasons.keys():
        H = seasonal_avg_height[season]
        T = seasonal_avg_period[season]
        # Simplified wave power formula (relative units)
        seasonal_power[season] = H * H * T

    # Plot seasonal wave power potential
    seasons_list = list(seasonal_power.keys())
    power_list = list(seasonal_power.values())

    # Ocean-themed colors for seasons
    season_colors = ['#08519c', '#3182bd', '#fee391', '#fd8d3c']  # Dark blue, blue, yellow, orange

    bars = plt.bar(seasons_list, power_list, color=season_colors, width=0.6)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height:.1f}', ha='center', va='bottom', fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.ylabel('Wave Power Potential (H²T)', fontsize=12)
    plt.title(f'Seasonal Wave Energy Analysis - {location_name}', fontsize=14)

    # Find best and worst seasons
    best_season = seasons_list[power_list.index(max(power_list))]
    worst_season = seasons_list[power_list.index(min(power_list))]

    # Calculate seasonal variation
    if min(power_list) > 0:
        variation_factor = max(power_list) / min(power_list)
    else:
        variation_factor = 0

    # Add detailed annotations
    plt.figtext(0.5, 0.01,
                f"Best season: {best_season} (H={seasonal_avg_height[best_season]:.1f}m, T={seasonal_avg_period[best_season]:.1f}s)\n"
                f"Calmest season: {worst_season} (H={seasonal_avg_height[worst_season]:.1f}m, T={seasonal_avg_period[worst_season]:.1f}s)\n"
                f"Power variation: {variation_factor:.1f}x between seasons\n"
                f"Note: Winter storms provide most energy but challenge device survival",
                ha='center', bbox=dict(facecolor='lightblue', alpha=0.8), fontsize=11)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_seasonal_wave_analysis.png"
    plt.savefig(output_file)
    plt.close()

    return output_file, best_season, worst_season, seasonal_avg_height, seasonal_avg_period

def create_wave_rose(wave_heights, location_name):
    """Create a wave rose diagram showing directional wave climate"""
    plt.figure(figsize=(8, 8))

    # Directions for the wave rose
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    # Create realistic directional weights based on Irish coast orientation
    # Wave energy on Irish coast is predominantly from W and SW (Atlantic)
    if "Northwest" in location_name or "North" in location_name:
        # Northwest/North coast - waves from W, NW, and N
        weights = [0.12, 0.05, 0.03, 0.02, 0.05, 0.20, 0.35, 0.18]
    elif "West" in location_name:
        # West coast - dominant W and SW waves
        weights = [0.05, 0.03, 0.02, 0.03, 0.08, 0.30, 0.40, 0.09]
    elif "Southwest" in location_name or "South" in location_name:
        # Southwest/South coast - SW dominant with some S
        weights = [0.04, 0.03, 0.05, 0.08, 0.15, 0.40, 0.20, 0.05]
    elif "Southeast" in location_name or "East" in location_name:
        # Southeast/East coast - more varied, some from E
        weights = [0.08, 0.12, 0.15, 0.10, 0.08, 0.15, 0.20, 0.12]
    else:
        # Default - typical Atlantic pattern
        weights = [0.06, 0.04, 0.03, 0.05, 0.10, 0.35, 0.30, 0.07]

    # Add location-specific random variation
    random.seed(sum(ord(c) for c in location_name))
    weights = [w * random.uniform(0.85, 1.15) for w in weights]

    # Normalize weights
    weights = [w / sum(weights) for w in weights]

    # Scale wave heights by directional weights
    avg_height = np.mean(wave_heights)
    directional_heights = [avg_height * w * 8 for w in weights]  # Scale for visibility

    # Plot the wave rose
    angles = np.linspace(0, 2*np.pi, len(directions), endpoint=False)

    # Close the plot
    directional_heights.append(directional_heights[0])
    angles = np.append(angles, angles[0])

    # Create polar plot
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, directional_heights, 'o-', linewidth=2, color='#1f77b4')
    ax.fill(angles, directional_heights, alpha=0.25, color='#1f77b4')

    # Set direction labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(directions)

    # Add gridlines
    ax.grid(True)

    # Find dominant direction
    dominant_idx = weights.index(max(weights))
    dominant_direction = directions[dominant_idx]
    dominant_percent = weights[dominant_idx] * 100

    # Title with wave climate info
    plt.title(f'Wave Rose - {location_name}\nDominant Wave Direction: {dominant_direction} ({dominant_percent:.1f}%)',
              size=14)

    # Save the wave rose
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_wave_rose.png"
    plt.savefig(output_file)
    plt.close()

    # Wave direction analysis
    weights_copy = weights.copy()
    weights_copy[dominant_idx] = 0
    secondary_idx = weights_copy.index(max(weights_copy))
    secondary_direction = directions[secondary_idx]

    direction_analysis = {
        'dominant': dominant_direction,
        'dominant_percent': dominant_percent,
        'secondary': secondary_direction,
        'secondary_percent': weights[secondary_idx] * 100,
        'exposure_rating': 'Highly exposed' if dominant_percent > 35 else 'Moderately exposed' if dominant_percent > 25 else 'Sheltered'
    }

    return output_file, dominant_direction, direction_analysis

def calculate_carbon_savings(annual_energy_MWh):
    """Calculate carbon savings from wave energy"""
    # CO2 emissions from fossil fuel electricity in Ireland
    fossil_emissions = 450  # kg CO2 per MWh

    # Calculate CO2 savings
    co2_savings = annual_energy_MWh * fossil_emissions
    co2_savings_tons = co2_savings / 1000

    # Environmental equivalents
    equivalent_trees = int(co2_savings / 22)  # One tree absorbs ~22 kg CO2/year
    cars_equivalent = int(co2_savings_tons / 4.6)  # Average car emits 4.6 tons CO2/year
    homes_powered = int(annual_energy_MWh / 4.2)  # Irish home uses ~4.2 MWh/year

    # Marine-specific benefits
    # Wave energy devices can act as artificial reefs
    reef_area = homes_powered * 2  # Rough estimate: 2m² of reef per home powered

    # Calculate percentage of Irish coastal communities
    # Ireland has about 200,000 coastal households
    percent_coastal = (homes_powered / 200000) * 100

    return {
        'co2_savings_tons': co2_savings_tons,
        'equivalent_trees': equivalent_trees,
        'cars_equivalent': cars_equivalent,
        'homes_powered': homes_powered,
        'percent_coastal': percent_coastal,
        'reef_area': reef_area
    }

def calculate_economic_factors(annual_energy_MWh, wave_farm_capacity_MW=30, location_name=""):
    """Calculate economic factors for a wave energy farm"""
    # Base parameters for wave energy
    electricity_price = 180  # €/MWh (higher than wind due to incentives)

    # Location-based factors for wave energy
    if "Fastnet" in location_name or "Aran" in location_name:
        # Extreme exposure - highest cost but best resource
        capacity_factor = 0.40  # 40% efficiency (good for wave energy)
        cost_per_MW = 6000000  # €6M per MW installed
        maintenance_factor = 0.045  # 4.5% of capital cost annually
    elif "Northwest" in location_name or "West" in location_name:
        # Good exposure - high performance
        capacity_factor = 0.35  # 35% efficiency
        cost_per_MW = 5500000  # €5.5M per MW
        maintenance_factor = 0.040  # 4% annually
    elif "South" in location_name:
        # Moderate exposure
        capacity_factor = 0.30  # 30% efficiency
        cost_per_MW = 5000000  # €5M per MW
        maintenance_factor = 0.035  # 3.5% annually
    else:
        # Sheltered sites - lower performance
        capacity_factor = 0.25  # 25% efficiency
        cost_per_MW = 4500000  # €4.5M per MW
        maintenance_factor = 0.030  # 3% annually

    # Calculate number of devices (assume 750kW devices)
    device_capacity = 0.75  # MW per device
    num_devices = int(wave_farm_capacity_MW / device_capacity)

    # Annual revenue
    annual_revenue = annual_energy_MWh * electricity_price

    # Installation costs
    installation_cost = wave_farm_capacity_MW * cost_per_MW

    # Additional marine-specific costs
    mooring_cost = num_devices * 250000  # €250k per device for mooring
    subsea_cable_cost = installation_cost * 0.20  # 20% for subsea cables
    marine_ops_cost = installation_cost * 0.10  # 10% for marine operations
    total_cost = installation_cost + mooring_cost + subsea_cable_cost + marine_ops_cost

    # Annual costs
    annual_maintenance = installation_cost * maintenance_factor
    annual_insurance = installation_cost * 0.015  # 1.5% for marine insurance
    annual_costs = annual_maintenance + annual_insurance

    # Annual profit
    annual_profit = annual_revenue - annual_costs

    # Simple payback period
    payback_period = total_cost / annual_profit if annual_profit > 0 else 999

    # Jobs created (marine energy creates more jobs)
    construction_jobs = num_devices * 20  # 20 jobs per device during construction
    permanent_jobs = num_devices * 1.5  # 1.5 permanent jobs per device
    marine_jobs = num_devices * 0.5  # Additional marine operations jobs

    return {
        'num_devices': num_devices,
        'annual_revenue': annual_revenue,
        'installation_cost': installation_cost,
        'mooring_cost': mooring_cost,
        'subsea_cable_cost': subsea_cable_cost,
        'marine_ops_cost': marine_ops_cost,
        'total_cost': total_cost,
        'annual_maintenance': annual_maintenance,
        'annual_insurance': annual_insurance,
        'annual_profit': annual_profit,
        'payback_period': payback_period,
        'capacity_factor': capacity_factor,
        'construction_jobs': int(construction_jobs),
        'permanent_jobs': int(permanent_jobs),
        'marine_jobs': int(marine_jobs)
    }

def generate_text_report(student_name, detective_rank, analyzed_locations, score):
    """Generate a professional text report for wave energy findings"""
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("WAVE ENERGY DETECTIVE CHALLENGE - FINAL REPORT")
    report_lines.append("="*60)
    report_lines.append(f"Marine Energy Detective: {student_name}")
    report_lines.append(f"Rank: {detective_rank}")
    report_lines.append(f"Date: {datetime.now().strftime('%d %B %Y')}")
    report_lines.append(f"Final Score: {score} points")
    report_lines.append("-"*60)

    # Sort locations by wave power potential (H²T)
    for loc in analyzed_locations:
        loc['wave_power_potential'] = loc['avg_wave_height']**2 * loc['avg_wave_period']

    sorted_locations = sorted(analyzed_locations,
                            key=lambda x: x['wave_power_potential'],
                            reverse=True)

    # Executive summary
    report_lines.append("EXECUTIVE SUMMARY:")
    report_lines.append("")

    best_location = sorted_locations[0]['name']
    report_lines.append(f"After analyzing {len(analyzed_locations)} coastal locations around Ireland,")
    report_lines.append(f"we have determined that {best_location} offers the best potential for")
    report_lines.append(f"wave energy development with average waves of {sorted_locations[0]['avg_wave_height']:.1f}m height")
    report_lines.append(f"and {sorted_locations[0]['avg_wave_period']:.1f}s period, producing {sorted_locations[0]['annual_energy_MWh']:.1f} MWh annually,")
    report_lines.append(f"enough to power {sorted_locations[0]['homes_powered']} homes.")

    # Location rankings
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("LOCATION RANKINGS (by wave power potential H²T):")
    report_lines.append("")

    for i, location in enumerate(sorted_locations):
        suitability = "SUITABLE" if location['is_suitable'] else "NOT SUITABLE"
        report_lines.append(f"{i+1}. {location['name']} - H²T={location['wave_power_potential']:.1f} - {suitability}")
        report_lines.append(f"   (H={location['avg_wave_height']:.1f}m, T={location['avg_wave_period']:.1f}s)")

    # Recommendations
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("RECOMMENDATIONS:")
    report_lines.append("")

    recommended = [loc for loc in sorted_locations if loc['is_suitable']]
    if recommended:
        report_lines.append("Based on our analysis, we recommend developing wave energy farms at:")
        for i, loc in enumerate(recommended[:3]):
            report_lines.append(f"{i+1}. {loc['name']}")

            # Add technical reasoning
            reasons = []
            if loc['wave_power_potential'] > 50:
                reasons.append("exceptional wave resource")
            if 'dominant_direction' in loc:
                reasons.append(f"consistent waves from {loc['dominant_direction']}")
            if 'best_season' in loc:
                reasons.append(f"peak energy in {loc['best_season']}")
            if 'carbon_savings' in loc:
                reasons.append(f"saving {loc['carbon_savings']:.1f} tons CO2 annually")

            if reasons:
                report_lines.append(f"   Key advantages: {', '.join(reasons)}")
    else:
        report_lines.append("None of the analyzed locations meet minimum requirements for wave farms.")
        report_lines.append("Minimum requirements: H²T > 20 (typically H>2m and T>8s)")

    # Detailed location analysis
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("DETAILED LOCATION ANALYSIS:")

    for i, location in enumerate(sorted_locations):
        report_lines.append("")
        report_lines.append(f"Location #{i+1}: {location['name']}")
        report_lines.append(f"Average Wave Height: {location['avg_wave_height']:.1f} m")
        report_lines.append(f"Average Wave Period: {location['avg_wave_period']:.1f} s")
        report_lines.append(f"Wave Power Potential (H²T): {location['wave_power_potential']:.1f}")
        report_lines.append(f"Average Power Output: {location['avg_power']:.1f} kW/m")
        report_lines.append(f"Annual Energy Production: {location['annual_energy_MWh']:.1f} MWh")
        report_lines.append(f"Homes Powered: {location['homes_powered']}")

        if 'best_season' in location:
            report_lines.append(f"Best Season: {location['best_season']}")
            report_lines.append(f"Calmest Season: {location.get('worst_season', 'Unknown')}")

        if 'direction_analysis' in location:
            da = location['direction_analysis']
            report_lines.append(f"Dominant Wave Direction: {da['dominant']} ({da['dominant_percent']:.1f}%)")
            report_lines.append(f"Exposure Rating: {da['exposure_rating']}")

        if 'environmental_impact' in location:
            ei = location['environmental_impact']
            report_lines.append(f"Environmental Benefits:")
            report_lines.append(f"  - CO2 Savings: {ei['co2_savings_tons']:.1f} tons/year")
            report_lines.append(f"  - Artificial Reef Area: {ei['reef_area']} m²")
            report_lines.append(f"  - Serves {ei['percent_coastal']:.2f}% of coastal communities")

        if 'economic_data' in location:
            econ = location['economic_data']
            report_lines.append(f"Economic Assessment (30MW farm):")
            report_lines.append(f"  - Wave Energy Converters: {econ['num_devices']} devices")
            report_lines.append(f"  - Annual Revenue: €{econ['annual_revenue']:,.0f}")
            report_lines.append(f"  - Total Investment: €{econ['total_cost']:,.0f}")
            report_lines.append(f"  - Annual Profit: €{econ['annual_profit']:,.0f}")
            report_lines.append(f"  - Payback Period: {econ['payback_period']:.1f} years")
            report_lines.append(f"  - Jobs: {econ['construction_jobs']} construction, {econ['permanent_jobs']} permanent, {econ['marine_jobs']} marine ops")

    # Conclusion
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("CONCLUSION:")
    report_lines.append("")
    report_lines.append("Ireland's Atlantic coastline offers world-class wave energy resources,")
    report_lines.append("particularly along the western and northwestern shores. Strategic")
    report_lines.append("development of wave energy could provide predictable renewable power,")
    report_lines.append("create marine industry jobs, and establish Ireland as a leader in")
    report_lines.append("ocean energy technology.")

    # Save to file
    report_filename = f"Wave_Detective_Report_{student_name.replace(' ', '_')}.txt"
    try:
        with open(report_filename, 'w') as f:
            f.write("\n".join(report_lines))
        return report_filename
    except Exception as e:
        print(f"Error saving report: {e}")
        return None

def mini_game_wave_physics():
    """Mini-game to test knowledge of wave energy physics"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("🌊 SPECIAL CHALLENGE: WAVE ENERGY PHYSICS EXPERT 🌊", 0.05)
    print("="*60)

    print_slow("\nThe Marine Energy Board wants to test your understanding")
    print_slow("of wave energy physics. Answer correctly to earn bonus points!")

    questions = [
        {
            "question": "What happens to wave power when wave height doubles?",
            "options": ["It doubles", "It triples", "It quadruples", "It stays the same"],
            "correct": 2,
            "explanation": "Wave power is proportional to the SQUARE of wave height (P ∝ H²). So doubling height quadruples the power!"
        },
        {
            "question": "Which wave parameter is most important for energy extraction?",
            "options": ["Wave height only", "Wave period only", "Both height and period equally", "Wave direction only"],
            "correct": 2,
            "explanation": "Wave power depends on BOTH height squared (H²) AND period (T). The formula is P ∝ H²T."
        },
        {
            "question": "Why does Ireland have excellent wave energy resources?",
            "options": ["Warm water", "Exposure to Atlantic Ocean", "Shallow seas", "Tidal effects"],
            "correct": 1,
            "explanation": "Ireland's exposure to the Atlantic Ocean means consistent swells travel thousands of miles, building up energy."
        },
        {
            "question": "What is the typical wave period for Atlantic swells?",
            "options": ["1-3 seconds", "4-6 seconds", "8-12 seconds", "15-20 seconds"],
            "correct": 2,
            "explanation": "Atlantic swells typically have periods of 8-12 seconds. Longer periods mean waves have traveled farther and carry more energy."
        },
        {
            "question": "What's the minimum average wave height generally needed for commercial wave farms?",
            "options": ["0.5 meters", "1.0 meters", "2.0 meters", "4.0 meters"],
            "correct": 2,
            "explanation": "Commercial wave energy typically needs average wave heights of at least 2 meters for economic viability."
        },
        {
            "question": "What challenge do wave energy devices face that wind turbines don't?",
            "options": ["Variable resource", "Corrosion from saltwater", "Visual impact", "Noise pollution"],
            "correct": 1,
            "explanation": "Wave energy devices must survive in corrosive saltwater and extreme storm conditions, making them more challenging to engineer."
        }
    ]

    score = 0
    for i, q in enumerate(questions):
        print("\n" + "-"*60)
        print_slow(f"Question {i+1}: {q['question']}")

        for j, option in enumerate(q['options']):
            print(f"{j+1}. {option}")

        answer = -1
        while answer < 1 or answer > len(q['options']):
            try:
                answer = int(input(f"\nYour answer (1-{len(q['options'])}): "))
            except ValueError:
                print("Please enter a valid number!")

        # Check if correct
        if answer - 1 == q['correct']:
            print_slow("✓ CORRECT! +5 points")
            score += 5
        else:
            print_slow(f"✗ Not quite. The correct answer is: {q['options'][q['correct']]}")

        # Show explanation
        print_slow(f"📚 {q['explanation']}")
        time.sleep(1)

    print("\n" + "-"*60)
    print_slow(f"You scored {score} out of {len(questions)*5} possible points!")

    if score >= len(questions)*5 * 0.8:
        print_slow("🌟 EXCELLENT! You're a wave energy physics expert!")
    elif score >= len(questions)*5 * 0.6:
        print_slow("👍 GOOD JOB! You understand the key principles of wave energy.")
    else:
        print_slow("🔍 Keep studying! Wave energy has unique physics challenges.")

    return score

def mini_game_device_selection():
    """Mini-game to select appropriate wave energy converter types"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("⚙️ SPECIAL CHALLENGE: WAVE ENERGY DEVICE SELECTOR ⚙️", 0.05)
    print("="*60)

    print_slow("\nThe Engineering Team needs your help selecting the right")
    print_slow("wave energy converter (WEC) type for different locations!")

    score = 0

    # Challenge 1: Device type for exposed Atlantic site
    print("\n" + "-"*60)
    print_slow("CHALLENGE #1: Device for Fastnet Rock (extreme exposure)")
    print_slow("\nThis site has 4m average waves with 12s periods and severe storms.")
    print_slow("Which device type would be most suitable?")

    options = [
        "Oscillating Water Column (OWC) - fixed to shore/seabed",
        "Point Absorber - floating buoy that bobs up and down",
        "Attenuator - long floating device parallel to waves",
        "Overtopping Device - waves flow over into reservoir"
    ]

    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    answer = -1
    while answer < 1 or answer > len(options):
        try:
            answer = int(input(f"\nYour choice (1-{len(options)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer == 2:  # Point Absorber
        print_slow("✓ EXCELLENT CHOICE! +10 points")
        print_slow("Point absorbers can survive extreme conditions by submerging in storms")
        print_slow("and are efficient at extracting energy from long-period swells.")
        score += 10
    elif answer == 3:  # Attenuator
        print_slow("✓ GOOD CHOICE! +7 points")
        print_slow("Attenuators like Pelamis can flex with waves and survive storms,")
        print_slow("though they need robust mooring in extreme conditions.")
        score += 7
    else:
        print_slow("✗ This device might struggle in such extreme conditions.")
        print_slow("Fixed structures face enormous forces in 10m+ storm waves.")

    # Challenge 2: Device for sheltered bay
    print("\n" + "-"*60)
    print_slow("CHALLENGE #2: Device for Dunmore East (sheltered, 1.5m waves)")
    print_slow("\nThis site has smaller waves but is close to shore with good grid access.")
    print_slow("Which approach makes most sense?")

    options2 = [
        "Large offshore wave farm with 30+ devices",
        "Small nearshore OWC integrated into harbor breakwater",
        "Floating attenuator farm in deep water",
        "Wait for bigger waves - site isn't suitable"
    ]

    for i, option in enumerate(options2):
        print(f"{i+1}. {option}")

    answer2 = -1
    while answer2 < 1 or answer2 > len(options2):
        try:
            answer2 = int(input(f"\nYour choice (1-{len(options2)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer2 == 2:  # Nearshore OWC
        print_slow("✓ PERFECT! +10 points")
        print_slow("Integrating wave energy into existing infrastructure like breakwaters")
        print_slow("reduces costs and is ideal for smaller wave climates.")
        score += 10
    elif answer2 == 4:  # Not suitable
        print_slow("✓ REASONABLE! +5 points")
        print_slow("You're right that 1.5m waves are marginal for commercial projects,")
        print_slow("but small demonstration projects could still be valuable.")
        score += 5
    else:
        print_slow("✗ Large offshore installations need bigger waves to be economic.")
        print_slow("Always match the technology scale to the available resource.")

    # Challenge 3: Storm survival strategy
    print("\n" + "-"*60)
    print_slow("CHALLENGE #3: Storm Survival Strategy")
    print_slow("\nA major Atlantic storm with 15m waves is approaching your wave farm.")
    print_slow("What's the best survival strategy for floating WECs?")

    options3 = [
        "Keep operating normally to capture maximum energy",
        "Increase mooring tension to hold position firmly",
        "Enter survival mode - submerge or reduce wave interaction",
        "Emergency retrieval - bring all devices to harbor"
    ]

    for i, option in enumerate(options3):
        print(f"{i+1}. {option}")

    answer3 = -1
    while answer3 < 1 or answer3 > len(options3):
        try:
            answer3 = int(input(f"\nYour choice (1-{len(options3)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer3 == 3:  # Survival mode
        print_slow("✓ EXCELLENT! +10 points")
        print_slow("Modern WECs have survival modes where they submerge, detune,")
        print_slow("or otherwise minimize wave loads during extreme conditions.")
        score += 10
    else:
        print_slow("✗ This could damage or destroy your devices!")
        print_slow("Extreme waves can be 100x more powerful than operating conditions.")
        print_slow("Smart devices protect themselves rather than chase extreme power.")

    print("\n" + "-"*60)
    print_slow(f"DEVICE SELECTION COMPLETE! You scored {score} out of 30 points!")

    if score >= 25:
        print_slow("🌟 EXCELLENT! You'd make a great wave energy engineer!")
    elif score >= 15:
        print_slow("👍 GOOD JOB! You understand key device selection principles.")
    else:
        print_slow("🔍 Wave device selection is complex - keep learning!")

    return score

# Main game function
def run_wave_detective_game():
    # Title screen
    clear_screen()
    print("\n" + "="*80)
    print_slow("🌊 WAVE ENERGY DETECTIVE CHALLENGE - MARINE ENGINEERING EDITION 🌊", 0.05)
    print("="*80)
    print_slow("\nWelcome young marine engineers! Ireland needs your expertise!")
    print_slow("The Minister of Marine Energy has tasked YOU with finding the best")
    print_slow("locations for wave energy converters around Ireland's coast.")
    print()
    print_slow("Your mission: Analyze wave climate data from different coastal")
    print_slow("sites and determine which locations are suitable for")
    print_slow("harvesting clean energy from ocean waves!")
    print()
    print_slow("At the end of your investigation, you'll create a")
    print_slow("professional report for the Marine Energy Board with your findings.")
    print("\n" + "-"*80)

    # Ask for student name
    student_name = input("\nPlease enter your name, Wave Energy Detective: ")
    if not student_name:
        student_name = "Detective Marina"

    print_slow(f"\nWelcome to the investigation, Detective {student_name}!")
    print_slow("Let's begin your marine energy training...")

    input("\nPress Enter to begin your mission... ")

    # Game variables
    player_score = 0
    locations_analyzed = 0
    detective_rank = "Apprentice Wave Detective"
    analyzed_locations = []

    # Introductory tutorial
    clear_screen()
    print("\n" + "="*60)
    print_slow("🔍 DETECTIVE TRAINING: WAVE ENERGY BASICS 🔍", 0.05)
    print("="*60)

    print_slow("\nBefore investigating coastal sites, let's review")
    print_slow("key facts about wave energy:")

    print_slow("\n1. Ocean waves are created by wind blowing over water")
    print_slow("2. Wave power depends on height² × period (P ∝ H²T)")
    print_slow("3. Atlantic swells can travel thousands of miles")
    print_slow("4. Good sites need consistent waves of 2m+ height")
    print_slow("5. Wave energy is more predictable than wind")
    print_slow("6. Devices must survive extreme storms (100-year waves)")

    print_slow("\nNow, let's test your knowledge with a physics quiz...")
    time.sleep(1)

    # Quick quiz to engage students
    quiz_score = mini_game_wave_physics()

    # Add quiz score to total
    player_score += quiz_score

    # Update detective rank
    if player_score >= 20:
        detective_rank = "Wave Detective"

    # Load all available datasets
    location_files = [f for f in os.listdir() if f.endswith('_Wave_2024.xlsx')]

    if len(location_files) == 0:
        print_slow("No wave data files found! Make sure to run the data generator first.")
        exit()

    # Ask how many locations to analyze
    print("\n" + "-"*60)
    print_slow("Training complete! Time for real coastal investigation.")
    print_slow(f"\nWe have wave data from {len(location_files)} coastal locations around Ireland.")

    max_locations = min(len(location_files), 8)
    num_locations = 0

    while num_locations < 3 or num_locations > max_locations:
        try:
            print_slow(f"\nHow many locations would you like to investigate? (3-{max_locations})")
            print_slow("(More locations = more complete analysis)")
            num_locations = int(input("Number of locations: "))
        except ValueError:
            print("Please enter a valid number!")

    print_slow(f"\nExcellent! You'll investigate {num_locations} coastal locations.")
    print_slow("The Marine Energy Board will be impressed by your thorough analysis!")
    time.sleep(1)

    # Let student choose selection mode
    print_slow("\nWould you like to choose specific locations or investigate random ones?")
    print("1. Choose specific locations")
    print("2. Investigate random locations")

    selection_mode = 0
    while selection_mode not in [1, 2]:
        try:
            selection_mode = int(input("\nEnter your choice (1-2): "))
        except ValueError:
            print("Please enter a valid number!")

    if selection_mode == 1:
        # Let student choose specific locations
        print_slow("\nAvailable coastal sites:")
        for i, loc in enumerate(location_files, 1):
            loc_name = loc.replace('_Wave_2024.xlsx', '').replace('_', ' ')
            print(f"{i}. {loc_name}")

        selected_locations = []
        for i in range(num_locations):
            choice = 0
            while choice < 1 or choice > len(location_files):
                try:
                    choice = int(input(f"\nSelect location #{i+1}: "))
                except ValueError:
                    print("Please enter a valid number!")
            selected_locations.append(location_files[choice-1])

        location_files = selected_locations
    else:
        # Random locations
        random.shuffle(location_files)
        location_files = location_files[:num_locations]

    # Game loop
    while location_files and locations_analyzed < num_locations:
        clear_screen()

        # Update detective rank
        if player_score >= 100:
            detective_rank = "Master Wave Energy Detective"
        elif player_score >= 60:
            detective_rank = "Senior Wave Detective"
        elif player_score >= 30:
            detective_rank = "Wave Detective"

        print("\n" + "="*60)
        print_slow(f"🌊 LOCATION #{locations_analyzed + 1} INVESTIGATION 🌊")
        print("="*60)
        print(f"Marine Detective: {student_name}")
        print(f"Rank: {detective_rank}")
        print(f"Current Score: {player_score} points")
        print("-"*60 + "\n")

        # Select next location
        current_file = location_files.pop(0)
        location_name = current_file.replace('_Wave_2024.xlsx', '').replace('_', ' ')

        print_slow(f"You're investigating: {location_name}")
        print_slow("Let's analyze the wave climate and determine site suitability!")
        print()

        # Load and analyze data
        try:
            data = pd.read_excel(current_file)
            months = data['Month']
            wave_heights = data['Significant Wave Height (m)']
            wave_periods = data['Average Wave Period (s)']

            # Calculate key statistics
            avg_wave_height = wave_heights.mean()
            max_wave_height = wave_heights.max()
            min_wave_height = wave_heights.min()
            avg_wave_period = wave_periods.mean()

            # Find months with biggest/smallest waves
            max_month = months[wave_heights.idxmax()]
            min_month = months[wave_heights.idxmin()]

            # Calculate wave power using simplified formula
            # P = 0.5 × ρ × g × H² × T / 4π (kW/m of wave crest)
            # Simplified: P ≈ 0.49 × H² × T
            def calculate_wave_power(height, period):
                return 0.49 * (height ** 2) * period

            wave_power_kW = []
            for h, t in zip(wave_heights, wave_periods):
                power = calculate_wave_power(h, t)
                wave_power_kW.append(power)

            avg_power = sum(wave_power_kW) / len(wave_power_kW)

            # Calculate annual energy (assuming 30m wide device)
            device_width = 30  # meters of wave crest
            capacity_factor = 0.35  # Typical for wave energy
            annual_energy_MWh = (avg_power * device_width * 8760 * capacity_factor) / 1000
            homes_powered = int(annual_energy_MWh / 4.2)  # Irish home uses ~4.2 MWh/year

            # Calculate H²T for site assessment
            wave_power_potential = avg_wave_height ** 2 * avg_wave_period

            # Site suitability (need H²T > 20 for commercial viability)
            is_suitable = wave_power_potential >= 20

            # Display wave climate summary
            print_slow("🌊 WAVE CLIMATE ANALYSIS:")
            print(f"  • Average wave height: {avg_wave_height:.1f} m")
            print(f"  • Average wave period: {avg_wave_period:.1f} s")
            print(f"  • Wave power potential (H²T): {wave_power_potential:.1f}")
            print(f"  • Biggest waves: {max_wave_height:.1f} m in {max_month}")
            print(f"  • Smallest waves: {min_wave_height:.1f} m in {min_month}")
            print(f"  • Average power density: {avg_power:.1f} kW/m")
            print(f"  • Annual energy (30m device): {annual_energy_MWh:.1f} MWh")
            print(f"  • Could power approximately {homes_powered} homes")
            print("\n" + "-"*60)

            # Visual representation of monthly wave climate
            print_slow("Monthly Wave Climate:")
            max_bar_length = 40
            for i in range(len(months)):
                # Show wave height as bar
                height_bar_length = int((wave_heights[i] / max_wave_height) * max_bar_length)
                height_bar = "█" * height_bar_length
                print(f"{months[i]:10}: H={wave_heights[i]:.1f}m {height_bar}")
                # Show period info
                period_info = f"           T={wave_periods[i]:.1f}s"
                power_info = f" → Power={wave_power_kW[i]:.1f} kW/m"
                print(period_info + power_info)

            print("\n" + "-"*60)

            # Challenge question
            print_slow("DETECTIVE CHALLENGE:")
            print_slow("Based on your analysis, is this location suitable")
            print_slow("for commercial wave energy development? (yes/no)")
            print_slow("\nConsider: H²T should be >20, and average H >2m")

            # Get student's answer
            student_answer = ""
            while student_answer.lower() not in ["yes", "no", "y", "n"]:
                student_answer = input("Your answer (yes/no): ").lower()

            student_answer = student_answer.lower() in ["yes", "y"]

            # Check if correct
            correct = (student_answer == is_suitable)

            # Give feedback
            print("\n" + "-"*60)
            if correct:
                print_slow("🌟 CORRECT! Excellent wave climate analysis! 🌟")
                points_earned = 10
                player_score += points_earned
                print_slow(f"You earned {points_earned} points!")
            else:
                print_slow("❌ Not quite right. Let's review:")
                points_earned = 0

            # Explain the answer
            if is_suitable:
                print_slow(f"With H²T = {wave_power_potential:.1f}, this site IS suitable!")
                print_slow("The combination of wave height and period provides good energy.")
                print_slow(f"A wave farm here could power {homes_powered} coastal homes!")
            else:
                print_slow(f"With H²T = {wave_power_potential:.1f}, this site is NOT ideal.")
                print_slow("Commercial wave farms typically need H²T > 20.")
                print_slow("This site might work for research but not commercial generation.")

            # Additional analysis options
            print("\n" + "-"*60)
            print_slow("🔬 ADVANCED ANALYSIS OPTIONS:")
            print_slow("What would you like to investigate next?")

            analysis_options = [
                "Seasonal wave patterns (storm vs calm seasons)",
                "Wave direction analysis (wave rose)",
                "Environmental impact & marine habitat",
                "Economic feasibility for wave farm",
                "Continue to next location"
            ]

            for i, option in enumerate(analysis_options):
                print(f"{i+1}. {option}")

            # Get choice
            choice = 0
            while choice < 1 or choice > len(analysis_options):
                try:
                    choice = int(input(f"\nYour choice (1-{len(analysis_options)}): "))
                except ValueError:
                    print("Please enter a valid number!")

            # Store location data
            location_data = {
                'name': location_name,
                'file': current_file,
                'months': months,
                'wave_heights': wave_heights,
                'wave_periods': wave_periods,
                'wave_power_kW': wave_power_kW,
                'avg_wave_height': avg_wave_height,
                'avg_wave_period': avg_wave_period,
                'avg_power': avg_power,
                'annual_energy_MWh': annual_energy_MWh,
                'homes_powered': homes_powered,
                'is_suitable': is_suitable,
                'wave_power_potential': wave_power_potential
            }

            # Perform additional analysis
            if choice == 1:  # Seasonal analysis
                print_slow("\nAnalyzing seasonal wave patterns...")
                seasonal_file, best_season, worst_season, seasonal_heights, seasonal_periods = create_seasonal_analysis(
                    months, wave_heights, wave_periods, location_name
                )

                print_slow(f"\nSeasonal analysis chart created: {seasonal_file}")
                print_slow(f"Highest energy season: {best_season}")
                print_slow(f"Calmest season: {worst_season}")
                print_slow("Note: Devices must survive winter storms to harvest that energy!")

                # Store seasonal data
                location_data['seasonal_file'] = seasonal_file
                location_data['best_season'] = best_season
                location_data['worst_season'] = worst_season
                location_data['seasonal_heights'] = seasonal_heights
                location_data['seasonal_periods'] = seasonal_periods

                # Bonus points
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for seasonal analysis!")

            elif choice == 2:  # Wave direction
                print_slow("\nAnalyzing wave direction patterns...")
                wave_rose_file, dominant_direction, direction_analysis = create_wave_rose(
                    wave_heights, location_name
                )

                print_slow(f"\nWave rose created: {wave_rose_file}")
                print_slow(f"Dominant waves from: {dominant_direction} ({direction_analysis['dominant_percent']:.1f}%)")
                print_slow(f"Site exposure: {direction_analysis['exposure_rating']}")

                # Store direction data
                location_data['wave_rose_file'] = wave_rose_file
                location_data['dominant_direction'] = dominant_direction
                location_data['direction_analysis'] = direction_analysis

                # Bonus points
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for directional analysis!")

            elif choice == 3:  # Environmental impact
                print_slow("\nAssessing environmental impact...")

                # Calculate environmental benefits
                environmental_impact = calculate_carbon_savings(annual_energy_MWh)

                print_slow(f"\nA wave farm at {location_name} could provide:")
                print_slow(f"• {environmental_impact['co2_savings_tons']:.1f} tons CO2 savings/year")
                print_slow(f"• Equivalent to planting {environmental_impact['equivalent_trees']} trees")
                print_slow(f"• Power for {environmental_impact['homes_powered']} homes")
                print_slow(f"• Serving {environmental_impact['percent_coastal']:.2f}% of coastal communities")
                print_slow(f"• Creating {environmental_impact['reef_area']} m² of artificial reef habitat")

                # Store environmental data
                location_data['environmental_impact'] = environmental_impact
                location_data['carbon_savings'] = environmental_impact['co2_savings_tons']

                # Bonus points
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for environmental analysis!")

            elif choice == 4:  # Economic analysis
                print_slow("\nAnalyzing economic feasibility...")

                # Calculate economics for 30MW wave farm
                econ_data = calculate_economic_factors(annual_energy_MWh,
                                                      wave_farm_capacity_MW=30,
                                                      location_name=location_name)

                print_slow(f"\nEconomic analysis for 30MW wave farm at {location_name}:")
                print_slow(f"• Wave energy converters: {econ_data['num_devices']} devices")
                print_slow(f"• Total investment: €{econ_data['total_cost']:,.0f}")
                print_slow(f"  - Devices: €{econ_data['installation_cost']:,.0f}")
                print_slow(f"  - Moorings: €{econ_data['mooring_cost']:,.0f}")
                print_slow(f"  - Subsea cables: €{econ_data['subsea_cable_cost']:,.0f}")
                print_slow(f"• Annual revenue: €{econ_data['annual_revenue']:,.0f}")
                print_slow(f"• Annual profit: €{econ_data['annual_profit']:,.0f}")
                print_slow(f"• Simple payback: {econ_data['payback_period']:.1f} years")
                print_slow(f"• Jobs: {econ_data['construction_jobs']} construction, "
                          f"{econ_data['permanent_jobs']} permanent, "
                          f"{econ_data['marine_jobs']} marine operations")

                # Store economic data
                location_data['economic_data'] = econ_data

                # Bonus points
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for economic analysis!")

            # Add location to analyzed list
            analyzed_locations.append(location_data)

            # Generate power analysis chart
            print_slow("\nGenerating wave power analysis charts...")
            chart_file = create_power_plot(
                months, wave_heights, wave_periods, wave_power_kW,
                avg_wave_height, avg_wave_period, avg_power,
                annual_energy_MWh, homes_powered, location_name
            )
            print_slow(f"Charts saved as: {chart_file}")

            # Update game state
            locations_analyzed += 1

            # Continue prompt
            print("\n" + "-"*60)
            input("Press Enter to continue... ")

        except Exception as e:
            print(f"Error analyzing location: {e}")
            print("Skipping to next location...")
            time.sleep(3)

    # Device selection mini-game
    device_score = mini_game_device_selection()
    player_score += device_score

    # Update final rank
    if player_score >= 100:
        detective_rank = "Master Wave Energy Detective"
    elif player_score >= 60:
        detective_rank = "Senior Wave Detective"
    elif player_score >= 30:
        detective_rank = "Wave Detective"

    # Generate final report
    clear_screen()
    print("\n" + "="*60)
    print_slow("📋 FINAL REPORT PREPARATION 📋", 0.05)
    print("="*60)

    print_slow(f"\nCongratulations, {detective_rank} {student_name}!")
    print_slow(f"You've successfully analyzed {locations_analyzed} coastal locations")
    print_slow(f"and earned a total of {player_score} points!")

    print_slow("\nTime to prepare your report for the Marine Energy Board.")
    print_slow("This will summarize your findings and recommendations.")

    # Ask if they want to generate report
    print_slow("\nWould you like to generate an official report? (yes/no)")

    generate_report = input("Generate report? ").lower() in ["y", "yes"]

    if generate_report:
        print_slow("\nGenerating your wave energy report...")
        report_file = generate_text_report(student_name, detective_rank, analyzed_locations, player_score)

        if report_file:
            print_slow(f"\nReport generated: {report_file}")
            print_slow("You can open this file to view your complete findings.")
        else:
            print_slow("\nCouldn't generate report file.")
            generate_report = False

    # Show summary if no report
    if not generate_report:
        clear_screen()
        print("\n" + "="*60)
        print_slow("🌊 WAVE DETECTIVE FINAL SUMMARY 🌊", 0.05)
        print("="*60)

        print_slow(f"Marine Detective: {student_name}")
        print_slow(f"Final Rank: {detective_rank}")
        print_slow(f"Total Score: {player_score} points")

        print_slow("\n" + "-"*60)
        print_slow("KEY FINDINGS:")

        # Sort by wave power potential
        sorted_locations = sorted(analyzed_locations,
                                key=lambda x: x['wave_power_potential'],
                                reverse=True)

        if sorted_locations:
            best_location = sorted_locations[0]['name']
            print_slow(f"\nBest wave energy site: {best_location}")
            print_slow(f"Wave power potential (H²T): {sorted_locations[0]['wave_power_potential']:.1f}")
            print_slow(f"Could power {sorted_locations[0]['homes_powered']} homes annually")

            print_slow("\n" + "-"*60)
            print_slow("LOCATION RANKINGS:")

            for i, loc in enumerate(sorted_locations):
                status = "SUITABLE" if loc['is_suitable'] else "MARGINAL"
                print_slow(f"{i+1}. {loc['name']} - H²T={loc['wave_power_potential']:.1f} - {status}")

    # Game finale
    print("\n" + "-"*60)
    print_slow("🌍 MISSION COMPLETE!", 0.05)

    print_slow("\nThank you for your service as a Wave Energy Detective!")
    print_slow("Your analysis will help Ireland harness the power of the Atlantic")
    print_slow("to provide clean, renewable energy from our ocean resources.")

    print_slow("\nKey learnings:")
    print_slow("• Wave power depends on both height² and period (P ∝ H²T)")
    print_slow("• Ireland's Atlantic coast has world-class wave resources")
    print_slow("• Wave devices must survive extreme storms")
    print_slow("• Ocean energy can power coastal communities sustainably")

    print("\n" + "="*60)
    print_slow("🌊 THE OCEAN'S POWER AWAITS! 🌊", 0.05)
    print("="*60)

    input("\nPress Enter to exit... ")

# Run the game if executed directly
if __name__ == "__main__":
    run_wave_detective_game()

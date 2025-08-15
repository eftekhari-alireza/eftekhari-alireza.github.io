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

def create_power_plot(months, tidal_ranges, current_velocities, tidal_power_kW,
                      avg_range, avg_velocity, avg_power, annual_energy_MWh,
                      homes_powered, location_name):
    """Create and save a tidal power visualization"""
    fig = plt.figure(figsize=(14, 10))

    # Create grid for subplots
    gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3, wspace=0.3)

    # Main power plot (top, spanning both columns)
    ax1 = fig.add_subplot(gs[0, :])

    # Tidal-themed colormap (deep blue to light blue to turquoise)
    colors = ["#084594", "#2171b5", "#4292c6", "#6baed6",
              "#9ecae1", "#c6dbef", "#deebf7", "#08519c"]
    cmap = LinearSegmentedColormap.from_list("tidal_colors", colors)

    # Plot monthly power with tidal theme
    bars = ax1.bar(range(1, 13), tidal_power_kW, color=cmap(np.linspace(0, 1, 12)))
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(months, rotation=45)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
                 f'{height:.0f}', ha='center', va='bottom', fontsize=9)

    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_ylabel('Tidal Power (kW)', fontsize=12)
    ax1.set_title(f'Tidal Stream Power Output at {location_name}', fontsize=14)

    # Tidal range plot (bottom left)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(range(1, 13), tidal_ranges, 'o-', color='navy', linewidth=2, markersize=8)
    ax2.fill_between(range(1, 13), 0, tidal_ranges, alpha=0.3, color='skyblue')
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels([m[:3] for m in months], rotation=45)
    ax2.set_ylabel('Tidal Range (m)', fontsize=10)
    ax2.set_title('Monthly Mean Tidal Range', fontsize=11)
    ax2.grid(True, alpha=0.3)

    # Current velocity plot (bottom right)
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(range(1, 13), current_velocities, 'o-', color='darkgreen', linewidth=2, markersize=8)
    ax3.fill_between(range(1, 13), 0, current_velocities, alpha=0.3, color='lightgreen')
    ax3.axhline(y=2.0, color='red', linestyle='--', alpha=0.5, label='Commercial threshold')
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels([m[:3] for m in months], rotation=45)
    ax3.set_ylabel('Peak Velocity (m/s)', fontsize=10)
    ax3.set_title('Peak Tidal Current Velocity', fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=8)

    # Spring/Neap cycle illustration (bottom, spanning both columns)
    ax4 = fig.add_subplot(gs[2, :])

    # Create synthetic spring/neap cycle for one month
    days = np.linspace(0, 29.5, 60)  # Lunar month
    spring_neap_cycle = 1 + 0.4 * np.sin(2 * np.pi * days / 14.75)  # 14.75 day cycle
    daily_tide = 1 + 0.9 * np.sin(2 * np.pi * days * 2)  # 2 tides per day
    combined = spring_neap_cycle * daily_tide * avg_velocity

    ax4.plot(days, combined, color='teal', linewidth=1)
    ax4.fill_between(days, 0, combined, alpha=0.2, color='teal')
    ax4.set_xlabel('Days in Lunar Month', fontsize=10)
    ax4.set_ylabel('Current Velocity (m/s)', fontsize=10)
    ax4.set_title('Spring-Neap Tidal Cycle (example month)', fontsize=11)
    ax4.grid(True, alpha=0.3)

    # Mark spring and neap tides
    ax4.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax4.axvline(x=14.75, color='red', linestyle='--', alpha=0.5)
    ax4.axvline(x=29.5, color='red', linestyle='--', alpha=0.5)
    ax4.text(0, max(combined)*0.9, 'Spring', fontsize=8, color='red')
    ax4.text(14.75, max(combined)*0.9, 'Spring', fontsize=8, color='red')
    ax4.axvline(x=7.375, color='blue', linestyle='--', alpha=0.5)
    ax4.axvline(x=22.125, color='blue', linestyle='--', alpha=0.5)
    ax4.text(7.375, max(combined)*0.5, 'Neap', fontsize=8, color='blue')

    # Information box
    info_text = (
        f"🌊 Average tidal range: {avg_range:.1f} m\n"
        f"💨 Average peak velocity: {avg_velocity:.2f} m/s\n"
        f"⚡ Average power: {avg_power:.1f} kW\n"
        f"🔋 Annual energy: {annual_energy_MWh:.1f} MWh\n"
        f"🏠 Can power: {homes_powered} homes\n"
        f"📅 Predictability: >95% (lunar cycles)"
    )

    plt.figtext(0.02, 0.02, info_text, bbox=dict(facecolor='lightcyan', alpha=0.8), fontsize=10)

    plt.tight_layout()

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_tidal_power_analysis.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    return output_file

def create_tidal_resource_analysis(data, location_name):
    """Create detailed tidal resource analysis showing spring/neap variations"""
    plt.figure(figsize=(12, 8))

    months = data['Month']
    spring_ranges = data['Spring Tide Range (m)']
    neap_ranges = data['Neap Tide Range (m)']
    mean_ranges = data['Mean Tidal Range (m)']

    # Calculate power potential for spring vs neap
    # Using peak velocities which scale with tidal range
    spring_power = [r * 1.2 for r in data['Peak Current Velocity (m/s)']]  # Spring tides faster
    neap_power = [r / 1.4 for r in data['Peak Current Velocity (m/s)']]   # Neap tides slower

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Tidal range comparison
    x = np.arange(len(months))
    width = 0.35

    bars1 = ax1.bar(x - width/2, spring_ranges, width, label='Spring Tides', color='darkblue', alpha=0.7)
    bars2 = ax1.bar(x + width/2, neap_ranges, width, label='Neap Tides', color='lightblue', alpha=0.7)
    ax1.plot(x, mean_ranges, 'ro-', label='Monthly Mean', linewidth=2, markersize=8)

    ax1.set_ylabel('Tidal Range (m)', fontsize=12)
    ax1.set_title(f'Spring vs Neap Tidal Ranges - {location_name}', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(months, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Power generation comparison
    # Power varies with velocity cubed, showing dramatic spring/neap differences
    spring_power_kW = [(v**3) * 50 for v in spring_power]  # Simplified power calculation
    neap_power_kW = [(v**3) * 50 for v in neap_power]

    bars3 = ax2.bar(x - width/2, spring_power_kW, width, label='Spring Tide Power', color='darkgreen', alpha=0.7)
    bars4 = ax2.bar(x + width/2, neap_power_kW, width, label='Neap Tide Power', color='lightgreen', alpha=0.7)

    ax2.set_ylabel('Relative Power Output (kW)', fontsize=12)
    ax2.set_xlabel('Month', fontsize=12)
    ax2.set_title('Power Generation: Spring vs Neap Tides', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(months, rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Calculate capacity factor variation
    avg_spring_power = np.mean(spring_power_kW)
    avg_neap_power = np.mean(neap_power_kW)
    power_variation = (avg_spring_power - avg_neap_power) / avg_spring_power * 100

    # Add text box with key findings
    textstr = (f'Key Findings:\n'
               f'• Spring tides generate {avg_spring_power/avg_neap_power:.1f}x more power than neap tides\n'
               f'• Power output varies by {power_variation:.0f}% over lunar cycle\n'
               f'• Predictable variations allow grid planning\n'
               f'• Average capacity factor: ~35-40%')

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax2.text(0.02, 0.95, textstr, transform=ax2.transAxes, fontsize=11,
             verticalalignment='top', bbox=props)

    plt.tight_layout()

    # Save the analysis
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_tidal_resource_analysis.png"
    plt.savefig(output_file, dpi=150)
    plt.close()

    return output_file, avg_spring_power/avg_neap_power, power_variation

def create_tidal_ellipse(data, location_name):
    """Create tidal ellipse diagram showing flood/ebb asymmetry"""
    plt.figure(figsize=(8, 8))

    # Get flood and ebb velocities
    flood_velocities = data['Peak Flood Velocity (m/s)']
    ebb_velocities = data['Peak Ebb Velocity (m/s)']

    # Calculate average asymmetry
    avg_flood = np.mean(flood_velocities)
    avg_ebb = np.mean(ebb_velocities)

    # Create polar plot showing tidal current directions
    ax = plt.subplot(111, projection='polar')

    # Flood tide (incoming) - typically from SW in Ireland
    flood_direction = 225 * np.pi / 180  # SW
    ebb_direction = 45 * np.pi / 180    # NE (opposite)

    # Plot tidal current vectors
    ax.arrow(flood_direction, 0, 0, avg_flood, width=0.1,
             head_width=0.2, head_length=0.1, fc='blue', ec='blue',
             label=f'Flood: {avg_flood:.2f} m/s')
    ax.arrow(ebb_direction, 0, 0, avg_ebb, width=0.1,
             head_width=0.2, head_length=0.1, fc='red', ec='red',
             label=f'Ebb: {avg_ebb:.2f} m/s')

    # Add tidal ellipse
    theta = np.linspace(0, 2*np.pi, 100)
    r_flood = avg_flood * np.abs(np.cos(theta - flood_direction))
    r_ebb = avg_ebb * np.abs(np.cos(theta - ebb_direction))
    r_combined = np.maximum(r_flood, r_ebb)

    ax.plot(theta, r_combined, 'g--', linewidth=2, label='Tidal ellipse')
    ax.fill(theta, r_combined, alpha=0.2, color='cyan')

    # Configure plot
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_ylim(0, max(avg_flood, avg_ebb) * 1.2)
    ax.set_title(f'Tidal Current Pattern - {location_name}\n', fontsize=14)

    # Add compass directions
    ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315],
                      ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

    # Determine flood/ebb dominance
    if avg_flood > avg_ebb * 1.1:
        dominance = "Flood dominant"
        reason = "stronger incoming tides"
    elif avg_ebb > avg_flood * 1.1:
        dominance = "Ebb dominant"
        reason = "stronger outgoing tides"
    else:
        dominance = "Symmetric"
        reason = "balanced flood and ebb"

    # Add text box
    textstr = (f'{dominance}\n'
               f'Flood: {avg_flood:.2f} m/s\n'
               f'Ebb: {avg_ebb:.2f} m/s\n'
               f'Asymmetry: {abs(avg_flood-avg_ebb)/max(avg_flood,avg_ebb)*100:.0f}%')

    props = dict(boxstyle='round', facecolor='yellow', alpha=0.7)
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_tidal_ellipse.png"
    plt.savefig(output_file, dpi=150)
    plt.close()

    return output_file, dominance, reason, avg_flood, avg_ebb

def calculate_carbon_savings(annual_energy_MWh):
    """Calculate carbon savings from tidal energy"""
    # CO2 emissions from fossil fuels
    fossil_emissions = 450  # kg CO2 per MWh

    # Calculate CO2 savings
    co2_savings = annual_energy_MWh * fossil_emissions
    co2_savings_tons = co2_savings / 1000

    # Environmental equivalents
    equivalent_trees = int(co2_savings / 22)
    cars_equivalent = int(co2_savings_tons / 4.6)
    homes_powered = int(annual_energy_MWh / 4.2)

    # Tidal-specific benefits
    # Predictable power reduces need for backup generation
    backup_reduction = co2_savings_tons * 0.15  # 15% additional savings

    # Marine habitat considerations
    # Tidal turbines can create artificial reef effects
    reef_area = homes_powered * 1.5  # m² of artificial reef

    # Calculate percentage of island communities powered
    # Focus on island/coastal communities
    percent_islands = (homes_powered / 50000) * 100  # ~50k island households

    return {
        'co2_savings_tons': co2_savings_tons,
        'backup_reduction': backup_reduction,
        'total_co2_savings': co2_savings_tons + backup_reduction,
        'equivalent_trees': equivalent_trees,
        'cars_equivalent': cars_equivalent,
        'homes_powered': homes_powered,
        'percent_islands': percent_islands,
        'reef_area': reef_area,
        'predictability_benefit': 'Reduces grid balancing costs by €' + str(int(annual_energy_MWh * 20))
    }

def calculate_economic_factors(annual_energy_MWh, tidal_farm_capacity_MW=10, location_name=""):
    """Calculate economic factors for a tidal energy farm"""
    # Base parameters for tidal energy
    electricity_price = 200  # €/MWh (higher due to predictability value)

    # Location-based factors
    if "Strangford" in location_name or "Bulls" in location_name:
        # Narrow channels with very strong currents
        capacity_factor = 0.40  # 40% (excellent for tidal)
        cost_per_MW = 4500000  # €4.5M per MW
        maintenance_factor = 0.035  # 3.5% annually
    elif "Sound" in location_name or "Blasket" in location_name:
        # Good channels with strong currents
        capacity_factor = 0.35  # 35%
        cost_per_MW = 4000000  # €4M per MW
        maintenance_factor = 0.030  # 3% annually
    elif "Harbour" in location_name or "Entrance" in location_name:
        # Harbor entrances - good access but environmental concerns
        capacity_factor = 0.30  # 30%
        cost_per_MW = 3500000  # €3.5M per MW
        maintenance_factor = 0.025  # 2.5% annually
    else:
        # Standard sites
        capacity_factor = 0.32  # 32%
        cost_per_MW = 3800000  # €3.8M per MW
        maintenance_factor = 0.028  # 2.8% annually

    # Calculate number of turbines (assume 1.5MW turbines)
    turbine_capacity = 1.5  # MW per turbine
    num_turbines = int(tidal_farm_capacity_MW / turbine_capacity)

    # Annual revenue (includes predictability premium)
    base_revenue = annual_energy_MWh * electricity_price
    predictability_premium = base_revenue * 0.15  # 15% premium for predictability
    annual_revenue = base_revenue + predictability_premium

    # Installation costs
    turbine_cost = tidal_farm_capacity_MW * cost_per_MW

    # Marine-specific costs
    foundation_cost = num_turbines * 400000  # €400k per turbine foundation
    subsea_cable_cost = turbine_cost * 0.15  # 15% for cables
    environmental_monitoring = turbine_cost * 0.05  # 5% for monitoring
    total_cost = turbine_cost + foundation_cost + subsea_cable_cost + environmental_monitoring

    # Annual costs
    annual_maintenance = turbine_cost * maintenance_factor
    annual_monitoring = environmental_monitoring * 0.10  # 10% of setup annually
    annual_costs = annual_maintenance + annual_monitoring

    # Annual profit
    annual_profit = annual_revenue - annual_costs

    # Payback period
    payback_period = total_cost / annual_profit if annual_profit > 0 else 999

    # Jobs (tidal creates specialized marine jobs)
    construction_jobs = num_turbines * 25  # More jobs due to marine work
    permanent_jobs = num_turbines * 2.0  # Higher than wind
    marine_specialist_jobs = num_turbines * 0.8  # Divers, ROV operators

    # Calculate LCOE (Levelized Cost of Energy)
    project_lifetime = 25  # years
    total_lifetime_cost = total_cost + (annual_costs * project_lifetime)
    total_lifetime_energy = annual_energy_MWh * project_lifetime
    lcoe = total_lifetime_cost / total_lifetime_energy if total_lifetime_energy > 0 else 0

    return {
        'num_turbines': num_turbines,
        'annual_revenue': annual_revenue,
        'predictability_premium': predictability_premium,
        'turbine_cost': turbine_cost,
        'foundation_cost': foundation_cost,
        'subsea_cable_cost': subsea_cable_cost,
        'environmental_monitoring': environmental_monitoring,
        'total_cost': total_cost,
        'annual_maintenance': annual_maintenance,
        'annual_monitoring': annual_monitoring,
        'annual_profit': annual_profit,
        'payback_period': payback_period,
        'capacity_factor': capacity_factor,
        'construction_jobs': int(construction_jobs),
        'permanent_jobs': int(permanent_jobs),
        'marine_specialist_jobs': int(marine_specialist_jobs),
        'lcoe': lcoe
    }

def generate_text_report(student_name, detective_rank, analyzed_locations, score):
    """Generate a professional text report for tidal energy findings"""
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("TIDAL ENERGY DETECTIVE CHALLENGE - FINAL REPORT")
    report_lines.append("="*60)
    report_lines.append(f"Marine Energy Detective: {student_name}")
    report_lines.append(f"Rank: {detective_rank}")
    report_lines.append(f"Date: {datetime.now().strftime('%d %B %Y')}")
    report_lines.append(f"Final Score: {score} points")
    report_lines.append("-"*60)

    # Sort locations by tidal power potential (velocity cubed)
    for loc in analyzed_locations:
        loc['tidal_power_score'] = loc['avg_velocity'] ** 3

    sorted_locations = sorted(analyzed_locations,
                            key=lambda x: x['tidal_power_score'],
                            reverse=True)

    # Executive summary
    report_lines.append("EXECUTIVE SUMMARY:")
    report_lines.append("")

    if sorted_locations:
        best_location = sorted_locations[0]['name']
        report_lines.append(f"After analyzing {len(analyzed_locations)} tidal energy sites around Ireland,")
        report_lines.append(f"{best_location} offers the highest potential with peak currents")
        report_lines.append(f"of {sorted_locations[0]['avg_velocity']:.2f} m/s and {sorted_locations[0]['avg_range']:.1f}m tidal range.")
        report_lines.append(f"A 10MW tidal farm here could generate {sorted_locations[0]['annual_energy_MWh']:.1f} MWh annually,")
        report_lines.append(f"powering {sorted_locations[0]['homes_powered']} homes with >95% predictability.")

    # Location rankings
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("LOCATION RANKINGS (by tidal power potential v³):")
    report_lines.append("")

    for i, location in enumerate(sorted_locations):
        suitability = "EXCELLENT" if location['avg_velocity'] >= 2.5 else "SUITABLE" if location['is_suitable'] else "MARGINAL"
        report_lines.append(f"{i+1}. {location['name']} - v³={location['tidal_power_score']:.2f} - {suitability}")
        report_lines.append(f"   Peak velocity: {location['avg_velocity']:.2f} m/s, Range: {location['avg_range']:.1f}m")

    # Technical recommendations
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("TECHNICAL RECOMMENDATIONS:")
    report_lines.append("")

    recommended = [loc for loc in sorted_locations if loc['is_suitable']]
    if recommended:
        report_lines.append("Priority sites for tidal energy development:")
        for i, loc in enumerate(recommended[:3]):
            report_lines.append(f"\n{i+1}. {loc['name']}")
            report_lines.append(f"   Technical advantages:")

            advantages = []
            if loc['avg_velocity'] >= 2.5:
                advantages.append(f"excellent currents ({loc['avg_velocity']:.2f} m/s)")
            if 'flood_ebb_ratio' in loc and loc['flood_ebb_ratio'] > 1.5:
                advantages.append("strong asymmetry for optimization")
            if 'spring_neap_ratio' in loc:
                advantages.append(f"{loc['spring_neap_ratio']:.1f}x spring/neap variation")
            if loc.get('channel_type') == 'narrow':
                advantages.append("narrow channel accelerates flow")

            for adv in advantages:
                report_lines.append(f"   • {adv}")

    # Detailed location analysis
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("DETAILED SITE ASSESSMENTS:")

    for i, location in enumerate(sorted_locations):
        report_lines.append("")
        report_lines.append(f"Site #{i+1}: {location['name']}")
        report_lines.append(f"Tidal Characteristics:")
        report_lines.append(f"  • Mean tidal range: {location['avg_range']:.1f} m")
        report_lines.append(f"  • Peak current velocity: {location['avg_velocity']:.2f} m/s")
        report_lines.append(f"  • Power density score (v³): {location['tidal_power_score']:.2f}")
        report_lines.append(f"  • Average power output: {location['avg_power']:.1f} kW")
        report_lines.append(f"  • Annual energy (10MW farm): {location['annual_energy_MWh']:.1f} MWh")
        report_lines.append(f"  • Homes powered: {location['homes_powered']}")

        if 'tidal_pattern' in location:
            report_lines.append(f"  • Tidal pattern: {location['tidal_pattern']}")

        if 'flood_velocity' in location and 'ebb_velocity' in location:
            report_lines.append(f"  • Flood velocity: {location['flood_velocity']:.2f} m/s")
            report_lines.append(f"  • Ebb velocity: {location['ebb_velocity']:.2f} m/s")
            report_lines.append(f"  • Flow asymmetry: {location.get('flow_dominance', 'Balanced')}")

        if 'environmental_impact' in location:
            ei = location['environmental_impact']
            report_lines.append(f"Environmental Benefits:")
            report_lines.append(f"  • CO2 savings: {ei['total_co2_savings']:.1f} tons/year")
            report_lines.append(f"  • Grid stability: {ei['predictability_benefit']}")
            report_lines.append(f"  • Powers {ei['percent_islands']:.1f}% of island communities")

        if 'economic_data' in location:
            econ = location['economic_data']
            report_lines.append(f"Economic Analysis (10MW installation):")
            report_lines.append(f"  • Tidal turbines: {econ['num_turbines']} × 1.5MW units")
            report_lines.append(f"  • Total investment: €{econ['total_cost']:,.0f}")
            report_lines.append(f"  • Annual revenue: €{econ['annual_revenue']:,.0f}")
            report_lines.append(f"    (includes €{econ['predictability_premium']:,.0f} predictability premium)")
            report_lines.append(f"  • Payback period: {econ['payback_period']:.1f} years")
            report_lines.append(f"  • LCOE: €{econ['lcoe']:.0f}/MWh")
            report_lines.append(f"  • Jobs: {econ['construction_jobs']} construction, "
                              f"{econ['permanent_jobs']} permanent, "
                              f"{econ['marine_specialist_jobs']} marine specialists")

    # Strategic conclusions
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("STRATEGIC CONCLUSIONS:")
    report_lines.append("")
    report_lines.append("Ireland's tidal energy resources offer unique advantages:")
    report_lines.append("• Highly predictable (>95%) enabling better grid management")
    report_lines.append("• Strong resources in channels and straits")
    report_lines.append("• Complements wind and wave with different generation patterns")
    report_lines.append("• Creates specialized marine engineering jobs")
    report_lines.append("• Supports energy independence for island communities")
    report_lines.append("")
    report_lines.append("Recommended next steps:")
    report_lines.append("1. Detailed bathymetric surveys at priority sites")
    report_lines.append("2. Environmental impact assessments")
    report_lines.append("3. Grid connection studies")
    report_lines.append("4. Community engagement programs")
    report_lines.append("5. Technology demonstration projects")

    # Save report
    report_filename = f"Tidal_Detective_Report_{student_name.replace(' ', '_')}.txt"
    try:
        with open(report_filename, 'w') as f:
            f.write("\n".join(report_lines))
        return report_filename
    except Exception as e:
        print(f"Error saving report: {e}")
        return None

def mini_game_tidal_physics():
    """Mini-game to test knowledge of tidal energy physics"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("🌊 SPECIAL CHALLENGE: TIDAL PHYSICS EXPERT 🌊", 0.05)
    print("="*60)

    print_slow("\nThe Marine Energy Board wants to test your understanding")
    print_slow("of tidal energy physics and lunar cycles!")

    questions = [
        {
            "question": "What happens to tidal power when current velocity doubles?",
            "options": ["It doubles", "It quadruples", "It increases 8 times", "No change"],
            "correct": 2,
            "explanation": "Tidal power is proportional to velocity CUBED (P ∝ v³). Doubling velocity increases power by 2³ = 8 times!"
        },
        {
            "question": "How often do spring tides occur?",
            "options": ["Daily", "Weekly", "Every two weeks", "Monthly"],
            "correct": 2,
            "explanation": "Spring tides occur twice per lunar month (every ~14.75 days) during new and full moons when Sun, Earth, and Moon align."
        },
        {
            "question": "What causes tides?",
            "options": ["Wind", "Gravitational pull of Moon and Sun", "Ocean currents", "Earth's rotation only"],
            "correct": 1,
            "explanation": "Tides are caused by gravitational forces from the Moon (primary) and Sun (secondary), creating bulges in Earth's oceans."
        },
        {
            "question": "Why are tidal currents strongest in narrow channels?",
            "options": ["More moonlight", "Water is compressed and accelerates", "Deeper water", "Warmer temperatures"],
            "correct": 1,
            "explanation": "Narrow channels force the same volume of water through a smaller area, dramatically increasing flow velocity."
        },
        {
            "question": "What's the main advantage of tidal over wind/wave energy?",
            "options": ["Cheaper", "More powerful", "Highly predictable", "Easier to build"],
            "correct": 2,
            "explanation": "Tidal energy is >95% predictable years in advance using astronomical calculations, unlike variable wind/waves."
        },
        {
            "question": "What minimum current speed is typically needed for commercial tidal energy?",
            "options": ["0.5 m/s", "1.0 m/s", "2.0 m/s", "4.0 m/s"],
            "correct": 2,
            "explanation": "Commercial tidal projects typically need peak currents of at least 2.0 m/s for economic viability."
        },
        {
            "question": "How many high tides occur in most locations per day?",
            "options": ["One", "Two", "Four", "It varies randomly"],
            "correct": 1,
            "explanation": "Most locations have semi-diurnal tides with TWO high tides and TWO low tides per day (roughly every 12.4 hours)."
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
        print_slow("🌟 EXCELLENT! You're a tidal energy expert!")
    elif score >= len(questions)*5 * 0.6:
        print_slow("👍 GOOD JOB! You understand tidal energy principles.")
    else:
        print_slow("🔍 Keep studying! Tidal physics is fascinating.")

    return score

def mini_game_site_selection():
    """Mini-game for selecting optimal tidal turbine locations"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("🎯 SPECIAL CHALLENGE: TIDAL SITE OPTIMIZER 🎯", 0.05)
    print("="*60)

    print_slow("\nThe Engineering Team needs help optimizing turbine placement")
    print_slow("for maximum energy extraction and minimal environmental impact!")

    score = 0

    # Challenge 1: Turbine placement in channel
    print("\n" + "-"*60)
    print_slow("CHALLENGE #1: Turbine Array Layout")
    print_slow("\nYou have a 500m wide channel with 3 m/s peak currents.")
    print_slow("Where should you place your tidal turbines?")

    options = [
        "Single row across entire channel width",
        "Multiple rows filling the whole channel",
        "Leave shipping lane, turbines on sides only",
        "Random placement for maximum coverage"
    ]

    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    answer = -1
    while answer < 1 or answer > len(options):
        try:
            answer = int(input(f"\nYour choice (1-{len(options)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer == 3:  # Shipping lane option
        print_slow("✓ EXCELLENT! +10 points")
        print_slow("Leaving navigation channels clear is essential for safety")
        print_slow("and regulatory approval. Side placement still captures good flow.")
        score += 10
    elif answer == 1:  # Single row
        print_slow("✓ REASONABLE! +5 points")
        print_slow("A single row minimizes wake effects between turbines,")
        print_slow("but remember to consider navigation requirements.")
        score += 5
    else:
        print_slow("✗ This layout has significant problems.")
        print_slow("Multiple rows create wake interference, and random placement")
        print_slow("is inefficient and dangerous for maintenance.")

    # Challenge 2: Environmental consideration
    print("\n" + "-"*60)
    print_slow("CHALLENGE #2: Marine Life Protection")
    print_slow("\nYour site assessment shows it's a migration route for salmon.")
    print_slow("What's the best approach?")

    options2 = [
        "Cancel the project - environment comes first",
        "Install turbines with environmental monitoring",
        "Use slow-rotating turbines with fish protection",
        "Ignore it - fish will adapt"
    ]

    for i, option in enumerate(options2):
        print(f"{i+1}. {option}")

    answer2 = -1
    while answer2 < 1 or answer2 > len(options2):
        try:
            answer2 = int(input(f"\nYour choice (1-{len(options2)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer2 == 3:  # Fish protection
        print_slow("✓ PERFECT! +10 points")
        print_slow("Modern tidal turbines rotate slowly (10-20 rpm) and can include")
        print_slow("fish protection screens. Studies show minimal impact on marine life.")
        score += 10
    elif answer2 == 2:  # Monitoring
        print_slow("✓ GOOD! +7 points")
        print_slow("Environmental monitoring is essential, but active protection")
        print_slow("measures are even better for sensitive species.")
        score += 7
    else:
        print_slow("✗ Not the best approach.")
        print_slow("We can harness tidal energy while protecting marine life")
        print_slow("through careful design and technology choices.")

    # Challenge 3: Maintenance access
    print("\n" + "-"*60)
    print_slow("CHALLENGE #3: Maintenance Strategy")
    print_slow("\nYour turbines need inspection every 6 months.")
    print_slow("The site has 4 m/s currents at peak. When do you schedule maintenance?")

    options3 = [
        "During spring tides for maximum visibility",
        "During neap tides when currents are weakest",
        "At slack water between tides",
        "Anytime - use remote operated vehicles (ROVs)"
    ]

    for i, option in enumerate(options3):
        print(f"{i+1}. {option}")

    answer3 = -1
    while answer3 < 1 or answer3 > len(options3):
        try:
            answer3 = int(input(f"\nYour choice (1-{len(options3)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer3 == 3:  # Slack water
        print_slow("✓ EXCELLENT! +10 points")
        print_slow("Slack water (between flood and ebb) provides a 20-30 minute window")
        print_slow("with minimal currents - ideal for diver safety and precise work.")
        score += 10
    elif answer3 == 2:  # Neap tides
        print_slow("✓ GOOD! +7 points")
        print_slow("Neap tides have weaker currents, but slack water periods")
        print_slow("are even better for safety.")
        score += 7
    elif answer3 == 4:  # ROVs
        print_slow("✓ REASONABLE! +5 points")
        print_slow("ROVs are useful but some maintenance requires human divers.")
        print_slow("Always plan around tidal conditions for safety.")
        score += 5
    else:
        print_slow("✗ DANGEROUS! Spring tides have the strongest currents.")
        print_slow("This would put maintenance crews at serious risk.")

    print("\n" + "-"*60)
    print_slow(f"SITE OPTIMIZATION COMPLETE! You scored {score} out of 30 points!")

    if score >= 25:
        print_slow("🌟 EXCELLENT! You're ready to lead tidal energy projects!")
    elif score >= 15:
        print_slow("👍 GOOD JOB! You understand key site selection factors.")
    else:
        print_slow("🔍 Site selection is complex - keep learning!")

    return score

# Main game function
def run_tide_detective_game():
    # Title screen
    clear_screen()
    print("\n" + "="*80)
    print_slow("🌊 TIDAL ENERGY DETECTIVE CHALLENGE - LUNAR POWER EDITION 🌊", 0.05)
    print("="*80)
    print_slow("\nGreetings, marine energy investigators!")
    print_slow("The Irish Marine Energy Board needs YOUR expertise to identify")
    print_slow("the best locations for tidal energy systems around our coasts.")
    print()
    print_slow("Your mission: Analyze tidal data from strategic channels,")
    print_slow("straits, and estuaries to find sites where we can harness")
    print_slow("the predictable power of the tides!")
    print()
    print_slow("Unlike wind and waves, tidal energy is predictable centuries")
    print_slow("in advance - making it invaluable for grid stability.")
    print("\n" + "-"*80)

    # Get student name
    student_name = input("\nEnter your name, Tidal Detective: ")
    if not student_name:
        student_name = "Detective Luna"

    print_slow(f"\nWelcome aboard, Detective {student_name}!")
    print_slow("Let's begin your tidal energy investigation...")

    input("\nPress Enter to start your training... ")

    # Game variables
    player_score = 0
    locations_analyzed = 0
    detective_rank = "Apprentice Tidal Detective"
    analyzed_locations = []

    # Tutorial section
    clear_screen()
    print("\n" + "="*60)
    print_slow("🔍 DETECTIVE TRAINING: TIDAL ENERGY FUNDAMENTALS 🔍", 0.05)
    print("="*60)

    print_slow("\nBefore investigating sites, understand these tidal facts:")

    print_slow("\n1. Tides are caused by gravitational pull of Moon and Sun")
    print_slow("2. Most locations have 2 high and 2 low tides daily")
    print_slow("3. Spring tides (new/full moon) are ~40% stronger than neap tides")
    print_slow("4. Tidal power = 0.5 × ρ × A × v³ (velocity cubed!)")
    print_slow("5. Narrow channels accelerate tidal currents")
    print_slow("6. We need currents >2 m/s for commercial viability")
    print_slow("7. Tidal energy is >95% predictable years ahead")

    print_slow("\nLet's test your understanding...")
    time.sleep(1)

    # Initial quiz
    quiz_score = mini_game_tidal_physics()
    player_score += quiz_score

    # Update rank
    if player_score >= 25:
        detective_rank = "Tidal Detective"

    # Load available datasets
    location_files = [f for f in os.listdir() if f.endswith('_Tide_2024.xlsx')]

    if len(location_files) == 0:
        print_slow("No tidal data files found! Run the data generator first.")
        exit()

    # Ask how many locations to analyze
    print("\n" + "-"*60)
    print_slow("Excellent work! Time to investigate real tidal sites.")
    print_slow(f"\nWe have tidal data from {len(location_files)} strategic locations.")

    max_locations = min(len(location_files), 8)
    num_locations = 0

    while num_locations < 3 or num_locations > max_locations:
        try:
            print_slow(f"\nHow many sites would you like to assess? (3-{max_locations})")
            print_slow("(More sites = more comprehensive analysis)")
            num_locations = int(input("Number of sites: "))
        except ValueError:
            print("Please enter a valid number!")

    print_slow(f"\nPerfect! You'll investigate {num_locations} tidal energy sites.")
    print_slow("The Marine Energy Board awaits your findings!")
    time.sleep(1)

    # Selection mode
    print_slow("\nWould you like to choose specific sites or investigate random ones?")
    print("1. Choose specific sites")
    print("2. Random site selection")

    selection_mode = 0
    while selection_mode not in [1, 2]:
        try:
            selection_mode = int(input("\nYour choice (1-2): "))
        except ValueError:
            print("Please enter 1 or 2!")

    if selection_mode == 1:
        # Manual selection
        print_slow("\nAvailable tidal energy sites:")
        for i, loc in enumerate(location_files, 1):
            loc_name = loc.replace('_Tide_2024.xlsx', '').replace('_', ' ')
            print(f"{i}. {loc_name}")

        selected_locations = []
        for i in range(num_locations):
            choice = 0
            while choice < 1 or choice > len(location_files):
                try:
                    choice = int(input(f"\nSelect site #{i+1}: "))
                except ValueError:
                    print("Please enter a valid number!")
            selected_locations.append(location_files[choice-1])

        location_files = selected_locations
    else:
        # Random selection
        random.shuffle(location_files)
        location_files = location_files[:num_locations]

    # Main game loop
    while location_files and locations_analyzed < num_locations:
        clear_screen()

        # Update rank
        if player_score >= 120:
            detective_rank = "Master Tidal Energy Detective"
        elif player_score >= 70:
            detective_rank = "Senior Tidal Detective"
        elif player_score >= 35:
            detective_rank = "Tidal Detective"

        print("\n" + "="*60)
        print_slow(f"🌊 SITE #{locations_analyzed + 1} INVESTIGATION 🌊")
        print("="*60)
        print(f"Tidal Detective: {student_name}")
        print(f"Rank: {detective_rank}")
        print(f"Score: {player_score} points")
        print("-"*60 + "\n")

        # Get next location
        current_file = location_files.pop(0)
        location_name = current_file.replace('_Tide_2024.xlsx', '').replace('_', ' ')

        print_slow(f"Investigating: {location_name}")
        print_slow("Analyzing tidal patterns and energy potential...")
        print()

        # Load and analyze data
        try:
            data = pd.read_excel(current_file)
            months = data['Month']
            tidal_ranges = data['Mean Tidal Range (m)']
            current_velocities = data['Peak Current Velocity (m/s)']
            spring_ranges = data['Spring Tide Range (m)']
            neap_ranges = data['Neap Tide Range (m)']
            flood_velocities = data['Peak Flood Velocity (m/s)']
            ebb_velocities = data['Peak Ebb Velocity (m/s)']

            # Calculate statistics
            avg_range = tidal_ranges.mean()
            avg_velocity = current_velocities.mean()
            max_velocity = current_velocities.max()
            min_velocity = current_velocities.min()

            # Spring/neap analysis
            avg_spring_range = spring_ranges.mean()
            avg_neap_range = neap_ranges.mean()
            spring_neap_ratio = avg_spring_range / avg_neap_range if avg_neap_range > 0 else 1

            # Flood/ebb analysis
            avg_flood = flood_velocities.mean()
            avg_ebb = ebb_velocities.mean()

            # Calculate tidal power (simplified)
            # P = 0.5 × ρ × A × v³
            # Using 1 m² swept area and seawater density 1025 kg/m³
            def calculate_tidal_power(velocity):
                return 0.5 * 1025 * 1 * (velocity ** 3) / 1000  # kW

            tidal_power_kW = []
            for v in current_velocities:
                power = calculate_tidal_power(v) * 100  # Scale for 100m² turbine
                tidal_power_kW.append(power)

            avg_power = sum(tidal_power_kW) / len(tidal_power_kW)

            # Annual energy calculation
            # Tidal turbines typically 1.5MW, 35% capacity factor
            turbine_rating = 1500  # kW
            capacity_factor = 0.35
            num_turbines = 7  # Small farm
            farm_capacity = num_turbines * turbine_rating / 1000  # MW
            annual_energy_MWh = farm_capacity * 8760 * capacity_factor
            homes_powered = int(annual_energy_MWh / 4.2)

            # Site suitability (need velocity >2 m/s)
            is_suitable = avg_velocity >= 2.0

            # Determine site characteristics
            if "Lough" in location_name:
                channel_type = "enclosed"
                site_description = "Enclosed sea lough with controlled flow"
            elif "Sound" in location_name or "Channel" in location_name:
                channel_type = "narrow"
                site_description = "Narrow channel with accelerated currents"
            elif "Harbour" in location_name or "Entrance" in location_name:
                channel_type = "entrance"
                site_description = "Harbor entrance with bi-directional flow"
            else:
                channel_type = "open"
                site_description = "Open water site with tidal streams"

            # Display analysis
            print_slow("🌊 TIDAL RESOURCE ASSESSMENT:")
            print(f"  • Site type: {site_description}")
            print(f"  • Mean tidal range: {avg_range:.1f} m")
            print(f"  • Spring tide range: {avg_spring_range:.1f} m")
            print(f"  • Neap tide range: {avg_neap_range:.1f} m")
            print(f"  • Spring/neap ratio: {spring_neap_ratio:.1f}x")
            print(f"  • Peak current velocity: {max_velocity:.2f} m/s")
            print(f"  • Average velocity: {avg_velocity:.2f} m/s")
            print(f"  • Power density: {avg_power:.1f} kW per turbine")
            print(f"  • 10MW farm annual output: {annual_energy_MWh:.1f} MWh")
            print(f"  • Homes powered: {homes_powered}")
            print("\n" + "-"*60)

            # Visual representation
            print_slow("Monthly Tidal Conditions:")
            max_bar = 40

            for i in range(len(months)):
                # Show tidal range
                range_bar_length = int((tidal_ranges[i] / max(tidal_ranges)) * max_bar)
                range_bar = "▓" * range_bar_length

                # Show current velocity
                velocity_bar_length = int((current_velocities[i] / max(current_velocities)) * max_bar)
                velocity_bar = "█" * velocity_bar_length

                print(f"{months[i]:10}: Range {tidal_ranges[i]:.1f}m {range_bar}")
                print(f"{'':10}  Speed {current_velocities[i]:.2f}m/s {velocity_bar}")

                # Power indicator
                if current_velocities[i] >= 2.5:
                    power_status = "⚡⚡⚡ Excellent"
                elif current_velocities[i] >= 2.0:
                    power_status = "⚡⚡ Good"
                elif current_velocities[i] >= 1.5:
                    power_status = "⚡ Marginal"
                else:
                    power_status = "○ Insufficient"
                print(f"{'':10}  Power: {power_status}")
                print()

            print("-"*60)

            # Challenge question
            print_slow("DETECTIVE CHALLENGE:")
            print_slow("Based on the tidal data, is this site suitable for")
            print_slow("commercial tidal energy development? (yes/no)")
            print_slow("\nConsider: Need average velocity >2 m/s for viability")

            # Get answer
            student_answer = ""
            while student_answer.lower() not in ["yes", "no", "y", "n"]:
                student_answer = input("Your assessment (yes/no): ").lower()

            student_answer = student_answer.lower() in ["yes", "y"]

            # Check correctness
            correct = (student_answer == is_suitable)

            # Feedback
            print("\n" + "-"*60)
            if correct:
                print_slow("🌟 CORRECT! Excellent tidal assessment! 🌟")
                points_earned = 10
                player_score += points_earned
                print_slow(f"You earned {points_earned} points!")
            else:
                print_slow("❌ Not quite right. Let's review:")
                points_earned = 0

            # Explain
            if is_suitable:
                print_slow(f"With {avg_velocity:.2f} m/s average velocity, this site IS suitable!")
                print_slow("Velocities above 2 m/s provide good power generation.")
                print_slow(f"The predictable currents here could reliably power {homes_powered} homes.")
            else:
                print_slow(f"With only {avg_velocity:.2f} m/s average velocity, this site is marginal.")
                print_slow("Commercial tidal farms need at least 2 m/s currents.")
                print_slow("This site might work for research but not large-scale generation.")

            # Advanced analysis options
            print("\n" + "-"*60)
            print_slow("🔬 ADVANCED ANALYSIS OPTIONS:")
            print_slow("Select additional investigation:")

            analysis_options = [
                "Spring/Neap tide analysis",
                "Flood/Ebb flow patterns (tidal ellipse)",
                "Environmental impact assessment",
                "Economic feasibility study",
                "Continue to next site"
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
                'tidal_ranges': tidal_ranges,
                'current_velocities': current_velocities,
                'spring_ranges': spring_ranges,
                'neap_ranges': neap_ranges,
                'avg_range': avg_range,
                'avg_velocity': avg_velocity,
                'avg_power': avg_power,
                'annual_energy_MWh': annual_energy_MWh,
                'homes_powered': homes_powered,
                'is_suitable': is_suitable,
                'channel_type': channel_type,
                'spring_neap_ratio': spring_neap_ratio,
                'flood_velocity': avg_flood,
                'ebb_velocity': avg_ebb,
                'flood_ebb_ratio': avg_flood/avg_ebb if avg_ebb > 0 else 1
            }

            # Perform additional analysis
            if choice == 1:  # Spring/Neap analysis
                print_slow("\nAnalyzing spring/neap tide cycles...")
                resource_file, ratio, variation = create_tidal_resource_analysis(data, location_name)

                print_slow(f"\nResource analysis saved: {resource_file}")
                print_slow(f"Spring tides are {ratio:.1f}x more powerful than neap tides")
                print_slow(f"Power varies by {variation:.0f}% over the lunar month")
                print_slow("This predictable variation helps grid operators plan ahead!")

                location_data['resource_file'] = resource_file
                location_data['spring_neap_power_ratio'] = ratio
                location_data['power_variation'] = variation

                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points!")

            elif choice == 2:  # Tidal ellipse
                print_slow("\nAnalyzing flood/ebb flow patterns...")
                ellipse_file, dominance, reason, flood_v, ebb_v = create_tidal_ellipse(data, location_name)

                print_slow(f"\nTidal ellipse saved: {ellipse_file}")
                print_slow(f"Flow pattern: {dominance} - {reason}")
                print_slow(f"Flood: {flood_v:.2f} m/s, Ebb: {ebb_v:.2f} m/s")

                location_data['ellipse_file'] = ellipse_file
                location_data['flow_dominance'] = dominance
                location_data['tidal_pattern'] = f"{dominance} ({reason})"

                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points!")

            elif choice == 3:  # Environmental impact
                print_slow("\nAssessing environmental benefits...")

                environmental_impact = calculate_carbon_savings(annual_energy_MWh)

                print_slow(f"\nA 10MW tidal farm at {location_name} would provide:")
                print_slow(f"• {environmental_impact['total_co2_savings']:.1f} tons CO2 savings/year")
                print_slow(f"  (including {environmental_impact['backup_reduction']:.1f} tons from reduced backup generation)")
                print_slow(f"• Equivalent to {environmental_impact['equivalent_trees']} trees planted")
                print_slow(f"• Powers {environmental_impact['homes_powered']} homes predictably")
                print_slow(f"• Serves {environmental_impact['percent_islands']:.1f}% of island communities")
                print_slow(f"• Creates {environmental_impact['reef_area']:.0f} m² artificial reef habitat")
                print_slow(f"• {environmental_impact['predictability_benefit']}")

                location_data['environmental_impact'] = environmental_impact

                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points!")

            elif choice == 4:  # Economic analysis
                print_slow("\nCalculating project economics...")

                econ_data = calculate_economic_factors(annual_energy_MWh, 10, location_name)

                print_slow(f"\nEconomic analysis for 10MW tidal farm at {location_name}:")
                print_slow(f"• Tidal turbines: {econ_data['num_turbines']} × 1.5MW units")
                print_slow(f"• Total investment needed: €{econ_data['total_cost']:,.0f}")
                print_slow(f"  - Turbines: €{econ_data['turbine_cost']:,.0f}")
                print_slow(f"  - Foundations: €{econ_data['foundation_cost']:,.0f}")
                print_slow(f"  - Subsea cables: €{econ_data['subsea_cable_cost']:,.0f}")
                print_slow(f"  - Environmental systems: €{econ_data['environmental_monitoring']:,.0f}")
                print_slow(f"• Annual revenue: €{econ_data['annual_revenue']:,.0f}")
                print_slow(f"  (includes €{econ_data['predictability_premium']:,.0f} grid stability premium)")
                print_slow(f"• Annual profit: €{econ_data['annual_profit']:,.0f}")
                print_slow(f"• Simple payback: {econ_data['payback_period']:.1f} years")
                print_slow(f"• Levelized cost: €{econ_data['lcoe']:.0f}/MWh")
                print_slow(f"• Jobs created: {econ_data['construction_jobs']} construction,")
                print_slow(f"  {econ_data['permanent_jobs']} permanent, {econ_data['marine_specialist_jobs']} marine specialists")

                location_data['economic_data'] = econ_data

                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points!")

            # Add to analyzed locations
            analyzed_locations.append(location_data)

            # Generate main visualization
            print_slow("\nGenerating tidal analysis visualizations...")
            chart_file = create_power_plot(
                months, tidal_ranges, current_velocities, tidal_power_kW,
                avg_range, avg_velocity, avg_power, annual_energy_MWh,
                homes_powered, location_name
            )
            print_slow(f"Analysis saved: {chart_file}")

            # Update progress
            locations_analyzed += 1

            # Continue
            print("\n" + "-"*60)
            input("Press Enter to continue... ")

        except Exception as e:
            print(f"Error analyzing site: {e}")
            print("Moving to next site...")
            time.sleep(3)

    # Site optimization mini-game
    optimization_score = mini_game_site_selection()
    player_score += optimization_score

    # Final rank update
    if player_score >= 120:
        detective_rank = "Master Tidal Energy Detective"
    elif player_score >= 70:
        detective_rank = "Senior Tidal Detective"
    elif player_score >= 35:
        detective_rank = "Tidal Detective"

    # Report generation
    clear_screen()
    print("\n" + "="*60)
    print_slow("📋 FINAL REPORT GENERATION 📋", 0.05)
    print("="*60)

    print_slow(f"\nOutstanding work, {detective_rank} {student_name}!")
    print_slow(f"You've analyzed {locations_analyzed} tidal energy sites")
    print_slow(f"and achieved {player_score} points!")

    print_slow("\nTime to compile your findings for the Marine Energy Board.")

    # Ask about report
    print_slow("\nGenerate official assessment report? (yes/no)")

    generate_report = input("Generate report? ").lower() in ["y", "yes"]

    if generate_report:
        print_slow("\nCompiling tidal energy assessment...")
        report_file = generate_text_report(student_name, detective_rank, analyzed_locations, player_score)

        if report_file:
            print_slow(f"\nReport generated: {report_file}")
            print_slow("The Marine Energy Board will review your findings!")
        else:
            print_slow("\nUnable to save report file.")
            generate_report = False

    # Summary if no report
    if not generate_report:
        clear_screen()
        print("\n" + "="*60)
        print_slow("🌊 TIDAL DETECTIVE MISSION SUMMARY 🌊", 0.05)
        print("="*60)

        print_slow(f"Tidal Detective: {student_name}")
        print_slow(f"Final Rank: {detective_rank}")
        print_slow(f"Total Score: {player_score} points")

        if analyzed_locations:
            print_slow("\n" + "-"*60)
            print_slow("KEY DISCOVERIES:")

            # Sort by power potential
            sorted_locs = sorted(analyzed_locations,
                               key=lambda x: x['avg_velocity']**3,
                               reverse=True)

            if sorted_locs:
                best = sorted_locs[0]
                print_slow(f"\nStrongest tidal resource: {best['name']}")
                print_slow(f"Peak velocity: {best['avg_velocity']:.2f} m/s")
                print_slow(f"Could power {best['homes_powered']} homes yearly")

                print_slow("\n" + "-"*60)
                print_slow("SITE RANKINGS:")

                for i, loc in enumerate(sorted_locs):
                    status = "EXCELLENT" if loc['avg_velocity'] >= 2.5 else "SUITABLE" if loc['is_suitable'] else "MARGINAL"
                    print_slow(f"{i+1}. {loc['name']} - {loc['avg_velocity']:.2f} m/s - {status}")

    # Finale
    print("\n" + "-"*60)
    print_slow("🌍 MISSION ACCOMPLISHED!", 0.05)

    print_slow("\nThank you for your service as a Tidal Energy Detective!")
    print_slow("Your analysis helps Ireland harness predictable lunar power")
    print_slow("for a sustainable energy future.")

    print_slow("\nKey takeaways:")
    print_slow("• Tidal power depends on velocity cubed (v³)")
    print_slow("• Narrow channels and straits offer best resources")
    print_slow("• Spring/neap cycles create predictable variations")
    print_slow("• >95% predictability aids grid stability")
    print_slow("• Environmental monitoring protects marine life")

    print("\n" + "="*60)
    print_slow("🌊 THE TIDES WAIT FOR NO ONE - USE THEM WISELY! 🌊", 0.05)
    print("="*60)

    input("\nPress Enter to complete mission... ")

# Run the game
if __name__ == "__main__":
    run_tide_detective_game()

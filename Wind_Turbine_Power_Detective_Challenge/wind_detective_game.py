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

def create_power_plot(months, wind_speeds, wind_power_kW, avg_wind_speed, avg_power, annual_energy_MWh, homes_powered, location_name):
    """Create and save a colorful power plot for the location"""
    # Create colorful power plot
    plt.figure(figsize=(10, 6))

    # Create a colormap that goes from blue to green to yellow to red
    colors = ["#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
              "#fee090", "#fdae61", "#f46d43", "#d73027"]
    cmap = LinearSegmentedColormap.from_list("wind_colors", colors)

    # Plot with colorful bars
    bars = plt.bar(range(1, 13), wind_power_kW, color=cmap(np.linspace(0, 1, 12)))
    plt.xticks(range(1, 13), labels=months, rotation=45)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 20,
                 f'{height:.0f}', ha='center', va='bottom')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Wind Power (kW)', fontsize=12)
    plt.title(f'Wind Power Output at {location_name} (kW)', fontsize=14)

    # Add information box
    info_text = (
        f"📌 Average wind speed: {avg_wind_speed:.1f} m/s\n"
        f"💡 Average power: {avg_power:.1f} kW\n"
        f"🔋 Annual energy: {annual_energy_MWh:.1f} MWh\n"
        f"🏠 Can power: {homes_powered} homes"
    )

    plt.figtext(0.15, 0.02, info_text, bbox=dict(facecolor='white', alpha=0.8), fontsize=10)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_power_analysis.png"
    plt.savefig(output_file)
    plt.close()

    return output_file

def create_seasonal_analysis(months, wind_speeds, location_name):
    """Create a seasonal analysis chart for the location"""
    plt.figure(figsize=(10, 6))

    # Define seasons with their corresponding months
    seasons = {
        'Winter': ['December', 'January', 'February'],
        'Spring': ['March', 'April', 'May'],
        'Summer': ['June', 'July', 'August'],
        'Autumn': ['September', 'October', 'November']
    }

    # Calculate seasonal averages - improved matching
    seasonal_avg = {}
    for season, season_months in seasons.items():
        # Get indices of months belonging to this season
        season_values = []
        for i, month in enumerate(months):
            # Check if the month belongs to this season (more robust matching)
            if month in season_months:
                season_values.append(wind_speeds[i])

        # Calculate average if we have values
        if season_values:
            seasonal_avg[season] = sum(season_values) / len(season_values)
        else:
            seasonal_avg[season] = 0

    # Plot seasonal data
    seasons_list = list(seasonal_avg.keys())
    speeds_list = list(seasonal_avg.values())

    # Create a colormap for seasons - visually distinct colors
    season_colors = ['#4575b4', '#74c476', '#fd8d3c', '#8c564b']  # Blue, Green, Orange, Brown

    bars = plt.bar(seasons_list, speeds_list, color=season_colors, width=0.6)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.1f}', ha='center', va='bottom', fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.ylabel('Average Wind Speed (m/s)', fontsize=12)
    plt.title(f'Seasonal Wind Analysis - {location_name}', fontsize=14)

    # Add annotations
    best_season = seasons_list[speeds_list.index(max(speeds_list))]
    worst_season = seasons_list[speeds_list.index(min(speeds_list))]

    # Calculate how much stronger the best season is compared to the worst
    percent_stronger = ((max(speeds_list) - min(speeds_list)) / min(speeds_list)) * 100 if min(speeds_list) > 0 else 0

    # Add variance calculation to show consistency
    variance = np.var(speeds_list)
    consistency = "Very consistent" if variance < 0.5 else "Moderately consistent" if variance < 1.5 else "Highly variable"

    plt.figtext(0.5, 0.01,
                f"Best season: {best_season} ({max(speeds_list):.1f} m/s)\n"
                f"Worst season: {worst_season} ({min(speeds_list):.1f} m/s)\n"
                f"{best_season} is {percent_stronger:.1f}% stronger than {worst_season}\n"
                f"Seasonal consistency: {consistency} (variance: {variance:.2f})",
                ha='center', bbox=dict(facecolor='white', alpha=0.8), fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Save the plot
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_seasonal_analysis.png"
    plt.savefig(output_file)
    plt.close()

    return output_file, best_season, worst_season, seasonal_avg

def create_wind_rose(wind_speeds, location_name):
    """Create a more realistic wind rose diagram based on location"""
    plt.figure(figsize=(8, 8))

    # Directions for the wind rose
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    # Create more meaningful direction weights based on location
    # These are now more realistic with clearer dominant directions
    if "East" in location_name:
        # East coast - predominantly westerly winds with SW secondary
        weights = [0.05, 0.07, 0.10, 0.08, 0.12, 0.18, 0.25, 0.15]
    elif "West" in location_name:
        # West coast - strong SW winds typical of Atlantic exposure
        weights = [0.08, 0.05, 0.04, 0.07, 0.15, 0.30, 0.20, 0.11]
    elif "South" in location_name:
        # South coast - SW predominant with westerly secondary
        weights = [0.06, 0.08, 0.10, 0.12, 0.09, 0.25, 0.20, 0.10]
    elif "North" in location_name:
        # North coast - SW and W winds with stronger northerly component
        weights = [0.15, 0.08, 0.06, 0.05, 0.07, 0.20, 0.26, 0.13]
    else:
        # Default - typical Irish pattern with SW predominance
        weights = [0.08, 0.07, 0.08, 0.09, 0.12, 0.25, 0.20, 0.11]

    # Add random variation to make each location unique but consistent
    # Use location name as seed for reproducibility
    random.seed(sum(ord(c) for c in location_name))
    weights = [w * random.uniform(0.85, 1.15) for w in weights]

    # Normalize to ensure weights sum to 1
    weights = [w / sum(weights) for w in weights]

    # Scale wind speeds by the weights and apply a multiplier for visual impact
    avg_speed = np.mean(wind_speeds)
    speeds = [avg_speed * w * 10 for w in weights]

    # Plot the wind rose
    angles = np.linspace(0, 2*np.pi, len(directions), endpoint=False)

    # Close the plot by repeating the first point
    speeds.append(speeds[0])
    angles = np.append(angles, angles[0])

    # Create the polar plot
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, speeds, 'o-', linewidth=2, color='#4682B4')
    ax.fill(angles, speeds, alpha=0.25, color='#4682B4')

    # Set direction labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(directions)

    # Add gridlines
    ax.grid(True)

    # Calculate dominant direction and its percentage
    dominant_idx = weights.index(max(weights))
    dominant_direction = directions[dominant_idx]
    dominant_percent = weights[dominant_idx] * 100

    # Title with dominant information
    plt.title(f'Wind Rose - {location_name}\nDominant Direction: {dominant_direction} ({dominant_percent:.1f}%)', size=14)

    # Save the wind rose
    clean_name = location_name.replace(' ', '_')
    output_file = f"{clean_name}_wind_rose.png"
    plt.savefig(output_file)
    plt.close()

    # Calculate secondary direction (second highest)
    weights_copy = weights.copy()
    weights_copy[dominant_idx] = 0  # Remove dominant
    secondary_idx = weights_copy.index(max(weights_copy))
    secondary_direction = directions[secondary_idx]

    # Additional analysis text
    direction_analysis = {
        'dominant': dominant_direction,
        'dominant_percent': dominant_percent,
        'secondary': secondary_direction,
        'secondary_percent': weights[secondary_idx] * 100,
        'ratio': dominant_percent / weights[secondary_idx] / 100 if weights[secondary_idx] > 0 else 0
    }

    return output_file, dominant_direction, direction_analysis

def calculate_carbon_savings(annual_energy_MWh):
    """Calculate carbon savings from wind energy"""
    # Average CO2 emissions from fossil fuel electricity in Ireland
    # (in kg CO2 per MWh)
    fossil_emissions = 450

    # Calculate CO2 savings
    co2_savings = annual_energy_MWh * fossil_emissions

    # Convert to tons
    co2_savings_tons = co2_savings / 1000

    # Calculate equivalent trees
    # One tree absorbs about 22 kg of CO2 per year
    equivalent_trees = int(co2_savings / 22)

    # Calculate equivalent:
    # - Cars removed from road (4.6 tons CO2 per car per year)
    # - Homes powered (4.2 MWh per home per year)
    cars_equivalent = int(co2_savings_tons / 4.6)
    homes_powered = int(annual_energy_MWh / 4.2)

    # Calculate percentage of Irish household emissions
    # Ireland has about 1.7 million households
    percent_of_country = (homes_powered / 1700000) * 100

    return {
        'co2_savings_tons': co2_savings_tons,
        'equivalent_trees': equivalent_trees,
        'cars_equivalent': cars_equivalent,
        'homes_powered': homes_powered,
        'percent_of_country': percent_of_country
    }

def calculate_economic_factors(annual_energy_MWh, num_turbines=10, location_name=""):
    """Calculate economic factors for a wind farm with more detail"""
    # Base parameters
    electricity_price = 150  # €/MWh

    # Location-based factors (offshore is more expensive but more productive)
    if "Atlantic" in location_name:
        # Deep offshore - highest cost, highest productivity
        capacity_factor = 0.48  # 48% efficiency
        cost_per_turbine = 4800000  # €4.8 million per turbine
        maintenance_factor = 0.035  # 3.5% of installation cost per year
    elif "Ocean" in location_name or "Sea" in location_name:
        # Offshore - high cost, good productivity
        capacity_factor = 0.45  # 45% efficiency
        cost_per_turbine = 4500000  # €4.5 million per turbine
        maintenance_factor = 0.033  # 3.3% of installation cost per year
    elif "Bay" in location_name:
        # Near shore - medium cost, medium productivity
        capacity_factor = 0.42  # 42% efficiency
        cost_per_turbine = 4200000  # €4.2 million per turbine
        maintenance_factor = 0.031  # 3.1% of installation cost per year
    else:
        # Default - standard offshore
        capacity_factor = 0.43  # 43% efficiency
        cost_per_turbine = 4300000  # €4.3 million per turbine
        maintenance_factor = 0.032  # 3.2% of installation cost per year

    # Annual revenue
    annual_revenue = annual_energy_MWh * electricity_price

    # Installation costs
    installation_cost = num_turbines * cost_per_turbine

    # Additional costs
    grid_connection_cost = installation_cost * 0.15  # 15% of installation cost
    planning_cost = installation_cost * 0.05  # 5% of installation cost
    total_cost = installation_cost + grid_connection_cost + planning_cost

    # Maintenance costs
    annual_maintenance = installation_cost * maintenance_factor

    # Annual profit
    annual_profit = annual_revenue - annual_maintenance

    # Simple payback period (years)
    payback_period = total_cost / annual_profit

    # Jobs created (construction and permanent)
    construction_jobs = num_turbines * 15  # 15 jobs per turbine during construction
    permanent_jobs = num_turbines * 0.5  # 0.5 permanent jobs per turbine

    # Return all data in a dictionary
    return {
        'annual_revenue': annual_revenue,
        'installation_cost': installation_cost,
        'grid_connection_cost': grid_connection_cost,
        'planning_cost': planning_cost,
        'total_cost': total_cost,
        'annual_maintenance': annual_maintenance,
        'annual_profit': annual_profit,
        'payback_period': payback_period,
        'capacity_factor': capacity_factor,
        'construction_jobs': int(construction_jobs),
        'permanent_jobs': int(permanent_jobs)
    }

def generate_text_report(student_name, detective_rank, analyzed_locations, score):
    """Generate a simple text report"""
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("WIND DETECTIVE CHALLENGE - FINAL REPORT")
    report_lines.append("="*60)
    report_lines.append(f"Detective: {student_name}")
    report_lines.append(f"Rank: {detective_rank}")
    report_lines.append(f"Date: {datetime.now().strftime('%d %B %Y')}")
    report_lines.append(f"Final Score: {score} points")
    report_lines.append("-"*60)

    # Sort locations by average wind speed
    sorted_locations = sorted(analyzed_locations,
                            key=lambda x: x['avg_wind_speed'],
                            reverse=True)

    # Add executive summary
    report_lines.append("EXECUTIVE SUMMARY:")
    report_lines.append("")

    best_location = sorted_locations[0]['name']
    report_lines.append(f"After analyzing {len(analyzed_locations)} offshore locations around Ireland,")
    report_lines.append(f"we have determined that {best_location} offers the best potential for")
    report_lines.append(f"wind energy development with an average wind speed of {sorted_locations[0]['avg_wind_speed']:.1f} m/s")
    report_lines.append(f"and estimated annual energy production of {sorted_locations[0]['annual_energy_MWh']:.1f} MWh,")
    report_lines.append(f"enough to power {sorted_locations[0]['homes_powered']} homes.")

    # Add location rankings
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("LOCATION RANKINGS (by average wind speed):")
    report_lines.append("")

    for i, location in enumerate(sorted_locations):
        suitability = "SUITABLE" if location['is_suitable'] else "NOT SUITABLE"
        report_lines.append(f"{i+1}. {location['name']} - {location['avg_wind_speed']:.1f} m/s - {suitability}")

    # Add recommendations
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("RECOMMENDATIONS:")
    report_lines.append("")

    recommended = [loc for loc in sorted_locations if loc['is_suitable']]
    if recommended:
        report_lines.append("Based on our analysis, we recommend developing wind farms at:")
        for i, loc in enumerate(recommended[:3]):
            report_lines.append(f"{i+1}. {loc['name']}")

            # Add reasoning if available
            reasons = []
            if 'dominant_direction' in loc:
                reasons.append(f"dominant wind from {loc['dominant_direction']}")
            if 'best_season' in loc:
                reasons.append(f"strongest winds in {loc['best_season']}")
            if 'carbon_savings' in loc:
                reasons.append(f"saving {loc.get('carbon_savings', 0):.1f} tons CO2 annually")

            if reasons:
                report_lines.append(f"   Reasons: {', '.join(reasons)}")
    else:
        report_lines.append("None of the analyzed locations meet the minimum requirements for wind farms.")

    # Add detailed location information
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("DETAILED LOCATION ANALYSIS:")

    for i, location in enumerate(sorted_locations):
        report_lines.append("")
        report_lines.append(f"Location #{i+1}: {location['name']}")
        report_lines.append(f"Average Wind Speed: {location['avg_wind_speed']:.1f} m/s")
        report_lines.append(f"Average Power Output: {location['avg_power']:.1f} kW")
        report_lines.append(f"Annual Energy Production: {location['annual_energy_MWh']:.1f} MWh")
        report_lines.append(f"Homes Powered: {location['homes_powered']}")

        if 'best_season' in location:
            report_lines.append(f"Best Season: {location['best_season']}")
            report_lines.append(f"Worst Season: {location.get('worst_season', 'Unknown')}")

        if 'direction_analysis' in location:
            da = location['direction_analysis']
            report_lines.append(f"Dominant Wind Direction: {da['dominant']} ({da['dominant_percent']:.1f}%)")
            report_lines.append(f"Secondary Wind Direction: {da['secondary']} ({da['secondary_percent']:.1f}%)")

        if 'environmental_impact' in location:
            ei = location['environmental_impact']
            report_lines.append(f"CO2 Savings: {ei['co2_savings_tons']:.1f} tons/year")
            report_lines.append(f"Equivalent to: {ei['equivalent_trees']} trees or {ei['cars_equivalent']} cars")

        if 'economic_data' in location:
            econ = location['economic_data']
            report_lines.append(f"Economic Assessment:")
            report_lines.append(f"  - Annual Revenue: €{econ['annual_revenue']:,.0f}")
            report_lines.append(f"  - Total Cost: €{econ.get('total_cost', econ['installation_cost']):,.0f}")
            report_lines.append(f"  - Annual Profit: €{econ['annual_profit']:,.0f}")
            report_lines.append(f"  - Payback Period: {econ['payback_period']:.1f} years")
            if 'construction_jobs' in econ:
                report_lines.append(f"  - Jobs Created: {econ['construction_jobs']} construction, {econ['permanent_jobs']} permanent")

    # Conclusion
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("CONCLUSION:")
    report_lines.append("")
    report_lines.append("Ireland has significant potential for offshore wind energy development,")
    report_lines.append("particularly along the western and northwestern coasts. Strategic")
    report_lines.append("development of these resources would provide clean, renewable energy")
    report_lines.append("for thousands of homes while creating jobs and reducing carbon emissions.")

    # Save to file
    report_filename = f"Wind_Detective_Report_{student_name.replace(' ', '_')}.txt"
    try:
        with open(report_filename, 'w') as f:
            f.write("\n".join(report_lines))
        return report_filename
    except Exception as e:
        print(f"Error saving report: {e}")
        return None

def mini_game_turbine_efficiency():
    """Mini-game to test knowledge of factors affecting wind turbine efficiency"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("🔍 SPECIAL CHALLENGE: TURBINE EFFICIENCY EXPERT 🔍", 0.05)
    print("="*60)

    print_slow("\nThe Minister wants to know if you understand what makes")
    print_slow("wind turbines more efficient. Answer these questions to earn bonus points!")

    questions = [
        {
            "question": "Which factor affects wind power generation the most?",
            "options": ["Wind speed", "Air temperature", "Humidity", "Barometric pressure"],
            "correct": 0,
            "explanation": "Wind speed has the greatest impact because power increases with the CUBE of wind speed. Doubling wind speed creates 8 times more power!"
        },
        {
            "question": "What happens to power output when wind speed doubles?",
            "options": ["It doubles", "It triples", "It quadruples", "It increases by 8 times"],
            "correct": 3,
            "explanation": "Power increases with the CUBE of wind speed (P ∝ v³), so doubling wind speed increases power by 2³ = 8 times."
        },
        {
            "question": "Which part of Ireland typically has the strongest winds?",
            "options": ["East coast", "South coast", "West coast", "Central regions"],
            "correct": 2,
            "explanation": "The west coast of Ireland typically has the strongest winds due to Atlantic weather systems and less land interference."
        },
        {
            "question": "Why are offshore wind farms often more productive than onshore?",
            "options": ["Newer technology", "Stronger and more consistent winds", "Cheaper to build", "Less maintenance required"],
            "correct": 1,
            "explanation": "Offshore wind farms benefit from stronger and more consistent winds over the ocean, with no obstacles to slow down the wind."
        },
        {
            "question": "What's the minimum wind speed generally needed for a commercial offshore wind farm?",
            "options": ["3 m/s", "5 m/s", "7 m/s", "10 m/s"],
            "correct": 2,
            "explanation": "Generally, a minimum average wind speed of 7 m/s is considered necessary for a commercially viable offshore wind farm."
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

        # Check if correct (adjusting for 0-indexing)
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
        print_slow("🌟 EXCELLENT! You're a turbine efficiency expert!")
    elif score >= len(questions)*5 * 0.6:
        print_slow("👍 GOOD JOB! You understand the key principles of wind energy.")
    else:
        print_slow("🔍 Keep learning! Wind energy has some tricky physics concepts.")

    return score

def mini_game_design_challenge():
    """Mini-game to design the ideal wind farm layout"""
    clear_screen()
    print("\n" + "="*60)
    print_slow("🔧 SPECIAL CHALLENGE: WIND FARM DESIGNER 🔧", 0.05)
    print("="*60)

    print_slow("\nThe Minister has asked you to make some design decisions")
    print_slow("for the new wind farm. Your choices will affect its performance!")

    score = 0

    # Challenge 1: Turbine spacing
    print("\n" + "-"*60)
    print_slow("DESIGN CHALLENGE #1: Turbine Spacing")
    print_slow("\nHow far apart should you place the wind turbines?")
    options = [
        "2 rotor diameters apart (very close)",
        "5 rotor diameters apart (medium spacing)",
        "8 rotor diameters apart (wide spacing)",
        "12 rotor diameters apart (very wide spacing)"
    ]

    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    answer = -1
    while answer < 1 or answer > len(options):
        try:
            answer = int(input(f"\nYour choice (1-{len(options)}): "))
        except ValueError:
            print("Please enter a valid number!")

    if answer == 3:  # Correct answer is staggered grid
        print_slow("✓ EXCELLENT CHOICE! +10 points")
        print_slow("A staggered grid allows more turbines to access undisturbed wind,")
        print_slow("reducing wake effects and increasing overall farm efficiency.")
        score += 10
    elif answer == 1:  # Somewhat reasonable
        print_slow("✓ REASONABLE CHOICE! +5 points")
        print_slow("Rows perpendicular to the wind can work well for the first row,")
        print_slow("but downwind turbines will experience reduced wind speeds.")
        score += 5
    else:  # Poor choices
        print_slow("✗ This layout might reduce your wind farm's efficiency.")
        print_slow("Rows parallel to the wind create maximum wake interference,")
        print_slow("while curved arrays might not optimize for the prevailing wind direction.")

    print("\n" + "-"*60)
    print_slow(f"DESIGN CHALLENGE COMPLETE! You scored {score} out of 30 possible points!")

    if score >= 25:
        print_slow("🌟 EXCELLENT! You'd make a great wind farm designer!")
    elif score >= 15:
        print_slow("👍 GOOD JOB! Your wind farm design shows promise.")
    else:
        print_slow("🔍 Wind farm design is tricky! Keep learning about optimizing layouts.")

    return score

# Main game function
def run_wind_detective_game():
    # Title screen
    clear_screen()
    print("\n" + "="*80)
    print_slow("🌊 WIND TURBINE POWER DETECTIVE CHALLENGE - EXTENDED EDITION 🌊", 0.05)
    print("="*80)
    print_slow("\nWelcome young scientists! Ireland needs your help!")
    print_slow("The Minister of Energy has tasked YOU with finding the best")
    print_slow("locations for new wind turbines around Ireland's coast.")
    print()
    print_slow("Your mission: Analyze wind data from different offshore")
    print_slow("locations and determine which sites are suitable for")
    print_slow("building powerful wind turbines!")
    print()
    print_slow("At the end of your investigation, you'll create a")
    print_slow("professional report for the Minister of Energy with your findings.")
    print("\n" + "-"*80)

    # Ask for student name
    student_name = input("\nPlease enter your name, Wind Detective: ")
    if not student_name:
        student_name = "Detective Anonymous"

    print_slow(f"\nWelcome to the case, Detective {student_name}!")
    print_slow("Let's begin your training and investigation...")

    input("\nPress Enter to begin your mission... ")

    # Game variables
    player_score = 0
    locations_analyzed = 0
    detective_rank = "Beginner Wind Detective"
    analyzed_locations = []

    # Introductory tutorial
    clear_screen()
    print("\n" + "="*60)
    print_slow("🔍 DETECTIVE TRAINING: WIND POWER BASICS 🔍", 0.05)
    print("="*60)

    print_slow("\nBefore you begin your field investigation, let's review")
    print_slow("some key facts about wind power:")

    print_slow("\n1. Wind turbines convert kinetic energy from moving air into electricity")
    print_slow("2. Wind power increases with the CUBE of wind speed")
    print_slow("   (double the wind speed = 8 times the power!)")
    print_slow("3. Bigger turbine blades capture more energy")
    print_slow("4. Good wind farm locations need consistent, strong winds")
    print_slow("5. We need average wind speeds of at least 7 m/s for offshore sites")

    print_slow("\nNow, let's test your knowledge with a quick quiz...")
    time.sleep(1)

    # Quick quiz to engage students
    quiz_score = mini_game_turbine_efficiency()

    # Add quiz score to total score
    player_score += quiz_score

    # Update detective rank
    if player_score >= 20:
        detective_rank = "Wind Detective"

    # Load all available datasets
    location_files = [f for f in os.listdir() if f.endswith('_Wind_2024.xlsx')]

    if len(location_files) == 0:
        print_slow("Uh oh! No wind data files found! Make sure to run the data generator first.")
        exit()

    # Ask how many locations they want to analyze (minimum 3, maximum 8)
    print("\n" + "-"*60)
    print_slow("Your training is complete! Now for your real investigation.")
    print_slow(f"\nWe have data from {len(location_files)} offshore locations around Ireland.")

    max_locations = min(len(location_files), 8)
    num_locations = 0

    while num_locations < 3 or num_locations > max_locations:
        try:
            print_slow(f"\nHow many locations would you like to investigate? (3-{max_locations})")
            print_slow("(More locations = more complete analysis, but will take longer)")
            num_locations = int(input("Number of locations: "))
        except ValueError:
            print("Please enter a valid number!")

    print_slow(f"\nExcellent! You'll investigate {num_locations} offshore locations.")
    print_slow("The Minister will be impressed by your thorough analysis!")
    time.sleep(1)

    # Let student choose between random or specific locations
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
        print_slow("\nAvailable locations:")
        for i, loc in enumerate(location_files, 1):
            loc_name = loc.replace('_Wind_2024.xlsx', '').replace('_', ' ')
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

        # Current detective rank
        if player_score >= 80:
            detective_rank = "Master Wind Detective"
        elif player_score >= 50:
            detective_rank = "Senior Wind Detective"
        elif player_score >= 20:
            detective_rank = "Wind Detective"

        print("\n" + "="*60)
        print_slow(f"🔍 LOCATION #{locations_analyzed + 1} INVESTIGATION 🔍")
        print("="*60)
        print(f"Detective: {student_name}")
        print(f"Rank: {detective_rank}")
        print(f"Current Score: {player_score} points")
        print("-"*60 + "\n")

        # Select the next location
        current_file = location_files.pop(0)
        location_name = current_file.replace('_Wind_2024.xlsx', '').replace('_', ' ')

        print_slow(f"You're investigating: {location_name}")
        print_slow("Let's examine the wind data and determine if this site is suitable!")
        print()

        # Load and analyze data
        try:
            data = pd.read_excel(current_file)
            months = data['Month']
            wind_speeds = data['Wind Speed (m/s)']

            # Calculate key stats
            avg_wind_speed = wind_speeds.mean()
            max_wind_speed = wind_speeds.max()
            min_wind_speed = wind_speeds.min()
            max_month = months[wind_speeds.idxmax()]
            min_month = months[wind_speeds.idxmin()]

            # Calculate wind power
            def calculate_wind_power(wind_speed, turbine_diameter=100):
                rho = 1.225  # Air density (kg/m³)
                A = (np.pi * turbine_diameter**2) / 4  # Swept area (m²)
                power_W = 0.5 * rho * A * (wind_speed**3)
                return power_W / 1000  # Convert to kilowatts

            wind_power_kW = [calculate_wind_power(speed) for speed in wind_speeds]
            avg_power = sum(wind_power_kW) / len(wind_power_kW)

            # Calculate annual energy
            annual_energy_MWh = (avg_power * 8760) / 1000  # 8760 hours in a year
            homes_powered = int(annual_energy_MWh / 4.2)  # Average Irish home uses ~4.2 MWh/year

            # Is this site suitable? (offshore sites should have avg wind speed >= 7.0 m/s)
            is_suitable = avg_wind_speed >= 7.0

            # Display data summary with more detail
            print_slow("📊 WIND DATA SUMMARY:")
            print(f"  • Average wind speed: {avg_wind_speed:.1f} m/s")
            print(f"  • Highest wind speed: {max_wind_speed:.1f} m/s in {max_month}")
            print(f"  • Lowest wind speed: {min_wind_speed:.1f} m/s in {min_month}")
            print(f"  • Wind speed variance: {np.var(wind_speeds):.2f} (lower = more consistent)")
            print(f"  • Average power output: {avg_power:.1f} kW")
            print(f"  • Estimated annual energy: {annual_energy_MWh:.1f} MWh")
            print(f"  • This could power approximately {homes_powered} homes")
            print("\n" + "-"*60)

            # Show a simple visualization of monthly wind speeds
            print_slow("Monthly Wind Speeds:")
            max_bar_length = 40
            for i, speed in enumerate(wind_speeds):
                bar_length = int((speed / max_wind_speed) * max_bar_length)
                bar = "█" * bar_length
                print(f"{months[i]:10}: {speed:.1f} m/s {bar}")

            print("\n" + "-"*60)

            # Challenge question - let students make the decision
            print_slow("DETECTIVE CHALLENGE:")
            print_slow("Based on your analysis, do you think this location is suitable")
            print_slow("for building offshore wind turbines? (yes/no)")

            # Get student's answer
            student_answer = ""
            while student_answer.lower() not in ["yes", "no", "y", "n"]:
                student_answer = input("Your answer (yes/no): ").lower()

            student_answer = student_answer.lower() in ["yes", "y"]

            # Check if student is correct
            correct = (student_answer == is_suitable)

            # Give feedback
            print("\n" + "-"*60)
            if correct:
                print_slow("🌟 CORRECT! Great analysis, detective! 🌟")
                points_earned = 10
                player_score += points_earned
                print_slow(f"You earned {points_earned} points!")
            else:
                print_slow("❌ Not quite right. Let's review why:")
                points_earned = 0

            # Explain the correct answer
            if is_suitable:
                print_slow(f"The average wind speed of {avg_wind_speed:.1f} m/s IS suitable for wind turbines.")
                print_slow("For offshore wind farms, we typically look for average wind speeds of at least 7.0 m/s.")
                print_slow(f"This site could power around {homes_powered} homes!")
            else:
                print_slow(f"The average wind speed of {avg_wind_speed:.1f} m/s is NOT ideal for wind turbines.")
                print_slow("For offshore wind farms, we typically look for average wind speeds of at least 7.0 m/s.")
                print_slow("This site might not produce enough energy to be cost-effective.")

            # ADDITIONAL ANALYSIS SECTION - Expand the investigation
            print("\n" + "-"*60)
            print_slow("🔬 ADVANCED ANALYSIS OPTIONS:")
            print_slow("As a good detective, you can investigate further. What would you like to analyze next?")

            analysis_options = [
                "Seasonal wind patterns",
                "Wind direction analysis",
                "Environmental impact assessment",
                "Economic feasibility study",
                "Continue to next location"
            ]

            for i, option in enumerate(analysis_options):
                print(f"{i+1}. {option}")

            # Get student's choice for additional analysis
            choice = 0
            while choice < 1 or choice > len(analysis_options):
                try:
                    choice = int(input(f"\nYour choice (1-{len(analysis_options)}): "))
                except ValueError:
                    print("Please enter a valid number!")

            # Store basic location data
            location_data = {
                'name': location_name,
                'file': current_file,
                'months': months,
                'wind_speeds': wind_speeds,
                'wind_power_kW': wind_power_kW,
                'avg_wind_speed': avg_wind_speed,
                'avg_power': avg_power,
                'annual_energy_MWh': annual_energy_MWh,
                'homes_powered': homes_powered,
                'is_suitable': is_suitable
            }

            # Perform additional analysis based on student's choice
            if choice == 1:  # Seasonal analysis
                print_slow("\nAnalyzing seasonal wind patterns...")
                seasonal_file, best_season, worst_season, seasonal_data = create_seasonal_analysis(
                    months, wind_speeds, location_name
                )

                print_slow(f"\nSeasonal analysis chart created: {seasonal_file}")
                print_slow(f"Best season for wind power: {best_season}")
                print_slow(f"Worst season for wind power: {worst_season}")

                # Add seasonal data to location data
                location_data['seasonal_file'] = seasonal_file
                location_data['best_season'] = best_season
                location_data['worst_season'] = worst_season
                location_data['seasonal_data'] = seasonal_data

                # Add bonus points for conducting seasonal analysis
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for conducting seasonal analysis!")

            elif choice == 2:  # Wind direction analysis
                print_slow("\nAnalyzing wind direction patterns...")
                wind_rose_file, dominant_direction, direction_analysis = create_wind_rose(
                    wind_speeds, location_name
                )

                print_slow(f"\nWind rose diagram created: {wind_rose_file}")
                print_slow(f"Dominant wind direction at {location_name}: {dominant_direction} ({direction_analysis['dominant_percent']:.1f}%)")
                print_slow(f"Secondary wind direction: {direction_analysis['secondary']} ({direction_analysis['secondary_percent']:.1f}%)")

                # Add wind direction data to location data
                location_data['wind_rose_file'] = wind_rose_file
                location_data['dominant_direction'] = dominant_direction
                location_data['direction_analysis'] = direction_analysis

                # Add bonus points for conducting wind direction analysis
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for conducting wind direction analysis!")

            elif choice == 3:  # Environmental impact assessment
                print_slow("\nAssessing potential environmental impact...")

                # Calculate carbon savings
                environmental_impact = calculate_carbon_savings(annual_energy_MWh)

                print_slow(f"\nA wind farm at {location_name} could save approximately:")
                print_slow(f"• {environmental_impact['co2_savings_tons']:.1f} tons of CO2 emissions per year")
                print_slow(f"• Equivalent to planting {environmental_impact['equivalent_trees']} trees annually")
                print_slow(f"• Or taking {environmental_impact['cars_equivalent']} cars off the road")
                print_slow(f"• The wind farm could power {environmental_impact['homes_powered']} homes")
                print_slow(f"• This represents {environmental_impact['percent_of_country']:.3f}% of Irish households")

                # Add environmental impact data to location data
                location_data['environmental_impact'] = environmental_impact

                # Add bonus points for conducting environmental analysis
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for conducting environmental analysis!")

            elif choice == 4:  # Economic feasibility
                print_slow("\nAnalyzing economic feasibility...")

                # Calculate economic factors
                econ_data = calculate_economic_factors(annual_energy_MWh, num_turbines=10, location_name=location_name)

                print_slow(f"\nEconomic analysis for a 10-turbine wind farm at {location_name}:")
                print_slow(f"• Annual revenue: €{econ_data['annual_revenue']:,.0f}")
                print_slow(f"• Installation cost: €{econ_data['installation_cost']:,.0f}")
                print_slow(f"• Grid connection: €{econ_data['grid_connection_cost']:,.0f}")
                print_slow(f"• Total cost: €{econ_data['total_cost']:,.0f}")
                print_slow(f"• Annual maintenance: €{econ_data['annual_maintenance']:,.0f}")
                print_slow(f"• Annual profit: €{econ_data['annual_profit']:,.0f}")
                print_slow(f"• Payback period: {econ_data['payback_period']:.1f} years")
                print_slow(f"• Jobs created: {econ_data['construction_jobs']} during construction, {econ_data['permanent_jobs']} permanent")

                # Add economic data to location data
                location_data['economic_data'] = econ_data

                # Add bonus points for conducting economic analysis
                bonus_points = 5
                player_score += bonus_points
                print_slow(f"\nYou earned {bonus_points} bonus points for conducting economic analysis!")

            # Add the location data to our analyzed locations
            analyzed_locations.append(location_data)

            # Generate basic analysis chart
            print_slow("\nGenerating power analysis chart...")
            chart_file = create_power_plot(
                months, wind_speeds, wind_power_kW,
                avg_wind_speed, avg_power, annual_energy_MWh,
                homes_powered, location_name
            )
            print_slow(f"Chart saved as: {chart_file}")

            # Update game variables
            locations_analyzed += 1

            # Update detective rank
            if player_score >= 80:
                detective_rank = "Master Wind Detective"
            elif player_score >= 50:
                detective_rank = "Senior Wind Detective"
            elif player_score >= 20:
                detective_rank = "Wind Detective"

            # Continue prompt
            print("\n" + "-"*60)
            input("Press Enter to continue to the next stage... ")

        except Exception as e:
            print(f"Oops! Something went wrong: {e}")
            print("Skipping to the next location...")
            time.sleep(3)

    # Wind farm design challenge after all locations are analyzed
    design_score = mini_game_design_challenge()
    player_score += design_score

    # Update detective rank one last time
    if player_score >= 80:
        detective_rank = "Master Wind Detective"
    elif player_score >= 50:
        detective_rank = "Senior Wind Detective"
    elif player_score >= 20:
        detective_rank = "Wind Detective"

    # Generate final report
    clear_screen()
    print("\n" + "="*60)
    print_slow("📋 FINAL REPORT PREPARATION 📋", 0.05)
    print("="*60)

    print_slow(f"\nCongratulations, {detective_rank} {student_name}!")
    print_slow(f"You've successfully analyzed {locations_analyzed} offshore locations")
    print_slow(f"and earned a total of {player_score} points!")

    print_slow("\nNow it's time to prepare your official report for the Minister of Energy.")
    print_slow("This report will summarize your findings and recommendations.")

    # Ask if they want to generate a report
    print_slow("\nWould you like to generate an official report? (yes/no)")

    generate_report = input("Generate report? ").lower() in ["y", "yes"]

    if generate_report:
        print_slow("\nGenerating your report...")
        report_file = generate_text_report(student_name, detective_rank, analyzed_locations, player_score)

        if report_file:
            print_slow(f"\nYour report has been generated: {report_file}")
            print_slow("You can open this text file to view your complete findings.")
        else:
            print_slow("\nCouldn't generate report file. Here's a summary instead:")
            generate_report = False

    # If report generation is skipped or failed, show a text summary
    if not generate_report:
        clear_screen()
        print("\n" + "="*60)
        print_slow("📊 WIND DETECTIVE FINAL REPORT 📊", 0.05)
        print("="*60)

        print_slow(f"Detective: {student_name}")
        print_slow(f"Rank: {detective_rank}")
        print_slow(f"Date: {datetime.now().strftime('%d %B %Y')}")
        print_slow(f"Final Score: {player_score} points")

        print_slow("\n" + "-"*60)
        print_slow("EXECUTIVE SUMMARY:")

        # Sort locations by average wind speed
        sorted_locations = sorted(analyzed_locations,
                                 key=lambda x: x['avg_wind_speed'],
                                 reverse=True)

        best_location = sorted_locations[0]['name']
        worst_location = sorted_locations[-1]['name']

        print_slow(f"\nAfter analyzing {len(analyzed_locations)} offshore locations around Ireland,")
        print_slow(f"we have determined that {best_location} offers the best potential for")
        print_slow(f"wind energy development with an average wind speed of {sorted_locations[0]['avg_wind_speed']:.1f} m/s")
        print_slow(f"and estimated annual energy production of {sorted_locations[0]['annual_energy_MWh']:.1f} MWh,")
        print_slow(f"enough to power {sorted_locations[0]['homes_powered']} homes.")

        print_slow("\n" + "-"*60)
        print_slow("LOCATION RANKINGS (by average wind speed):")

        for i, location in enumerate(sorted_locations):
            suitability = "SUITABLE" if location['is_suitable'] else "NOT SUITABLE"
            print_slow(f"{i+1}. {location['name']} - {location['avg_wind_speed']:.1f} m/s - {suitability}")

        print_slow("\n" + "-"*60)
        print_slow("RECOMMENDATIONS:")

        print_slow(f"\nBased on our analysis, we recommend developing wind farms at:")
        for i in range(min(3, len(sorted_locations))):
            if sorted_locations[i]['is_suitable']:
                print_slow(f"{i+1}. {sorted_locations[i]['name']}")

        print_slow("\nThese sites offer the best combination of strong and consistent")
        print_slow("wind resources, which would maximize renewable energy generation.")

    # Game finale
    print("\n" + "-"*60)
    print_slow("🌍 CONCLUSION:", 0.05)

    print_slow("\nThank you for your service as a Wind Detective!")
    print_slow("Your analysis will help Ireland develop clean, renewable energy")
    print_slow("and reduce our carbon emissions for generations to come.")

    print_slow("\nKey charts and visualizations have been saved for each location you analyzed.")
    print_slow("These include power analysis charts, seasonal analyses, and wind roses.")

    print("\n" + "="*60)
    print_slow("🌟 MISSION COMPLETE! 🌟", 0.05)
    print("="*60)

    input("\nPress Enter to exit... ")

# Run the game if this script is executed directly
if __name__ == "__main__":
    run_wind_detective_game()

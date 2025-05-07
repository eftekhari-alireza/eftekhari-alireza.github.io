# ==============================
# Ocean Defenders of Ireland 🌊🏝️🇮🇪
# Enhanced Interactive Educational Simulation
# ==============================
#  For 10-14 year olds

import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from matplotlib import cm
import sys
import random

# --------- COLOR CONSTANTS --------- #
IRELAND_GREEN = '#009A63'
OCEAN_BLUE = '#064273'
SAND_COLOR = '#FDCA40'
CLIFF_COLOR = '#7A542E'
TOWN_COLOR = '#FF6B6B'

# =====================
# HELPER FUNCTIONS
# =====================

def typewriter_effect(text, delay=0.03):
    """
    Creates a typewriter effect for text output - makes it appear
    character by character instead of all at once
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # New line at end

def ask_question(question, correct_answer, explanation):
    """
    Ask a science question and check the answer
    """
    typewriter_effect("\n📚 Quick question to test your knowledge:")
    typewriter_effect(question)
    student_answer = input("Your answer: ").strip().lower()

    correct_answer = str(correct_answer).lower()
    if student_answer == correct_answer:
        typewriter_effect("✅ That's correct! Well done!")
    else:
        typewriter_effect(f"That's not quite right. The answer is {correct_answer}.")

    typewriter_effect(explanation)
    print()

# =====================
# IMPROVED SIMULATION FUNCTIONS
# =====================

def simulate_ocean_waves(wave_height=1.0, wave_speed=1.0, grid_size=50):
    """
    More realistic ocean wave simulation with improved physics and visualization
    """
    # Educational information about ocean waves
    wave_info = [
        "🌊 Ocean waves are ripples of energy traveling through water.",
        "🌊 They're usually created by wind pushing on the water's surface.",
        "🌊 The stronger the wind, and the longer it blows, the bigger the waves!",
        "🌊 In Ireland, the west coast gets the biggest waves because of Atlantic storms.",
        "🌊 Wave height is measured from trough (lowest point) to crest (highest point).",
        "🌊 Scientists use special buoys to measure real waves in the ocean."
    ]

    for info in wave_info:
        typewriter_effect(info)
        time.sleep(0.5)

    # Ask a relevant question before simulation
    ask_question(
        "What causes most ocean waves? (wind/earthquakes/moon)",
        "wind",
        "Wind is the main cause of everyday ocean waves. The moon causes tides, and earthquakes can cause tsunami waves."
    )

    # More realistic wave parameters
    # Wave height is attenuated by depth
    # Add randomness to simulate natural variability
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    X, Y = np.meshgrid(x, y)

    # Create a depth profile (shallower near "shore")
    depth = np.ones((grid_size, grid_size)) * 50  # base depth in meters
    for i in range(grid_size):
        for j in range(grid_size):
            # Make it shallower toward one edge (shore)
            shore_distance = (grid_size - i) / grid_size
            depth[i, j] *= (0.2 + 0.8 * shore_distance)

    typewriter_effect("\nRunning ocean wave simulation...")
    print("This will show how waves change as they approach the shore.")

    # Wave simulation with frames
    for frame in range(10):
        plt.figure(figsize=(10, 7))
        ax = plt.subplot(111, projection='3d')

        frame_time = frame * 0.5 * wave_speed

        # Multiple wave components with different frequencies and directions
        # for more realistic appearance
        Z = np.zeros((grid_size, grid_size))

        # Main wave
        Z += wave_height * np.sin(0.5 * X + frame_time) * np.cos(0.5 * Y + frame_time)

        # Secondary waves with different frequencies and phases
        Z += wave_height * 0.3 * np.sin(0.8 * X + 1.2 * frame_time + 0.5)
        Z += wave_height * 0.2 * np.sin(0.3 * Y + 0.7 * frame_time + 1.3)

        # Add minor random fluctuations
        Z += np.random.normal(0, wave_height * 0.05, Z.shape)

        # Apply depth effects - waves get higher and steeper in shallow water
        for i in range(grid_size):
            for j in range(grid_size):
                # Wave height increases in shallow water (until breaking)
                depth_effect = np.sqrt(50 / max(depth[i, j], 5))
                Z[i, j] *= min(depth_effect, 2.0)  # Cap the amplification

                # Breaking waves (extreme steepening) when depth is very shallow
                if depth[i, j] < 5:
                    # Asymmetric wave shape when breaking
                    asymmetry = 0.3 * (5 - depth[i, j]) / 5
                    if Z[i, j] > 0:  # For crests
                        Z[i, j] *= (1 + asymmetry)

        # Plot with improved coloring and shading
        surf = ax.plot_surface(X, Y, Z, cmap='Blues',
                              rstride=1, cstride=1, alpha=0.8,
                              linewidth=0, antialiased=True)

        # Add the seafloor for context
        ax.plot_surface(X, Y, -depth/10, color='sandybrown', alpha=0.7,
                       rstride=3, cstride=3, shade=True)

        # Improved labels and title
        ax.set_xlabel('Distance (km)', fontsize=12)
        ax.set_ylabel('Distance (km)', fontsize=12)
        ax.set_zlabel('Height (m)', fontsize=12)
        ax.set_zlim(-5, wave_height*2)
        ax.set_title(f"Ocean Waves Simulation (Frame {frame+1}/10)\n"
                    f"Wave Height={wave_height:.1f}m, Wind Speed={wave_speed*10:.1f} km/h",
                    fontsize=13)

        # Add a "shore" indicator
        ax.text(10, 0, 0, "SHORE", color='brown', fontsize=14)

        plt.tight_layout()
        plt.show()

        # Short pause between frames
        time.sleep(0.5)

    typewriter_effect("\n✅ Simulation complete! Now you've seen how ocean waves move and change!")
    typewriter_effect("Did you notice how the waves grew taller as they approached the shore?")
    typewriter_effect("This happens because the energy gets compressed into a smaller water volume.")

def simulate_coastal_erosion(years=10, storm_intensity=0.5, sea_level_rise=0.2):
    """
    Improved coastal erosion simulation with more realistic geology and processes
    """
    # Educational information
    erosion_info = [
        "🏝️ Coastal erosion is when the sea gradually wears away the land.",
        "🏝️ Different types of rock erode at different rates - soft rocks like clay erode quickly.",
        "🏝️ Hard rocks like granite can resist erosion for thousands of years!",
        "🏝️ Storms dramatically speed up coastal erosion with powerful waves.",
        "🏝️ Rising sea levels due to climate change are making coastal erosion worse.",
        "🏝️ Ireland loses about 0.2-0.5 meters of coastline each year in many areas."
    ]

    for info in erosion_info:
        typewriter_effect(info)
        time.sleep(0.5)

    # Ask a question before simulation
    ask_question(
        "True or False: All types of rock erode at the same rate. (true/false)",
        "false",
        "Different rocks erode at different rates. Soft rocks like sandstone or clay erode much faster than hard rocks like granite."
    )

    typewriter_effect("\nStarting coastal erosion simulation...")
    typewriter_effect(f"We'll see how the coast changes over {years} years with storm intensity of {storm_intensity} and sea level rise of {sea_level_rise}m.")

    # Create a more realistic coastal profile with different rock types
    distance = np.linspace(0, 100, 100)  # horizontal distance in meters

    # Initial elevation profile - more realistic geology
    elevation = np.zeros_like(distance)

    # Seafloor/underwater (sloping)
    elevation[:30] = -5 + distance[:30]/6

    # Beach area
    elevation[30:40] = distance[30:40]/10

    # Mixed geology cliff face with varying hardness
    rock_hardness = np.ones(len(distance))

    # Add bands of different rock types (harder and softer)
    for i in range(40, len(distance)):
        # Base cliff profile
        if i < 50:
            elevation[i] = 2 + (i-40)*0.5  # Gentle slope up
        else:
            elevation[i] = 7 + (i-50)*0.4  # Steeper slope up

        # Create bands of different rock hardness
        if 45 <= i < 55:  # Soft rock band (e.g., clay)
            rock_hardness[i] = 0.4
        elif 65 <= i < 75:  # Hard rock band (e.g., granite)
            rock_hardness[i] = 2.5
        else:  # Medium hardness (e.g., sandstone)
            rock_hardness[i] = 1.0

    # Town on the cliff
    town_position = 80

    # Setup plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # Sea level will rise over time
    initial_sea_level = 0

    # Initial land + ocean visualization
    ax.fill_between(distance, -10, initial_sea_level, color=OCEAN_BLUE, alpha=0.6, label='Ocean')
    ax.fill_between(distance, elevation, where=(elevation>initial_sea_level),
                   y2=initial_sea_level, color=SAND_COLOR, alpha=0.7, label='Beach')
    ax.fill_between(distance, elevation, 30, where=(elevation>initial_sea_level),
                   color=CLIFF_COLOR, alpha=0.6, label='Cliff')

    # Town representation
    ax.scatter([town_position], [elevation[town_position]+1], s=120, marker='s',
              color=TOWN_COLOR, zorder=5, label='Town')

    # Create legend for rock types
    ax.plot([], [], color='darkred', linewidth=3, label='Soft Rock (Clay)')
    ax.plot([], [], color='sienna', linewidth=3, label='Medium Rock (Sandstone)')
    ax.plot([], [], color='darkgray', linewidth=3, label='Hard Rock (Granite)')

    # Visualize rock bands in the cliff
    for i in range(40, len(distance)):
        if rock_hardness[i] < 0.5:  # Soft rock
            ax.plot([i, i], [elevation[i], min(elevation[i]+2, 30)], color='darkred', linewidth=3, alpha=0.5)
        elif rock_hardness[i] > 2.0:  # Hard rock
            ax.plot([i, i], [elevation[i], min(elevation[i]+2, 30)], color='darkgray', linewidth=3, alpha=0.5)

    steps = min(5, years)
    step_years = np.linspace(0, years, steps+1)[1:]
    erosion_colors = cm.plasma(np.linspace(0.1, 0.9, steps))

    current_elev = elevation.copy()
    sea_level = initial_sea_level

    for idx, current_year in enumerate(step_years):
        # Update sea level based on cumulative rise
        sea_level = initial_sea_level + (sea_level_rise * current_year / years)

        # Calculate years elapsed in this step
        years_in_period = current_year if idx == 0 else step_years[idx] - step_years[idx-1]

        # Copy elevation for modification
        new_elevation = current_elev.copy()

        # Calculate erosion for each point
        for i in range(len(distance)):
            if current_elev[i] > sea_level:
                # Factors affecting erosion rate:

                # 1. Distance from the sea (exponential decay)
                distance_factor = np.exp(-0.07 * max(0, i - 30))

                # 2. Elevation relative to sea level (wave energy decreases with height)
                wave_reach = 5 + storm_intensity * 10  # How high waves can reach
                elev_above_sea = current_elev[i] - sea_level
                elevation_factor = max(0, 1 - elev_above_sea / wave_reach)

                # 3. Rock hardness (inverse relationship)
                hardness_factor = 1.0 / rock_hardness[i]

                # 4. Storm energy
                storm_factor = 0.2 + storm_intensity * 0.8

                # 5. Sea level rise effect (increases erosion near sea level)
                sea_level_factor = 1.0 + sea_level_rise * 2

                # Combined erosion rate (meters per year)
                base_erosion_rate = 0.2  # baseline rate in meters/year
                erosion = (base_erosion_rate * distance_factor * elevation_factor *
                          hardness_factor * storm_factor * sea_level_factor * years_in_period)

                # Apply erosion
                new_elevation[i] = max(sea_level - 0.5, current_elev[i] - erosion)

            # Underwater areas still experience some erosion
            elif current_elev[i] <= sea_level:
                underwater_erosion = 0.1 * storm_intensity * years_in_period
                new_elevation[i] = current_elev[i] - underwater_erosion

        # Apply slope stability - steep sections collapse
        for i in range(1, len(distance)-1):
            left_slope = abs(new_elevation[i] - new_elevation[i-1])
            right_slope = abs(new_elevation[i+1] - new_elevation[i])

            # If slope is too steep, material falls to create natural angle of repose
            if left_slope > 2.0 or right_slope > 2.0:
                # Simulate collapse to natural angle of repose
                new_elevation[i] = min(new_elevation[i],
                                     (new_elevation[i-1] + new_elevation[i+1])/2 + 1)

        # Plot the eroded profile
        ax.plot(distance, new_elevation, color=erosion_colors[idx],
               linewidth=2, label=f'After {int(current_year)} years')

        # Fill new ocean area
        if idx == steps-1:  # Only fill for the last stage
            ax.fill_between(distance, -10, sea_level, color=OCEAN_BLUE, alpha=0.6)

            # Show future sea level
            ax.axhline(y=sea_level, color='navy', linestyle='--',
                      label=f'Sea Level (+{sea_level_rise:.2f}m)')

        # Update for next iteration
        current_elev = new_elevation.copy()

    # Check if town is at risk (within 5m of cliff edge)
    final_cliff_edge = np.where(current_elev > sea_level)[0][0]
    town_at_risk = town_position - final_cliff_edge < 10

    if town_at_risk:
        ax.scatter([town_position], [elevation[town_position]+1], s=120, marker='s',
                  color='red', edgecolor='black', zorder=5)
        ax.text(town_position+2, elevation[town_position]+2, "TOWN AT RISK!", color='red',
              fontsize=12, fontweight='bold')

    # Improve chart appearance
    ax.set_xlabel('Distance from Sea (m)', fontsize=12)
    ax.set_ylabel('Height (m)', fontsize=12)
    ax.set_ylim(-6, 30)
    ax.set_title(f"Coastal Erosion Simulation over {years} years\n" +
                f"Storm Intensity={storm_intensity:.1f}, Sea Level Rise={sea_level_rise:.2f}m",
                fontsize=14)
    ax.legend(loc='upper left')

    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    if town_at_risk:
        typewriter_effect("\n⚠️ Warning! The town is at risk from coastal erosion!")
        typewriter_effect("The cliff edge has moved dangerously close to the town.")
    else:
        typewriter_effect("\n✅ The town appears safe for now, but continued erosion could threaten it in the future.")

    typewriter_effect("\nThis simulation shows how coastal erosion happens faster:")
    typewriter_effect("1. Where rocks are softer (the red clay layers)")
    typewriter_effect("2. During storms with powerful waves")
    typewriter_effect("3. As sea levels rise due to climate change")
    typewriter_effect("\nThis is why coastal protection and planning is so important in Ireland!")

def storm_protection_game(barrier_height=2.0, barrier_width=10, storm_strength=5):
    """
    Improved storm surge protection scenario with realistic physics
    """
    # Educational information
    protection_info = [
        "🌪️ Storm surges happen when strong winds push extra water toward land during storms.",
        "🌪️ They can raise water levels by several meters above normal high tide.",
        "🌪️ This causes flooding that can damage coastal towns and habitats.",
        "🌪️ Ireland has experienced severe storm surges, especially on the Atlantic coast.",
        "🌪️ Engineers build sea walls, barriers and sand dunes to protect coastal areas.",
        "🌪️ Natural defenses like salt marshes and mangroves also help absorb wave energy."
    ]

    for info in protection_info:
        typewriter_effect(info)
        time.sleep(0.5)

    # Ask a question before simulation
    ask_question(
        "What causes a storm surge? (earthquakes/strong winds/high temperatures)",
        "strong winds",
        "Strong winds during storms push water toward the shore, creating a storm surge that raises water levels and can cause severe coastal flooding."
    )

    typewriter_effect("\nStarting storm protection simulation...")
    typewriter_effect(f"We'll test a barrier of height {barrier_height}m and width {barrier_width}m against a level {storm_strength} storm.")

    # Create a more realistic coastal profile
    distance = np.linspace(0, 200, 200)  # in meters

    # More realistic topography
    elevation = np.zeros_like(distance)

    # Beach slope
    elevation[20:50] = np.linspace(0, 1, 30)

    # Flat area
    elevation[50:] = 1

    # Add some small natural variations
    for i in range(len(elevation)):
        if i > 20:  # Only add variations above water
            elevation[i] += np.random.normal(0, 0.1)

    # Smooth the profile
    from scipy.ndimage import gaussian_filter
    elevation = gaussian_filter(elevation, sigma=2)

    # Add town at higher elevation
    town_start = 120
    town_end = 150
    elevation[town_start:town_end] = 1.5  # Town on slightly higher ground

    # Calculate barrier position (further from water than original)
    barrier_pos = 70

    # Add the barrier to the elevation profile
    original_elev = elevation.copy()
    elevation[barrier_pos:barrier_pos+barrier_width] = max(elevation[barrier_pos], barrier_height)

    # Realistic storm surge calculation
    max_surge_height = 7.0  # maximum possible in extreme storms (meters)

    # Base surge height on storm strength (1-10 scale)
    base_surge = (storm_strength / 10) * max_surge_height

    # Add high tide component
    tide_level = 1.0  # meters above mean sea level

    # Calculate the total surge including tide
    total_surge_height = base_surge + tide_level

    # Create realistic surge profile
    surge_x = np.linspace(0, 200, 200)
    surge_y = np.zeros_like(surge_x)

    # Shore distance factor
    for i in range(len(surge_x)):
        # Surge decreases with distance from shore, with some inland penetration
        if surge_x[i] <= 20:  # Open water
            surge_y[i] = total_surge_height
        else:  # Inland attenuation
            # Calculate how far inland
            inland_distance = surge_x[i] - 20

            # Barrier effect - significant reduction after barrier
            if barrier_pos <= surge_x[i]:
                barrier_effect = max(0, 1 - (elevation[barrier_pos] / total_surge_height))
                barrier_distance = surge_x[i] - barrier_pos
                attenuation = np.exp(-0.03 * inland_distance) * barrier_effect * np.exp(-0.05 * barrier_distance)
            else:
                # Before barrier
                attenuation = np.exp(-0.015 * inland_distance)

            # Topography effect - water can't go uphill easily
            for j in range(20, int(surge_x[i])):
                if elevation[j] > total_surge_height:
                    attenuation *= 0.5  # Significant reduction if high ground in path

            surge_y[i] = total_surge_height * attenuation

    # Create the visualization
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot land with green for vegetation
    ax.fill_between(distance, -1, original_elev, color=SAND_COLOR, alpha=0.7, label='Beach')
    ax.fill_between(distance, original_elev, 10, color=IRELAND_GREEN, alpha=0.3, label='Land')

    # Plot water and surge
    ax.fill_between(distance, -1, 0, color=OCEAN_BLUE, alpha=0.6, label='Normal Sea Level')

    # Plot storm surge
    ax.plot(surge_x, surge_y, color='navy', linewidth=2, label=f'Storm Surge ({total_surge_height:.1f}m)')
    ax.fill_between(surge_x, 0, surge_y, color=OCEAN_BLUE, alpha=0.4)

    # Plot barrier
    barrier_color = 'gray'
    ax.fill_between(
        distance[barrier_pos:barrier_pos+barrier_width],
        original_elev[barrier_pos:barrier_pos+barrier_width],
        elevation[barrier_pos:barrier_pos+barrier_width],
        color=barrier_color, alpha=0.8, label='Protection Barrier'
    )

    # Plot town with houses
    for house_pos in range(town_start, town_end, 5):
        # House body
        house_height = 3
        ax.fill_between(
            [house_pos-2, house_pos+2],
            [elevation[house_pos], elevation[house_pos]],
            [elevation[house_pos]+house_height, elevation[house_pos]+house_height],
            color=TOWN_COLOR, alpha=0.7
        )
        # Roof
        ax.plot(
            [house_pos-2.5, house_pos, house_pos+2.5],
            [elevation[house_pos]+house_height, elevation[house_pos]+house_height+1.5, elevation[house_pos]+house_height],
            color='darkred', linewidth=2
        )

    # Add Town label
    ax.text(town_start+5, elevation[town_start]+5, "TOWN", fontsize=14, fontweight='bold')

    # Evaluate flooding
    town_flooded = False
    flood_depth = 0
    for i in range(town_start, town_end):
        if surge_y[i] > elevation[i]:
            town_flooded = True
            flood_depth = max(flood_depth, surge_y[i] - elevation[i])

    # Check if barrier was overtopped (important for consistency in feedback)
    barrier_overtopped = False
    for i in range(barrier_pos, barrier_pos+barrier_width):
        if surge_y[i] > elevation[i]:
            barrier_overtopped = True
            break

    # Show if town is flooded
    if town_flooded:
        ax.text(town_start+15, elevation[town_start]+4, f"FLOODED!\nDepth: {flood_depth:.2f}m",
               color='red', fontsize=14, fontweight='bold')

    # Barrier effectiveness score
    if town_flooded:
        protection_score = max(0, 50 - 20 * flood_depth)
        efficiency_score = 0  # Not efficient if town flooded
    else:
        safety_margin = min([elevation[i] - surge_y[i] for i in range(town_start, town_end)])
        efficiency_score = 50 * (1 - min(safety_margin, barrier_height/2) / (barrier_height/2))
        protection_score = 50 + efficiency_score

    total_score = int(protection_score)

    # Improve chart appearance
    ax.set_title(f"Storm Surge Protection Simulation\n" +
                f"Barrier: H={barrier_height}m, W={barrier_width}m | Storm Level: {storm_strength}/10",
                fontsize=14)
    ax.set_xlabel('Distance from Sea (m)', fontsize=12)
    ax.set_ylabel('Height (m)', fontsize=12)
    ax.set_ylim(-1, 10)
    ax.grid(alpha=0.3)
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

    if town_flooded:
        typewriter_effect("\n❌ Oh no! The storm surge flooded the town!")
        typewriter_effect(f"The flood water reached {flood_depth:.2f}m deep in the town.")
        typewriter_effect("This would cause serious damage to buildings and infrastructure.")
    else:
        if barrier_overtopped:
            typewriter_effect("\n⚠️ The barrier was overtopped by the surge, but the town was saved!")
            typewriter_effect("This was lucky - the water lost enough energy crossing the land between")
            typewriter_effect("the barrier and town, but this isn't reliable protection.")
        else:
            typewriter_effect("\n✅ Great job! Your barrier successfully blocked the storm surge!")

    typewriter_effect(f"\nYour protection score is: {total_score}/100.")

    typewriter_effect("\nThings to consider for better protection:")

    if barrier_height < total_surge_height:
        typewriter_effect("- Your barrier wasn't tall enough for the surge height")
        if not town_flooded:
            typewriter_effect("  (The town was saved by distance/elevation, not your barrier)")

    if barrier_width < 15:
        typewriter_effect("- A wider barrier provides better protection")

    if barrier_pos > 60:
        typewriter_effect("- Placing the barrier closer to the water can help")

    typewriter_effect("\nEngineers must carefully design coastal defenses to protect communities from storms!")

# ===========================
# "MAIN GAME" FLOW
# ===========================
def run_ocean_defenders_game():
    """
    Main game flow with enhanced educational content
    """
    typewriter_effect("="*60)
    typewriter_effect("🦀 OCEAN DEFENDERS OF IRELAND 🌊🏝️ - Interactive Science Simulation")
    typewriter_effect("="*60)

    intro_text = [
        "Welcome to Ocean Defenders of Ireland!",
        "",
        "In this program, you'll learn about how the ocean shapes Ireland's coastlines.",
        "You'll explore waves, coastal erosion, and protection against storms.",
        "",
        "Ireland has over 3,000 kilometers of coastline, with beautiful beaches,",
        "dramatic cliffs, and coastal towns that need protection.",
        "",
        "As climate change leads to rising sea levels and stronger storms,",
        "understanding how to protect our coasts is more important than ever!",
        "",
        "Get ready to become a coastal defender! Let's dive in..."
    ]

    for line in intro_text:
        typewriter_effect(line)
        time.sleep(0.2)

    while True:
        print("\n" + "="*40)
        typewriter_effect("Which coastal science scenario would you like to explore?")
        print("1) 🌊 Ocean Waves Simulation")
        print("2) 🏝️ Coastal Erosion Model")
        print("3) 🌪️ Storm Protection Challenge")
        print("4) 📚 Learn About Irish Coasts")
        print("5) 👋 Exit the Program")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            # Wave simulation setup
            print("\n" + "-"*40)
            typewriter_effect("🌊 OCEAN WAVES SIMULATION 🌊")
            typewriter_effect("Wave height varies from small ripples (0.5m) to large storm waves (3m+).")
            typewriter_effect("Let's customize your wave simulation:")

            try:
                height = float(input("\nWave height in meters (0.5-5.0)? "))
                height = min(max(height, 0.5), 5.0)  # Limit to reasonable range

                speed = float(input("Wind speed factor (0.5-2.0)? "))
                speed = min(max(speed, 0.5), 2.0)  # Limit to reasonable range

                grid_size = int(input("Grid resolution (30-80)? "))
                grid_size = min(max(grid_size, 30), 80)  # Limit to reasonable range
            except:
                print("Invalid input, using default values.")
                height, speed, grid_size = 1.5, 1.0, 50

            simulate_ocean_waves(wave_height=height, wave_speed=speed, grid_size=grid_size)

        elif choice == '2':
            # Coastal erosion simulation setup
            print("\n" + "-"*40)
            typewriter_effect("🏝️ COASTAL EROSION SIMULATION 🏝️")
            typewriter_effect("Coastal erosion happens over many years, shaped by waves, storms, and rising seas.")
            typewriter_effect("Let's customize your erosion simulation:")

            try:
                yrs = int(input("\nHow many years to simulate (5-100)? "))
                yrs = min(max(yrs, 5), 100)  # Limit to reasonable range

                storm = float(input("Storm intensity (0.1-1.0)? "))
                storm = min(max(storm, 0.1), 1.0)  # Limit to reasonable range

                rise = float(input("Sea level rise in meters (0.0-1.0)? "))
                rise = min(max(rise, 0.0), 1.0)  # Limit to reasonable range
            except:
                print("Invalid input, using default values.")
                yrs, storm, rise = 20, 0.5, 0.2

            simulate_coastal_erosion(years=yrs, storm_intensity=storm, sea_level_rise=rise)

        elif choice == '3':
            # Storm protection scenario setup
            print("\n" + "-"*40)
            typewriter_effect("🌪️ STORM PROTECTION CHALLENGE 🌪️")
            typewriter_effect("Can you protect the coastal town from a storm surge?")
            typewriter_effect("Let's design your coastal defense barrier:")

            try:
                bh = float(input("\nBarrier height in meters (1.0-6.0)? "))
                bh = min(max(bh, 1.0), 6.0)  # Limit to reasonable range

                bw = int(input("Barrier width in meters (5-30)? "))
                bw = min(max(bw, 5), 30)  # Limit to reasonable range

                st = int(input("Storm strength (1-10)? "))
                st = min(max(st, 1), 10)  # Limit to reasonable range
            except:
                print("Invalid input, using default values.")
                bh, bw, st = 3.0, 15, 6

            storm_protection_game(barrier_height=bh, barrier_width=bw, storm_strength=st)

        elif choice == '4':
            # Educational facts about Irish coasts
            print("\n" + "-"*40)
            typewriter_effect("📚 IRISH COASTAL FACTS 📚")

            ireland_facts = [
                "🇮🇪 Ireland's coastline stretches over 3,000 kilometers.",
                "🇮🇪 The tallest sea cliffs in Ireland are the Slieve League cliffs in Donegal, rising 601 meters!",
                "🇮🇪 The famous Cliffs of Moher receive over 1.5 million visitors each year.",
                "🇮🇪 The Wild Atlantic Way is one of the world's longest coastal driving routes at 2,500 km.",
                "🇮🇪 Ireland has over 80 Blue Flag beaches, recognized for their cleanliness and water quality.",
                "🇮🇪 Lahinch Beach in County Clare is one of Europe's top surfing destinations.",
                "🇮🇪 The Giant's Causeway in Northern Ireland has about 40,000 hexagonal basalt columns.",
                "🇮🇪 The highest tides in Ireland can reach over 5 meters in height.",
                "🇮🇪 Ireland's coastal waters are home to whales, dolphins, seals, and basking sharks.",
                "🇮🇪 Some coastal areas in Ireland are eroding by up to 1.5 meters per year."
            ]

            random.shuffle(ireland_facts)
            print()
            for i, fact in enumerate(ireland_facts[:5]):
                typewriter_effect(fact)
                time.sleep(1)

            # Ask a related question
            print()
            irish_questions = [
                ("How long is Ireland's coastline? (1,000 km/3,000 km/5,000 km)", "3,000 km",
                 "Ireland's coastline stretches over 3,000 kilometers, creating a diverse landscape of beaches, cliffs, and bays."),
                ("Which famous cliffs in County Clare attract 1.5 million visitors yearly?", "Cliffs of Moher",
                 "The Cliffs of Moher in County Clare rise up to 214 meters and are one of Ireland's most visited natural attractions."),
                ("What is the Wild Atlantic Way?", "coastal driving route",
                 "The Wild Atlantic Way is a 2,500 km coastal driving route along Ireland's western seaboard, showcasing breathtaking views and coastal communities.")
            ]

            random_q = random.choice(irish_questions)
            ask_question(random_q[0], random_q[1], random_q[2])

            print("\nPress Enter to return to the main menu...")
            input()

        elif choice == '5':
            # Exit the program
            typewriter_effect("\nThank you for exploring Ocean Defenders of Ireland!")
            typewriter_effect("Remember, understanding our coasts helps us protect them for the future.")
            typewriter_effect("Slán go fóill! (Goodbye for now in Irish)")
            break

        else:
            print("Invalid choice. Please try again.\n")

# ===========================
# Run the enhanced game
# ===========================
if __name__ == "__main__":
    run_ocean_defenders_game()

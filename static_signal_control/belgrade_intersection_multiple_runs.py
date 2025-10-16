import os
import sys
import traci
import xml.etree.ElementTree as ET
import numpy as np
import time
import csv  

# --- SUMO setup ---
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# --- File paths ---
sumo_cfg_file = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\belgrade_intersection.sumocfg"
statistics_file = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\statistics.xml"
csv_output = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\results.csv"  # ✅ results file

# --- Base SUMO config ---
base_config = [
    "sumo",
    "-c", sumo_cfg_file,
    "--step-length", "0.33",
    "--duration-log.statistics", "true",
    "--statistic-output", statistics_file,
    "--random"  # ensures different seeds per run
]

# --- Run one simulation ---
def run_sumo(run_id):
    print(f"\n=== Starting simulation {run_id} ===")

    # Run SUMO
    traci.start(base_config)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
    traci.close()

    time.sleep(1)

    if not os.path.exists(statistics_file):
        print("❌ No statistics file found.")
        return np.nan, np.nan

    # Parse XML statistics
    tree = ET.parse(statistics_file)
    root = tree.getroot()

    veh_loss = np.nan
    ped_loss = np.nan

    v_stats = root.find("vehicleTripStatistics")
    if v_stats is not None:
        veh_loss = float(v_stats.get("timeLoss", "nan"))

    p_stats = root.find("pedestrianStatistics")
    if p_stats is not None:
        ped_loss = float(p_stats.get("timeLoss", "nan"))

    print(f"→ Vehicle timeLoss: {veh_loss:.2f}")
    print(f"→ Pedestrian timeLoss: {ped_loss:.2f}")
    return veh_loss, ped_loss


# --- Run multiple simulations ---
num_runs = 50
veh_losses = []
ped_losses = []

# Create CSV and write header
with open(csv_output, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["simulation_no", "vehicle_time_loss", "pedestrian_time_loss"])  # ✅ header

    for i in range(num_runs):
        veh_loss, ped_loss = run_sumo(i)
        veh_losses.append(veh_loss)
        ped_losses.append(ped_loss)

        # Write each result immediately
        writer.writerow([i + 1, veh_loss, ped_loss])

# --- Final summary ---
print("\n=== Summary over all runs ===")
print(f"Vehicle timeLoss: mean = {np.nanmean(veh_losses):.2f}, std = {np.nanstd(veh_losses):.2f}")
print(f"Pedestrian timeLoss: mean = {np.nanmean(ped_losses):.2f}, std = {np.nanstd(ped_losses):.2f}")

print(f"\n✅ Results saved to: {csv_output}")
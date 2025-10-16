import os
import sys
import numpy as np

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

import traci
import xml.etree.ElementTree as ET

sumo_cfg_file = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\belgrade_intersection.sumocfg"
tripinfo_file = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\tripinfo.xml"
statistics_file = r"C:\NIKOLA\SUMO\belgrade\static_signal_control\statistics.xml"

Sumo_config = [
    'sumo-gui',
    '-c', sumo_cfg_file,
    '--step-length', '0.05',
    '--delay', '1000',
    '--lateral-resolution', '0.1',
    '--tripinfo-output', tripinfo_file,
    "--duration-log.statistics", "true",      
    "--statistic-output", "C:/NIKOLA/SUMO/belgrade/static_signal_control/statistics.xml"
]

traci.start(Sumo_config)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

traci.close()

if os.path.exists(statistics_file):
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

else:
    print("statistics.xml not found — simulation may not have produced any trips.")
"""
Dam Reservoir Telemetry & Travel Lead-Time Engine
Part of Trinetra AI (PRAVAH) - Dam Intelligence System

Handles hydrological state tracking, structural health metadata, and flood-wave lead-time propagation.
Target Dams: Tehri Dam, Tapovan Vishnugad, Maneri Bhali (Uttarakhand), Ranganadi, Subansiri Lower, Kurichhu (Assam/Bhutan).
"""

import math
from typing import Dict, List, Any

class DamMonitoringEngine:
    def __init__(self):
        # Database of target 6 dams across Uttarakhand and Assam/Bhutan
        self.dams_db: Dict[str, Dict[str, Any]] = {
            "DAM_TEHRI": {
                "id": "DAM_TEHRI",
                "name": "Tehri Dam",
                "river": "Bhagirathi",
                "state": "Uttarakhand",
                "district": "Tehri Garhwal",
                "downstream_city": "Rishikesh & Haridwar",
                "full_reservoir_level_m": 830.0,
                "current_level_m": 829.08,
                "storage_capacity_mcm": 3540.0,
                "live_capacity_bcm": 2.615,
                "current_live_storage_bcm": 2.483,
                "current_storage_pct": 94.94,
                "inflow_cusecs": 28500.0,
                "outflow_cusecs": 22000.0,
                "spillway_gates_total": 8,
                "spillway_gates_open": 3,
                "hydel_mw": 1000.0,
                "cwc_bulletin_date": "24.09.2026",
                "structural_health": {
                    "crack_width_mm": 1.2,
                    "seepage_rate_lps": 4.5,
                    "vibration_hz": 0.08,
                    "structural_status": "NORMAL"
                },
                "wave_reach_distance_km": 85.0
            },
            "DAM_TAPOVAN": {
                "id": "DAM_TAPOVAN",
                "name": "Tapovan Vishnugad Hydroelectric Project",
                "river": "Dhauliganga",
                "state": "Uttarakhand",
                "district": "Chamoli",
                "downstream_city": "Joshimath & Chamoli",
                "full_reservoir_level_m": 1800.0,
                "current_level_m": 1792.0,
                "storage_capacity_mcm": 45.0,
                "current_storage_pct": 88.0,
                "inflow_cusecs": 14200.0,
                "outflow_cusecs": 13800.0,
                "spillway_gates_total": 4,
                "spillway_gates_open": 2,
                "structural_health": {
                    "crack_width_mm": 2.8,
                    "seepage_rate_lps": 8.2,
                    "vibration_hz": 0.15,
                    "structural_status": "WATCH"
                },
                "wave_reach_distance_km": 32.0
            },
            "DAM_MANERI": {
                "id": "DAM_MANERI",
                "name": "Maneri Bhali Stage I & II",
                "river": "Bhagirathi",
                "state": "Uttarakhand",
                "district": "Uttarkashi",
                "downstream_city": "Uttarkashi Town",
                "full_reservoir_level_m": 1288.0,
                "current_level_m": 1282.4,
                "storage_capacity_mcm": 68.0,
                "current_storage_pct": 79.5,
                "inflow_cusecs": 18900.0,
                "outflow_cusecs": 17500.0,
                "spillway_gates_total": 6,
                "spillway_gates_open": 2,
                "structural_health": {
                    "crack_width_mm": 0.9,
                    "seepage_rate_lps": 3.1,
                    "vibration_hz": 0.05,
                    "structural_status": "NORMAL"
                },
                "wave_reach_distance_km": 24.0
            },
            "DAM_RANGANADI": {
                "id": "DAM_RANGANADI",
                "name": "Ranganadi Hydroelectric Project",
                "river": "Ranganadi",
                "state": "Arunachal / Assam Upstream",
                "district": "Lakhimpur Boundary",
                "downstream_city": "Lakhimpur Town",
                "full_reservoir_level_m": 565.0,
                "current_level_m": 561.2,
                "storage_capacity_mcm": 210.0,
                "current_storage_pct": 89.2,
                "inflow_cusecs": 34000.0,
                "outflow_cusecs": 31500.0,
                "spillway_gates_total": 5,
                "spillway_gates_open": 4,
                "structural_health": {
                    "crack_width_mm": 3.4,
                    "seepage_rate_lps": 12.8,
                    "vibration_hz": 0.22,
                    "structural_status": "WARNING"
                },
                "wave_reach_distance_km": 54.0
            },
            "DAM_SUBANSIRI": {
                "id": "DAM_SUBANSIRI",
                "name": "Subansiri Lower Hydroelectric Project",
                "river": "Subansiri",
                "state": "Assam / Arunachal Border",
                "district": "Dhemaji & Lakhimpur",
                "downstream_city": "Dhemaji & Majuli",
                "full_reservoir_level_m": 205.0,
                "current_level_m": 198.6,
                "storage_capacity_mcm": 1365.0,
                "current_storage_pct": 74.0,
                "inflow_cusecs": 42000.0,
                "outflow_cusecs": 38000.0,
                "spillway_gates_total": 9,
                "spillway_gates_open": 4,
                "structural_health": {
                    "crack_width_mm": 1.6,
                    "seepage_rate_lps": 5.4,
                    "vibration_hz": 0.09,
                    "structural_status": "NORMAL"
                },
                "wave_reach_distance_km": 62.0
            },
            "DAM_KURICHHU": {
                "id": "DAM_KURICHHU",
                "name": "Kurichhu Dam",
                "river": "Kurichhu / Manas System",
                "state": "Bhutan (Assam Downstream Impact)",
                "district": "Mongar / Barpeta Impact",
                "downstream_city": "Barpeta & Baksa (Assam)",
                "full_reservoir_level_m": 540.0,
                "current_level_m": 536.0,
                "storage_capacity_mcm": 140.0,
                "current_storage_pct": 81.0,
                "inflow_cusecs": 21000.0,
                "outflow_cusecs": 19500.0,
                "spillway_gates_total": 5,
                "spillway_gates_open": 3,
                "structural_health": {
                    "crack_width_mm": 1.1,
                    "seepage_rate_lps": 4.0,
                    "vibration_hz": 0.07,
                    "structural_status": "NORMAL"
                },
                "wave_reach_distance_km": 92.0
            }
        }

    def calculate_lead_time_propagation(self, dam_id: str, outflow_cusecs: float) -> Dict[str, Any]:
        """
        Computes reach-wise wave travel speed and lead-time window based on outflow discharge (Cusecs).
        Higher outflow discharge increases wave velocity (Manning's equation proxy for flood wave celerity).
        """
        dam = self.dams_db.get(dam_id, self.dams_db["DAM_TEHRI"])
        distance_km = dam.get("wave_reach_distance_km", 60.0)

        # Baseline wave speed in km/h (typically 12 - 25 km/h for steep mountain rivers)
        # Scaled by logarithmic surge factor of outflow discharge
        cusec_ratio = max(0.5, outflow_cusecs / 20000.0)
        estimated_wave_speed_kmh = 14.0 * math.pow(cusec_ratio, 0.35)
        estimated_wave_speed_kmh = max(8.0, min(38.0, estimated_wave_speed_kmh))

        min_hours = round(distance_km / (estimated_wave_speed_kmh * 1.25), 1)
        max_hours = round(distance_km / (estimated_wave_speed_kmh * 0.85), 1)
        avg_hours = round((min_hours + max_hours) / 2.0, 1)

        # Escalation severity score
        risk_score_pct = min(98.0, round((outflow_cusecs / 45000.0) * 85.0 + (dam["current_storage_pct"] - 70.0) * 0.4, 1))
        risk_score_pct = max(10.0, risk_score_pct)

        return {
            "dam_id": dam_id,
            "dam_name": dam["name"],
            "downstream_city": dam["downstream_city"],
            "distance_km": distance_km,
            "outflow_cusecs": outflow_cusecs,
            "wave_speed_kmh": round(estimated_wave_speed_kmh, 1),
            "lead_time_window": f"{min_hours} to {max_hours} hours",
            "lead_time_min_hrs": min_hours,
            "lead_time_max_hrs": max_hours,
            "lead_time_avg_hrs": avg_hours,
            "risk_score_pct": risk_score_pct,
            "alert_level": "RED EMERGENCY" if risk_score_pct >= 80 else ("ORANGE WARNING" if risk_score_pct >= 55 else "GREEN NORMAL")
        }

    def get_dam_sensor_grid(self, dam_id: str) -> Dict[str, Any]:
        """
        Generates 5x8 Distributed Sensing Grid Matrix representing 5 Dam Gallery Levels x 8 Concrete Monolith Blocks.
        Each node tracks micro-strain (με), crack opening (mm), seepage (L/s), and operational safety grade.
        """
        dam = self.dams_db.get(dam_id, self.dams_db["DAM_TEHRI"])
        rows = 5  # Crest, Upper Gallery, Mid Wall, Lower Gallery, Base Toe
        cols = 8  # Monolith Blocks 1 to 8
        level_names = ["Crest Deck (El. +830m)", "Upper Gallery (El. +780m)", "Mid Monolith Wall (El. +720m)", "Lower Drainage Gallery (El. +650m)", "Base Foundation Toe (El. +580m)"]
        
        # Determine specific fracture anchor coordinates per dam
        critical_nodes = {}
        if dam_id == "DAM_TEHRI":
            critical_nodes = {(1, 5): {"status": "WATCH", "crack_mm": 1.2, "strain": 420, "seepage": 2.1, "name": "Spillway Pier Monolith #6"}}
        elif dam_id == "DAM_TAPOVAN":
            critical_nodes = {
                (2, 3): {"status": "CRITICAL", "crack_mm": 2.8, "strain": 840, "seepage": 6.8, "name": "Head Race Intake Block #4"},
                (3, 2): {"status": "WATCH", "crack_mm": 1.6, "strain": 510, "seepage": 3.4, "name": "Drainage Gallery Block #3"}
            }
        elif dam_id == "DAM_RANGANADI":
            critical_nodes = {
                (1, 4): {"status": "CRITICAL", "crack_mm": 3.4, "strain": 960, "seepage": 9.5, "name": "Spillway Gate #4 Chute Wall"},
                (2, 4): {"status": "WATCH", "crack_mm": 1.9, "strain": 530, "seepage": 4.1, "name": "Energy Dissipator Block #5"}
            }
        elif dam_id == "DAM_SUBANSIRI":
            critical_nodes = {(3, 4): {"status": "WATCH", "crack_mm": 1.6, "strain": 460, "seepage": 2.8, "name": "Diversion Tunnel Plug Block #5"}}
        elif dam_id == "DAM_MANERI":
            critical_nodes = {(2, 2): {"status": "NORMAL", "crack_mm": 0.9, "strain": 280, "seepage": 1.2, "name": "Desilting Chamber Block #3"}}
        elif dam_id == "DAM_KURICHHU":
            critical_nodes = {(1, 3): {"status": "WATCH", "crack_mm": 1.1, "strain": 360, "seepage": 1.9, "name": "Right Abutment Monolith #4"}}

        grid_matrix = []
        total_nodes = rows * cols
        alert_count = 0

        for r in range(rows):
            row_nodes = []
            for c in range(cols):
                coord = (r, c)
                node_id = f"NODE_R{r+1}_C{c+1}"
                if coord in critical_nodes:
                    spec = critical_nodes[coord]
                    status = spec["status"]
                    crack_mm = spec["crack_mm"]
                    strain = spec["strain"]
                    seepage = spec["seepage"]
                    block_name = spec["name"]
                    if status != "NORMAL":
                        alert_count += 1
                else:
                    status = "NORMAL"
                    crack_mm = 0.0
                    strain = round(120.0 + (r * 15.0) + (c * 8.0), 1)
                    seepage = round(0.1 + (r * 0.08), 2)
                    block_name = f"Monolith Block #{c+1} ({level_names[r].split('(')[0].strip()})"

                row_nodes.append({
                    "node_id": node_id,
                    "row": r,
                    "col": c,
                    "level_name": level_names[r],
                    "block_name": block_name,
                    "status": status,
                    "crack_displacement_mm": crack_mm,
                    "strain_microstrain": strain,
                    "seepage_lps": seepage,
                    "is_active_alert": status != "NORMAL"
                })
            grid_matrix.append(row_nodes)

        return {
            "dam_id": dam_id,
            "rows": rows,
            "cols": cols,
            "total_nodes": total_nodes,
            "alert_nodes_count": alert_count,
            "overall_grid_status": "CRITICAL WARNING" if any(spec["status"] == "CRITICAL" for spec in critical_nodes.values()) else ("WATCH" if alert_count > 0 else "NORMAL"),
            "grid": grid_matrix
        }

    def get_all_dams_status(self) -> List[Dict[str, Any]]:
        """Returns hydrological, structural status, and 2D sensor grid for all 6 target dams."""
        results = []
        for dam_id, dam in self.dams_db.items():
            lead_info = self.calculate_lead_time_propagation(dam_id, dam["outflow_cusecs"])
            grid_info = self.get_dam_sensor_grid(dam_id)
            dam_data = dict(dam)
            dam_data["lead_time"] = lead_info
            dam_data["sensor_grid"] = grid_info
            results.append(dam_data)
        return results

    def simulate_scenario(self, dam_id: str, outflow_cusecs: float, gates_open: int, downstream_stage_m: float) -> Dict[str, Any]:
        """
        Accepts scenario sliders input and computes updated flood risk & lead-time propagation window.
        """
        dam = self.dams_db.get(dam_id, self.dams_db["DAM_TEHRI"])
        lead_info = self.calculate_lead_time_propagation(dam_id, outflow_cusecs)
        
        # Combined risk calculation formula
        base_risk = (outflow_cusecs / 50000.0) * 60.0
        stage_risk = (downstream_stage_m / 10.0) * 25.0
        gate_factor = (gates_open / max(1, dam["spillway_gates_total"])) * 15.0
        combined_risk_pct = min(99.0, max(5.0, round(base_risk + stage_risk + gate_factor, 1)))

        return {
            "dam_id": dam_id,
            "dam_name": dam["name"],
            "simulated_outflow_cusecs": outflow_cusecs,
            "simulated_gates_open": gates_open,
            "spillway_gates_total": dam["spillway_gates_total"],
            "downstream_stage_m": downstream_stage_m,
            "combined_risk_pct": combined_risk_pct,
            "lead_time_window": lead_info["lead_time_window"],
            "lead_time_min_hrs": lead_info["lead_time_min_hrs"],
            "lead_time_max_hrs": lead_info["lead_time_max_hrs"],
            "wave_speed_kmh": lead_info["wave_speed_kmh"],
            "downstream_city": dam["downstream_city"],
            "evacuation_recommended": combined_risk_pct >= 75.0
        }

if __name__ == "__main__":
    engine = DamMonitoringEngine()
    print("=== Dam Telemetry Engine Unit Test ===")
    status = engine.get_all_dams_status()
    print(f"Loaded {len(status)} dams successfully.")
    for d in status:
        print(f"[{d['id']}] {d['name']} -> Outflow: {d['outflow_cusecs']} Cusecs | Lead Time: {d['lead_time']['lead_time_window']}")

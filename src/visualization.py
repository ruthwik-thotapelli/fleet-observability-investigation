import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def plot_timeseries(df: pd.DataFrame, x_col: str, y_col: str, hue_col: str, title: str, output_path: str):
    """
    Generic visualization helper for plotting telemetry timeseries data.
    """
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    sns.lineplot(data=df, x=x_col, y=y_col, hue=hue_col, marker='o', linewidth=2)
    
    plt.title(title, fontsize=14, pad=15)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel(y_col.replace('_', ' ').title(), fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    
def generate_incident_dashboard(telemetry: pd.DataFrame):
    """Generates all standard incident investigation charts."""
    plot_timeseries(telemetry, 'timestamp', 'network_latency_ms', 'robot_id', 
                    'Fleet Network Latency (Highlighting Robot_01 Spike)', 'outputs/figures/latency_dashboard.png')
    plot_timeseries(telemetry, 'timestamp', 'cpu_usage', 'robot_id', 
                    'Fleet CPU Utilization (Highlighting Robot_02 Saturation)', 'outputs/figures/cpu_dashboard.png')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ExploratoryAnalyzer:
    def __init__(self, output_dir='outputs/figures'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Set visualization style
        sns.set_theme(style="whitegrid")

    def plot_battery_behavior(self, telemetry: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=telemetry, x='timestamp', y='battery_level', hue='robot_id', marker='o')
        plt.title('Battery Drain over Time per Robot')
        plt.xlabel('Time')
        plt.ylabel('Battery Level (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'battery_drain.png'))
        plt.close()

    def plot_cpu_behavior(self, telemetry: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=telemetry, x='timestamp', y='cpu_usage', hue='robot_id', marker='o')
        plt.title('CPU Usage over Time per Robot')
        plt.xlabel('Time')
        plt.ylabel('CPU Usage (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'cpu_usage.png'))
        plt.close()

    def plot_network_latency(self, telemetry: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=telemetry, x='timestamp', y='network_latency_ms', hue='robot_id', marker='o')
        plt.title('Network Latency over Time per Robot')
        plt.xlabel('Time')
        plt.ylabel('Latency (ms)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'network_latency.png'))
        plt.close()

    def run_all_eda(self, telemetry: pd.DataFrame):
        print("Running Exploratory Data Analysis...")
        self.plot_battery_behavior(telemetry)
        self.plot_cpu_behavior(telemetry)
        self.plot_network_latency(telemetry)
        print("EDA Visualizations saved to outputs/figures/")
 

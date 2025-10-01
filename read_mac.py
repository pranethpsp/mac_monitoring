import subprocess
import re
import psutil
import platform

class SystemMonitor:
    """
    A class to fetch and report system statistics like disk, memory, and battery.
    """
    def __init__(self, path="/"):
        """
        Initializes the SystemMonitor.
        
        Args:
            path (str): The disk path to monitor (e.g., "/"). Defaults to root.
        """
        self.path = path
        # Determine the OS at initialization to avoid repeated checks.
        self.os_type = platform.system()

    # --- Private methods for raw data retrieval ---

    def _get_disk_usage_data(self):
        """Returns a dictionary with disk usage statistics in GB."""
        try:
            usage = psutil.disk_usage(self.path)
            return {
                "total": round(usage.total / 1e9, 2),
                "used": round(usage.used / 1e9, 2),
                "free": round(usage.free / 1e9, 2),
                "percent": usage.percent
            }
        except Exception:
            return None

    def _get_battery_data(self):
        """
        Returns battery percentage.
        Uses `psutil` for cross-platform support where available.
        Falls back to macOS-specific command if needed.
        """
        try:
            # `psutil` provides a cross-platform way to get battery status
            battery = psutil.sensors_battery()
            if battery:
                return int(battery.percent)
            
            # Fallback for systems where psutil might fail but pmset works (macOS)
            if self.os_type == "Darwin":
                output = subprocess.check_output(["pmset", "-g", "batt"]).decode("utf-8")
                match = re.search(r'(\d+)%', output)
                if match:
                    return int(match.group(1))
            return None
        except Exception:
            return None
            
    def _get_memory_string_from_top(self):
            """
            Returns a string describing memory usage using the original 'top' command.
            This method is macOS-specific.
            """
            # This logic is specific to macOS ('Darwin')
            if self.os_type != "Darwin":
                return None
                
            command = "top -l 1 | grep PhysMem"
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Clean up the output string by removing the prefix and stripping whitespace.
                return result.stdout.replace("PhysMem:", "").strip()
            except Exception:
                return None

    def get_disk_report(self):
        """Returns a formatted string describing disk usage."""
        disk_info = self._get_disk_usage_data()
        if disk_info:
            return (
                f"Here is the current disk usage report: The total disk space is {disk_info['total']} GB, "
                f"with {disk_info['used']} GB used and {disk_info['free']} GB free. "
                f"This means the disk is currently {disk_info['percent']}% full."
            )
        return "I was unable to retrieve the disk usage information."

    def get_battery_report(self):
        """Returns a formatted string describing the battery status."""
        battery_level = self._get_battery_data()
        if battery_level is not None:
            return f"The current battery level is at {battery_level}%."
        return "I could not retrieve the current battery status. It might be unavailable or not applicable (e.g., on a desktop)."

    def get_memory_report(self):
        """Returns a formatted string describing memory usage based on the 'top' command."""
        mem_info_string = self._get_memory_string_from_top()
        if mem_info_string:
            return f"The system's physical memory (RAM) usage is currently: {mem_info_string}."
        
        if self.os_type != "Darwin":
            return "Memory usage from 'top' command is only available on macOS."
            
        return "I was unable to fetch the system's current memory usage."
        
    def get_report(self,resource_type):
        """
        Returns a dictionary containing all individual system reports.
        This is the most convenient method for getting all data at once.
        """
        if resource_type == "disk":
            return self.get_disk_report()
        elif resource_type == "battery":
            return self.get_battery_report()
        elif resource_type == "memory":
            return self.get_memory_report()
        else:
            return "No Reports Found!"
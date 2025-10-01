from unittest.mock import Mock
from mac_assist.read_mac import SystemMonitor
from mac_assist.understand_question import ask
from mac_assist.answering import answer_for_question

# ========== 1. Tests for read_mac.py (SystemMonitor) ==========
# We use the 'mocker' fixture from pytest-mock to replace real functions
# with fake ones that return predictable data.

def test_get_disk_report_success(mocker):
    """
    Test Case 1: Checks if get_disk_report formats a successful disk usage check correctly.
    """
    # Create a fake disk usage object
    mock_disk_usage = Mock(total=500e9, used=200e9, free=300e9, percent=40.0)
    # Patch the real psutil.disk_usage to return our fake object
    mocker.patch('psutil.disk_usage', return_value=mock_disk_usage)
    
    monitor = SystemMonitor()
    report = monitor.get_disk_report()
    
    assert "total disk space is 500.0 GB" in report
    assert "200.0 GB used" in report
    assert "300.0 GB free" in report
    assert "disk is currently 40.0% full" in report

def test_get_disk_report_failure(mocker):
    """
    Test Case 2: Checks if get_disk_report handles an error from psutil gracefully.
    """
    # Patch psutil.disk_usage to raise an exception
    mocker.patch('psutil.disk_usage', side_effect=Exception("Disk not found"))
    
    monitor = SystemMonitor()
    report = monitor.get_disk_report()
    
    assert report == "I was unable to retrieve the disk usage information."

def test_get_battery_report_success(mocker):
    """
    Test Case 3: Checks if get_battery_report works correctly using psutil.
    """
    # Fake a battery object with 88% charge
    mock_battery = Mock(percent=88)
    mocker.patch('psutil.sensors_battery', return_value=mock_battery)
    
    monitor = SystemMonitor()
    report = monitor.get_battery_report()
    
    assert report == "The current battery level is at 88%."

def test_get_battery_report_failure(mocker):
    """
    Test Case 4: Checks the graceful failure message for battery status.
    """
    # Patch the function to return None, simulating an error
    mocker.patch('psutil.sensors_battery', return_value=None)
    
    # Also patch the mac-specific fallback to ensure it also fails
    mocker.patch('subprocess.check_output', side_effect=Exception("Command failed"))
    
    monitor = SystemMonitor()
    report = monitor.get_battery_report()
    
    assert "Could not retrieve the current battery status" in report

def test_get_memory_report_success_on_mac(mocker):
    """
    Test Case 5: Checks memory report on macOS when the 'top' command succeeds.
    """
    # Mock the platform to be 'Darwin' (macOS)
    mocker.patch('platform.system', return_value="Darwin")
    
    # Fake the output of the 'top' command
    fake_stdout = "PhysMem: 12G used (4G wired), 4G unused."
    mock_run_result = Mock(stdout=fake_stdout, check_returncode=lambda: None)
    mocker.patch('subprocess.run', return_value=mock_run_result)
    
    monitor = SystemMonitor()
    report = monitor.get_memory_report()
    
    expected_string = "12G used (4G wired), 4G unused."
    assert report == f"The system's physical memory (RAM) usage is currently: {expected_string}."

def test_get_memory_report_failure_on_mac(mocker):
    """
    Test Case 6: Checks memory report on macOS when the 'top' command fails.
    """
    mocker.patch('platform.system', return_value="Darwin")
    # Patch the subprocess command to raise an error
    mocker.patch('subprocess.run', side_effect=Exception("Command failed"))
    
    monitor = SystemMonitor()
    report = monitor.get_memory_report()
    
    assert report == "I was unable to fetch the system's current memory usage."

def test_get_memory_report_on_other_os(mocker):
    """
    Test Case 7: Checks that the memory report gives the correct message on non-macOS systems.
    """
    # Mock the platform to be 'Linux'
    mocker.patch('platform.system', return_value="Linux")
    
    monitor = SystemMonitor()
    report = monitor.get_memory_report()
    
    assert report == "Memory usage from 'top' command is only available on macOS."

# ========== 2. Tests for understand_question.py ==========

def test_ask_function_classifies_disk(mocker):
    """
    Test Case 8: Checks if the 'ask' function correctly classifies a disk-related query.
    """
    # Create a fake response from the ollama library
    mock_response = {"message": {"content": "disk"}}
    mocker.patch('ollama.chat', return_value=mock_response)
    
    result = ask("How much storage is left?")
    
    assert result == ["disk"]

def test_ask_function_classifies_multiple(mocker):
    """
    Test Case 9: Checks if 'ask' handles multiple keywords correctly.
    """
    mock_response = {"message": {"content": "disk battery"}}
    mocker.patch('ollama.chat', return_value=mock_response)
    
    result = ask("What's my disk and battery status?")
    
    assert result == ["disk", "battery"]

# ========== 3. Tests for answering.py ==========

def test_answer_for_question_generates_natural_response(mocker):
    """
    Test Case 10: Checks if the final answering function formats a response conversationally.
    """
    final_response = "Sure, the battery is currently at 95%."
    mock_response = {"message": {"content": final_response}}
    mocker.patch('ollama.chat', return_value=mock_response)
    
    question = "what is the battery"
    context = "The current battery level is at 95%."
    
    result = answer_for_question(question, context)
    
    assert result == final_response
"""
Main GUI for the Advanced Port Scanner and Wireless Attack Tool
Author: morningstarxcdcode
Description: Provides a graphical interface for users to perform port scans and wireless attacks.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import socket
import queue
from wireless import wireless_attacks

# Handle cases where tkinter might not be available

class AnimatedProgressBar(tk.Canvas):
    def __init__(self, parent: tk.Widget, width: int = 700, height: int = 25, max_value: int = 100, **kwargs):
        """
        Initialize the animated progress bar.

        :param parent: The parent widget.
        :param width: The width of the progress bar.
        :param height: The height of the progress bar.
        :param max_value: The maximum value of the progress bar.
        """
        super().__init__(parent, width=width, height=height, bg="#000000", **kwargs)
        self.width = width
        self.height = height
        self.max_value = max_value
        self.progress = 0
        self.rect = self.create_rectangle(0, 0, 0, height, fill="#00FF00")
        self.text = self.create_text(width // 2, height // 2, text="0%", fill="#00FF00", font=("Consolas", 12, "bold"))

    def update_progress(self, value: int) -> None:
        """Update the progress bar with the current value."""
        self.progress = value
        fill_width = int(self.width * (self.progress / self.max_value))
        self.coords(self.rect, 0, 0, fill_width, self.height)
        self.itemconfig(self.text, text=f"{int((self.progress / self.max_value) * 100)}%")
        self.update()

def get_local_ip() -> str:
    """Retrieve the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_default_port_range() -> str:
    """Return the default port range for scanning."""
    return "1-1000"

def run_port_scan() -> None:
    """Initiate the port scan based on user input."""
    target = port_target_entry.get().strip()
    port_range = port_range_entry.get().strip()
    if not target:
        messagebox.showerror("Input Error", "Please enter a target IP address.")
        return
    if not port_range:
        port_range = get_default_port_range()
    port_scan_button.config(state=tk.DISABLED)
    port_output_text.config(state=tk.NORMAL)
    port_output_text.delete(1.0, tk.END)
    port_progress_bar.update_progress(0)
    port_elapsed_label.config(text="Elapsed Time: 0.0s")
    start_time = time.time()

    def update_elapsed() -> None:
        """Update the elapsed time label during the scan."""
        while not port_scan_done.is_set():
            elapsed = time.time() - start_time
            port_elapsed_label.config(text=f"Elapsed Time: {elapsed:.1f}s")
            time.sleep(0.1)

    def scan() -> None:
        """Perform the port scan using the port scanner module."""
        from scanner.port_scanner import run_scan
        import io
        import sys
        
        try:
            # Capture the output from run_scan
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            # Run the scan
            run_scan(target, port_range)
            
            # Get the output
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            # Display output line by line
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if line.strip():
                    port_output_text.insert(tk.END, line + '\n')
                    port_output_text.see(tk.END)
                    progress = min((i + 1) / len(lines) * 100, 100)
                    port_progress_bar.update_progress(progress)
                    root.update()  # Update GUI
                    
        except Exception as e:
            port_output_text.insert(tk.END, f"Error during scan: {str(e)}\n")
        finally:
            sys.stdout = old_stdout
            port_scan_done.set()
            elapsed = time.time() - start_time
            port_output_text.insert(tk.END, f"\nScan completed in {elapsed:.2f} seconds.\n")
            port_scan_button.config(state=tk.NORMAL)
            port_progress_bar.update_progress(100)
            port_output_text.config(state=tk.DISABLED)

    port_scan_done = threading.Event()
    threading.Thread(target=update_elapsed, daemon=True).start()
    threading.Thread(target=scan, daemon=True).start()

def run_wireless_attack() -> None:
    """Initiate the wireless attack based on user input."""
    target = wireless_target_entry.get().strip()
    if not target:
        messagebox.showerror("Input Error", "Please enter a target IP address.")
        return
    wireless_attack_button.config(state=tk.DISABLED)
    wireless_output_text.config(state=tk.NORMAL)
    wireless_output_text.delete(1.0, tk.END)
    wireless_progress_bar.update_progress(0)
    wireless_elapsed_label.config(text="Elapsed Time: 0.0s")
    start_time = time.time()

    log_queue = queue.Queue()

    def log_handler() -> None:
        """Handle logging output during the wireless attack."""
        while True:
            try:
                msg = log_queue.get(timeout=0.1)
                wireless_output_text.insert(tk.END, msg + "\\n")
                wireless_output_text.see(tk.END)
            except queue.Empty:
                if wireless_attack_done.is_set():
                    break

    def update_elapsed() -> None:
        """Update the elapsed time label during the wireless attack."""
        while not wireless_attack_done.is_set():
            elapsed = time.time() - start_time
            wireless_elapsed_label.config(text=f"Elapsed Time: {elapsed:.1f}s")
            time.sleep(0.1)

    def attack() -> None:
        """Perform the wireless attack using the wireless attacks module."""
        class QueueLogger:
            def info(self, msg: str) -> None:
                log_queue.put(msg)
        logger = QueueLogger()
        try:
            wireless_attacks.run_attack(target)
            logger.info("Wireless attack finished")
        except Exception as e:
            logger.info(f"Error: {e}")
        finally:
            wireless_attack_done.set()
            elapsed = time.time() - start_time
            log_queue.put(f"\\nWireless attack completed in {elapsed:.2f} seconds.")
            wireless_attack_button.config(state=tk.NORMAL)
            wireless_progress_bar.update_progress(100)
            wireless_output_text.config(state=tk.DISABLED)

    wireless_attack_done = threading.Event()
    threading.Thread(target=log_handler, daemon=True).start()
    threading.Thread(target=update_elapsed, daemon=True).start()
    threading.Thread(target=attack, daemon=True).start()

# Initialize the main GUI window
def run_gui():
    """Main entry point for the GUI application."""
    global root, port_target_entry, port_range_entry, port_scan_button, port_output_text
    global port_progress_bar, port_elapsed_label, wireless_target_entry, wireless_attack_button
    global wireless_output_text, wireless_progress_bar, wireless_elapsed_label

    root = tk.Tk()
    root.title("Advanced Port Scanner GUI")
    root.geometry("800x650")
    root.configure(bg="#000000")

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    # Port Scan Tab
    port_scan_tab = ttk.Frame(tab_control)
    tab_control.add(port_scan_tab, text="Port Scan")

    tk.Label(port_scan_tab, text="Target IP:", fg="#00FF00", bg="#000000", font=("Consolas", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    port_target_entry = tk.Entry(port_scan_tab, width=40, font=("Consolas", 12, "bold"), fg="#00FF00", bg="#000000", insertbackground="#00FF00")
    port_target_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(port_scan_tab, text="Port Range:", fg="#00FF00", bg="#000000", font=("Consolas", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    port_range_entry = tk.Entry(port_scan_tab, width=40, font=("Consolas", 12, "bold"), fg="#00FF00", bg="#000000", insertbackground="#00FF00")
    port_range_entry.grid(row=1, column=1, padx=5, pady=5)
    port_range_entry.insert(0, get_default_port_range())

    port_scan_button = tk.Button(port_scan_tab, text="Start Scan", command=run_port_scan, bg="#004400", fg="#00FF00", font=("Consolas", 14, "bold"))
    port_scan_button.grid(row=2, column=0, columnspan=2, pady=10)

    port_progress_bar = AnimatedProgressBar(port_scan_tab, width=700, height=25)
    port_progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    port_elapsed_label = tk.Label(port_scan_tab, text="Elapsed Time: 0.0s", fg="#00FF00", bg="#000000", font=("Consolas", 12, "bold"))
    port_elapsed_label.grid(row=4, column=0, columnspan=2, pady=5)

    port_output_text = tk.Text(port_scan_tab, height=20, width=90, fg="#00FF00", bg="#000000", font=("Consolas", 11, "bold"), insertbackground="#00FF00")
    port_output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    port_output_text.config(state=tk.DISABLED)

    # Wireless Attack Tab
    wireless_tab = ttk.Frame(tab_control)
    tab_control.add(wireless_tab, text="Wireless Attack")

    tk.Label(wireless_tab, text="Target IP:", fg="#00FF00", bg="#000000", font=("Consolas", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    wireless_target_entry = tk.Entry(wireless_tab, width=40, font=("Consolas", 12, "bold"), fg="#00FF00", bg="#000000", insertbackground="#00FF00")
    wireless_target_entry.grid(row=0, column=1, padx=5, pady=5)

    wireless_attack_button = tk.Button(wireless_tab, text="Start Wireless Attack", command=run_wireless_attack, bg="#004400", fg="#00FF00", font=("Consolas", 14, "bold"))
    wireless_attack_button.grid(row=1, column=0, columnspan=2, pady=10)

    wireless_progress_bar = AnimatedProgressBar(wireless_tab, width=700, height=25)
    wireless_progress_bar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    wireless_elapsed_label = tk.Label(wireless_tab, text="Elapsed Time: 0.0s", fg="#00FF00", bg="#000000", font=("Consolas", 12, "bold"))
    wireless_elapsed_label.grid(row=3, column=0, columnspan=2, pady=5)

    wireless_output_text = tk.Text(wireless_tab, height=20, width=90, fg="#00FF00", bg="#000000", font=("Consolas", 11, "bold"), insertbackground="#00FF00")
    wireless_output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    wireless_output_text.config(state=tk.DISABLED)

    # Auto-fill local IP in target fields
    local_ip = get_local_ip()
    port_target_entry.insert(0, local_ip)
    wireless_target_entry.insert(0, local_ip)

    root.mainloop()

if __name__ == "__main__":
    run_gui()

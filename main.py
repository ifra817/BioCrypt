import sys
import os
import time
from colorama import init, Fore, Back, Style

# Initialize colorama for clean cross-platform terminal colors
init(autoreset=True)

# Import workflows
from face_register import register_new_face
from face_recogniser import mark_attendance_workflow
from utils.admin_utils import verify_admin, get_attendance_logs, export_attendance_csv
from utils.storage_utils import get_all_users

def clear_screen():
    """Clears the terminal screen smoothly."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(title, color=Fore.CYAN):
    """Draws a standardized, striking application frame header."""
    print(color + "╔" + "═" * 50 + "╗")
    print(color + f"║ {title.center(48)} ║")
    print(color + "╚" + "═" * 50 + "╝")

def wait_for_user():
    """Utility to pause execution until user acknowledges."""
    print(Fore.BLACK + Back.WHITE + "\n [ Press ENTER to return to menu ] ", end="")
    input()

def admin_dashboard():
    """The secure administrative options dashboard panel."""
    while True:
        clear_screen()
        draw_header("⚙️ BIOCRYPT - ADMIN CONTROL PANEL", Fore.MAGENTA)
        print(Fore.MAGENTA + " 1. 📋 View All Attendance Logs")
        print(Fore.MAGENTA + " 2. 📊 Export Records to CSV")
        print(Fore.MAGENTA + " 3. 👥 View Enrolled Users")
        print(Fore.MAGENTA + " 4. 🚪 Logout & Return")
        print(Fore.MAGENTA + "╚" + "═" * 50 + "╝")
        
        choice = input(Fore.WHITE + "➔ Select management utility (1-4): ").strip()
        
        if choice == '1':
            clear_screen()
            draw_header("📋 SYSTEM ATTENDANCE LOGS", Fore.MAGENTA)
            logs = get_attendance_logs()
            if not logs:
                print(Fore.YELLOW + "\n[!] No attendance records found in the system database.")
            else:
                print(Fore.WHITE + f"{'Log ID':<8}{'Student ID':<15}{'Timestamp':<25}")
                print(Fore.MAGENTA + "-" * 48)
                for log in logs:
                    print(Fore.GREEN + f"{log[0]:<8}{log[1]:<15}{log[2]:<25}")
            wait_for_user()
            
        elif choice == '2':
            clear_screen()
            draw_header("📊 EXPORT TRANSACTION DATA", Fore.MAGENTA)
            filename = "biocrypt_attendance.csv"
            print(Fore.YELLOW + f"Writing logs to local root folder...")
            try:
                export_attendance_csv(filename)
                print(Fore.GREEN + f"✔ Success: Encrypted log exported cleanly to '{filename}'!")
            except Exception as e:
                print(Fore.RED + f"❌ Export Interrupted: {e}")
            wait_for_user()
            
        elif choice == '3':
            clear_screen()
            draw_header("👥 CURRENTLY ENROLLED STUDENTS", Fore.MAGENTA)
            users = get_all_users()
            if not users:
                print(Fore.YELLOW + "\n[!] Database is completely empty. No credentials found.")
            else:
                print(Fore.WHITE + f"{'DB ID':<8}{'Name':<20}{'Reg No':<15}")
                print(Fore.MAGENTA + "-" * 48)
                for user in users:
                    print(Fore.CYAN + f"{user[0]:<8}{user[1]:<20}{user[2]:<15}")
            wait_for_user()
            
        elif choice == '4':
            print(Fore.YELLOW + "\n🔒 Revoking administrative context tokens...")
            time.sleep(0.8)
            break
        else:
            print(Fore.RED + "❌ Action invalid. Select an index from 1 to 4.")
            time.sleep(1)

def handle_admin_login():
    """Handles secure authentication parsing utilizing Member 1's Bcrypt utils."""
    clear_screen()
    draw_header("🔒 ADMIN AUTHENTICATION REQUIRED", Fore.RED)
    
    username = input(Fore.WHITE + "Enter Admin Username: ").strip()
    password = input(Fore.WHITE + "Enter Admin Password: ").strip()
    
    print(Fore.YELLOW + "\nVerifying secure hash protocols...")
    time.sleep(0.5)
    
    # Securely queries Member 1's verification logic against DB
    if verify_admin(username, password):
        print(Fore.GREEN + "✔ Identity Confirmed. Welcome back Administrator.")
        time.sleep(0.8)
        admin_dashboard()
    else:
        print(Fore.RED + "❌ ACCESS DENIED: Hashing sequence failed or user does not exist.")
        wait_for_user()

def main_menu():
    """Core runtime engine driving user interface decisions."""
    while True:
        clear_screen()
        print(Fore.CYAN + "╔" + "═" * 50 + "╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + "   🔐 BioCrypt - Face Recognition System v1.0   " + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝")
        print(Fore.CYAN + " 1. 📝 Register New User")
        print(Fore.CYAN + " 2. ✅ Mark Attendance (Live Scan)")
        print(Fore.CYAN + " 3. 🔒 Secure Admin Login")
        print(Fore.CYAN + " 4. ❌ Exit Terminal Suite")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝")
        
        choice = input(Fore.WHITE + Style.BRIGHT + "➔ Select an option (1-4): ").strip()
        
        if choice == '1':
            register_new_face()
            wait_for_user()
        elif choice == '2':
            mark_attendance_workflow()
            wait_for_user()
        elif choice == '3':
            handle_admin_login()
        elif choice == '4':
            clear_screen()
            print(Fore.GREEN + "\n" + "═"*45)
            print("💾 Biometric data securely stored. Exiting suite...")
            print("═"*45 + "\n")
            sys.exit()
        else:
            print(Fore.RED + "❌ Selection unrecognized. Enter values between 1 and 4.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
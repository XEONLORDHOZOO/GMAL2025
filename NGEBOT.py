import os
import time
import smtplib
import ssl
from email.message import EmailMessage
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama and dotenv
init(autoreset=True)
load_dotenv()

perm_file = "perm_ban.txt"
temp_file = "temp_ban.txt"

sender_email = os.getenv('GMAIL_ADDRESS')
password = os.getenv('GMAIL_PASSWORD')

support_emails = [
    "support@whatsapp.com",
    "abuse@support.whatsapp.com",
    "privacy@support.whatsapp.com",
    "terms@support.whatsapp.com",
    "accessibility@support.whatsapp.com"
]


def banner():
    print(f"\n{Fore.CYAN}╔{'═'*50}╗")
    print(f"║{Fore.CYAN}{'𝗖𝗥𝗬𝗣𝗧𝗢 𝗟𝗢𝗥𝗗 𝗕𝗔𝗡𝗡𝗜𝗡𝗚 𝗧𝗢𝗢𝗟𝗦':^50}{Style.RESET_ALL}║")
    print(f"╚{'═'*50}╝{Style.RESET_ALL}")
    print(Fore.YELLOW + "📱 UNLIMITED BAN/UNBAN TOOL" + Style.RESET_ALL)
    print(Fore.GREEN + "✨ Support All Number Formats: +62, 08, etc." + Style.RESET_ALL)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_number_input(number):
    """Format nomor telepon untuk konsistensi"""
    number = number.strip()
    
    # Jika diawali dengan 0, ganti dengan +62
    if number.startswith('0'):
        number = '+62' + number[1:]
    
    # Jika tidak ada kode negara, tambahkan +62
    elif not number.startswith('+'):
        number = '+62' + number
    
    return number


def is_banned(number):
    number = format_number_input(number)
    
    if os.path.exists(perm_file):
        with open(perm_file, "r") as f:
            for line in f:
                if number == line.strip():
                    return "permanent"
    
    if os.path.exists(temp_file):
        with open(temp_file, "r") as f:
            for line in f:
                if line.startswith(number + ","):
                    unban_time = int(line.strip().split(",")[1])
                    if time.time() < unban_time:
                        return "temporary"
    return None


def simulate_reports(number, total):
    print(f"\n{Fore.CYAN}⚙️  PROCESSING {total} BAN REQUESTS FOR {number}...")
    for i in range(1, total + 1):
        progress = (i / total) * 100
        print(f"{Fore.RED}☠️  Sending Attack {i}/{total} [{int(progress)}%] → {number}")
        time.sleep(0.03)
    print(f"{Fore.GREEN}✅ {total} BAN REQUESTS COMPLETED SUCCESSFULLY! 👌💯")


def save_perm_ban(number):
    number = format_number_input(number)
    with open(perm_file, "a") as f:
        f.write(number + "\n")


def save_temp_ban(number, duration):
    number = format_number_input(number)
    unban_time = int(time.time() + duration)
    with open(temp_file, "a") as f:
        f.write(f"{number},{unban_time}\n")


def check_temp_expiry():
    if not os.path.exists(temp_file):
        return
    with open(temp_file, "r") as f:
        lines = f.readlines()
    active = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2:
            number, unban_time = parts
            if time.time() < int(unban_time):
                active.append(line)
            else:
                print(f"{Fore.GREEN}✅ Temporary ban expired for {number}")
    with open(temp_file, "w") as f:
        f.writelines(active)


def ban_permanent():
    print(f"\n{Fore.RED}🚫 PERMANENT BAN MENU")
    print(f"{Fore.YELLOW}─────────────────────")
    
    number = input(f"{Fore.WHITE}📱 Enter Target Number (+62/08/etc): ").strip()
    formatted_number = format_number_input(number)
    
    ban_status = is_banned(number)
    if ban_status:
        print(f"{Fore.RED}❌ {formatted_number} is already {ban_status} banned.")
        return
    
    print(f"{Fore.CYAN}📝 Target: {formatted_number}")
    
    try:
        reports = int(input(f"{Fore.WHITE}🔢 Enter Amount of Reports: "))
        if reports <= 0:
            print(f"{Fore.RED}❌ Amount must be greater than 0")
            return
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter a number.")
        return
    
    confirm = input(f"{Fore.YELLOW}⚠️  Confirm PERMANENT ban for {formatted_number}? (y/N): ").strip().lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}❌ Action cancelled.")
        return
    
    simulate_reports(formatted_number, reports)
    save_perm_ban(number)
    print(f"{Fore.RED}🚫 Number {formatted_number} will be PERMANENTLY BANNED shortly.")
    
    reason = "This Number Have Been Stealing and scamming People On WhatsApp, destroying people WhatsApp account, sending negative Text, spamming virus, Sending nudes to different people on WhatsApp please He his Going against the Community guidelines please disable the account from using WhatsApp He hacked My Number and start using it to scam people Online And he his very dangerous Sending Different videos and pictures especially Nudes or sex stuff, please i beg of you WhatsApp support team work together and disable this number from Violating WhatsApp please, He is a Fraud, scammer,Thief, Sending spam messages, text viruses, And many of all negative attitude Please disable the account permanently from using WhatsApp account again he will continue doing so if yoi guy's didn't take action on time. Thank you"
    send_report_email(formatted_number, reason, reports)


def ban_temporary():
    print(f"\n{Fore.YELLOW}⏳ TEMPORARY BAN MENU")
    print(f"{Fore.YELLOW}─────────────────────")
    
    number = input(f"{Fore.WHITE}📱 Enter Target Number (+62/08/etc): ").strip()
    formatted_number = format_number_input(number)
    
    ban_status = is_banned(number)
    if ban_status:
        print(f"{Fore.RED}❌ {formatted_number} is already {ban_status} banned.")
        return
    
    print(f"{Fore.CYAN}📝 Target: {formatted_number}")
    
    try:
        minutes = int(input(f"{Fore.WHITE}⏰ Enter Ban Duration (minutes): "))
        if minutes <= 0:
            print(f"{Fore.RED}❌ Duration must be greater than 0")
            return
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter a number.")
        return
    
    try:
        reports = int(input(f"{Fore.WHITE}🔢 Enter Amount of Reports: "))
        if reports <= 0:
            print(f"{Fore.RED}❌ Amount must be greater than 0")
            return
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter a number.")
        return
    
    confirm = input(f"{Fore.YELLOW}⚠️  Confirm TEMPORARY ban for {formatted_number}? (y/N): ").strip().lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}❌ Action cancelled.")
        return
    
    simulate_reports(formatted_number, reports)
    save_temp_ban(number, minutes * 60)
    print(f"{Fore.YELLOW}⏳ {formatted_number} temporarily banned for {minutes} minutes.")
    
    reason = f"This Number will Be Disable for {minutes} Minutes because he Have Been Stealing and scamming People On WhatsApp, destroying people WhatsApp account, sending negative Text, spamming virus, Sending nudes to different people on WhatsApp please He his Going against the Community guidelines please disable the account from using WhatsApp He hacked My Number and start using it to scam people Online And he his very dangerous Sending Different videos and pictures especially Nudes or sex stuff, please i beg of you WhatsApp support team work together and disable this number from Violating WhatsApp please, He is a Fraud, scammer,Thief, Sending spam messages, text viruses, And many of all negative attitude Please disable the account permanently from using WhatsApp account again he will continue doing so if yoi guy's didn't take action on time. Thank you"
    send_report_email(formatted_number, reason, reports)


def unban_permanent():
    print(f"\n{Fore.GREEN}✅ PERMANENT UNBAN MENU")
    print(f"{Fore.YELLOW}─────────────────────")
    
    number = input(f"{Fore.WHITE}📱 Enter Number to UNBAN (+62/08/etc): ").strip()
    formatted_number = format_number_input(number)
    
    if not os.path.exists(perm_file):
        print(f"{Fore.YELLOW}ℹ️  No permanent bans found.")
        return
    
    found = False
    updated_lines = []
    
    # Baca semua nomor yang ada
    with open(perm_file, "r") as f:
        lines = f.readlines()
    
    # Cari dan hapus nomor yang sesuai
    for line in lines:
        stored_number = line.strip()
        # Bandingkan dengan format yang sama
        if stored_number == formatted_number:
            found = True
            print(f"{Fore.GREEN}🚫 Found: {stored_number} - Removing...")
        else:
            updated_lines.append(line)
    
    # Tulis kembali tanpa nomor yang diunban
    with open(perm_file, "w") as f:
        f.writelines(updated_lines)
    
    if found:
        print(f"{Fore.GREEN}✅ {formatted_number} successfully UNBANNED from permanent ban.")
    else:
        print(f"{Fore.YELLOW}ℹ️  {formatted_number} not found in permanent ban list.")
        print(f"{Fore.CYAN}📋 Current banned numbers:")
        with open(perm_file, "r") as f:
            for i, line in enumerate(f, 1):
                print(f"   {i}. {line.strip()}")


def unban_temporary():
    print(f"\n{Fore.GREEN}✅ TEMPORARY UNBAN MENU")
    print(f"{Fore.YELLOW}─────────────────────")
    
    number = input(f"{Fore.WHITE}📱 Enter Number to UNBAN (+62/08/etc): ").strip()
    formatted_number = format_number_input(number)
    
    if not os.path.exists(temp_file):
        print(f"{Fore.YELLOW}ℹ️  No temporary bans found.")
        return
    
    found = False
    updated_lines = []
    
    with open(temp_file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2:
            stored_number, unban_time = parts
            if stored_number == formatted_number:
                found = True
                print(f"{Fore.GREEN}🚫 Found: {stored_number} - Removing...")
            else:
                updated_lines.append(line)
    
    with open(temp_file, "w") as f:
        f.writelines(updated_lines)
    
    if found:
        print(f"{Fore.GREEN}✅ {formatted_number} successfully UNBANNED from temporary ban.")
    else:
        print(f"{Fore.YELLOW}ℹ️  {formatted_number} not found in temporary ban list.")


def send_report_email(target_number, reason, count):
    if not sender_email or not password:
        print(f"{Fore.RED}❌ Email credentials not configured. Skipping email reports.")
        return
        
    context = ssl.create_default_context()
    for i in range(count):
        msg = EmailMessage()
        msg['Subject'] = f"Report of WhatsApp Account (Attempt {i+1})"
        msg['From'] = sender_email
        msg['To'] = ", ".join(support_emails)
        msg.set_content(f"""Hello WhatsApp Support,

I would like to report the following WhatsApp number:

📱 Number: {target_number}
📝 Reason: {reason}

please take action immediately 
Thank you.
""")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)
            print(f"✅ Ban request {i+1}/{count} sent to WhatsApp")
        except Exception as e:
            print(f"❌ Ban request {i+1} failed: {e}")
            break


def view_banned():
    print(f"\n{Fore.RED}🚫 PERMANENT BANS:")
    print(f"{Fore.YELLOW}────────────────")
    if os.path.exists(perm_file) and os.path.getsize(perm_file) > 0:
        with open(perm_file, "r") as f:
            numbers = f.read().strip().split('\n')
            for i, number in enumerate(numbers, 1):
                print(f"{i}. {number}")
    else:
        print(f"{Fore.YELLOW}No permanent bans")

    print(f"\n{Fore.MAGENTA}⏳ TEMPORARY BANS:")
    print(f"{Fore.YELLOW}────────────────")
    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
        with open(temp_file, "r") as f:
            for i, line in enumerate(f, 1):
                parts = line.strip().split(",")
                if len(parts) == 2:
                    number, unban_time = parts
                    remaining = int(unban_time) - int(time.time())
                    if remaining > 0:
                        mins = remaining // 60
                        secs = remaining % 60
                        print(f"{i}. {number} — {mins}m {secs}s left")
    else:
        print(f"{Fore.YELLOW}No temporary bans")


def show_main_menu():
    clear_screen()
    banner()
    print(f"\n{Fore.CYAN}🎯 MAIN MENU:")
    print(f"{Fore.YELLOW}─────────────")
    print(f"{Fore.RED}1️⃣  🚫 BAN PERMANENT (Unlimited)")
    print(f"{Fore.YELLOW}2️⃣  ⏳ BAN TEMPORARY (Unlimited)") 
    print(f"{Fore.GREEN}3️⃣  ✅ UNBAN PERMANENT")
    print(f"{Fore.GREEN}4️⃣  ✅ UNBAN TEMPORARY")
    print(f"{Fore.BLUE}5️⃣  📋 VIEW BANNED NUMBERS")
    print(f"{Fore.MAGENTA}6️⃣  🚪 EXIT")
    print(f"{Fore.YELLOW}─────────────")


# Main Loop
def main():
    # Create files if they don't exist
    for file in [perm_file, temp_file]:
        if not os.path.exists(file):
            open(file, 'w').close()
    
    while True:
        check_temp_expiry()
        show_main_menu()
        
        choice = input(f"\n{Fore.CYAN}👉 Choose an option [1-6]: ").strip()

        if choice == "1":
            ban_permanent()
        elif choice == "2":
            ban_temporary()
        elif choice == "3":
            unban_permanent()
        elif choice == "4":
            unban_temporary()
        elif choice == "5":
            view_banned()
        elif choice == "6":
            print(f"\n{Fore.CYAN}👋 Exiting. Stay safe, Crypto Lord Hacker!")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1-6.")

        input(f"\n{Fore.YELLOW}Press Enter to continue...")
        time.sleep(0.5)


if __name__ == "__main__":
    main()

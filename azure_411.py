#!/usr/bin/env python3
"""
Azure 411 - PLATINUM EDITION
Generates Azure resource names following Microsoft CAF best practices
"""

import sys
import random
import time
from resource_rules import RESOURCE_TYPES, generate_name, AZURE_REGIONS, ENVIRONMENTS


class C:
    """Terminal colors - OVO themed"""
    PLATINUM = '\033[38;5;250m'
    GOLD = '\033[38;5;220m'
    OVO = '\033[38;5;214m'
    CHAMPAGNE = '\033[38;5;229m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


HEADER = C.GOLD + r"""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║      █████╗  ███████╗ ██╗   ██╗ ██████╗  ███████╗    ██╗  ██╗  ██╗  ██╗   ║
    ║     ██╔══██╗ ╚══███╔╝ ██║   ██║ ██╔══██╗ ██╔════╝    ██║  ██║ ███║ ███║   ║
    ║     ███████║   ███╔╝  ██║   ██║ ██████╔╝ █████╗      ███████║ ╚██║ ╚██║   ║
    ║     ██╔══██║  ███╔╝   ██║   ██║ ██╔══██╗ ██╔══╝      ╚════██║  ██║  ██║   ║
    ║     ██║  ██║ ███████╗ ╚██████╔╝ ██║  ██║ ███████╗         ██║  ██║  ██║   ║
    ║     ╚═╝  ╚═╝ ╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚══════╝         ╚═╝  ╚═╝  ╚═╝   ║
    ╚═══════════════════════════════════════════════════════════════════════════╝""" + C.END + C.OVO + C.BOLD + """

                        🏆  P L A T I N U M   E D I T I O N  🏆
                       Cloud Adoption Framework Name Generator
    """ + C.END


MENU_ITEMS = [
    ("1", "storage_account", "Storage Account", "💾"),
    ("2", "blob_container", "Blob Container", "📦"),
    ("3", "vpn_gateway", "VPN Gateway", "🔐"),
    ("4", "vpn_connection", "VPN Connection", "🔗"),
    ("5", "sql_server", "SQL Server", "🗄️ "),
    ("6", "sql_database", "SQL Database", "💿"),
    ("7", "resource_group", "Resource Group", "📁"),
    ("8", "virtual_network", "Virtual Network", "🌐"),
]


DRAKE_SONGS = [
    "Champagne Poetry", "Way 2 Sexy", "Knife Talk", "Pipe Down", "No Friends In The Industry",
    "Gods Plan", "Nonstop", "In My Feelings", "Nice For What", "Mob Ties",
    "One Dance", "Controlla", "Hotline Bling", "Feel No Ways", "Views",
    "Passionfruit", "Portland", "Fake Love", "Do Not Disturb", "Gyalchester",
    "Take Care", "Marvins Room", "Headlines", "Crew Love", "The Motto",
    "Started From The Bottom", "Hold On Were Going Home", "Worst Behavior",
    "Energy", "Know Yourself", "Legend", "Jungle", "6 God",
    "Best I Ever Had", "Forever", "0 to 100", "Back to Back", "Jumpman",
    "Sicko Mode", "Toosie Slide", "Laugh Now Cry Later", "Whats Next",
    "First Person Shooter", "IDGAF", "Virginia Beach", "Rich Flex",
]


def animate(text, duration=1.0):
    """Simple loading animation"""
    frames = ["🎵 ♪", "🎵 ♫", "🎶 ♪", "💿 ♫", "🏆 ♪"]
    end = time.time() + duration
    i = 0
    sys.stdout.write(f"\n{C.GOLD}{C.BOLD}")
    while time.time() < end:
        sys.stdout.write(f"\r{frames[i % len(frames)]}  {text} {'.' * (i % 4)}   ")
        sys.stdout.flush()
        time.sleep(0.12)
        i += 1
    sys.stdout.write(f"\r✨  {text} ... CERTIFIED! 🏆   \n{C.END}")


def get_input(prompt, required=True, default=None):
    """Get user input with styling"""
    while True:
        if default:
            val = input(f"    {C.CHAMPAGNE}► {prompt}{C.DIM} (default: {default}){C.CHAMPAGNE}: {C.END}").strip()
            if not val:
                return default
        else:
            val = input(f"    {C.CHAMPAGNE}► {prompt}: {C.END}").strip()
        if val or not required:
            return val
        print(f"    {C.RED}✗ Required field.{C.END}")


def display_menu():
    """Display resource type menu"""
    print(f"\n{C.CHAMPAGNE}{C.BOLD}                         🎤 SELECT YOUR RESOURCE TYPE 🎤{C.END}\n")
    for num, key, name, emoji in MENU_ITEMS:
        print(f"    {C.GOLD}[{num}]{C.END} {emoji}  {C.BOLD}{name}{C.END}")
    print(f"\n    {C.RED}[0]{C.END} 🚪  {C.BOLD}Exit{C.END}\n")


def get_choice():
    """Get user menu choice"""
    while True:
        choice = input(f"    {C.OVO}🎯 Enter choice (0-8): {C.END}").strip()
        if choice == "0":
            return None
        for num, key, name, _ in MENU_ITEMS:
            if choice == num:
                print(f"\n    {C.GREEN}✓ Selected: {name}{C.END}")
                return key
        print(f"    {C.RED}✗ Invalid choice.{C.END}")


def collect_inputs(resource_key):
    """Collect inputs for name generation"""
    print(f"\n{C.CHAMPAGNE}{C.BOLD}                         🎹 ENTER RESOURCE DETAILS 🎹{C.END}\n")
    print(f"{C.DIM}    Type 'drizzy' for a random Drake track name{C.END}")

    workload = get_input("Workload/Application name")
    if workload.lower() in ["drizzy", "drake", "ovo", "certified", "rando"]:
        song = random.choice(DRAKE_SONGS)
        print(f"\n{C.GOLD}{C.BOLD}    🎵 DRIZZY MODE: {C.CHAMPAGNE}♫ {song} ♫{C.END}\n")
        workload = song

    print(f"\n{C.DIM}    Environments: {', '.join(ENVIRONMENTS[:5])}{C.END}")
    environment = get_input("Environment")

    region = ""
    if RESOURCE_TYPES[resource_key].requires_region:
        print(f"\n{C.DIM}    Examples: {', '.join(AZURE_REGIONS[:4])}{C.END}")
        region = get_input("Azure region")

    instance = get_input("Instance number", default="001")
    return workload, environment, region, instance


def get_yes_no(prompt):
    """Get Y/N input from user"""
    while True:
        val = input(f"    {C.CHAMPAGNE}► {prompt} (y/n): {C.END}").strip().lower()
        if val in ['y', 'yes']:
            return True
        if val in ['n', 'no']:
            return False
        print(f"    {C.RED}✗ Please enter y or n.{C.END}")


def display_result(resource_key, name, pip_name=None):
    """Display generated name with validation"""
    resource = RESOURCE_TYPES[resource_key]
    is_valid, error = resource.validate(name)

    # If pip_name provided, also validate it
    pip_valid = True
    pip_error = None
    if pip_name:
        pip_resource = RESOURCE_TYPES["public_ip"]
        pip_valid, pip_error = pip_resource.validate(pip_name)

    all_valid = is_valid and pip_valid

    if all_valid:
        print(C.PLATINUM + """
                    ═══════════════════════════════════
                 ═══════════════╔═══════════╗═══════════════
                 ═══════════════║ PLATINUM  ║═══════════════
                 ═══════════════║ CERTIFIED ║═══════════════
                 ═══════════════╚═══════════╝═══════════════
                    ═══════════════════════════════════""" + C.END)
        print(f"\n    {C.GOLD}{C.BOLD}🏆  C E R T I F I E D   F R E S H  🏆{C.END}\n")
    else:
        print(f"\n    {C.RED}⚠️  VALIDATION FAILED  ⚠️{C.END}\n")

    name_color = C.GREEN if is_valid else C.RED
    scope_color = C.RED if resource.scope == "Global" else C.CHAMPAGNE

    print(f"    {C.DIM}Resource Type:{C.END}  {C.CYAN}{resource.name}{C.END}")
    print(f"    {C.DIM}Generated Name:{C.END} {name_color}{C.BOLD}{name}{C.END}")
    print(f"    {C.DIM}Length:{C.END}         {len(name)} chars")
    print(f"    {C.DIM}Scope:{C.END}          {scope_color}{resource.scope}{' (GLOBALLY UNIQUE!)' if resource.scope == 'Global' else ''}{C.END}")
    print(f"    {C.DIM}Pattern:{C.END}        {C.BLUE}{resource.pattern_template}{C.END}")

    # Display Public IP details if provided
    if pip_name:
        pip_resource = RESOURCE_TYPES["public_ip"]
        pip_name_color = C.GREEN if pip_valid else C.RED
        pip_scope_color = C.RED if pip_resource.scope == "Global" else C.CHAMPAGNE

        print(f"\n    {C.DIM}Resource Type:{C.END}  {C.CYAN}{pip_resource.name}{C.END}")
        print(f"    {C.DIM}Generated Name:{C.END} {pip_name_color}{C.BOLD}{pip_name}{C.END}")
        print(f"    {C.DIM}Length:{C.END}         {len(pip_name)} chars")
        print(f"    {C.DIM}Scope:{C.END}          {pip_scope_color}{pip_resource.scope}{' (GLOBALLY UNIQUE!)' if pip_resource.scope == 'Global' else ''}{C.END}")
        print(f"    {C.DIM}Pattern:{C.END}        {C.BLUE}{pip_resource.pattern_template}{C.END}")

    if all_valid:
        print(f"\n    {C.GREEN}{C.BOLD}✓ VALIDATION PASSED 🏆{C.END}\n")
    else:
        if not is_valid:
            print(f"\n    {C.RED}{C.BOLD}✗ {error}{C.END}")
        if pip_name and not pip_valid:
            print(f"\n    {C.RED}{C.BOLD}✗ Public IP: {pip_error}{C.END}")
        print()


def main():
    print(HEADER)
    while True:
        display_menu()
        resource_key = get_choice()
        if not resource_key:
            sys.exit(0)

        workload, env, region, instance = collect_inputs(resource_key)

        # VPN Gateway special flow - ask about Public IP before displaying results
        pip_name = None
        if resource_key == "vpn_gateway":
            print(f"\n{C.CHAMPAGNE}{C.BOLD}                    🌐 VPN GATEWAY PUBLIC IP ADDRESS 🌐{C.END}\n")
            print(f"    {C.DIM}VPN Gateways require a Public IP address in Azure Portal.{C.END}")
            print(f"    {C.DIM}CAF recommends naming convention: pip-<workload>-<env>-<region>-<instance>{C.END}\n")

            if get_yes_no("Also generate Public IP address name"):
                pip_name = True  # Flag to generate pip name after vpn name is created

        animate("Applying CAF Best Practices", 1.0)

        name = generate_name(resource_key, workload, env, region, instance)

        # Generate Public IP name if requested
        if pip_name:
            pip_name = f"pip-{name}"

        display_result(resource_key, name, pip_name)

        if input(f"    {C.OVO}🎤 Generate another? (y/n): {C.END}").strip().lower() not in ['y', 'yes']:
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

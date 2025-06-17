# onionvuln_pro.py - OnionVuln 2025 Edition
# Ethical Security Toolkit by OnionVuln (No API Key Needed)

import hashlib
import requests
import webbrowser
import socket
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console()

# Banner Display
def banner():
    console.print(Panel("""
  [bold red]██████  ██████  ███    ██ ██ ███    ██ ██    ██ ██      ██ ███    ██[/]
 [bold red]██      ██    ██ ████   ██ ██ ████   ██ ██    ██ ██      ██ ████   ██[/]
 [bold red]██      ██    ██ ██ ██  ██ ██ ██ ██  ██ ██    ██ ██      ██ ██ ██  ██[/]
 [bold red]██      ██    ██ ██  ██ ██ ██ ██  ██ ██ ██    ██ ██      ██ ██  ██ ██[/]
  [bold red]██████  ██████  ██   ████ ██ ██   ████  ██████  ███████ ██ ██   ████[/]
           [green]OnionVuln 2025 - Ethical OSINT & Security Suite[/]
    """, title="[cyan]Welcome to OnionVuln", subtitle="[blue]Ethical Edition", style="bold white"))

# 1. Password Pwned Check

def check_password_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    console.print("\n[cyan]Checking if password has been leaked...[/]")
    try:
        res = requests.get(url)
        for line in res.text.splitlines():
            h, count = line.split(":")
            if h == suffix:
                console.print(f"[red bold]⚠️  This password appeared {count} times in public breaches![/]")
                return
        console.print("[green bold]✅ Password not found in known breaches.[/]")
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")

# 2. DuckDuckGo OSINT Leak Search

def search_email_leaks(email):
    query = f"\"{email}\" site:pastebin.com OR site:throwbin.io OR site:anonfiles.com"
    search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
    console.print("\n[cyan]Opening browser for OSINT email leak search...[/]")
    webbrowser.open(search_url)

# 3. IP Info (SHODAN-style lightweight)

def shodan_eyes(ip):
    console.print(f"\n[cyan]Fetching public data for:[/] [bold]{ip}[/]")
    try:
        host = socket.gethostbyaddr(ip)[0]
        console.print(f" - Hostname: {host}")
    except:
        console.print(" - Hostname: [yellow]Unavailable[/]")
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json").json()
        console.print(f" - Location: {r.get('city')} {r.get('region')} {r.get('country')}")
        console.print(f" - Org: {r.get('org')}")
    except:
        console.print(" - IPInfo: [yellow]Unavailable[/]")

# 4. Google Dorks for Email Breach Detection

def dork_email_search(email):
    console.print(f"\n[cyan]Using Google Dorks for breach info on:[/] {email}")
    dork = f"\"{email}\" intext:password | intext:pass site:pastebin.com"
    url = f"https://www.google.com/search?q={dork.replace(' ', '+')}"
    webbrowser.open(url)
    console.print("[green]Opened Google search for possible breaches.[/]")

# 5. Tips

def password_tips():
    tips = [
        "Use 12+ characters with upper/lowercase, symbols, and numbers",
        "Enable 2FA on all important accounts",
        "Don’t reuse passwords",
        "Use a trusted password manager",
        "Avoid entering passwords on public/shared computers"
    ]
    table = Table(title="Security Tips", box=box.HEAVY)
    table.add_column("#", style="cyan", width=5)
    table.add_column("Tip", style="white")
    for idx, tip in enumerate(tips, 1):
        table.add_row(str(idx), tip)
    console.print(table)

# 6. Recovery Help

def recovery_links():
    links = {
        "Facebook": "https://www.facebook.com/hacked",
        "Instagram": "https://www.instagram.com/hacked/",
        "Gmail": "https://accounts.google.com/signin/recovery"
    }
    table = Table(title="Recovery Portals", box=box.SQUARE_DOUBLE_HEAD)
    table.add_column("Platform", style="cyan")
    table.add_column("Link", style="magenta")
    for name, link in links.items():
        table.add_row(name, link)
    console.print(table)
    if Prompt.ask("Open Gmail recovery in browser?", choices=["y", "n"], default="n") == "y":
        webbrowser.open(links["Gmail"])

# Main Menu

def main():
    banner()
    while True:
        console.print("\n[yellow]Menu:[/]")
        console.print("[1] Check if password is leaked")
        console.print("[2] Search OSINT email leaks (DuckDuckGo)")
        console.print("[3] SHODAN Eyes Lite (IP public data)")
        console.print("[4] Google Dork email breach search")
        console.print("[5] Security tips")
        console.print("[6] Account recovery help")
        console.print("[7] Exit")

        choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "5", "6", "7"])
        if choice == "1":
            pw = Prompt.ask("Enter password (hidden)", password=True)
            check_password_pwned(pw)
        elif choice == "2":
            email = Prompt.ask("Enter email to search")
            search_email_leaks(email)
        elif choice == "3":
            ip = Prompt.ask("Enter IP address (e.g. 8.8.8.8)")
            shodan_eyes(ip)
        elif choice == "4":
            email = Prompt.ask("Enter email")
            dork_email_search(email)
        elif choice == "5":
            password_tips()
        elif choice == "6":
            recovery_links()
        elif choice == "7":
            console.print("\n[bold green]Thank you for using OnionVuln. Stay secure![/]")
            break

if __name__ == "__main__":
    main()

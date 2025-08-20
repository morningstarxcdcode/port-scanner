"""
Open Source Intelligence (OSINT) Module
Author: morningstarxcdcode
Description: Comprehensive OSINT gathering and analysis tools
"""

import asyncio
import base64
import json
import re
import socket
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse

import requests
import whois
from bs4 import BeautifulSoup

from config.config_manager import config
from utils.logger import get_logger

logger = get_logger()


@dataclass
class OSINTResult:
    """Represents OSINT intelligence data."""

    source: str
    category: str
    data: Dict
    confidence: float
    timestamp: str


@dataclass
class DomainInfo:
    """Comprehensive domain information."""

    domain: str
    registrar: str
    creation_date: Optional[str]
    expiration_date: Optional[str]
    name_servers: List[str]
    emails: List[str]
    phone_numbers: List[str]
    addresses: List[str]
    subdomains: List[str]
    ip_addresses: List[str]
    technologies: List[str]
    certificates: List[Dict]
    social_media: Dict[str, str]


class OSINTGatherer:
    """Advanced OSINT collection and analysis engine."""

    def __init__(self):
        self.logger = get_logger()
        self.results = []
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": config.get(
                    "scanning.user_agent",
                    "Mozilla/5.0 (compatible; Advanced-Port-Scanner/1.0)",
                )
            }
        )

        # Common subdomain wordlist
        self.common_subdomains = [
            "www",
            "mail",
            "ftp",
            "admin",
            "test",
            "dev",
            "staging",
            "api",
            "blog",
            "shop",
            "store",
            "secure",
            "vpn",
            "remote",
            "portal",
            "dashboard",
            "panel",
            "cpanel",
            "webmail",
            "email",
            "mx",
            "ns1",
            "ns2",
            "dns",
            "server",
            "host",
            "cdn",
            "static",
            "assets",
            "img",
            "images",
            "media",
            "files",
            "download",
            "upload",
            "backup",
            "old",
            "new",
            "beta",
            "alpha",
            "demo",
        ]

    async def gather_intelligence(self, target: str) -> Dict:
        """Gather comprehensive OSINT data."""
        self.logger.info(f"🕵️ Starting OSINT gathering for {target}")

        # Determine if target is IP or domain
        is_ip = self.is_ip_address(target)

        if is_ip:
            return await self.gather_ip_intelligence(target)
        else:
            return await self.gather_domain_intelligence(target)

    def is_ip_address(self, target: str) -> bool:
        """Check if target is an IP address."""
        try:
            socket.inet_aton(target)
            return True
        except socket.error:
            return False

    async def gather_domain_intelligence(self, domain: str) -> Dict:
        """Gather intelligence on a domain."""
        intelligence = {
            "domain": domain,
            "whois": {},
            "dns": {},
            "subdomains": [],
            "technologies": [],
            "social_media": {},
            "certificates": [],
            "geolocation": {},
            "reputation": {},
            "related_domains": [],
            "breach_data": {},
        }

        # Run parallel intelligence gathering
        tasks = [
            self.get_whois_info(domain),
            self.get_dns_info(domain),
            self.discover_subdomains(domain),
            self.detect_technologies(domain),
            self.find_social_media(domain),
            self.get_ssl_certificates(domain),
            self.get_geolocation(domain),
            self.check_reputation(domain),
            self.find_related_domains(domain),
            self.check_breach_data(domain),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        intelligence["whois"] = (
            results[0] if not isinstance(results[0], Exception) else {}
        )
        intelligence["dns"] = (
            results[1] if not isinstance(results[1], Exception) else {}
        )
        intelligence["subdomains"] = (
            results[2] if not isinstance(results[2], Exception) else []
        )
        intelligence["technologies"] = (
            results[3] if not isinstance(results[3], Exception) else []
        )
        intelligence["social_media"] = (
            results[4] if not isinstance(results[4], Exception) else {}
        )
        intelligence["certificates"] = (
            results[5] if not isinstance(results[5], Exception) else []
        )
        intelligence["geolocation"] = (
            results[6] if not isinstance(results[6], Exception) else {}
        )
        intelligence["reputation"] = (
            results[7] if not isinstance(results[7], Exception) else {}
        )
        intelligence["related_domains"] = (
            results[8] if not isinstance(results[8], Exception) else []
        )
        intelligence["breach_data"] = (
            results[9] if not isinstance(results[9], Exception) else {}
        )

        return intelligence

    async def gather_ip_intelligence(self, ip: str) -> Dict:
        """Gather intelligence on an IP address."""
        intelligence = {
            "ip": ip,
            "geolocation": {},
            "whois": {},
            "reputation": {},
            "reverse_dns": "",
            "open_ports": [],
            "technologies": [],
            "certificates": [],
        }

        tasks = [
            self.get_ip_geolocation(ip),
            self.get_ip_whois(ip),
            self.check_ip_reputation(ip),
            self.get_reverse_dns(ip),
            self.scan_common_ports(ip),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        intelligence["geolocation"] = (
            results[0] if not isinstance(results[0], Exception) else {}
        )
        intelligence["whois"] = (
            results[1] if not isinstance(results[1], Exception) else {}
        )
        intelligence["reputation"] = (
            results[2] if not isinstance(results[2], Exception) else {}
        )
        intelligence["reverse_dns"] = (
            results[3] if not isinstance(results[3], Exception) else ""
        )
        intelligence["open_ports"] = (
            results[4] if not isinstance(results[4], Exception) else []
        )

        return intelligence

    async def get_whois_info(self, domain: str) -> Dict:
        """Get WHOIS information for domain."""
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": (
                    str(w.expiration_date) if w.expiration_date else None
                ),
                "updated_date": str(w.updated_date) if w.updated_date else None,
                "name_servers": w.name_servers if w.name_servers else [],
                "emails": w.emails if w.emails else [],
                "org": w.org,
                "country": w.country,
                "status": w.status if w.status else [],
            }
        except Exception as e:
            self.logger.debug(f"WHOIS lookup failed for {domain}: {e}")
            return {}

    async def get_dns_info(self, domain: str) -> Dict:
        """Get comprehensive DNS information."""
        dns_info = {
            "A": [],
            "AAAA": [],
            "MX": [],
            "NS": [],
            "TXT": [],
            "CNAME": [],
            "SOA": [],
        }

        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

        for record_type in record_types:
            try:
                result = subprocess.run(
                    ["dig", "+short", record_type, domain],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    records = [
                        line.strip()
                        for line in result.stdout.split("\n")
                        if line.strip()
                    ]
                    dns_info[record_type] = records
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # dig not available or timeout
                continue

        return dns_info

    async def discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains using multiple techniques."""
        subdomains = set()

        # Method 1: Brute force common subdomains
        for subdomain in self.common_subdomains:
            full_domain = f"{subdomain}.{domain}"
            if await self.check_subdomain_exists(full_domain):
                subdomains.add(full_domain)

        # Method 2: Certificate transparency logs
        ct_subdomains = await self.get_ct_subdomains(domain)
        subdomains.update(ct_subdomains)

        # Method 3: Search engine enumeration
        search_subdomains = await self.search_engine_subdomains(domain)
        subdomains.update(search_subdomains)

        return list(subdomains)

    async def check_subdomain_exists(self, subdomain: str) -> bool:
        """Check if a subdomain exists."""
        try:
            socket.gethostbyname(subdomain)
            return True
        except socket.gaierror:
            return False

    async def get_ct_subdomains(self, domain: str) -> Set[str]:
        """Get subdomains from Certificate Transparency logs."""
        subdomains = set()

        try:
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                certificates = response.json()
                for cert in certificates:
                    name_value = cert.get("name_value", "")
                    for name in name_value.split("\n"):
                        name = name.strip()
                        if name.endswith(f".{domain}") and not name.startswith("*"):
                            subdomains.add(name)
        except Exception as e:
            self.logger.debug(f"Certificate transparency lookup failed: {e}")

        return subdomains

    async def search_engine_subdomains(self, domain: str) -> Set[str]:
        """Find subdomains using search engines."""
        subdomains = set()

        # Google search
        try:
            query = f"site:{domain}"
            url = f"https://www.google.com/search?q={query}&num=100"
            headers = {"User-Agent": self.session.headers["User-Agent"]}

            response = self.session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a")

                for link in links:
                    href = link.get("href")
                    if href and "url?q=" in href:
                        url = href.split("url?q=")[1].split("&")[0]
                        parsed = urlparse(url)
                        if parsed.hostname and parsed.hostname.endswith(f".{domain}"):
                            subdomains.add(parsed.hostname)
        except Exception as e:
            self.logger.debug(f"Search engine enumeration failed: {e}")

        return subdomains

    async def detect_technologies(self, domain: str) -> List[str]:
        """Detect technologies used by the website."""
        technologies = []

        try:
            url = f"http://{domain}"
            response = self.session.get(url, timeout=10, allow_redirects=True)

            # Check headers for technology indicators
            headers = response.headers

            # Server header
            server = headers.get("Server", "")
            if "nginx" in server.lower():
                technologies.append("Nginx")
            elif "apache" in server.lower():
                technologies.append("Apache")
            elif "iis" in server.lower():
                technologies.append("IIS")

            # X-Powered-By header
            powered_by = headers.get("X-Powered-By", "")
            if "php" in powered_by.lower():
                technologies.append("PHP")
            elif "asp.net" in powered_by.lower():
                technologies.append("ASP.NET")

            # Check HTML content for technology indicators
            content = response.text.lower()

            if "wordpress" in content or "wp-content" in content:
                technologies.append("WordPress")
            if "drupal" in content:
                technologies.append("Drupal")
            if "joomla" in content:
                technologies.append("Joomla")
            if "jquery" in content:
                technologies.append("jQuery")
            if "bootstrap" in content:
                technologies.append("Bootstrap")
            if "angular" in content:
                technologies.append("AngularJS")
            if "react" in content:
                technologies.append("React")
            if "vue" in content:
                technologies.append("Vue.js")

        except Exception as e:
            self.logger.debug(f"Technology detection failed: {e}")

        return list(set(technologies))

    async def find_social_media(self, domain: str) -> Dict[str, str]:
        """Find social media profiles associated with domain."""
        social_media = {}

        try:
            url = f"http://{domain}"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text

                # Common social media patterns
                patterns = {
                    "facebook": r"facebook\.com/([a-zA-Z0-9._-]+)",
                    "twitter": r"twitter\.com/([a-zA-Z0-9._-]+)",
                    "linkedin": r"linkedin\.com/(?:company|in)/([a-zA-Z0-9._-]+)",
                    "instagram": r"instagram\.com/([a-zA-Z0-9._-]+)",
                    "youtube": r"youtube\.com/(?:channel|user|c)/([a-zA-Z0-9._-]+)",
                    "github": r"github\.com/([a-zA-Z0-9._-]+)",
                }

                for platform, pattern in patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        social_media[platform] = matches[0]

        except Exception as e:
            self.logger.debug(f"Social media search failed: {e}")

        return social_media

    async def get_ssl_certificates(self, domain: str) -> List[Dict]:
        """Get SSL certificate information."""
        certificates = []

        try:
            # Use crt.sh API
            url = f"https://crt.sh/?q={domain}&output=json"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                cert_data = response.json()
                for cert in cert_data[:10]:  # Limit to first 10
                    certificates.append(
                        {
                            "id": cert.get("id"),
                            "issuer": cert.get("issuer_name"),
                            "not_before": cert.get("not_before"),
                            "not_after": cert.get("not_after"),
                            "common_name": cert.get("common_name"),
                            "serial_number": cert.get("serial_number"),
                        }
                    )

        except Exception as e:
            self.logger.debug(f"SSL certificate lookup failed: {e}")

        return certificates

    async def get_geolocation(self, domain: str) -> Dict:
        """Get geolocation information for domain."""
        try:
            # First resolve domain to IP
            ip = socket.gethostbyname(domain)
            return await self.get_ip_geolocation(ip)
        except Exception as e:
            self.logger.debug(f"Geolocation lookup failed: {e}")
            return {}

    async def get_ip_geolocation(self, ip: str) -> Dict:
        """Get geolocation information for IP address."""
        try:
            # Using ipapi.co (free tier)
            url = f"https://ipapi.co/{ip}/json/"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    "ip": ip,
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country_name"),
                    "country_code": data.get("country_code"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude"),
                    "timezone": data.get("timezone"),
                    "isp": data.get("org"),
                    "asn": data.get("asn"),
                }
        except Exception as e:
            self.logger.debug(f"IP geolocation lookup failed: {e}")

        return {}

    async def check_reputation(self, domain: str) -> Dict:
        """Check domain reputation using multiple sources."""
        reputation = {
            "malicious": False,
            "suspicious": False,
            "phishing": False,
            "malware": False,
            "sources": [],
        }

        # Check against known reputation sources
        # This is a simplified implementation
        try:
            # VirusTotal API (requires API key)
            vt_api_key = config.get_api_key("virustotal")
            if vt_api_key:
                url = f"https://www.virustotal.com/vtapi/v2/domain/report"
                params = {"apikey": vt_api_key, "domain": domain}
                response = self.session.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("response_code") == 1:
                        positives = data.get("positives", 0)
                        total = data.get("total", 0)

                        if positives > 0:
                            reputation["malicious"] = True
                            reputation["sources"].append(
                                f"VirusTotal: {positives}/{total}"
                            )

        except Exception as e:
            self.logger.debug(f"Reputation check failed: {e}")

        return reputation

    async def check_ip_reputation(self, ip: str) -> Dict:
        """Check IP reputation."""
        reputation = {
            "malicious": False,
            "suspicious": False,
            "tor_exit": False,
            "proxy": False,
            "sources": [],
        }

        try:
            # Check if IP is a Tor exit node
            if await self.is_tor_exit_node(ip):
                reputation["tor_exit"] = True
                reputation["suspicious"] = True
                reputation["sources"].append("Tor Exit Node")

        except Exception as e:
            self.logger.debug(f"IP reputation check failed: {e}")

        return reputation

    async def is_tor_exit_node(self, ip: str) -> bool:
        """Check if IP is a Tor exit node."""
        try:
            url = "https://check.torproject.org/torbulkexitlist"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                tor_ips = response.text.split("\n")
                return ip in tor_ips
        except Exception:
            pass

        return False

    async def find_related_domains(self, domain: str) -> List[str]:
        """Find related domains."""
        related = []

        try:
            # Extract base domain for variations
            base = domain.split(".")[0]

            # Common domain variations
            variations = [
                f"{base}.net",
                f"{base}.org",
                f"{base}.info",
                f"{base}.biz",
                f"www{base}.com",
                f"{base}s.com",
                f"{base}-online.com",
                f"{base}.co",
            ]

            for variation in variations:
                if await self.check_subdomain_exists(variation):
                    related.append(variation)

        except Exception as e:
            self.logger.debug(f"Related domain search failed: {e}")

        return related

    async def check_breach_data(self, domain: str) -> Dict:
        """Check for breach data associated with domain."""
        breach_data = {
            "breaches": [],
            "paste_count": 0,
            "breach_count": 0,
        }

        try:
            # Have I Been Pwned API (requires API key for domain search)
            hibp_key = config.get_api_key("have_i_been_pwned")
            if hibp_key:
                url = f"https://haveibeenpwned.com/api/v3/breaches"
                headers = {"hibp-api-key": hibp_key}
                response = self.session.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    breaches = response.json()
                    domain_breaches = [
                        breach
                        for breach in breaches
                        if domain.lower() in breach.get("Domain", "").lower()
                    ]
                    breach_data["breaches"] = domain_breaches
                    breach_data["breach_count"] = len(domain_breaches)

        except Exception as e:
            self.logger.debug(f"Breach data check failed: {e}")

        return breach_data

    async def get_ip_whois(self, ip: str) -> Dict:
        """Get WHOIS information for IP address."""
        try:
            result = subprocess.run(
                ["whois", ip], capture_output=True, text=True, timeout=15
            )

            if result.returncode == 0:
                whois_data = result.stdout

                # Parse key information
                info = {}
                for line in whois_data.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()

                        if key in ["netname", "orgname", "country", "descr"]:
                            info[key] = value

                return info

        except Exception as e:
            self.logger.debug(f"IP WHOIS lookup failed: {e}")

        return {}

    async def get_reverse_dns(self, ip: str) -> str:
        """Get reverse DNS for IP address."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except socket.herror:
            return ""

    async def scan_common_ports(self, ip: str) -> List[int]:
        """Quick scan of common ports."""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443]
        open_ports = []

        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except Exception:
                continue

        return open_ports

    def generate_osint_report(self, intelligence: Dict) -> str:
        """Generate formatted OSINT report."""
        if "domain" in intelligence:
            return self.generate_domain_report(intelligence)
        else:
            return self.generate_ip_report(intelligence)

    def generate_domain_report(self, intelligence: Dict) -> str:
        """Generate domain intelligence report."""
        domain = intelligence["domain"]
        report = f"""
🕵️  OSINT INTELLIGENCE REPORT - {domain.upper()}
{'=' * 60}

📋 DOMAIN INFORMATION:
{'─' * 30}
Domain: {domain}
Registrar: {intelligence['whois'].get('registrar', 'Unknown')}
Created: {intelligence['whois'].get('creation_date', 'Unknown')}
Expires: {intelligence['whois'].get('expiration_date', 'Unknown')}
Country: {intelligence['whois'].get('country', 'Unknown')}

🌐 DNS RECORDS:
{'─' * 30}
A Records: {', '.join(intelligence['dns'].get('A', []))}
MX Records: {', '.join(intelligence['dns'].get('MX', []))}
NS Records: {', '.join(intelligence['dns'].get('NS', []))}

🔍 SUBDOMAINS DISCOVERED ({len(intelligence['subdomains'])}):
{'─' * 30}
{chr(10).join(f"  • {sub}" for sub in intelligence['subdomains'][:20])}
{f"  ... and {len(intelligence['subdomains']) - 20} more" if len(intelligence['subdomains']) > 20 else ""}

⚙️  TECHNOLOGIES DETECTED:
{'─' * 30}
{chr(10).join(f"  • {tech}" for tech in intelligence['technologies'])}

📱 SOCIAL MEDIA PRESENCE:
{'─' * 30}
{chr(10).join(f"  • {platform}: {profile}" for platform, profile in intelligence['social_media'].items())}

🌍 GEOLOCATION:
{'─' * 30}
Country: {intelligence['geolocation'].get('country', 'Unknown')}
City: {intelligence['geolocation'].get('city', 'Unknown')}
ISP: {intelligence['geolocation'].get('isp', 'Unknown')}

🛡️  SECURITY STATUS:
{'─' * 30}
Malicious: {'❌ YES' if intelligence['reputation'].get('malicious') else '✅ NO'}
Suspicious: {'⚠️  YES' if intelligence['reputation'].get('suspicious') else '✅ NO'}
Breach Data: {intelligence['breach_data'].get('breach_count', 0)} breaches found

🔒 SSL CERTIFICATES ({len(intelligence['certificates'])}):
{'─' * 30}
{chr(10).join(f"  • Issuer: {cert.get('issuer', 'Unknown')}" for cert in intelligence['certificates'][:5])}

🔗 RELATED DOMAINS:
{'─' * 30}
{chr(10).join(f"  • {domain}" for domain in intelligence['related_domains'])}

"""
        return report

    def generate_ip_report(self, intelligence: Dict) -> str:
        """Generate IP intelligence report."""
        ip = intelligence["ip"]
        report = f"""
🕵️  OSINT INTELLIGENCE REPORT - {ip}
{'=' * 60}

🌐 IP INFORMATION:
{'─' * 30}
IP Address: {ip}
Reverse DNS: {intelligence.get('reverse_dns', 'None')}

🌍 GEOLOCATION:
{'─' * 30}
Country: {intelligence['geolocation'].get('country', 'Unknown')}
City: {intelligence['geolocation'].get('city', 'Unknown')}
Region: {intelligence['geolocation'].get('region', 'Unknown')}
ISP: {intelligence['geolocation'].get('isp', 'Unknown')}
ASN: {intelligence['geolocation'].get('asn', 'Unknown')}

🔓 OPEN PORTS:
{'─' * 30}
{', '.join(map(str, intelligence['open_ports'])) if intelligence['open_ports'] else 'None detected'}

🛡️  SECURITY STATUS:
{'─' * 30}
Malicious: {'❌ YES' if intelligence['reputation'].get('malicious') else '✅ NO'}
Tor Exit Node: {'⚠️  YES' if intelligence['reputation'].get('tor_exit') else '✅ NO'}
Proxy: {'⚠️  YES' if intelligence['reputation'].get('proxy') else '✅ NO'}

📋 WHOIS INFORMATION:
{'─' * 30}
Organization: {intelligence['whois'].get('orgname', 'Unknown')}
Network: {intelligence['whois'].get('netname', 'Unknown')}
Country: {intelligence['whois'].get('country', 'Unknown')}

"""
        return report


async def run_osint_scan(target: str) -> Dict:
    """Run comprehensive OSINT scan."""
    gatherer = OSINTGatherer()
    return await gatherer.gather_intelligence(target)

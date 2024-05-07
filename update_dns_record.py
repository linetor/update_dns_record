import requests
import json

import os
vault_addr = os.environ.get("VAULT_ADDR")
vault_token = os.environ.get("VAULT_TOKEN")



def update_dns_record(zone_id, record_name, record_id, new_ip , api_token,mail):
    """
    Cloudflare DNS 레코드를 업데이트합니다.

    Args:
        zone_id: Cloudflare Zone ID
        record_name: DNS 레코드 이름 (예: example.com)
        record_type: DNS 레코드 유형 (예: A)
        new_ip: 새로운 IP 주소
    """

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "X-Auth-Key": f"{api_token}",
        "Content-Type": "application/json",
        "X-Auth-Email": mail,
    }
    payload = {
        "content": new_ip,
        "name": "linetor.in",
        'type':'A'
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"DNS 레코드 업데이트 완료: {record_name} -> {new_ip}")
    else:
        print(f"DNS 레코드 업데이트 실패: {response.status_code}")

import json
def get_external_ip():
    response = requests.get('https://api64.ipify.org?format=json')
    if response.status_code == 200:
        return json.loads(response.text)['ip']
    else:
        raise Exception('외부 IP 주소를 가져오는데 실패했습니다.')

def get_vault_configuration(endpoint):
    endpoint = f"{vault_addr}/v1/kv/data/{endpoint}"

    # HTTP GET 요청을 통해 데이터를 가져옵니다.
    headers = {"X-Vault-Token": vault_token}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']['data']

    else:
        # 에러 응답의 경우 예외를 발생시킵니다.
        response.raise_for_status()

if __name__ == "__main__":

    import requests
    cloudflare_info = get_vault_configuration("update_dns")
    api_token = cloudflare_info['api_token']
    record_name = cloudflare_info['record_name']
    record_type = cloudflare_info['record_type']
    record_id  = cloudflare_info['record_id']
    zone_id = cloudflare_info['zone_id']
    mail = cloudflare_info['mail']

    new_ip = get_external_ip()  # 현재 IP 주소를 가져오는 함수를 구현해야 합니다.
    update_dns_record(zone_id, record_name, record_id, new_ip,api_token,mail)
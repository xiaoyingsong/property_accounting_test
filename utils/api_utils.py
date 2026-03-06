import requests
from config.config import SELF_SYSTEM_API, THIRD_PARTY_API
from utils.log_utils import logger

# 自研系统对接工具（优先）
def sync_bill_to_self_system(bill_data):
    """同步账单至自研系统，核心对接场景"""
    try:
        url = f"{SELF_SYSTEM_API['base_url']}/sync-bill"
        headers = {
            "Authorization": f"Bearer {SELF_SYSTEM_API['token']}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=bill_data, timeout=10)
        response.raise_for_status()  # 触发HTTP异常（4xx/5xx）
        resp_json = response.json()
        logger.info(f"账单同步至自研系统成功：bill_id={bill_data['bill_id']}，状态={resp_json['data']['sync_status']}")
        return resp_json
    except requests.exceptions.RequestException as e:
        logger.error(f"账单同步至自研系统失败：{str(e)}")
        raise

# 第三方系统对接工具（次要）
def sync_bill_to_third_party(bill_data):
    """同步账单至第三方会计系统，次要对接场景"""
    try:
        url = f"{THIRD_PARTY_API['base_url']}/sync-bill"
        headers = {
            "Authorization": f"Bearer {THIRD_PARTY_API['token']}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=bill_data, timeout=10)
        response.raise_for_status()
        resp_json = response.json()
        logger.info(f"账单同步至第三方系统成功：bill_id={bill_data['bill_id']}，状态={resp_json['data']['sync_status']}")
        return resp_json
    except requests.exceptions.RequestException as e:
        logger.error(f"账单同步至第三方系统失败：{str(e)}")
        raise

def query_sync_status(bill_id, docking_type):
    """查询同步状态，区分自研/第三方对接场景"""
    try:
        if docking_type == "self_system":
            url = f"{SELF_SYSTEM_API['base_url']}/sync/status"
            headers = {"Authorization": f"Bearer {SELF_SYSTEM_API['token']}"}
        else:
            url = f"{THIRD_PARTY_API['base_url']}/sync/status"
            headers = {"Authorization": f"Bearer {THIRD_PARTY_API['token']}"}
        params = {"bill_id": bill_id}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        sync_status = response.json()["data"]["sync_status"]
        logger.info(f"查询同步状态成功：bill_id={bill_id}，对接场景={docking_type}，状态={sync_status}")
        return sync_status
    except Exception as e:
        logger.error(f"查询同步状态失败：{str(e)}，对接场景={docking_type}")
        raise
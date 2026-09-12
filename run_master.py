import subprocess
import time
import os
import sys
import requests # 新增 requests 模組來呼叫 API

os.environ["PYTHONIOENCODING"] = "utf-8"

# ⚠️ 注意：GitHub Actions 是雲端 Linux 伺服器，找不到 Windows 的 C 槽
# 建議將路徑改為相對路徑（例如 "./Chip_Analyzer"），這裡先保留你原有的設定
CHIP_ANALYZER_PATH = r"C:\Users\kweiw\Desktop\我的專案\Chip_Analyzer"  
DNA_ASSISTANT_PATH = r"C:\Users\kweiw\Desktop\我的專案\股票"     
TELEGRAM_BOT_PATH = r"C:\Users\kweiw\Desktop\我的專案\taiwan_stock_bot" 

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    print(f"Telegram API 回應: {response.text}")  # 印出回應方便在 GitHub Actions 記錄中檢查
    return response.json()

def run_step(script_name, folder_path):
    print(f"\n🚀 正在執行：{script_name} ...")
    # 加上 "-X", "utf8" 強制讓子程式以 UTF-8 執行，避免 Windows 終端機編碼崩潰
    result = subprocess.run(["python", "-X", "utf8", script_name], cwd=folder_path, capture_output=True, text=True, encoding="utf-8")
    
    if result.returncode == 0:
        print(f"✅ {script_name} 執行成功！")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"❌ {script_name} 執行失敗！錯誤訊息：")
        print(result.stderr)
        raise RuntimeError(f"{script_name} 執行中斷")

if __name__ == "__main__":
    print("="*50)
    print("🎯 開始執行台股量化選股與推播總指揮流程")
    print("="*50)
    
    try:
        # 測試：一啟動就先發一條訊息，確保 Token 和 Chat ID 沒問題
        send_telegram_message("🚀 台股總指揮系統啟動中！正在執行 GitHub Actions...")
        
        # 第一步：執行籌碼下載與分析 (對應 Chip_Analyzer 內的下載主程式)
        run_step("main_chip.py", CHIP_ANALYZER_PATH)
        
        # 稍作等待確保檔案順利寫入硬碟
        time.sleep(2)
        
        # 第二步：執行 DNA 核心篩選與評分 (目前為註解狀態)
        # run_step("你的評分計算腳本.py", DNA_ASSISTANT_PATH)
        
        # 第三步：執行 Telegram 機器人推播 (對應 taiwan_stock_bot 內的執行檔)
        run_step("stock_bot_main.py", TELEGRAM_BOT_PATH)
        
        print("\n" + "="*50)
        print("🎉 恭喜！今日全自動量化選股與 Telegram 推播已全數執行完畢！")
        print("="*50)
        send_telegram_message("🎉 今日全自動量化選股已全數執行完畢！")
        
    except Exception as e:
        print(f"\n⚠️ 流程中斷：{e}")
        # 若流程中斷，將錯誤訊息傳到 Telegram
        send_telegram_message(f"⚠️ 流程中斷：{e}")
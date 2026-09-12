import subprocess
import time
import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"

# 定義你原本各個獨立模組的絕對路徑（確保絕對不會跑錯路）
CHIP_ANALYZER_PATH = r"C:\Users\kweiw\Desktop\我的專案\Chip_Analyzer"  # 請依你實際的 Chip_Analyzer 資料夾位置調整
DNA_ASSISTANT_PATH = r"C:\Users\kweiw\Desktop\我的專案\股票"     # 你的 DNA 2.0 / 評分系統資料夾
TELEGRAM_BOT_PATH = r"C:\Users\kweiw\Desktop\我的專案\taiwan_stock_bot" # 你的 Telegram 機器人資料夾

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
        # 第一步：執行籌碼下載與分析 (對應 Chip_Analyzer 內的下載主程式)
        # 假設你的籌碼主程式檔名是 main_chip.py 或 chip_downloader.py，可自行替換
        run_step("main_chip.py", CHIP_ANALYZER_PATH)
        
        # 稍作等待確保檔案順利寫入硬碟
        time.sleep(2)
        
        # 第二步：執行 DNA 核心篩選與評分 (對應 app.py 或 dna_core 相關運算)
        # 若需要自動產出最新清單，可以呼叫對應的運算腳本
        # run_step("你的評分計算腳本.py", DNA_ASSISTANT_PATH)
        
        # 第三步：執行 Telegram 機器人推播 (對應 taiwan_stock_bot 內的執行檔)
        run_step("stock_bot_main.py", TELEGRAM_BOT_PATH)
        
        print("\n" + "="*50)
        print("🎉 恭喜！今日全自動量化選股與 Telegram 推播已全數執行完畢！")
        print("="*50)
        
    except Exception as e:
        print(f"\n⚠️ 流程中斷：{e}")
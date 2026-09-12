import streamlit as st
import yfinance as yf
import pandas as pd
import os, time, random
from datetime import datetime

# --- 1. 系統設定 ---
st.set_page_config(page_title="Sarah 3.2 Pro - 桌面專案版", layout="wide")
st.title("🚀 Sarah 3.2 Pro (v5.9)")
st.markdown("### 儲存目標：`Desktop\我的專案\stock_analyzer\excel`")

# --- 2. 桌面絕對路徑設定 (精確對齊您的需求) ---
# 使用 r"" 原始字串來處理 Windows 反斜線
FOLDER_PATH = r"C:\Users\kweiw\desktop\我的專案\stock_analyzer\excel"

# 自動檢查並建立資料夾，避免報錯
if not os.path.exists(FOLDER_PATH):
    try:
        os.makedirs(FOLDER_PATH)
        st.success(f"📂 已為您建立新資料夾：{FOLDER_PATH}")
    except Exception as e:
        st.error(f"無法建立資料夾，請檢查權限或路徑：{e}")

today = datetime.now().strftime("%Y_%m_%d")
DATA_FILE_XLSX = os.path.join(FOLDER_PATH, f"taiwan_stock_{today}.xlsx")

# --- 3. 側邊欄設定 ---
st.sidebar.header("⚙️ 篩選標準")
roe_target = st.sidebar.slider("最低 ROE (%)", 0, 25, 12) / 100

# --- 4. 掃描邏輯 (精簡高效區間) ---
def get_active_symbols():
    # 涵蓋您關注的 11xx, 12xx, 23xx, 24xx, 30xx, 62xx 等區間
    ranges = [range(1101, 1111), range(1201, 1230), range(2301, 2399), range(6201, 6299)]
    return [f"{i}.TW" for r in ranges for i in r]

if st.sidebar.button("📥 執行掃描並存至桌面專案"):
    targets = get_active_symbols()
    results = []
    p_bar = st.progress(0)
    
    for i, symbol in enumerate(targets):
        try:
            time.sleep(random.uniform(1.2, 2.0)) # 手機熱點友善延遲
            tk = yf.Ticker(symbol)
            info = tk.info
            name = info.get('shortName')
            
            if name:
                roe = info.get('returnOnEquity', 0)
                if roe >= roe_target:
                    results.append({
                        "日期": today,
                        "代碼": symbol,
                        "名稱": name,
                        "ROE": f"{roe:.2%}",
                        "PE": info.get('trailingPE'),
                        "目前股價": info.get('currentPrice')
                    })
            p_bar.progress((i + 1) / len(targets))
        except: continue
            
    if results:
        df = pd.DataFrame(results)
        # 存成 OpenOffice 友善格式
        df.to_excel(DATA_FILE_XLSX, index=False, engine='openpyxl')
        
        st.success("🎉 檔案已成功歸檔！")
        st.info(f"📁 存放位置：\n{DATA_FILE_XLSX}")
        st.dataframe(df)

# --- 5. 本地讀取功能 (方便您隨時查看今日成果) ---
st.markdown("---")
if os.path.exists(DATA_FILE_XLSX):
    st.write(f"📂 今日數據已在 `excel` 資料夾就緒。")
    if st.button("🔍 點此讀取桌面專案庫存"):
        st.dataframe(pd.read_excel(DATA_FILE_XLSX))/

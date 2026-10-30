import streamlit as st
import yfinance as yf
import pandas as pd

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="美股研究",
    page_icon="📈",
    layout="centered"
)

# =========================
# 公司研究資料庫
# =========================
COMPANY_RESEARCH = {
    "NVDA": {
        "position": "AI GPU｜AI 加速運算｜資料中心",
        "products": [
            "AI GPU",
            "Blackwell / Rubin 平台",
            "CUDA 軟體生態系",
            "AI Networking",
            "DGX AI 系統"
        ],
        "partners": [
            "TSMC－先進製程與晶圓代工",
            "SK hynix－HBM 高頻寬記憶體",
            "Micron－HBM / 記憶體",
            "Microsoft－Azure AI",
            "Google－Google Cloud",
            "Amazon AWS－AI Cloud",
            "Dell－AI Server",
            "Supermicro－AI Server"
        ],
        "competitors": [
            "AMD－AI GPU",
            "Broadcom－客製化 ASIC",
            "Google TPU－自研 AI 晶片",
            "Amazon Trainium－自研 AI 晶片"
        ],
        "outlook": [
            "AI 資料中心資本支出",
            "新一代 GPU 平台放量",
            "AI Agent 帶動推論需求",
            "Hyperscaler 擴建 AI 基礎建設"
        ],
        "risks": [
            "AI 資本支出成長放緩",
            "大型雲端公司增加自研 ASIC",
            "出口限制",
            "高估值造成股價波動"
        ]
    },

    "AVGO": {
        "position": "AI ASIC｜Networking｜資料中心互連",
        "products": [
            "客製化 AI ASIC",
            "Tomahawk 網路交換晶片",
            "Jericho 網路晶片",
            "VMware 企業軟體"
        ],
        "partners": [
            "Google－客製化 AI 晶片",
            "TSMC－晶片製造",
            "大型 Hyperscaler－AI ASIC",
            "Apple－無線通訊相關元件"
        ],
        "competitors": [
            "NVIDIA",
            "Marvell",
            "AMD"
        ],
        "outlook": [
            "AI ASIC 市場成長",
            "AI Data Center Networking 升級",
            "Hyperscaler 自研晶片需求",
            "VMware 軟體營收"
        ],
        "risks": [
            "大型客戶集中",
            "AI ASIC 競爭",
            "半導體景氣循環",
            "VMware 整合風險"
        ]
    },

    "ALAB": {
        "position": "AI 資料中心｜PCIe｜CXL｜高速互連",
        "products": [
            "PCIe Connectivity",
            "CXL Connectivity",
            "AI Server 高速互連",
            "資料中心連接晶片"
        ],
        "partners": [
            "NVIDIA－AI Server 生態系",
            "AMD－資料中心平台",
            "Intel－PCIe / CXL 生態系",
            "Hyperscaler－AI Data Center"
        ],
        "competitors": [
            "Broadcom",
            "Marvell",
            "Credo Technology"
        ],
        "outlook": [
            "AI Server 數量增加",
            "GPU Cluster 規模擴大",
            "PCIe / CXL 升級",
            "高速互連需求成長"
        ],
        "risks": [
            "客戶集中",
            "AI Server 建置速度下降",
            "大型半導體公司競爭",
            "高成長股估值波動"
        ]
    },

    "GOOG": {
        "position": "AI｜Cloud｜Search｜AI ASIC",
        "products": [
            "Google Search",
            "YouTube",
            "Google Cloud",
            "Gemini AI",
            "TPU"
        ],
        "partners": [
            "Broadcom－AI ASIC / TPU 生態系",
            "NVIDIA－Google Cloud GPU",
            "TSMC－半導體供應鏈"
        ],
        "competitors": [
            "Microsoft",
            "Amazon AWS",
            "Meta",
            "OpenAI"
        ],
        "outlook": [
            "Gemini AI 商業化",
            "Google Cloud 成長",
            "AI Search",
            "企業 AI 需求"
        ],
        "risks": [
            "AI 競爭",
            "AI 資本支出增加",
            "搜尋市場競爭",
            "反壟斷與監管風險"
        ]
    },

    "MU": {
        "position": "AI 記憶體｜HBM｜DRAM｜NAND",
        "products": [
            "HBM 高頻寬記憶體",
            "DRAM",
            "NAND Flash",
            "資料中心記憶體"
        ],
        "partners": [
            "AI GPU / AI Server 生態系",
            "資料中心客戶",
            "伺服器 OEM / ODM"
        ],
        "competitors": [
            "SK hynix",
            "Samsung Electronics"
        ],
        "outlook": [
            "HBM 需求成長",
            "AI Server 記憶體容量提升",
            "記憶體供需改善"
        ],
        "risks": [
            "記憶體價格循環",
            "HBM 競爭",
            "資本支出增加"
        ]
    },

    "PLTR": {
        "position": "企業 AI｜資料分析｜AI 軟體平台",
        "products": [
            "AIP",
            "Foundry",
            "Gotham",
            "Apollo"
        ],
        "partners": [
            "企業客戶",
            "美國政府與國防相關客戶",
            "Cloud / AI 生態系"
        ],
        "competitors": [
            "Microsoft",
            "Snowflake",
            "Databricks",
            "大型企業軟體公司"
        ],
        "outlook": [
            "企業生成式 AI 導入",
            "AIP 商業化",
            "企業 AI 支出增加"
        ],
        "risks": [
            "高估值",
            "企業 AI 競爭",
            "政府合約波動"
        ]
    }
}


# =========================
# Yahoo Finance
# =========================
@st.cache_data(ttl=300)
def get_stock_data(symbol, period):
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period)


@st.cache_data(ttl=3600)
def get_company_info(symbol):
    try:
        return yf.Ticker(symbol).info
    except Exception:
        return {}


@st.cache_data(ttl=3600)
def get_financials(symbol):
    try:
        return yf.Ticker(symbol).quarterly_income_stmt
    except Exception:
        return pd.DataFrame()


def format_money(value):
    if value is None or pd.isna(value):
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"

    return f"${value:,.2f}"


# =========================
# App 標題
# =========================
st.title("📈 美股研究")

st.caption(
    "股價・財報・產業鏈・合作公司・競爭對手・展望與風險"
)

# =========================
# 股票搜尋
# =========================
symbol = st.text_input(
    "🔍 輸入美股股票代碼",
    value="NVDA",
    placeholder="例如 NVDA、AVGO、ALAB、GOOG"
).upper().strip()

period_label = st.radio(
    "股價區間",
    ["30D", "3M", "6M", "1Y"],
    horizontal=True
)

period_map = {
    "30D": "1mo",
    "3M": "3mo",
    "6M": "6mo",
    "1Y": "1y"
}

if symbol:

    try:
        history = get_stock_data(
            symbol,
            period_map[period_label]
        )

        info = get_company_info(symbol)

        if history.empty:
            st.error("查無股票資料，請確認股票代碼。")
            st.stop()

        company_name = info.get(
            "longName",
            symbol
        )

        current_price = history["Close"].iloc[-1]

        if len(history) >= 2:
            previous_price = history["Close"].iloc[-2]
            change = current_price - previous_price
            change_pct = change / previous_price * 100
        else:
            change = 0
            change_pct = 0

        # =========================
        # 公司名稱 / 股價
        # =========================
        st.header(f"{company_name}")

        st.caption(symbol)

        col1, col2 = st.columns(2)

        col1.metric(
            "最新價格",
            f"${current_price:,.2f}",
            f"{change_pct:+.2f}%"
        )

        col2.metric(
            "今日漲跌",
            f"${change:+.2f}"
        )

        # =========================
        # 股價走勢
        # =========================
        st.subheader(f"📊 {period_label} 股價走勢")

        chart_data = history[["Close"]].copy()
        chart_data.columns = ["收盤價"]

        st.line_chart(
            chart_data,
            height=300
        )

        st.caption("資料來源：Yahoo Finance")

        st.divider()

        # =========================
        # 公司基本資料
        # =========================
        st.subheader("🏢 公司基本資料")

        st.write(
            f"**產業：** {info.get('industry', 'N/A')}"
        )

        st.write(
            f"**Sector：** {info.get('sector', 'N/A')}"
        )

        st.write(
            f"**市值：** {format_money(info.get('marketCap'))}"
        )

        # =========================
        # 公司介紹
        # =========================
        st.subheader("💼 公司在做什麼？")

        business = info.get("longBusinessSummary")

        if business:
            st.write(business)
        else:
            st.info("目前 Yahoo Finance 無公司介紹資料。")

        # =========================
        # 公司研究
        # =========================
        research = COMPANY_RESEARCH.get(symbol)

        if research:

            st.divider()

            st.subheader("🧩 產業鏈位置")

            st.info(research["position"])

            st.subheader("📦 主要產品 / 業務")

            for item in research["products"]:
                st.write(f"• {item}")

            st.subheader("🤝 合作 / 供應鏈")

            for item in research["partners"]:
                st.write(f"• {item}")

            st.subheader("⚔️ 主要競爭對手")

            for item in research["competitors"]:
                st.write(f"• {item}")

        else:
            st.info(
                "此股票目前尚未建立進階公司研究資料，"
                "股價與 Yahoo Finance 基本資料仍可正常使用。"
            )

        # =========================
        # 最新財報
        # =========================
        st.divider()

        st.subheader("📑 最近一期財報")

        financials = get_financials(symbol)

        if not financials.empty:

            latest_date = financials.columns[0]
            latest = financials[latest_date]

            revenue = latest.get(
                "Total Revenue"
            )

            net_income = latest.get(
                "Net Income"
            )

            eps = latest.get(
                "Diluted EPS"
            )

            st.metric(
                "營收",
                format_money(revenue)
            )

            st.metric(
                "淨利",
                format_money(net_income)
            )

            if eps is not None and not pd.isna(eps):
                st.metric(
                    "稀釋 EPS",
                    f"${float(eps):,.2f}"
                )
            else:
                st.metric(
                    "稀釋 EPS",
                    "N/A"
                )

            try:
                st.caption(
                    "財報日期："
                    + latest_date.strftime("%Y-%m-%d")
                )
            except Exception:
                pass

        else:
            st.warning(
                "Yahoo Finance 暫時無法取得季度財報。"
            )

        # =========================
        # 展望 / 風險
        # =========================
        if research:

            st.divider()

            st.subheader("🚀 未來展望")

            for item in research["outlook"]:
                st.write(f"✓ {item}")

            st.subheader("⚠️ 主要風險")

            for item in research["risks"]:
                st.write(f"• {item}")

        # =========================
        # Yahoo Finance
        # =========================
        st.divider()

        yahoo_url = (
            "https://finance.yahoo.com/quote/"
            + symbol
        )

        st.link_button(
            "🔗 Yahoo Finance 完整資料",
            yahoo_url
        )

    except Exception as e:

        st.error("資料取得失敗，請稍後再試。")

        with st.expander("查看錯誤資訊"):
            st.write(str(e))

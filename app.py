import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอแบบกว้าง
st.set_page_config(page_title="Truck Price Comparison 2026", layout="wide")

st.title("🚚 Interactive Dashboard: Truck Price Comparison")

# --- ส่วนของการสร้าง Sidebar ---
st.sidebar.header("📁 ตั้งค่าข้อมูล")
# สร้างปุ่ม Upload ไฟล์ จำกัดเฉพาะไฟล์ .xlsx และ .xls
uploaded_file = st.sidebar.file_uploader("อัปโหลดไฟล์ Excel ที่นี่", type=["xlsx", "xls"])

@st.cache_data
def load_data(file):
    # อ่านไฟล์ Excel จากไฟล์ที่อัปโหลด
    xls = pd.ExcelFile(file)
    first_sheet_name = xls.sheet_names[0]
    
    # โหลดข้อมูลเฉพาะ Sheet แรก
    # ปรับ header=[1, 2] ตามโครงสร้างไฟล์ต้นฉบับ
    df = pd.read_excel(file, sheet_name=first_sheet_name, header=[1, 2])
    return df, first_sheet_name

# ตรวจสอบว่ามีการอัปโหลดไฟล์เข้ามาหรือไม่
if uploaded_file is not None:
    try:
        df, sheet_name = load_data(uploaded_file)
        
        st.write(f"**กำลังแสดงข้อมูลจาก Sheet:** `{sheet_name}`")
        
        # ส่วนค้นหาข้อมูล
        search_query = st.text_input("🔍 ค้นหาข้อมูลในตาราง", "")
        
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        # แสดงผลตาราง
        st.dataframe(filtered_df, use_container_width=True, height=600)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
else:
    # ข้อความต้อนรับเมื่อยังไม่ได้อัปโหลดไฟล์
    st.info("👈 กรุณาอัปโหลดไฟล์ Excel จากแถบเมนูด้านซ้ายมือเพื่อเริ่มดูข้อมูล")

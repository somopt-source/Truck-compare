import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอแบบกว้าง
st.set_page_config(page_title="Truck Price Comparison 2026", layout="wide")

st.title("🚚 Interactive Dashboard: Truck Price Comparison 2026")

@st.cache_data
def load_data():
    file_path = "Compare price for Truck 2026 (Updated Summary).xlsx"
    
    # อ่านไฟล์ Excel เพื่อหาชื่อ Sheet ทั้งหมด
    xls = pd.ExcelFile(file_path)
    first_sheet_name = xls.sheet_names[0]
    
    # โหลดข้อมูลเฉพาะ Sheet แรก 
    # (ใช้ header=[1, 2] เพื่อให้รองรับหัวตารางแบบหลายชั้นตามโครงสร้างไฟล์ของคุณ)
    df = pd.read_excel(file_path, sheet_name=first_sheet_name, header=[1, 2])
    return df, first_sheet_name

try:
    df, sheet_name = load_data()
    
    st.write(f"**กำลังแสดงข้อมูลจาก Sheet:** `{sheet_name}`")
    
    # ส่วนของ Interactive: ช่องค้นหาข้อมูลเบื้องต้น
    search_query = st.text_input("🔍 ค้นหาข้อมูลในตาราง", "")
    
    if search_query:
        # แปลงข้อมูลเป็น string และค้นหาคำที่ต้องการ
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df
        
    # แสดงผลตารางแบบ Interactive (สามารถเลื่อน, จัดเรียง, ขยายได้)
    st.dataframe(filtered_df, use_container_width=True, height=600)
    
except FileNotFoundError:
    st.error(f"ไม่พบไฟล์ 'Compare price for Truck 2026 (Updated Summary).xlsx' ในโฟลเดอร์ กรุณาตรวจสอบให้แน่ใจว่าวางไฟล์ไว้ในที่เดียวกับ app.py")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")

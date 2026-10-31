import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Truck Price Comparison 2026", layout="wide")

st.title("🚚 Interactive Dashboard: Truck Price Comparison")

st.sidebar.header("📁 ตั้งค่าข้อมูล")
uploaded_file = st.sidebar.file_uploader("อัปโหลดไฟล์ Excel ที่นี่", type=["xlsx", "xls"])

@st.cache_data
def load_data(file):
    xls = pd.ExcelFile(file)
    first_sheet_name = xls.sheet_names[0]
    # โหลดข้อมูลเฉพาะ Sheet แรก
    df = pd.read_excel(file, sheet_name=first_sheet_name, header=[1, 2])
    return df, first_sheet_name

def create_bar_chart():
    # ข้อมูลจำลองตามรูปแบบกราฟในภาพ (เนื่องจากข้อมูล Excel ต้นฉบับมีโครงสร้างซับซ้อนและมีค่า NaN เยอะ จึงสร้าง Mock Data ตามภาพเพื่อให้เห็นรูปแบบกราฟที่ต้องการ)
    # หากต้องการใช้ข้อมูลจริงจาก Excel ต้องมีการทำ Data Cleaning ก่อนครับ
    
    categories = ['North', 'South', 'West', 'East', 'Online']
    apple = [45, 30, 32, 52, 53]
    banana = [83, 79, 64, 88, 96]
    orange = [33, 57, 30, 83, 105]
    
    # คำนวณยอดรวมเพื่อใช้เป็นแท่งพื้นหลังสีเหลือง
    total = [a + b + o for a, b, o in zip(apple, banana, orange)]

    fig = go.Figure()

    # สร้างแท่งพื้นหลังสำหรับยอดรวม (สีเหลือง)
    fig.add_trace(go.Bar(
        x=categories,
        y=total,
        name='Total Background',
        marker_color='#FFC000', # สีเหลือง
        hoverinfo='skip', # ไม่ต้องแสดงข้อมูลเมื่อเอาเมาส์ชี้
        text=total,       # แสดงตัวเลขยอดรวม
        textposition='outside', # ให้ตัวเลขอยู่ด้านบนของแท่ง
        textfont=dict(size=14, color='black')
    ))

    # สร้างแท่งข้อมูลย่อยแบบกลุ่ม (Grouped Bar Chart) ซ้อนอยู่บนพื้นหลัง
    fig.add_trace(go.Bar(x=categories, y=apple, name='Apple', marker_color='#5B9BD5'))
    fig.add_trace(go.Bar(x=categories, y=banana, name='Banana', marker_color='#ED7D31'))
    fig.add_trace(go.Bar(x=categories, y=orange, name='Orange', marker_color='#A5A5A5'))

    # ปรับแต่ง Layout ของกราฟ
    fig.update_layout(
        barmode='group', # จัดรูปแบบให้แท่งย่อยอยู่เป็นกลุ่ม
        title='Fruit Sales Breakdown with Total',
        xaxis_title='Region',
        yaxis_title='Sales',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # ซ่อนแท่ง Total จาก Legend เพราะใช้เป็นแค่ฉากหลัง
    fig.data[0].showlegend = False 

    return fig

if uploaded_file is not None:
    try:
        df, sheet_name = load_data(uploaded_file)
        
        st.write(f"**กำลังแสดงข้อมูลจาก Sheet:** `{sheet_name}`")
        
        # --- ส่วนแสดงกราฟ ---
        st.subheader("📊 Sales Chart with Total Background")
        st.info("💡 หมายเหตุ: กราฟด้านล่างเป็นข้อมูลจำลองเพื่อแสดงโครงสร้างกราฟตามภาพตัวอย่าง หากต้องการใช้ข้อมูลจริงจากตาราง Excel จำเป็นต้องทำ Data Cleaning (จัดการค่าว่างและการรวมหัวตาราง) ก่อนนำมาพลอตครับ")
        
        fig = create_bar_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # --- ส่วนค้นหาข้อมูลในตาราง ---
        st.subheader("📋 ตารางข้อมูล")
        search_query = st.text_input("🔍 ค้นหาข้อมูลในตาราง", "")
        
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
else:
    st.info("👈 กรุณาอัปโหลดไฟล์ Excel จากแถบเมนูด้านซ้ายมือเพื่อเริ่มดูข้อมูล")

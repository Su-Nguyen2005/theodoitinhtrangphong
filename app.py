import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & NGUYÊN TẮC THIẾT KẾ UI/UX
# ---------------------------------------------------------
st.set_page_config(
    page_title="Quản Lý & Theo Dõi Tình Trạng Phòng",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho thẻ phòng & giao diện
st.markdown("""
    <style>
    .room-card {
        padding: 12px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: sans-serif;
    }
    .room-number {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .room-type {
        font-size: 13px;
        opacity: 0.9;
        margin-bottom: 6px;
    }
    .room-status {
        font-size: 13px;
        font-weight: 600;
        background-color: rgba(255, 255, 255, 0.25);
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    /* Màu trạng thái */
    .status-trong { background-color: #2e7d32; } /* Xanh lá */
    .status-dang-o { background-color: #c62828; } /* Đỏ */
    .status-dang-dondep { background-color: #f57c00; } /* Cam */
    .status-bao-tri { background-color: #616161; } /* Xám */
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KHỞI TẠO DỮ LIỆU MẪU CÓ CHÈN ẢNH (SESSION STATE)
# ---------------------------------------------------------
if "rooms" not in st.session_state:
    st.session_state.rooms = pd.DataFrame([
        {
            "Phòng": "101", "Tầng": 1, "Loại phòng": "Standard", "Trạng thái": "Trống", 
            "Giá (VNĐ)": 500000, "Ghi chú": "Sạch sẻ, sẵn sàng",
            "Hình ảnh": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=500"
        },
        {
            "Phòng": "102", "Tầng": 1, "Loại phòng": "Standard", "Trạng thái": "Đang ở", 
            "Giá (VNĐ)": 500000, "Ghi chú": "Khách checkout 12h",
            "Hình ảnh": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500"
        },
        {
            "Phòng": "103", "Tầng": 1, "Loại phòng": "Deluxe", "Trạng thái": "Đang dọn dẹp", 
            "Giá (VNĐ)": 800000, "Ghi chú": "Đang thay ga giường",
            "Hình ảnh": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=500"
        },
        {
            "Phòng": "104", "Tầng": 1, "Loại phòng": "Deluxe", "Trạng thái": "Bảo trì", 
            "Giá (VNĐ)": 800000, "Ghi chú": "Hỏng điều hòa",
            "Hình ảnh": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=500"
        },
        {
            "Phòng": "201", "Tầng": 2, "Loại phòng": "Standard", "Trạng thái": "Trống", 
            "Giá (VNĐ)": 550000, "Ghi chú": "",
            "Hình ảnh": "https://images.unsplash.com/photo-1591088398332-8a7791972843?w=500"
        },
        {
            "Phòng": "202", "Tầng": 2, "Loại phòng": "VIP Suite", "Trạng thái": "Đang ở", 
            "Giá (VNĐ)": 1500000, "Ghi chú": "VIP - Khách VIP",
            "Hình ảnh": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500"
        },
        {
            "Phòng": "203", "Tầng": 2, "Loại phòng": "VIP Suite", "Trạng thái": "Trống", 
            "Giá (VNĐ)": 1500000, "Ghi chú": "",
            "Hình ảnh": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=500"
        },
        {
            "Phòng": "204", "Tầng": 2, "Loại phòng": "Deluxe", "Trạng thái": "Đang dọn dẹp", 
            "Giá (VNĐ)": 850000, "Ghi chú": "",
            "Hình ảnh": "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=500"
        },
    ])

STATUS_COLORS = {
    "Trống": "#2e7d32",
    "Đang ở": "#c62828",
    "Đang dọn dẹp": "#f57c00",
    "Bảo trì": "#616161"
}

STATUS_CLASS = {
    "Trống": "status-trong",
    "Đang ở": "status-dang-o",
    "Đang dọn dẹp": "status-dang-dondep",
    "Bảo trì": "status-bao-tri"
}

# ---------------------------------------------------------
# 3. SIDEBAR: BỘ LỌC & CẬP NHẬT TRẠNG THÁI / ẢNH
# ---------------------------------------------------------
st.sidebar.title("🏨 Điều Khiển Hệ Thống")

# Bộ lọc
st.sidebar.subheader("🔍 Bộ lọc sơ đồ")
selected_floor = st.sidebar.multiselect(
    "Chọn Tầng",
    options=sorted(st.session_state.rooms["Tầng"].unique()),
    default=sorted(st.session_state.rooms["Tầng"].unique())
)

selected_status = st.sidebar.multiselect(
    "Trạng thái phòng",
    options=list(STATUS_COLORS.keys()),
    default=list(STATUS_COLORS.keys())
)

st.sidebar.divider()

# Form Cập nhật nhanh
st.sidebar.subheader("⚡ Cập nhật nhanh thông tin")
with st.sidebar.form("update_room_form"):
    room_to_update = st.selectbox("Chọn Phòng", options=st.session_state.rooms["Phòng"].tolist())
    new_status = st.selectbox("Trạng thái mới", options=list(STATUS_COLORS.keys()))
    new_img = st.text_input("Link ảnh phòng (URL)", value="")
    new_note = st.text_input("Ghi chú bổ sung", value="")
    submit_update = st.form_submit_button("Cập Nhật Tình Trạng", use_container_width=True)

    if submit_update:
        idx = st.session_state.rooms[st.session_state.rooms["Phòng"] == room_to_update].index[0]
        st.session_state.rooms.at[idx, "Trạng thái"] = new_status
        if new_img:
            st.session_state.rooms.at[idx, "Hình ảnh"] = new_img
        if new_note:
            st.session_state.rooms.at[idx, "Ghi chú"] = new_note
        st.sidebar.success(f"Đã cập nhật Phòng {room_to_update} thành công!")
        st.rerun()

# ---------------------------------------------------------
# 4. GIAO DIỆN CHÍNH (MAIN DASHBOARD)
# ---------------------------------------------------------
st.title("🏨 Hệ Thống Theo Dõi Tình Trạng Phòng")

# --- LỌC DỮ LIỆU ---
filtered_df = st.session_state.rooms[
    (st.session_state.rooms["Tầng"].isin(selected_floor)) &
    (st.session_state.rooms["Trạng thái"].isin(selected_status))
]

# --- THỐNG KÊ TỔNG QUAN (METRICS) ---
st.subheader("📊 Thống Kê Tổng Quan")
total_rooms = len(st.session_state.rooms)
count_trong = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Trống"])
count_dango = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Đang ở"])
count_dondep = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Đang dọn dẹp"])
count_baotri = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Bảo trì"])

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Tổng số phòng", total_rooms)
col_m2.metric("Phòng Trống", count_trong, f"{count_trong/total_rooms*100:.0f}%")
col_m3.metric("Đang Ở", count_dango, f"{count_dango/total_rooms*100:.0f}%")
col_m4.metric("Đang Dọn Dẹp", count_dondep)
col_m5.metric("Bảo Trì", count_baotri)

st.divider()

# --- TABS GIAO DIỆN ---
tab_sodo, tab_danhsach, tab_bieudo = st.tabs(["🗺️ Sơ Đồ Phòng Direct View", "📋 Danh Sách Chi Tiết", "📈 Biểu Đồ Báo Cáo"])

# --- TAB 1: SƠ ĐỒ PHÒNG HỖ TRỢ HIỂN THỊ ẢNH ---
with tab_sodo:
    st.subheader("Sơ Đồ Trực Quan Theo Tầng")
    
    if filtered_df.empty:
        st.warning("Không có phòng nào phù hợp với bộ lọc hiện tại.")
    else:
        floors = sorted(filtered_df["Tầng"].unique())
        for floor in floors:
            st.markdown(f"#### 🏢 Tầng {floor}")
            floor_rooms = filtered_df[filtered_df["Tầng"] == floor]
            
            # Chia cột linh hoạt dựa trên số phòng (tối đa 4 phòng/dòng)
            cols = st.columns(4)
            for idx, (_, room) in enumerate(floor_rooms.iterrows()):
                col_idx = idx % 4
                status_cls = STATUS_CLASS.get(room["Trạng thái"], "status-bao-tri")
                note_display = f"<br><i>Note: {room['Ghi chú']}</i>" if room['Ghi chú'] else ""
                
                with cols[col_idx]:
                    # Hiển thị ảnh phòng
                    if room.get("Hình ảnh"):
                        st.image(room["Hình ảnh"], use_container_width=True)
                    
                    # Khối thông tin trạng thái phòng
                    st.markdown(f"""
                        <div class="room-card {status_cls}">
                            <div class="room-number">Phòng {room['Phòng']}</div>
                            <div class="room-type">{room['Loại phòng']}</div>
                            <div class="room-status">{room['Trạng thái']}</div>
                            <div style="font-size:12px; margin-top:6px;">{room['Giá (VNĐ)']:,.0f} VNĐ{note_display}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- TAB 2: DANH SÁCH CHI TIẾT VÀ BẢNG ẢNH ---
with tab_danhsach:
    st.subheader("Quản Lý & Chỉnh Sửa Trực Tiếp")
    st.caption("Bạn có thể chỉnh sửa trực tiếp giá trị/URL ảnh trên bảng bên dưới và nhấn **'Lưu Thay Đổi'**.")
    
    edited_df = st.data_editor(
        st.session_state.rooms,
        column_config={
            "Hình ảnh": st.column_config.ImageColumn(
                "Hình ảnh phòng",
                help="Đường dẫn URL ảnh phòng",
                width="medium"
            ),
            "Trạng thái": st.column_config.SelectboxColumn(
                "Trạng thái",
                options=list(STATUS_COLORS.keys()),
                required=True
            ),
            "Giá (VNĐ)": st.column_config.NumberColumn(
                "Giá (VNĐ)",
                format="%d VNĐ",
                step=50000
            )
        },
        num_rows="dynamic",
        use_container_width=True
    )
    
    if st.button("💾 Lưu Thay Đổi Vào Hệ Thống", type="primary"):
        st.session_state.rooms = edited_df
        st.success("Đã lưu bảng dữ liệu mới thành công!")
        st.rerun()

# --- TAB 3: BIỂU ĐỒ BÁO CÁO ---
with tab_bieudo:
    st.subheader("Phân Tích Tỷ Lệ Sử Dụng Phòng")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        status_counts = st.session_state.rooms["Trạng thái"].value_counts().reset_index()
        status_counts.columns = ["Trạng thái", "Số lượng"]
        
        fig_pie = px.pie(
            status_counts,
            values="Số lượng",
            names="Trạng thái",
            title="Tỷ lệ Trạng thái Phòng Hiện tại",
            color="Trạng thái",
            color_discrete_map=STATUS_COLORS,
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        floor_status = st.session_state.rooms.groupby(["Tầng", "Trạng thái"]).size().reset_index(name="Số lượng")
        fig_bar = px.bar(
            floor_status,
            x="Tầng",
            y="Số lượng",
            color="Trạng thái",
            title="Phân bố Trạng thái Theo Tầng",
            barmode="stack",
            color_discrete_map=STATUS_COLORS
        )
        st.plotly_chart(fig_bar, use_container_width=True)
import streamlit as st
# (Nếu bạn dùng OpenAI hoặc Google Gemini API thì import thêm thư viện tương ứng ở đây)

# --- KHU VỰC TRỢ LÝ AI CHATBOT ---
st.divider() # Tạo đường kẻ phân cách
st.subheader("💬 Trợ Lý AI Khách Sạn")

# Khởi tạo lịch sử chat trong session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì cho bạn về thông tin phòng và trạng thái đặt phòng?"}
    ]

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập câu hỏi của người dùng
# --- KHU VỰC TRỢ LÝ AI CHATBOT ---
st.divider()
st.subheader("💬 Trợ Lý AI Khách Sạn")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì cho bạn về thông tin phòng và trạng thái đặt phòng?"}
    ]

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập câu hỏi của người dùng
if prompt := st.chat_input("Hỏi AI về trạng thái phòng..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Xử lý trả lời từ dữ liệu MySQL thực tế
    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()
        conn = st.connection("mysql", type="sql")
        
        # Xử lý câu hỏi về tổng số phòng
        if "bao nhiêu phòng" in prompt_lower or "tổng" in prompt_lower:
            df_rooms = conn.query("SELECT COUNT(*) as total FROM rooms;", ttl=0)
            total = df_rooms['total'].iloc[0]
            response = f"Hiện tại hệ thống đang quản lý tổng cộng **{total} phòng**."
            
        # Xử lý câu hỏi tìm phòng trống
        elif "trống" in prompt_lower:
            df_empty = conn.query("SELECT room_number FROM rooms WHERE status = 'Trống';", ttl=0)
            rooms_list = ", ".join(map(str, df_empty['room_number'].tolist()))
            response = f"Các phòng đang **Trống**: {rooms_list if rooms_list else 'Hiện không có phòng trống.'}"
            
        # Xử lý câu hỏi tìm phòng đang ở
        elif "đang ở" in prompt_lower:
            df_busy = conn.query("SELECT room_number FROM rooms WHERE status = 'Đang ở';", ttl=0)
            rooms_list = ", ".join(map(str, df_busy['room_number'].tolist()))
            response = f"Các phòng **Đang ở**: {rooms_list if rooms_list else 'Không có phòng nào đang ở.'}"
            
        else:
            response = "Tôi có thể hỗ trợ bạn kiểm tra: tổng số phòng, danh sách phòng trống, hoặc danh sách phòng đang ở. Bạn muốn kiểm tra thông tin nào?"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

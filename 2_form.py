import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
from datetime import datetime, timedelta
import database as db

st.set_page_config(
    page_title="Form Title here",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",        
)

# hide_st_style = '''<style>
#                     #MainMenu {visibility: hidden;}
#                     footer {visibility: hidden;}
#                     header {visibility: hidden;}
#                     </style>
#                     '''

# st.markdown(hide_st_style, unsafe_allow_html=True)

if 'greeting' not in st.session_state:
    st.session_state.greeting = "Hello, there!"
    st.session_state.idx = 1
# st.write(st.session_state)

# def load_image(img):
#     im = Image.open(img)
#     image = np.array(im)
#     return image

def get_products():
    items = db.fetch_all()
    products = [item["key"] for item in items]
    return products

keywords = []
def list_keywords(search):
    keywords.append(search)

with st.sidebar:
    selected = option_menu(menu_title=None, options = ["리뷰 요청 (판매자)", '리뷰 요청 (리뷰어)', '상품 선택', '로그인'], 
                            icons=['bag', 'bag-check', 'bag-check-fill', 'box-arrow-in-down-left'], menu_icon="list", default_index=st.session_state.idx) # orientation="horizontal"

st.title("Form Name here")
st.caption("Add a form name to give your form an internal nickname that people filling out your form won’t see. This is a good option to keep forms organized on your Forms page—especially if you have multiple forms with the same title.")

def main():
    if selected == "리뷰 요청 (판매자)":
        with st.form(key="form1", clear_on_submit=False):
            product_name = st.text_input('상품명', placeholder="상품명을 입력하세요.")
            product_link = st.text_input('구매 링크', placeholder="상품 상세 페이지 주소를 입력하세요.")
            st.write("######")

            col11, col12 = st.columns(2)
            with col11:
                st.text("상품 검색용 키워드를 입력하세요.")
                col111, col222 = st.columns(2)
                with col111:
                    search1 = st.text_input('검색어1', label_visibility="collapsed")
                with col222:
                    search2 = st.text_input('검색어2', label_visibility="collapsed")
                for i in [search1, search2]:
                    if not i == "":
                        list_keywords(i)
                st.session_state.keywords = keywords

            with col12:
                img_url = st.text_input('이미지 URL을 입력하세요.', help="'imgur.com'에서 무료로 이미지 주소 생성이 가능합니다.", placeholder='https://i.imgur.com/BsxLDu2.png', label_visibility="visible") 
                st.session_state.img_url = img_url
            if not st.session_state.img_url == "":
                try:
                    st.image(st.session_state.img_url)
                except:
                    st.success('유효한 이미지 URL을 입력하세요.', icon="🚨")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                review_date = st.date_input("리뷰 일정", value= datetime.today() + timedelta(1))
                review_date = review_date.strftime("%x")
                review_time = st.time_input('리뷰 일정', value= datetime.now(), label_visibility="collapsed")
                review_time = review_time.strftime("%X")
            with col2:                
                review_guide = st.text_area(
                    '리뷰 가이드', '리뷰 가이드 곧바로 사용 가능하도록 똑바로 상세하게, 그럼에도 간결하게', disabled=True, label_visibility="hidden")
            st.write("######")

            col3, col4 = st.columns(2)
            with col3:
                purchase_date = st.date_input("구매 일정", value= datetime.today())
                purchase_date = purchase_date.strftime("%x")
                purchase_time = st.time_input('구매 일정', value= datetime.now(), label_visibility="collapsed")
                purchase_time = purchase_time.strftime("%X")
                st.write("######")
                give_away = st.radio('리뷰 상품의 증정 또는 회수 여부를 선택하세요.',('증정', '회수'), index=1, horizontal=True)
            st.write("######")

            with col4:
                col33, col44=st.columns(2)  
                with col33:
                    product_price = st.number_input('상품 금액', step=1000, format="%i")
                with col44:
                    review_amount = st.number_input('리뷰 금액', step=1000, format="%i")
                total_sum = product_price + review_amount
                st.info("합계 금액은 {} 원입니다.".format('{:,}'.format(total_sum)), icon="ℹ️")
    
            with col4:
                st.write("######")
                submitted = st.form_submit_button(label='Submit', use_container_width=True)
 
            if submitted:
                st.session_state.prodcut_name = product_name
                st.session_state.review_details = [product_link, review_date, review_time, purchase_date, purchase_time, product_price, review_amount, total_sum, give_away]
                db.save_data(st.session_state.prodcut_name, st.session_state.keywords, st.session_state.img_url, st.session_state.review_details)

    elif selected == '리뷰 요청 (리뷰어)':
        product_key = st.selectbox('리뷰 상품을 선택하세요.', get_products())
        if product_key:
            details = db.get_product(product_key)
            product_link = st.text_input('구매 링크', value=details["other details"][0], disabled=True)
        st.write("######")

        col11, col12 = st.columns(2)
        with col11:
            st.text("상품 검색용 키워드입니다.")
            col111, col222 = st.columns(2)
            with col111:
                if len(details["keywords"])>0:
                    search1 = st.text_input('검색어1', value=details["keywords"][0], disabled=True, label_visibility="collapsed")
            with col222:
                if len(details["keywords"])>1:
                    search2 = st.text_input('검색어2', value=details["keywords"][1], disabled=True, label_visibility="collapsed")

        with col12:
            if details["image"] is not None:
                img_url = st.text_input('이미지 URL입니다.', value=details["image"], disabled=True, label_visibility="visible") 
        if details["image"] is not None:
            st.image(details["image"])
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            review_date = st.date_input("리뷰 일정", value=datetime.strptime(details["other details"][1],'%m/%d/%y'), disabled=True)
            review_time = st.time_input('리뷰 일정', value=datetime.strptime(details["other details"][2],'%H:%M:%S'), disabled=True)
        with col2:                
            review_guide = st.text_area(
                '리뷰 가이드', '리뷰 가이드 곧바로 사용 가능하도록 똑바로 상세하게, 그럼에도 간결하게', disabled=True, label_visibility="hidden")
        st.write("######")

        col3, col4 = st.columns(2)
        with col3:
            purchase_date = st.date_input("구매 일정",value=datetime.strptime(details["other details"][3],'%m/%d/%y'), disabled=True)
            purchase_time = st.time_input('구매 일정', value=datetime.strptime(details["other details"][4],'%H:%M:%S'), disabled=True)
            st.write("######")
            if details["other details"][-1] == "증정":
                idx2 = 0
            else:
                idx2 = 1
            give_away = st.radio(
                    '리뷰 상품의 증정 또는 회수 여부',('증정', '회수'), index=idx2, disabled=False, horizontal=True)
        st.write("######")

        with col4:
            col33, col44=st.columns(2)  
            with col33:
                product_price = st.number_input('상품 금액', value=details["other details"][5], step=1000, format="%i", disabled=True)
            with col44:
                review_amount = st.number_input('리뷰 금액', value=details["other details"][6], step=1000, format="%i", disabled=True)
            total_sum = product_price + review_amount
            st.info("합계 금액은 {} 원입니다.".format('{:,}'.format(total_sum)), icon="ℹ️")

if __name__ == '__main__':
   main()


            # if not st.session_state.keyword_inputs == "":  
            #     options = st.multiselect(
            #         '저장된 검색어 목록입니다.', st.session_state.keyword_inputs, st.session_state.keyword_inputs, disabled=st.session_state.disabled)

   


import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Form Title here",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",        
)

if 'greeting' not in st.session_state:
    st.session_state.greeting = "Hello, there!"
    st.session_state.idx = 0
    st.session_state.disabled = False
st.write(st.session_state)

def disable_inputs():
    st.session_state.disabled = True
def enable_inputs():
    st.session_state.disabled = False

# def load_image(img):
#     im = Image.open(img)
#     image = np.array(im)
#     return image

keywords = []
def list_keywords(search):
    keywords.append(search)

with st.sidebar:
    selected = option_menu("Form Title", ["리뷰 요청", '리뷰어 입력', '상품 선택', '로그인'], 
                            icons=['bag', 'bag-check', 'bag-check-fill', 'box-arrow-in-down-left'], menu_icon="list", default_index=st.session_state.idx)        
st.title("Form Name here")
st.caption("Add a form name to give your form an internal nickname that people filling out your form won’t see. This is a good option to keep forms organized on your Forms page—especially if you have multiple forms with the same title.")
st.write("######")

def main():
    if selected == "리뷰 요청":
        with st.form(key="form1", clear_on_submit=False):
            product_name = st.text_input(
                '상품명', placeholder="상품명을 입력하세요.", disabled=st.session_state.disabled)
            product_link = st.text_input(
                '구매 링크', placeholder="상품 상세 페이지 주소를 입력하세요.", disabled=st.session_state.disabled)
            st.write("######")

            ss_uploaded = st.file_uploader(
                "업로드할 이미지 파일을 선택하세요.", 
                type=['jpg', 'jpeg', 'png'], accept_multiple_files=False, 
                help="JPG/JPEG 또는 PNG 확장자의 단일 파일만 선택 가능합니다.", disabled=st.session_state.disabled)
            if ss_uploaded is not None:
                ss = Image.open(ss_uploaded)
            st.write("######")

            st.text("상품 검색용 키워드를 입력하세요.")
            col11, col12, col13, col14 = st.columns(4)
            with col11:
                search1 = st.text_input(
                    '검색어1', label_visibility="collapsed", disabled=st.session_state.disabled)
            with col12:
                search2 = st.text_input(
                    '검색어2', label_visibility="collapsed", disabled=st.session_state.disabled)
            with col13:
                search3 = st.text_input(
                    '검색어3', label_visibility="collapsed", disabled=st.session_state.disabled)
            with col14:
                add1 = st.form_submit_button(label='이미지 표시', disabled=st.session_state.disabled, use_container_width=True)
            st.info("'이미지 표시' 버튼 클릭 후에 업로드된 이미지의 정상 표시가 가능합니다.", icon="ℹ️")

            if add1:
                for i in [search1, search2, search3]:
                    if not i == "":
                        list_keywords(i)
                st.session_state.keyword_inputs = keywords
                st.session_state.prodcut_name = product_name
                st.session_state.product_link = product_link

                if ss is not None:
                    st.session_state.ss_image = ss
                    st.image(st.session_state.ss_image)
            
        with st.form(key="form2", clear_on_submit=False):
            give_away = st.radio(
                    '리뷰 상품의 증정 또는 회수 여부를 선택하세요.',('증정', '회수'), 
                    label_visibility="visible", index=1, horizontal=True, disabled=st.session_state.disabled)
            st.write("######")

            col1, col2 = st.columns(2)
            with col2:
                review_date = st.date_input("리뷰 일정", value= datetime.today() + timedelta(1), disabled=st.session_state.disabled)
                review_time = st.time_input('리뷰 일정', label_visibility="collapsed", value= datetime.now(), disabled=st.session_state.disabled)
            with col1:                
                review_guide = st.text_area('리뷰 가이드', '리뷰 없음, 5점 별점, 텍스트, 포토, 이게 뭐야 씨발 대체 좀 자세히 쓰던가', disabled=True)
            st.divider()

            col3, col4 = st.columns(2)
            with col4:
                purchase_date = st.date_input("구매 일정", value= datetime.today(), disabled=st.session_state.disabled)
                purchase_time = st.time_input('구매 일정', label_visibility="collapsed", value= datetime.now(), disabled=st.session_state.disabled)
            with col3:
                col33, col44=st.columns(2)
                with col33:
                    product_price = st.number_input(
                        '상품 금액', step=1000, disabled=st.session_state.disabled)
                    st.session_state.product_price = product_price                    
                with col44:
                    review_amount = st.number_input(
                        '리뷰 금액', step=1000, disabled=st.session_state.disabled)
                    st.session_state.review_amount = review_amount
                st.info('합계 금액은 {} 원입니다.'.format(int(st.session_state.product_price + st.session_state.review_amount)), icon="ℹ️")
                st.session_state.sum = st.session_state.product_price + st.session_state.review_amount
                st.write("######")
    
            with col4:
                col77, col88 =st.columns(2)
                with col77:
                    previous1 = st.form_submit_button(label='이전', on_click=enable_inputs, use_container_width=True)
                with col88:
                    next1 = st.form_submit_button(label='다음', on_click=disable_inputs, use_container_width=True)

 
            if next1:
                st.session_state.purchase_date = purchase_date
                st.session_state.purchase_time = purchase_time
                st.session_state.review_date = review_date
                st.session_state.review_time = review_time
                st.session_state.give_away = give_away


    if selected == '리뷰어 입력':
        st.write("ready to proceed to step 2")



if __name__ == '__main__':
   main()


            # if not st.session_state.keyword_inputs == "":  
            #     options = st.multiselect(
            #         '저장된 검색어 목록입니다.', st.session_state.keyword_inputs, st.session_state.keyword_inputs, disabled=st.session_state.disabled)



# if st.session_state["FormSubmitter:form2-Next"] == True:
#     st.write("ready to proceed to step 2")
    
#     selected = option_menu("Form Title", ["리뷰 요청", '리뷰어 입력', '상품 선택'], 
#                             icons=['bag', 'bag-check', 'bag-check-fill'], menu_icon="list", default_index=0)        


#    def sum_total():
#     return 

   

#    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
#    for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)

#     txt = st.text_area('리뷰 가이드', '''
#     리뷰 없음
#     5점별점
#     텍스트
#     텍스트, (...)
#     ''')
#     st.write(txt)


#    st.write("Inside the form")
#    slider_val = st.slider("Form slider")
#    checkbox_val = st.checkbox("Form checkbox")

#    # Every form must have a submit button.
#    submitted = st.form_submit_button("Submit")
#    if submitted:
#        st.write("slider", slider_val, "checkbox", checkbox_val)

# st.write("Outside the form")

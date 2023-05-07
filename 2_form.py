import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import datetime

st.set_page_config(
    page_title="Form Title here",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",        
)

if 'greeting' not in st.session_state:
    st.session_state.greeting = "Hello, there!"
    st.session_state.disabled = False
    st.session_state.ss_image = ""
    st.session_state.keyword_inputs = ""
# st.write(st.session_state)

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

def main():
    st.title("Form Name here")
    st.caption("Add a form name to give your form an internal nickname that people filling out your form won’t see. This is a good option to keep forms organized on your Forms page—especially if you have multiple forms with the same title.")
    with st.sidebar:
        selected = option_menu("Form Title", ["리뷰 요청", '리뷰어 입력', '상품 선택'], 
                                icons=['bag', 'bag-check', 'bag-check-fill'], menu_icon="list", default_index=0)        
    
    if selected == "리뷰 요청":
        with st.form(key="form1", clear_on_submit=False):
            st.session_state.product_name = st.text_input(
                '상품명', placeholder="상품명을 입력하세요.", disabled=st.session_state.disabled)
            st.session_state.product_link = st.text_input(
                '구매 링크', placeholder="상품 구매 링크를 입력하세요.", disabled=st.session_state.disabled)
            st.divider()
            
            ss_uploaded = st.file_uploader(
                "업로드할 이미지 파일을 선택하세요.", type=['jpg', 'png'], accept_multiple_files=False, help="JPG 또는 PNG 확장자의 단일 파일만 선택 가능합니다.", disabled=st.session_state.disabled)
            if ss_uploaded is not None:
                ss = Image.open(ss_uploaded)
                st.session_state.ss_image = ss
            st.divider()

            st.text("상품 검색용 키워드를 입력하세요.")
            col11, col12, col13, col14 = st.columns(4)
            with col11:
                search1 = st.text_input(
                    '검색어1', disabled=st.session_state.disabled)
            with col12:
                search2 = st.text_input(
                    '검색어2', disabled=st.session_state.disabled)
            with col13:
                search3 = st.text_input(
                    '검색어3', disabled=st.session_state.disabled)
            with col14:
                search4 = st.text_input(
                    '검색어4', disabled=st.session_state.disabled)
                add1 = st.form_submit_button(label='Save & Display', use_container_width=True)
            st.info("Save & Display 버튼 클릭 후 입력된 키워드의 저장 및 업로드된 이미지의 정상 표시가 가능합니다.", icon="ℹ️")

            if add1:
                for i in [search1, search2, search3, search4]:
                    if not i == "":
                        list_keywords(i)

                st.session_state.keyword_inputs = keywords
                options = st.multiselect(
                    '저장된 검색어 목록입니다.',
                    st.session_state.keyword_inputs,
                    st.session_state.keyword_inputs)

            if not st.session_state.ss_image == "":
                st.image(st.session_state.ss_image)

    # if st.session_state["FormSubmitter:form1-Next"] == True:
    with st.form(key="form2", clear_on_submit=False):
        st.session_state.give_away = st.radio(
                '판매 상품의 증정 또는 회수 여부를 선택하세요.',('증정', '회수'), index=1, disabled=st.session_state.disabled)
        st.divider()

        col3, col4 = st.columns(2)
        with col3:
            st.session_state.product_price = st.number_input(
                '상품 금액', step=1000, disabled=st.session_state.disabled)
        with col4:
            st.session_state.review_amount = st.number_input(
                '리뷰 금액', step=1000, disabled=st.session_state.disabled)
        st.write("######")
        col5, col6 = st.columns(2)
        with col6:
            col7, col8 = st.columns(2)
            with col7:
                previous1 = st.form_submit_button(label='Previous', on_click=enable_inputs, use_container_width=True)
            with col8:
                next1 = st.form_submit_button(label='Next', on_click=disable_inputs, use_container_width=True)
        if next1:
            with col5:
                st.write("합계 금액은", int(st.session_state.product_price + st.session_state.review_amount),"원입니다.")
   
if __name__ == '__main__':
   main()




#    def sum_total():
#     return 

   
#    d = st.date_input("구매 일정", datetime.date(2019, 7, 6))

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
import streamlit as st

st.title("こんにちは吉村ゼミ")
name = st.text_input("好きな言葉を入力してください")

st.write(name)

camera = st.camera_input("写真を撮影しますわ")
if camera:
      st.image(camera, caption="写真", use_column_width=True)

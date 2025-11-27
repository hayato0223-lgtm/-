import streamlit as st

st.title("こんにちは吉村ゼミ")
name = st.text_input("好きな言葉を入力してください")

st.write(name)

st.checkbox("同意します")
address = st.selectbox("次の中から現住所を教えてください",["京都","大阪"])
st.write(address)
hobby = st.multiselect("趣味を次から複数選択してください",["映画","漫画"])
st.write(hobby)
scotre = st.slider("この映画を10点満点で評価してください",0,10,0)
choice = st.radio("性別を選択してください",["男性","女性"])
st.write(choice)
list = [
      {"latitude":35.05,"longitude":135.76},
      {"latitude":35.04,"longitude":135.75},
]
st.map(list)
camera = st.camera_input("写真を撮影しますわ")
if camera:
      st.image(camera, caption="写真", use_column_width=True)

import os
import requests
import streamlit as st

API = "https://api.munsit.com/api/v1"
KEY = os.environ.get("MUNSIT_API_KEY")

st.set_page_config(page_title="استوديو الفويس أوفر", page_icon="🎙️", layout="wide")
st.markdown("<style>textarea {direction: rtl;}</style>", unsafe_allow_html=True)
st.title("🎙️ استوديو الفويس أوفر")

if not KEY:
    st.error("مفتاح MUNSIT_API_KEY مش موجود. اقفل VS Code وافتحه تاني.")
    st.stop()


@st.cache_data(ttl=3600)
def load_voices():
    r = requests.get(f"{API}/voices", headers={"x-api-key": KEY}, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else data.get("data", [])


voices = load_voices()

# ---------- الفلاتر ----------
c1, c2 = st.columns(2)
gender = c1.selectbox("النوع", ["الكل", "رجالي", "نسائي"])
dialects = sorted({d for v in voices for d in (v.get("dialect") or [])})
dialect = c2.selectbox("اللهجة", ["الكل"] + dialects)


def ok(v):
    g = (v.get("gender") or "").lower()
    if gender == "رجالي" and g != "male":
        return False
    if gender == "نسائي" and g != "female":
        return False
    if dialect != "الكل" and dialect not in (v.get("dialect") or []):
        return False
    return True


filtered = [v for v in voices if ok(v)]
st.write(f"عدد الأصوات: {len(filtered)}")

# ---------- المعرض ----------
PER_PAGE = 12
pages = max(1, (len(filtered) + PER_PAGE - 1) // PER_PAGE)
page = st.number_input("الصفحة", min_value=1, max_value=pages, value=1)
start = (page - 1) * PER_PAGE

if "voice_id" not in st.session_state:
    st.session_state.voice_id = None
if "audio" not in st.session_state:
    st.session_state.audio = None

cols = st.columns(3)
for i, v in enumerate(filtered[start:start + PER_PAGE]):
    with cols[i % 3].container(border=True):
        st.subheader(v.get("name") or "-")
        st.caption(f'{",".join(v.get("dialect") or [])} · {v.get("gender")}')
        if v.get("sample_url"):
            st.audio(v["sample_url"])
        if st.button("اختار الصوت ده", key=v["voice_id"]):
            st.session_state.voice_id = v["voice_id"]

# ---------- التوليد ----------
st.divider()
chosen = next((v for v in voices if v["voice_id"] == st.session_state.voice_id), None)
if chosen:
    st.success(f'الصوت المختار: {chosen.get("name")}')
else:
    st.info("اختار صوت من المعرض فوق.")

text = st.text_area("اكتب النص", height=160)
s1, s2 = st.columns(2)
speed = s1.slider("السرعة", 0.7, 1.2, 1.0, 0.05)
stability = s2.slider("ثبات الصوت", 0.0, 1.0, 0.5, 0.05)
st.caption(f"عدد الحروف: {len(text)} (الرصيد المجاني حوالي 5000 حرف)")

if st.button("🎙️ توليد الصوت", type="primary"):
    if not chosen or not text.strip():
        st.warning("اختار صوت واكتب النص الأول.")
    else:
        with st.spinner("جاري التوليد..."):
            r = requests.post(
                f"{API}/text-to-speech/faseeh-v1-preview",
                headers={"x-api-key": KEY, "Content-Type": "application/json"},
                json={
                    "voice_id": chosen["voice_id"],
                    "text": text,
                    "stability": stability,
                    "speed": speed,
                    "streaming": False,
                },
                timeout=120,
            )
        if r.status_code == 200:
            st.session_state.audio = r.content
        else:
            st.error(f"Error {r.status_code}: {r.text}")

if st.session_state.audio:
    st.audio(st.session_state.audio, format="audio/wav")
    st.download_button("⬇️ تحميل الصوت", st.session_state.audio, "voiceover.wav", "audio/wav")
    import streamlit as st

st.set_page_config(page_title="Abdelrahman Nabil Tools", page_icon="🎙️", layout="wide")
st.set_page_config = lambda *a, **k: None  # عشان أي set_page_config قديم ميعملش خطأ

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800&display=swap');
html, body, .stApp, button, input, textarea { font-family: 'Plus Jakarta Sans','Tajawal',sans-serif !important; }
.stApp {
  background:
    radial-gradient(ellipse 55% 45% at 0% 55%, rgba(255,109,41,.45), transparent 70%),
    radial-gradient(ellipse 45% 40% at 100% 100%, rgba(255,109,41,.18), transparent 70%),
    linear-gradient(165deg, #161316 0%, #1f120b 50%, #2e1a10 100%);
  background-attachment: fixed; color:#fff;
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stHeader"] { display:none !important; }
.block-container { max-width:1180px; padding-top:2rem; padding-bottom:4rem; }
h1 { display:none; }
.hero-badge { display:inline-block; padding:.35rem 1.1rem; border:1px solid #FF6D29; border-radius:999px; color:#FF6D29; background:rgba(255,109,41,.1); margin-bottom:1rem; }
.hero-title { font-size:clamp(2.4rem,5.5vw,4.4rem); line-height:1.05; font-weight:700; letter-spacing:-0.03em; color:#fff; }
.hero-title span { background:linear-gradient(90deg,#ff9a5c,#FF6D29); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-sub { color:#BABABA; font-size:1.15rem; margin:.9rem 0 2rem; }
[data-testid="stSidebar"] { background:rgba(22,19,22,.72); backdrop-filter:blur(18px); border-right:1px solid rgba(255,109,41,.38); }
[data-testid="stVerticalBlockBorderWrapper"]:not(:has([data-testid="stVerticalBlockBorderWrapper"])) {
  background:linear-gradient(145deg, rgba(255,255,255,.075), rgba(255,109,41,.05));
  border:1px solid rgba(255,109,41,.38); border-radius:28px; padding:.6rem .5rem;
  backdrop-filter:blur(14px); box-shadow:inset 0 1px 0 rgba(255,255,255,.08), 0 12px 40px rgba(0,0,0,.35);
}
.stButton > button, .stDownloadButton > button {
  border-radius:999px; padding:.65rem 1.8rem; font-size:1.05rem; font-weight:600;
  color:#fff; background:rgba(255,109,41,.14); border:1px solid #FF6D29;
}
.stButton > button:hover, .stDownloadButton > button:hover { background:#FF6D29; color:#161316; border-color:#FF6D29; }
.stButton > button[kind="primary"] { background:#FF6D29; color:#161316; }
[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, .stNumberInput input {
  background:rgba(255,255,255,.06) !important; border:1px solid rgba(255,109,41,.32) !important;
  border-radius:999px !important; color:#fff !important;
}
.stTextArea textarea { border-radius:24px !important; padding:1rem 1.2rem; font-size:1.05rem; }
[data-testid="stNumberInputContainer"] { border-radius:999px !important; overflow:hidden; border:0 !important; }
[data-testid="stNumberInputContainer"] button { background:#FF6D29 !important; color:#161316 !important; }
label, [data-testid="stWidgetLabel"] p { color:#BABABA !important; }
audio { width:100%; height:44px; border-radius:999px; color-scheme:dark; }
[data-testid="stAlert"] { border-radius:22px; border:1px solid rgba(255,109,41,.38); }
</style>
<div>
  <div class="hero-badge">Voice Over Studio</div>
  <div class="hero-title">Abdelrahman Nabil<br><span>Tools.</span></div>
  <div class="hero-sub">حوّل نصك لصوت احترافي بأكتر من ١٧٠ صوت.</div>
</div>
""", unsafe_allow_html=True)
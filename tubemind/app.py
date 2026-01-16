import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import ollama
import sqlite3
import json

# --- ⚙️ CONFIGURATION ---
DB_FILE = "tubemind.db"
MODEL_NAME = "llama3" # Make sure you have this pulled in Ollama

# --- 💾 DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (id TEXT PRIMARY KEY, title TEXT, transcript TEXT, summary TEXT)''')
    conn.commit()
    conn.close()

# --- 🎥 HELPER FUNCTIONS ---
def get_video_id(url):
    """Extracts video ID from URL"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    return None

def fetch_transcript(video_id):
    """Fetches subtitles from YouTube"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine list of dicts into a single string
        full_text = " ".join([t['text'] for t in transcript_list])
        return full_text
    except Exception as e:
        return None

def generate_summary(text):
    """Sends text to Local LLM for summarization"""
    prompt = f"""
    You are a technical assistant. Summarize the following video transcript. 
    Focus on extracting code concepts, libraries mentioned, and key architectural decisions.
    Keep it concise (under 200 words).
    
    Transcript: {text[:10000]} 
    """ 
    # Truncating text to 10k chars to fit context window if needed
    
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'user', 'content': prompt},
    ])
    return response['message']['content']

# --- 🖥️ STREAMLIT UI ---
def main():
    st.set_page_config(page_title="TubeMind AI", page_icon="🧠", layout="wide")
    
    # Custom CSS for that "2026 Dark Mode" look
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; }
        .stTextInput > div > div > input { background-color: #262730; color: white; }
        .stButton button { background-color: #FF4B4B; color: white; border-radius: 8px; }
        h1 { color: #FF4B4B; }
        </style>
    """, unsafe_allow_html=True)

    init_db()

    st.title("🧠 TubeMind: Local Video Knowledge Base")
    st.caption("Archive YouTube knowledge using Local LLMs.")

    # Sidebar: History
    st.sidebar.header("📚 Library")
    conn = sqlite3.connect(DB_FILE)
    saved_videos = conn.execute("SELECT title, id FROM videos").fetchall()
    conn.close()

    if saved_videos:
        for title, vid_id in saved_videos:
            if st.sidebar.button(f"📄 {title[:20]}...", key=vid_id):
                st.session_state['selected_video'] = vid_id

    # Main Input Area
    url = st.text_input("Paste YouTube URL here:", placeholder="https://youtube.com/watch?v=...")

    if st.button("Analyze Video"):
        video_id = get_video_id(url)
        
        if not video_id:
            st.error("Invalid YouTube URL")
        else:
            with st.status("🚀 Processing...", expanded=True) as status:
                st.write("📥 Fetching Transcript...")
                transcript = fetch_transcript(video_id)
                
                if not transcript:
                    status.update(label="❌ Failed to get transcript (Video might not have captions)", state="error")
                else:
                    st.write("🤖 Generating AI Summary (Llama 3)...")
                    summary = generate_summary(transcript)
                    
                    # Save to DB
                    # Note: We don't have the real title easily without an API key, 
                    # so we use a placeholder or extract from oEmbed (skipped for simplicity)
                    video_title = f"Video {video_id}" 
                    
                    conn = sqlite3.connect(DB_FILE)
                    conn.execute("INSERT OR REPLACE INTO videos (id, title, transcript, summary) VALUES (?, ?, ?, ?)", 
                                 (video_id, video_title, transcript, summary))
                    conn.commit()
                    conn.close()
                    
                    status.update(label="✅ Done!", state="complete")
                    st.rerun()

    # Display Selected Video Data
    if 'selected_video' in st.session_state:
        conn = sqlite3.connect(DB_FILE)
        data = conn.execute("SELECT * FROM videos WHERE id=?", (st.session_state['selected_video'],)).fetchone()
        conn.close()
        
        if data:
            vid_id, title, transcript, summary = data
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.video(f"https://www.youtube.com/watch?v={vid_id}")
                st.subheader("🤖 AI Summary")
                st.info(summary)
            
            with col2:
                st.subheader("📜 Full Transcript")
                st.text_area("Search transcript", transcript, height=600)

if __name__ == "__main__":
    main()
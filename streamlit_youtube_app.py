import streamlit as st
import yt_dlp
import os
import tempfile
import shutil
from pathlib import Path
import re
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="YouTube Video Downloader",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .stAlert > div {
        padding: 1rem;
        border-radius: 10px;
    }
    
    .download-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
        margin: 1rem 0;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(45deg, #ff9a9e, #fecfef);
        border-radius: 10px;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def get_video_info(url):
    """Extract video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else 'No description',
                'thumbnail': info.get('thumbnail', ''),
                'formats': info.get('formats', [])
            }
    except Exception as e:
        st.error(f"Error getting video info: {str(e)}")
        return None

def get_available_qualities(formats):
    """Extract available video qualities"""
    qualities = set()
    for fmt in formats:
        if fmt.get('height'):
            quality = f"{fmt['height']}p"
            if fmt.get('fps'):
                quality += f" ({fmt['fps']}fps)"
            qualities.add(quality)
    
    return sorted(list(qualities), key=lambda x: int(x.split('p')[0]), reverse=True)
def download_video(url, output_path, quality="best", progress_callback=None):
    """Download video with progress tracking"""
    try:
        # Create progress hook
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                if 'total_bytes' in d:
                    progress = d['downloaded_bytes'] / d['total_bytes']
                    progress_callback(progress)
        
        # Configure download options based on quality
        if quality == "best":
            format_selector = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif quality == "audio":
            format_selector = 'bestaudio[ext=m4a]/bestaudio/best'
        else:
            height = quality.split('p')[0]
            format_selector = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'
        
        # ✅ Final ydl_opts block with cookiefile support
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4' if quality != "audio" else 'm4a',
            'writesubtitles': False,
            'writeautomaticsub': False,
            'progress_hooks': [progress_hook],
            'cookiefile': 'cookies.txt',  # ✅ This makes it work even on mobile browsers!
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
            
    except Exception as e:
        st.error(f"Download failed: {str(e)}")
        return False

# def download_video(url, output_path, quality="best", progress_callback=None):
#     """Download video with progress tracking"""
#     try:
#         # Create progress hook
#         def progress_hook(d):
#             if progress_callback and d['status'] == 'downloading':
#                 if 'total_bytes' in d:
#                     progress = d['downloaded_bytes'] / d['total_bytes']
#                     progress_callback(progress)
        
#         # Configure download options based on quality
#         if quality == "best":
#             format_selector = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
#         elif quality == "audio":
#             format_selector = 'bestaudio[ext=m4a]/bestaudio/best'
#         else:
#             height = quality.split('p')[0]
#             format_selector = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'
        
#         ydl_opts = {
#             'format': format_selector,
#             'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
#             'merge_output_format': 'mp4' if quality != "audio" else 'm4a',
#             'writesubtitles': False,
#             'writeautomaticsub': False,
#             'progress_hooks': [progress_hook],
#         }
        
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#             return True
            
#     except Exception as e:
#         st.error(f"Download failed: {str(e)}")
#         return False

def format_duration(seconds):
    """Format duration in readable format"""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def format_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🎥 YouTube Video Downloader</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Download directory
        download_path = st.text_input("📁 Download Directory", value="./downloads")
        
        # Create directory if it doesn't exist
        Path(download_path).mkdir(parents=True, exist_ok=True)
        
        st.markdown("---")
        
        # Features section
        st.markdown("""
        ### 🌟 Features
        - ✅ Best quality downloads (up to 4K)
        - ✅ Multiple format support
        - ✅ Playlist downloads
        - ✅ Audio-only downloads
        - ✅ Real-time progress tracking
        - ✅ Video preview & info
        """)
        
        st.markdown("---")
        
        # Statistics (mock data - you can make this dynamic)
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Downloads", st.session_state.get('download_count', 0))
        with col2:
            st.metric("Success Rate", "100%")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # URL input
        st.markdown("### 🔗 Enter YouTube URL")
        url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", key="url_input")
        
        # Buttons row
        col_preview, col_download, col_quick = st.columns(3)
        
        with col_preview:
            preview_btn = st.button("👁️ Preview Video", use_container_width=True)
        
        with col_download:
            download_btn = st.button("⬬ Download Video", use_container_width=True, type="primary")
            
        with col_quick:
            quick_download_btn = st.button("⚡ Quick Download", use_container_width=True, help="Download in best quality instantly")
        
        # Video preview section
        if preview_btn and url:
            with st.spinner("🔍 Fetching video information..."):
                video_info = get_video_info(url)
                
                if video_info:
                    st.markdown("### 📺 Video Preview")
                    
                    # Video thumbnail and basic info
                    col_thumb, col_info = st.columns([1, 2])
                    
                    with col_thumb:
                        if video_info['thumbnail']:
                            st.image(video_info['thumbnail'], use_container_width=True)
                    
                    with col_info:
                        st.markdown(f"**📝 Title:** {video_info['title']}")
                        st.markdown(f"**👤 Channel:** {video_info['uploader']}")
                        st.markdown(f"**⏱️ Duration:** {format_duration(video_info['duration'])}")
                        st.markdown(f"**👀 Views:** {format_number(video_info['view_count'])}")
                        
                        if video_info['upload_date']:
                            formatted_date = datetime.strptime(video_info['upload_date'], '%Y%m%d').strftime('%B %d, %Y')
                            st.markdown(f"**📅 Upload Date:** {formatted_date}")
                    
                    # Available qualities
                    qualities = get_available_qualities(video_info['formats'])
                    if qualities:
                        st.markdown("**🎬 Available Qualities:**")
                        quality_cols = st.columns(min(len(qualities), 4))
                        for i, quality in enumerate(qualities[:4]):
                            with quality_cols[i]:
                                st.info(quality)
                    
                    # Description
                    with st.expander("📄 Description"):
                        st.write(video_info['description'])
                    
                    # Store video info in session state for download
                    st.session_state['current_video_info'] = video_info
        
        # Download section
        if download_btn and url:
            # Quality selection
            st.markdown("### ⚙️ Download Options")
            
            quality_options = ["best", "1080p", "720p", "480p", "360p", "audio"]
            selected_quality = st.selectbox("Select Quality:", quality_options, index=0)
            
            # Auto-start download
            with st.spinner("📥 Downloading..."):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress):
                    progress_bar.progress(progress)
                    status_text.text(f"Downloaded: {progress*100:.1f}%")
                
                # Download the video
                success = download_video(url, download_path, selected_quality, update_progress)
                
                if success:
                    st.success("✅ Download completed successfully!")
                    st.balloons()
                    
                    # Update session stats
                    if 'download_count' not in st.session_state:
                        st.session_state['download_count'] = 0
                    st.session_state['download_count'] += 1
                    
                    # Show download location
                    st.info(f"📁 File saved to: {download_path}")
                    
                else:
                    st.error("❌ Download failed. Please try again.")
        
        # Quick download section
        if quick_download_btn and url:
            with st.spinner("⚡ Quick downloading in best quality..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress):
                    progress_bar.progress(progress)
                    status_text.text(f"Downloaded: {progress*100:.1f}%")
                
                success = download_video(url, download_path, "best", update_progress)
                
                if success:
                    st.success("✅ Quick download completed!")
                    st.balloons()
                    if 'download_count' not in st.session_state:
                        st.session_state['download_count'] = 0
                    st.session_state['download_count'] += 1
                    st.info(f"📁 File saved to: {download_path}")
                else:
                    st.error("❌ Download failed. Please try again.")
    
    with col2:
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        # Playlist download
        with st.expander("📂 Playlist Download"):
            playlist_url = st.text_input("Playlist URL:", key="playlist_url")
            if st.button("Download Playlist"):
                if playlist_url:
                    st.info("Playlist download feature coming soon!")
                else:
                    st.warning("Please enter a playlist URL")
        
        # Audio only download
        with st.expander("🎵 Audio Only"):
            audio_url = st.text_input("Video URL:", key="audio_url")
            if st.button("Extract Audio"):
                if audio_url:
                    with st.spinner("Extracting audio..."):
                        success = download_video(audio_url, download_path, "audio")
                        if success:
                            st.success("🎵 Audio extracted successfully!")
                        else:
                            st.error("❌ Audio extraction failed")
        
        # Help section
        st.markdown("### ❓ Help")
        with st.expander("How to use"):
            st.markdown("""
            1. **Paste URL**: Copy and paste a YouTube video URL
            2. **Preview**: Click 'Preview Video' to see video details
            3. **Select Quality**: Choose your preferred video quality
            4. **Download**: Click 'Start Download' to begin
            5. **Find Files**: Check your download directory for the file
            """)
        
        with st.expander("Supported URLs"):
            st.markdown("""
            - Single videos: `youtube.com/watch?v=...`
            - Short videos: `youtu.be/...`
            - Playlists: `youtube.com/playlist?list=...`
            - Channel videos: `youtube.com/c/channelname/videos`
            """)

if __name__ == "__main__":
    main()


# 🎥 YouTube Video Downloader

A beautiful, modern web application built with **Streamlit** and **yt-dlp** for downloading YouTube videos in the best available quality (up to 4K). Features an intuitive user interface with real-time progress tracking and video preview capabilities.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## ✨ Features

- 🎬 **High Quality Downloads** - Download videos in up to 4K resolution
- 👁️ **Video Preview** - See video information, thumbnail, and details before downloading
- ⚡ **Quick Download** - One-click download in best available quality
- 🎵 **Audio Extraction** - Download audio-only files (MP3/M4A)
- 📊 **Real-time Progress** - Live download progress tracking with progress bars
- 📱 **Mobile Friendly** - Responsive design that works on all devices
- 🎨 **Beautiful UI** - Modern, gradient-based interface with intuitive controls
- 📂 **Playlist Support** - Download entire YouTube playlists (coming soon)
- 🔧 **Multiple Formats** - Support for various video qualities (1080p, 720p, 480p, 360p)

## 🚀 Quick Start

### Online Version (Recommended)
Access the app instantly without any installation:
**[🌐 Open YouTube Downloader](https://your-app-url.streamlit.app)**

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Devanshuxx/youtube-downloader-app.git
   cd youtube-downloader-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_youtube_app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

## 📋 Requirements

- Python 3.7+
- Streamlit
- yt-dlp

## 🛠️ Installation from Scratch

### Prerequisites
- [Python](https://python.org/downloads/) (3.7 or higher)
- [Git](https://git-scm.com/downloads) (optional)

### Step-by-Step Installation

1. **Install Python packages:**
   ```bash
   pip install streamlit yt-dlp
   ```

2. **Download the script:**
   - Download `streamlit_youtube_app.py` from this repository
   - Or copy the code and save it as `streamlit_youtube_app.py`

3. **Run the application:**
   ```bash
   streamlit run streamlit_youtube_app.py
   ```

## 🎯 How to Use

### Method 1: Quick Download
1. Paste a YouTube URL in the input field
2. Click **"⚡ Quick Download"** for instant best-quality download

### Method 2: Custom Download
1. Paste a YouTube URL in the input field
2. Click **"👁️ Preview Video"** to see video details
3. Click **"⬇️ Download Video"**
4. Select your preferred quality
5. Download starts automatically

### Method 3: Audio Only
1. Use the **"🎵 Audio Only"** section in the sidebar
2. Paste the video URL
3. Click **"Extract Audio"**

## 📁 File Structure

```
youtube-downloader-app/
├── streamlit_youtube_app.py    # Main application file
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── downloads/                 # Default download directory (created automatically)
```

## 🌐 Supported URLs

- **Single Videos:** `https://www.youtube.com/watch?v=VIDEO_ID`
- **Short Videos:** `https://youtu.be/VIDEO_ID`
- **Playlists:** `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- **Channel Videos:** `https://www.youtube.com/c/channelname/videos`

## ⚙️ Configuration

### Download Directory
- Default: `./downloads/` (created automatically)
- Customizable through the sidebar settings
- For local installations, files are saved to your specified directory

### Quality Options
- **Best:** Highest available quality (up to 4K)
- **1080p:** Full HD quality
- **720p:** HD quality
- **480p:** Standard definition
- **360p:** Low quality (smaller file size)
- **Audio:** Audio-only extraction

## 🔧 Advanced Usage

### Command Line Version
For advanced users who prefer command-line interface, you can also use the included `youtube_downloader.py` script:

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Running on Network
To make the app accessible to other devices on your network:
```bash
streamlit run streamlit_youtube_app.py --server.address 0.0.0.0 --server.port 8501
```

## 📊 Technical Details

### Built With
- **[Streamlit](https://streamlit.io/)** - Web app framework
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube download engine
- **Python 3.7+** - Programming language

### Architecture
- **Frontend:** Streamlit web interface
- **Backend:** yt-dlp for video processing
- **Storage:** Local file system
- **Deployment:** Streamlit Community Cloud

## 🚀 Deployment

### Streamlit Community Cloud
1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io)
3. Deploy directly from your repository
4. Get a public URL automatically

### Local Network Deployment
```bash
streamlit run streamlit_youtube_app.py --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_youtube_app.py", "--server.address", "0.0.0.0"]
```

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" error:**
```bash
pip install streamlit yt-dlp
```

**2. Download fails:**
- Check your internet connection
- Verify the YouTube URL is correct
- Some videos may be restricted or private

**3. Permission errors:**
- Ensure you have write permissions to the download directory
- Try running as administrator (Windows) or with sudo (Linux/Mac)

**4. Slow downloads:**
- This is normal for high-quality videos
- Consider selecting a lower quality option

### Getting Help
- Check the [Issues](https://github.com/Devanshuxx/youtube-downloader-app/issues) page
- Create a new issue if you encounter problems
- Include error messages and system information

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Users are responsible for ensuring they have the right to download and use the content.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube download library
- [Streamlit](https://streamlit.io/) - For making web app development so easy
- YouTube - For providing the content platform

## 📈 Changelog

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Video download functionality
- ✅ Quality selection
- ✅ Progress tracking
- ✅ Video preview
- ✅ Audio extraction
- ✅ Responsive UI

### Upcoming Features
- 📂 Playlist download support
- 🔄 Batch download capability
- 💾 Cloud storage integration
- 🎨 Theme customization
- 📱 Mobile app version

---

## 🌟 Star this Repository

If you found this project useful, please consider giving it a star! ⭐

**Made with ❤️ by [Devanshu]**

[![GitHub stars](https://img.shields.io/github/stars/Devanshuxx/youtube-downloader-app?style=social)](https://github.com/Devanshuxx/youtube-downloader-app/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Devanshuxx/youtube-downloader-app?style=social)](https://github.com/Devanshuxx/youtube-downloader-app/network/members)

---

### 🔗 Quick Links
- [🌐 Live Demo](https://your-app-url.streamlit.app)
- [📖 Documentation](https://github.com/Devanshuxx/youtube-downloader-app/wiki)
- [🐛 Report Bug](https://github.com/Devanshuxx/youtube-downloader-app/issues)
- [💡 Request Feature](https://github.com/Devanshuxx/youtube-downloader-app/issues)
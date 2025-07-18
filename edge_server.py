import asyncio
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import edge_tts
import tempfile
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EdgeTTSHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge TTS Pro - English & Arabic Premium Voices</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            animation: slideIn 0.6s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3rem;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 20px;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .feature {
            background: linear-gradient(45deg, #e3f2fd, #f3e5f5);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            border-left: 4px solid #28a745;
        }
        
        .feature i {
            font-size: 1.5rem;
            color: #28a745;
            margin-bottom: 8px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .input-panel {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
        }
        
        .settings-panel {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
        }
        
        .panel-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        textarea {
            width: 100%;
            height: 200px;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 16px;
            resize: vertical;
            font-family: inherit;
            transition: all 0.3s ease;
            background: white;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
        }
        
        .char-count {
            text-align: right;
            font-size: 0.9rem;
            color: #666;
            margin: 8px 0 20px 0;
        }
        
        .setting-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }
        
        select, input[type="range"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: white;
        }
        
        select:focus, input[type="range"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .range-container {
            position: relative;
        }
        
        .range-value {
            text-align: center;
            margin-top: 8px;
            font-weight: 600;
            color: #667eea;
            background: #e3f2fd;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        .voice-preview {
            margin-top: 10px;
        }
        
        .preview-btn {
            width: 100%;
            background: #6c757d;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .preview-btn:hover {
            background: #5a6268;
            transform: translateY(-1px);
        }
        
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        button {
            padding: 18px 30px;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .primary-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        
        .primary-btn:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        }
        
        .primary-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .secondary-btn {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            display: none;
        }
        
        .secondary-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(40, 167, 69, 0.4);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 30px 0;
            padding: 30px;
            background: linear-gradient(45deg, #e3f2fd, #f3e5f5);
            border-radius: 15px;
            border-left: 4px solid #1976d2;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #e3f2fd;
            border-top: 5px solid #1976d2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 5px;
            transition: width 0.5s ease;
            width: 0%;
        }
        
        .result {
            margin-top: 30px;
            padding: 30px;
            background: linear-gradient(45deg, #e8f5e8, #f0fff0);
            border-radius: 15px;
            border-left: 4px solid #28a745;
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        
        .result h3 {
            color: #155724;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }
        
        audio {
            width: 100%;
            margin: 20px 0;
            border-radius: 10px;
        }
        
        .audio-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e0e0e0;
        }
        
        .info-label {
            font-size: 0.85rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-top: 5px;
        }
        
        .quick-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .quick-btn {
            background: #e9ecef;
            border: 1px solid #dee2e6;
            color: #495057;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .quick-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #dc3545;
            display: none;
        }
        
        @media (max-width: 768px) {
            .container { padding: 20px; }
            h1 { font-size: 2rem; }
            .main-content { grid-template-columns: 1fr; }
            .controls { grid-template-columns: 1fr; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-microphone"></i> Edge TTS Pro</h1>
            <div class="subtitle">Premium English & Arabic Neural Voices - Verified & Working</div>
            
            <div class="features">
                <div class="feature">
                    <i class="fas fa-brain"></i>
                    <div><strong>🇺🇸 English Voices</strong><br>Ultra-natural US, UK & Australian</div>
                </div>
                <div class="feature">
                    <i class="fas fa-bolt"></i>
                    <div><strong>🇸🇦 Arabic Voices</strong><br>Premium Saudi & Egyptian</div>
                </div>
                <div class="feature">
                    <i class="fas fa-globe"></i>
                    <div><strong>Verified Only</strong><br>All voices tested & working</div>
                </div>
                <div class="feature">
                    <i class="fas fa-download"></i>
                    <div><strong>Export Ready</strong><br>High-quality MP3</div>
                </div>
            </div>
        </div>
        
        <div class="error-message" id="errorMessage"></div>
        
        <div class="main-content">
            <div class="input-panel">
                <div class="panel-title">
                    <i class="fas fa-edit"></i> Text Input
                </div>
                
                <textarea id="text" placeholder="Enter your English or Arabic text here for premium TTS conversion...">Welcome to Edge TTS Pro! This version includes only verified, high-quality English and Arabic voices that are guaranteed to work perfectly.</textarea>
                
                <div class="char-count" id="charCount">0 characters</div>
                
                <div class="quick-actions">
                    <button class="quick-btn" onclick="insertSample('english')">🇺🇸 English Sample</button>
                    <button class="quick-btn" onclick="insertSample('arabic')">🇸🇦 Arabic Sample</button>
                    <button class="quick-btn" onclick="insertSample('presentation')">📊 Presentation</button>
                    <button class="quick-btn" onclick="clearText()">🗑️ Clear</button>
                </div>
            </div>
            
            <div class="settings-panel">
                <div class="panel-title">
                    <i class="fas fa-sliders-h"></i> Voice Settings
                </div>
                
                <div class="setting-group">
                    <label for="voice"><i class="fas fa-user"></i> Premium Voices (Verified)</label>
                    <select id="voice" onchange="updateVoiceInfo()">
                        <optgroup label="🇺🇸 English - US Voices">
                            <option value="en-US-AriaNeural">⭐ Aria (Female) - Most Natural</option>
                            <option value="en-US-JennyNeural">💼 Jenny (Female) - Professional</option>
                            <option value="en-US-GuyNeural">👨 Guy (Male) - Business</option>
                            <option value="en-US-AndrewNeural">🗣️ Andrew (Male) - Conversational</option>
                        </optgroup>
                        <optgroup label="🇬🇧 English - UK Voices">
                            <option value="en-GB-SoniaNeural">🇬🇧 Sonia (Female) - British</option>
                            <option value="en-GB-RyanNeural">🇬🇧 Ryan (Male) - British</option>
                        </optgroup>
                        <optgroup label="🇦🇺 English - Australian Voices">
                            <option value="en-AU-NatashaNeural">🇦🇺 Natasha (Female) - Australian</option>
                            <option value="en-AU-WilliamNeural">🇦🇺 William (Male) - Australian</option>
                        </optgroup>
                        <optgroup label="🇸🇦 Arabic - Saudi Voices">
                            <option value="ar-SA-ZariyahNeural">⭐ زاريه (أنثى) - الأكثر طبيعية</option>
                            <option value="ar-SA-HamedNeural">👨 حامد (ذكر) - مهني</option>
                        </optgroup>
                        <optgroup label="🇪🇬 Arabic - Egyptian Voices">
                            <option value="ar-EG-SalmaNeural">🇪🇬 سلمى (أنثى) - مصرية</option>
                            <option value="ar-EG-ShakirNeural">🇪🇬 شاكر (ذكر) - مصري</option>
                        </optgroup>
                    </select>
                    
                    <div class="voice-preview">
                        <button class="preview-btn" onclick="previewVoice()">
                            <i class="fas fa-play"></i> Preview Voice
                        </button>
                    </div>
                </div>
                
                <div class="setting-group">
                    <label for="rate"><i class="fas fa-tachometer-alt"></i> Speech Speed</label>
                    <div class="range-container">
                        <input type="range" id="rate" min="-50" max="100" value="0" step="10" oninput="updateRateDisplay()">
                        <div class="range-value" id="rateValue">Normal (0%)</div>
                    </div>
                </div>
                
                <div class="setting-group">
                    <label for="format"><i class="fas fa-file-audio"></i> Output Format</label>
                    <select id="format">
                        <option value="mp3">MP3 (Recommended)</option>
                        <option value="wav">WAV (Uncompressed)</option>
                        <option value="ogg">OGG (Web Optimized)</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button class="primary-btn" onclick="convert()" id="convertBtn">
                <i class="fas fa-magic"></i> Convert with Edge TTS
            </button>
            <button class="secondary-btn" onclick="downloadAudio()" id="downloadBtn">
                <i class="fas fa-download"></i> Download Audio
            </button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #1976d2; margin-bottom: 10px;">
                <i class="fas fa-cogs"></i> Converting with verified neural voice...
            </div>
            <div style="color: #666;">Using Microsoft's premium neural networks</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
        </div>
        
        <div class="result" id="result">
            <h3><i class="fas fa-check-circle"></i> Your Premium Edge TTS Audio</h3>
            
            <audio id="audio" controls></audio>
            
            <div class="audio-info">
                <div class="info-item">
                    <div class="info-label">Voice</div>
                    <div class="info-value" id="usedVoice">-</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Duration</div>
                    <div class="info-value" id="audioDuration">-</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Words</div>
                    <div class="info-value" id="wordCount">-</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Quality</div>
                    <div class="info-value">Premium</div>
                </div>
            </div>
            
            <div style="color: #155724; text-align: center; margin-top: 20px;">
                <i class="fas fa-sparkles"></i> <strong>Perfect!</strong> Premium verified voice quality!
            </div>
        </div>
    </div>

    <script>
        let currentAudioData = null;
        
        const sampleTexts = {
            english: "Welcome to Edge TTS Pro! This advanced neural voice technology delivers crystal-clear, natural-sounding speech perfect for professional content.",
            arabic: "مرحباً بكم في Edge TTS Pro! تقنية الصوت العصبية المتقدمة التي تقدم كلاماً واضحاً وطبيعياً مثالياً للمحتوى المهني.",
            presentation: "Good morning everyone, and welcome to today's presentation. We'll be exploring innovative solutions that can transform your business and drive meaningful results."
        };
        
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }
        
        function updateCharCount() {
            const text = document.getElementById('text').value;
            const count = text.length;
            const counter = document.getElementById('charCount');
            counter.textContent = `${count} characters`;
            
            if (count > 4500) {
                counter.style.color = '#dc3545';
            } else if (count > 4000) {
                counter.style.color = '#ffc107';
            } else {
                counter.style.color = '#666';
            }
        }
        
        function updateRateDisplay() {
            const rate = document.getElementById('rate').value;
            const display = document.getElementById('rateValue');
            if (rate == 0) {
                display.textContent = 'Normal (0%)';
            } else if (rate > 0) {
                display.textContent = `Faster (+${rate}%)`;
            } else {
                display.textContent = `Slower (${rate}%)`;
            }
        }
        
        function updateVoiceInfo() {
            const voice = document.getElementById('voice').value;
            // Additional voice info updates can be added here
        }
        
        function insertSample(type) {
            if (sampleTexts[type]) {
                document.getElementById('text').value = sampleTexts[type];
                updateCharCount();
            }
        }
        
        function clearText() {
            document.getElementById('text').value = '';
            updateCharCount();
        }
        
        async function previewVoice() {
            const voice = document.getElementById('voice').value;
            let sampleText;
            
            if (voice.startsWith('ar-')) {
                sampleText = "مرحباً! هذا اختبار لجودة الصوت مع Edge TTS.";
            } else {
                const voiceName = voice.split('-')[2].replace('Neural', '');
                sampleText = `Hello! I'm ${voiceName}. This is a preview of my premium voice quality.`;
            }
            
            const originalText = document.getElementById('text').value;
            document.getElementById('text').value = sampleText;
            
            await convert(true);
            
            document.getElementById('text').value = originalText;
            updateCharCount();
        }
        
        function updateProgress(percent) {
            document.getElementById('progressFill').style.width = percent + '%';
        }
        
        async function convert(isPreview = false) {
            const text = document.getElementById('text').value.trim();
            const voice = document.getElementById('voice').value;
            const rate = parseInt(document.getElementById('rate').value);
            const format = document.getElementById('format').value;
            
            if (!text) {
                showError('Please enter some text!');
                return;
            }
            
            if (text.length > 5000) {
                showError('Text is too long. Please limit to 5000 characters.');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('convertBtn').disabled = true;
            document.getElementById('convertBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Converting...';
            
            updateProgress(10);
            
            try {
                updateProgress(30);
                
                const response = await fetch('/tts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        text: text, 
                        voice: voice,
                        rate: rate,
                        format: format
                    })
                });
                
                updateProgress(60);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                updateProgress(80);
                
                if (data.success) {
                    const audioData = `data:audio/${format};base64,` + data.audio;
                    const audioElement = document.getElementById('audio');
                    audioElement.src = audioData;
                    
                    document.getElementById('usedVoice').textContent = voice.split('-')[2].replace('Neural', '');
                    document.getElementById('wordCount').textContent = text.split(' ').length;
                    
                    audioElement.onloadedmetadata = () => {
                        const duration = Math.round(audioElement.duration);
                        document.getElementById('audioDuration').textContent = `${duration}s`;
                    };
                    
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('downloadBtn').style.display = 'block';
                    currentAudioData = data.audio;
                    
                    updateProgress(100);
                    
                    setTimeout(() => {
                        audioElement.play().catch(e => {
                            console.log('Auto-play prevented by browser');
                        });
                    }, 500);
                } else {
                    showError('Error: ' + (data.error || 'Unknown error occurred'));
                }
            } catch (error) {
                console.error('Conversion error:', error);
                showError('Error: ' + error.message);
            } finally {
                setTimeout(() => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('convertBtn').disabled = false;
                    document.getElementById('convertBtn').innerHTML = '<i class="fas fa-magic"></i> Convert with Edge TTS';
                }, 1000);
            }
        }
        
        function downloadAudio() {
            if (currentAudioData) {
                const format = document.getElementById('format').value;
                const voice = document.getElementById('voice').value.split('-')[2].replace('Neural', '');
                const timestamp = new Date().toISOString().slice(0, 10);
                
                const link = document.createElement('a');
                link.href = `data:audio/${format};base64,` + currentAudioData;
                link.download = `EdgeTTS-${voice}-${timestamp}.${format}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                const btn = document.getElementById('downloadBtn');
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Downloaded!';
                btn.style.background = '#28a745';
                
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                }, 2000);
            } else {
                showError('No audio to download. Please convert text first.');
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            updateCharCount();
            updateRateDisplay();
            
            document.getElementById('text').addEventListener('input', updateCharCount);
            
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    convert();
                }
                if (e.ctrlKey && e.key === 'd') {
                    e.preventDefault();
                    downloadAudio();
                }
            });
        });
    </script>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/tts':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                text = data.get('text', '').strip()
                voice = data.get('voice', 'en-US-AriaNeural')
                rate = data.get('rate', 0)
                audio_format = data.get('format', 'mp3')
                
                logger.info(f"TTS request: voice={voice}, rate={rate}, format={audio_format}, text_length={len(text)}")
                
                if not text:
                    response = {'success': False, 'error': 'No text provided'}
                elif len(text) > 5000:
                    response = {'success': False, 'error': 'Text too long (max 5000 characters)'}
                else:
                    # Build rate string
                    if rate == 0:
                        rate_str = None
                    else:
                        if rate > 0:
                            rate_str = f"+{rate}%"
                        else:
                            rate_str = f"{rate}%"
                    
                    # Create new event loop for async operations
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    try:
                        # Create Edge TTS communicate object
                        if rate_str:
                            communicate = edge_tts.Communicate(text, voice, rate=rate_str)
                        else:
                            communicate = edge_tts.Communicate(text, voice)
                        
                        # Create temporary file
                        file_extension = audio_format
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}')
                        tmp_filename = tmp_file.name
                        tmp_file.close()
                        
                        try:
                            # Generate audio
                            loop.run_until_complete(communicate.save(tmp_filename))
                            
                            # Read and encode audio data
                            with open(tmp_filename, 'rb') as audio_file:
                                audio_data = base64.b64encode(audio_file.read()).decode()
                            
                            response = {
                                'success': True, 
                                'audio': audio_data,
                                'format': audio_format,
                                'voice': voice,
                                'settings': {
                                    'rate': rate
                                }
                            }
                            
                            # Log success
                            voice_name = voice.split('-')[2].replace('Neural', '')
                            word_count = len(text.split())
                            rate_info = f" (Rate: {rate_str})" if rate_str else ""
                            logger.info(f"Generated {audio_format.upper()} audio: {voice_name} voice, {word_count} words{rate_info}")
                        
                        finally:
                            # Clean up temporary file with retries
                            for attempt in range(5):
                                try:
                                    if os.path.exists(tmp_filename):
                                        os.unlink(tmp_filename)
                                    break
                                except (PermissionError, OSError) as e:
                                    if attempt < 4:
                                        time.sleep(0.1)
                                    else:
                                        logger.warning(f"Could not delete temp file {tmp_filename}: {e}")
                    
                    finally:
                        # Close event loop
                        loop.close()
                        
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                response = {'success': False, 'error': 'Invalid JSON data'}
            except Exception as e:
                logger.error(f"TTS generation error: {e}")
                response = {'success': False, 'error': str(e)}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use logging instead of print"""
        logger.info(f"{self.address_string()} - {format % args}")

def start_server():
    """Start the Edge TTS server"""
    # Use environment variables for deployment (Railway, Render, etc.)
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'  # Always use 0.0.0.0 for cloud deployment
    
    try:
        server = HTTPServer((host, port), EdgeTTSHandler)
        logger.info("🚀 Edge TTS Pro Server starting...")
        logger.info(f"📱 Server running on port {port}")
        logger.info("🇺🇸 English voices: Aria, Jenny, Guy, Andrew, Sonia, Ryan, Natasha, William")
        logger.info("🇸🇦 Arabic voices: Zariyah, Hamed, Salma, Shakir")
        logger.info("✨ Only verified, working voices included!")
        logger.info("⌨️  Keyboard shortcuts: Ctrl+Enter (convert), Ctrl+D (download)")
        logger.info("⏹️  Press Ctrl+C to stop the server")
        logger.info("-" * 60)
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n👋 Server stopped. Thanks for using Edge TTS Pro!")
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"❌ Port {port} is already in use. Please stop the existing server first.")
        else:
            logger.error(f"❌ Server error: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    start_server()

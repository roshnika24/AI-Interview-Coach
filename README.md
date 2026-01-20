# AI Interview Coach - Local Development

An AI-powered interview coach that conducts mock interviews and provides feedback.

## Prerequisites
- **Python 3.10+** (for Backend)
- **Node.js 18+** (for Frontend)
- **OpenRouter API Key** (Get one at [openrouter.ai](https://openrouter.ai/keys))

## 1. Setup Backend
1. Open a terminal in the `Backend` folder.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate  # Mac/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Secrets**:
   - Create a file named `.env` in the `Backend` folder.
   - Add your key: `OPENROUTER_API_KEY=sk-or-your-key-here`
5. **Run the Server**:
   ```bash
   uvicorn main:app --reload
   ```
   *Server will start at http://localhost:8000*

## 2. Setup Frontend
1. Open a new terminal in the `frontend` folder.
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Run the App**:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Troubleshooting
- If you see "API Key Missing", check your `Backend/.env` file.
- If frontend can't connect, ensure backend is running on port 8000.

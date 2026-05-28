# 🚀 Pypilot
Lightweight AI orchestration system with strict client–server separation.
Pypilot is designed to keep the client small and controlled, while delegating heavy reasoning and code generation to a VPS backend.

## ✅ Built So Far
- Modular model abstraction layer
- Context builder + routing system
- CLI-based interaction
- VPS-based reasoning support
- Fast online reasoning integration
- Routing optimizations
- Multi-agent experimentation

## 🔜 Coming Next
- Add instructions to make easier for the user
- Performance improvements

## 🔮 Future Ideas
- Add functionality to make changes to the code directly

## 💻 Running Locally
### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/pypilot.git
cd pypilot
```
### 2️⃣ Create a Virtual Environment (Recommended)
macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```
Windows
```
python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```
pip install -r requirements_dev.txt
```
First installation may take time because torch is large.

### 4️⃣ Configure the VPS API
Create a private `.env` file from the example file:
```
copy .env.example .env
```

Set these values in `.env`:
```
PYSITANT_VPS_API_URL=https://your-domain.com/api/ask
PYSITANT_VPS_SESSION_URL=https://your-domain.com/api/session
PYSITANT_API_KEY=your-private-api-key
```

The API key is used only to create a short-lived server session token. Do not publish a real API key inside this package.

### 5️⃣ Run the CLI
```
cd src
python -m pypilot.cli
```
## 🧠 First Usage

Inside the CLI:
```
consent <path-to-project>
```
If no path is provided then it will take the path in which the file contains
```
build_once
ask explain the project structure
```
## ⚠ Notes
- This is still in early development
- The local model (Qwen2.5-Coder-1.5B-Instruct) will download on first use.
- Internet is required only for the initial model download.
- After that, the model runs fully offline.

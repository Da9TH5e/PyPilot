# 🚀 Pypilot
Lightweight AI orchestration system with strict client–server separation.
Pypilot is designed to keep the client small and controlled, while delegating heavy reasoning and code generation to a VPS backend.

## ✅ Built So Far
- Modular model abstraction layer
- Context builder + routing system
- CLI-based interaction
- Optional local model support (manual, limited)
- Offline non-ML fallback mode

## 🔜 Coming Next
- VPS-based reasoning support
- Fast online reasoning integration
- Deep reasoning / code generation via backend
- Structured logging system
- Routing optimizations
- Performance improvements
- Multi-agent experimentation
- Smarter task delegation

## 💻 Running Locally
### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/pypilot.git
cd pypilot
```
### 2️⃣ Create a Virtual Environment (Recommended)

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Windows
```
python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
First installation may take time because torch is large.

### 4️⃣ Run the CLI
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
- The local model (Qwen2.5-Coder-0.5B-Instruct) will download on first use.
- Internet is required only for the initial model download.
- After that, the model runs fully offline.





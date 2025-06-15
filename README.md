# SAIIUT

📚 **Integrated School System – Desktop App with API**  
This is an integrative project developed by 3rd-term software engineering students.

---

## 🖥️ SAIIUT - Electron App

**A desktop application built with **Electron**, using **Node.js** and **MySQL**, designed to manage school-related operations.**

---

## 🚀 Setup with Docker (Manual)  
1. **Clone the repository**

```bash
git clone https://github.com/EdgarLF27/SAIIUT.git
cd SAIIUT/app
```
---
2. **Download Docker**

**Is necesarry to have Docker because the app use MySQL to store data.**
[Download Docker](https://www.docker.com/get-started/)

---
3. **Open Docker and run the following command**

4. **Go to the project folder**
---

5. **Run the following commands**
```bash
docker-compose up --build
npm install
```
**This will:**

**Build the Electron app from the Dockerfile**

**Start all services defined in docker-compose.yml (including the app and MySQL database)**

--- 
6. # 🧱 Tech Stack
**Electron**

**Node.js**

**MySQL**

**Docker / Docker Compose**

7. # Notes
- node_modules is excluded from the repository
- If you see errors during development, try running npm install again.
- Use .env for your environment variables if needed but exclude it from repository


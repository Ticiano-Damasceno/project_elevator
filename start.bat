@echo off
chcp 65001 > nul
cd "C:\Users\tadamasceno\OneDrive - Stefanini\Área de Trabalho\project_elevator\backend-elevator"
.\venv\Scripts\activate
uvicorn app.main:app --reload
pause
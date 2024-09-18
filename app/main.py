from fastapi import FastAPI
from dotenv import load_dotenv
from controller.controller  import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

# Configurar los orígenes permitidos
origins = [
    "http://localhost:3000",  # Añade la URL de tu frontend (Nuxt)
    "http://127.0.0.1:3000",  # También considera el localhost con puerto específico
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir los orígenes especificados
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)
app.include_router(router)

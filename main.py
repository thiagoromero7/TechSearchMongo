from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import RedirectResponse

app = FastAPI()

# Configurações de pastas
templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Conexão com MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin_uninassau@techsearch.zppabuk.mongodb.net/techsearch_db?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
db = client["techsearch_db"]

# --- ROTAS DE PÁGINAS (GET) ---

@app.get("/")
async def home(request: Request):
    # Consulta ao banco
    produtos = await db.techs.find({}).to_list(length=100)
    return templates.TemplateResponse(request=request, name="home.html", context={"produtos": produtos})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # 1. Procura o usuário no MongoDB
    user = await db.users.find_one({"username": username, "password": password})
    
    if user:
        # Se encontrou, redireciona para a home
        return RedirectResponse(url="/", status_code=303)
    else:
        # Se a senha ou usuário estiverem incorretos, redireciona de volta para o login
        # (Em produção, você poderia passar um parâmetro de erro aqui)
        return RedirectResponse(url="/login", status_code=303)

@app.get("/cadastro.html")
async def cadastro_page(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html", context={})

@app.get("/carrinho.html")
async def carrinho_page(request: Request):
    items = await db.carrinho.find({}).to_list(length=100)
    subtotal = sum(item.get('preco', 0) for item in items)
    return templates.TemplateResponse(request=request, name="carrinho.html", context={"cart_items": items, "subtotal": subtotal})

@app.get("/favoritos.html")
async def favoritos_page(request: Request):
    favoritos = await db.favoritos.find({}).to_list(length=100)
    return templates.TemplateResponse(request=request, name="favoritos.html", context={"produtos_favoritos": favoritos})

# --- ROTAS DE AÇÃO (POST - REDIRECIONAMENTOS) ---

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Adicione aqui sua lógica de verificação
    return RedirectResponse(url="/", status_code=303)

@app.post("/cadastro")
async def processar_cadastro(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    await db.users.insert_one({"username": username, "email": email, "password": password})
    return RedirectResponse(url="/login", status_code=303)

@app.post("/cadastro-produto")
async def salvar_produto(nome: str = Form(...), preco: float = Form(...), categoria: str = Form(...), 
                         quantidade: int = Form(...), descricao: str = Form(...), imagem: str = Form(...)):
    await db.techs.insert_one({
        "nome": nome, "preco": preco, "categoria": categoria, 
        "quantidade": quantidade, "descricao": descricao, "imagem": imagem
    })
    return RedirectResponse(url="/", status_code=303)

@app.post("/salvar-endereco")
async def salvar_endereco(cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), 
                          bairro: str = Form(...), cidade: str = Form(...)):
    await db.enderecos.insert_one({
        "cep": cep, "rua": rua, "numero": numero, "bairro": bairro, "cidade": cidade
    })
    return RedirectResponse(url="/carrinho.html", status_code=303)

@app.post("/favoritos/adicionar")
async def adicionar_favorito(produto_id: str = Form(...)):
    await db.favoritos.insert_one({"produto_id": produto_id})
    return RedirectResponse(url="/favoritos.html", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
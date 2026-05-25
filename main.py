import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from bson.objectid import ObjectId

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="uma_chave_muito_secreta_e_segura")

# Configurações de pastas
templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["techsearch_db"]


@app.get("/")
async def home(request: Request):
    # Consulta ao banco
    produtos = await db.techs.find({}).to_list(length=100)
    
    user_session = request.session.get("username")
    user_context = {"username": user_session} if user_session else None
    
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={"produtos": produtos, "user": user_context}
    )


    
@app.get("/login.html")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/cadastro.html")
async def cadastro_page(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html", context={})

@app.get("/carrinho.html")
async def carrinho_page(request: Request):
    user_session = request.session.get("username")
    user_context = {"username": user_session} if user_session else None
    
    items = await db.carrinho.find({}).to_list(length=100)

    subtotal = sum(item.get('preco', 0) * item.get('quantidade', 1) for item in items)
    
    return templates.TemplateResponse(
        request=request, 
        name="carrinho.html", 
        context={
            "user": user_context,
            "cart_items": items, 
            "subtotal": f"{subtotal:.2f}".replace('.', ','),
            "total_price": f"{subtotal:.2f}".replace('.', ',')
        }
    )

@app.get("/favoritos.html")
async def favoritos_page(request: Request):
    # Pega o usuário da sessão para o topo da tela
    user_session = request.session.get("username")
    user_context = {"username": user_session} if user_session else None
    
    # Busca a lista de favoritos no MongoDB
    favoritos = await db.favoritos.find({}).to_list(length=100)
    
    return templates.TemplateResponse(
        request=request, 
        name="favoritos.html", 
        context={"user": user_context, "produtos_favoritos": favoritos}
    )

@app.get("/favoritos/adicionar/{produto_id}")
async def adicionar_favorito(request: Request, produto_id: str):
    # 1. Busca o produto completo na coleção de tecnologias
    produto = await db.techs.find_one({"_id": ObjectId(produto_id)})
    
    if produto:
        # 2. Verifica se o produto já está nos favoritos para evitar duplicação
        ja_existe = await db.favoritos.find_one({"produto_id": str(produto["_id"])})
        
        if not ja_existe:
            # 3. Salva os dados visuais do produto na coleção de favoritos
            await db.favoritos.insert_one({
                "produto_id": str(produto["_id"]), # ID original para mandar pro carrinho depois
                "nome": produto["nome"],
                "preco": f"{produto['preco']:.2f}".replace('.', ','),
                "imagem": produto.get("imagem", "")
            })
            
    # Redireciona para a tela de favoritos
    return RedirectResponse(url="/favoritos.html", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear() # Apaga o crachá de identificação
    return RedirectResponse(url="/", status_code=303)

@app.get("/dashboard_admin.html")
async def dashboard_admin_page(request: Request):
    user_session = request.session.get("username")
    
    if not user_session or user_session != "admin":
        return RedirectResponse(url="/", status_code=303)
    
    # 1. Busca a lista de produtos para a tabela
    produtos = await db.techs.find({}).to_list(length=100)
    
    # 2. Calcula o Total de Produtos Cadastrados
    total_produtos = await db.techs.count_documents({})
    
    # 3. Calcula as Encomendas Pendentes (Itens atualmente no carrinho)
    encomendas_pendentes = await db.carrinho.count_documents({})
    
    # 4. Calcula as Vendas Totais
    # O MongoDB vai procurar todos os documentos na coleção 'vendas', 
    # pegar o campo 'valor_total' de cada um e somar tudo.
    pipeline_vendas = [
        {"$group": {"_id": None, "total": {"$sum": "$valor_total"}}}
    ]
    resultado_vendas = await db.vendas.aggregate(pipeline_vendas).to_list(length=1)
    
    # Se já houver vendas, pega o total. Se não, começa em 0.0.
    vendas_totais = resultado_vendas[0]["total"] if resultado_vendas else 0.0
    
    # 5. Visualizações (Deixaremos estático por enquanto)
    visualizacoes = 142 

    return templates.TemplateResponse(
        request=request, 
        name="dashboard_admin.html", 
        context={
            "user": {"username": user_session}, 
            "produtos": produtos,
            "total_produtos": total_produtos,
            "encomendas_pendentes": encomendas_pendentes,
            "vendas_totais": vendas_totais,
            "visualizacoes": visualizacoes
        }
    )

@app.get("/cadastro_produto.html")
async def cadastro_produto_page(request: Request):
    # Opcional: Proteger essa rota para que apenas o admin consiga acessar
    user_session = request.session.get("username")
    if not user_session or user_session != "admin":
        return RedirectResponse(url="/", status_code=303)
        
    return templates.TemplateResponse(request=request, name="cadastro_produto.html", context={})

@app.get("/carrinho/adicionar/{produto_id}")
async def adicionar_ao_carrinho(request: Request, produto_id: str):
    # 1. Busca o produto original no banco de dados usando o ID
    produto = await db.techs.find_one({"_id": ObjectId(produto_id)})
    
    if produto:
        await db.carrinho.insert_one({
            "produto_id": str(produto["_id"]),
            "product": {"nome": produto["nome"]}, 
            "price": produto["preco"],            
            "preco": produto["preco"]            
        })
        
    return RedirectResponse(url="/carrinho.html", status_code=303)

@app.get("/endereco.html")
async def endereco_page(request: Request):
    user_session = request.session.get("username")
    
    username_display = user_session if user_session else "Visitante"
    
    return templates.TemplateResponse(
        request=request, 
        name="endereco.html", 
        context={"username": username_display}
    )

@app.get("/pagamento.html")
async def pagamento_page(request: Request):
    # Puxa os itens salvos no carrinho para montar o resumo da compra
    items = await db.carrinho.find({}).to_list(length=100)
    
    # Calcula o valor total multiplicando o preço unitário pela quantidade de cada item
    subtotal = sum(item.get('preco', 0) * item.get('quantidade', 1) for item in items)
    total_formatado = f"{subtotal:.2f}".replace('.', ',')
    
    # Formata a lista com os campos exatos que o seu arquivo pagamento.html precisa ler
    cart_items_formatados = []
    for item in items:
        qtd = item.get("quantidade", 1)
        valor = item.get("preco", 0)
        nome_produto = item.get("product", {}).get("nome", "Produto")
        
        cart_items_formatados.append({
            "product": {"nome": nome_produto},
            "quantity": qtd,
            "subtotal": f"{valor * qtd:.2f}".replace('.', ',')
        })

    return templates.TemplateResponse(
        request=request, 
        name="pagamento.html", 
        context={
            "cart_items": cart_items_formatados,
            "total_price": total_formatado
        }
    )

# --- ROTAS DE AÇÃO (POST - REDIRECIONAMENTOS) ---

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await db.users.find_one({"username": username, "password": password})
    
    if user:
        request.session["username"] = user["username"]
        return RedirectResponse(url="/", status_code=303)
    else:
        return RedirectResponse(url="/login.html", status_code=303)

@app.post("/cadastro")
async def processar_cadastro(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    await db.users.insert_one({"username": username, "email": email, "password": password})
    return RedirectResponse(url="/login.html", status_code=303)

@app.post("/cadastro-produto")
async def salvar_produto(nome: str = Form(...), preco: float = Form(...), categoria: str = Form(...), 
                         quantidade: int = Form(...), descricao: str = Form(...), imagem: str = Form(...)):
    await db.techs.insert_one({
        "nome": nome, "preco": preco, "categoria": categoria, 
        "quantidade": quantidade, "descricao": descricao, "imagem": imagem
    })
    return RedirectResponse(url="/", status_code=303)

@app.post("/deletar_produto/{produto_id}")
async def deletar_produto(request: Request, produto_id: str):
    # Proteção extra: só o admin pode deletar
    user_session = request.session.get("username")
    if not user_session or user_session != "admin":
        return RedirectResponse(url="/", status_code=303)
    
    # Tenta deletar o produto usando o ObjectId
    try:
        await db.techs.delete_one({"_id": ObjectId(produto_id)})
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        
    # Recarrega a página do painel
    return RedirectResponse(url="/dashboard_admin.html", status_code=303)

@app.post("/carrinho/remover/{item_id}")
async def remover_do_carrinho(request: Request, item_id: str):
    # Deleta do MongoDB usando o ObjectId único
    await db.carrinho.delete_one({"_id": ObjectId(item_id)})
    return RedirectResponse(url="/carrinho.html", status_code=303)

@app.post("/carrinho/atualizar/{item_id}")
async def atualizar_carrinho(request: Request, item_id: str, acao: str = Form(...)):
    # Busca o item no carrinho
    item = await db.carrinho.find_one({"_id": ObjectId(item_id)})
    
    if item:
        qtd_atual = item.get("quantidade", 1)
        
        if acao == "aumentar":
            nova_qtd = qtd_atual + 1
        elif acao == "diminuir" and qtd_atual > 1: 
            nova_qtd = qtd_atual - 1
        else:
            nova_qtd = qtd_atual
            
        await db.carrinho.update_one(
            {"_id": ObjectId(item_id)}, 
            {"$set": {"quantidade": nova_qtd}}
        )
        
    return RedirectResponse(url="/carrinho.html", status_code=303)

@app.post("/salvar-endereco")
async def salvar_endereco(cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), 
                          bairro: str = Form(...), cidade: str = Form(...), complemento: str = Form(None), estado: str = Form(...)):
    
    # Salva o endereço no banco de dados
    await db.enderecos.insert_one({
        "cep": cep, "rua": rua, "numero": numero, "bairro": bairro, 
        "cidade": cidade, "estado": estado, "complemento": complemento
    })
    
    # Redireciona para o pagamento!
    return RedirectResponse(url="/pagamento.html", status_code=303)

@app.post("/processar-pagamento")
async def processar_pagamento(request: Request, pagamento: str = Form(...)):
    # 1. Busca os itens que estão no carrinho para saber o valor cobrado
    items = await db.carrinho.find({}).to_list(length=100)
    
    # Se tiver algo no carrinho, processa a venda
    if items:
        # Calcula o total da compra
        total_venda = sum(item.get('preco', 0) * item.get('quantidade', 1) for item in items)
        
        # 2. Salva a venda no banco de dados! (Isso alimenta o seu Dashboard Admin)
        await db.vendas.insert_one({
            "valor_total": total_venda,
            "metodo_pagamento": pagamento,
            "status": "Aprovado"
        })
        
        # 3. Esvazia o carrinho, pois a compra foi finalizada
        await db.carrinho.delete_many({})
        
    # 4. Finalmente, redireciona o usuário de volta para a tela inicial
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

@app.post("/favoritos/remover/{item_id}")
async def remover_dos_favoritos(request: Request, item_id: str):
    # Remove o item da coleção de favoritos do MongoDB usando o ObjectId único
    await db.favoritos.delete_one({"_id": ObjectId(item_id)})
    
    # Redireciona de volta para a página de favoritos atualizada
    return RedirectResponse(url="/favoritos.html", status_code=303)
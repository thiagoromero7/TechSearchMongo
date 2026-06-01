import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Carrega a mesma URI que já usa no projeto principal
load_dotenv()

async def popular_base_de_dados():
    MONGO_URI = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["techsearch_db"]

    # Lista de produtos prontos a inserir
    produtos_iniciais = [
        {
            "nome": "Monitor Ultrawide LG 29\"",
            "preco": 1250.00,
            "categoria": "Monitor",
            "quantidade": 15,
            "descricao": "Monitor IPS com proporção 21:9, HDR10 e FreeSync, ideal para programação e gaming.",
            "imagem": "https://m.media-amazon.com/images/I/71120h42D4L._AC_SL1500_.jpg"
        },
        {
            "nome": "Teclado Mecânico HyperX Alloy Origins",
            "preco": 549.90,
            "categoria": "Teclado",
            "quantidade": 30,
            "descricao": "Teclado mecânico compacto com switches vermelhos e iluminação RGB personalizável.",
            "imagem": "https://m.media-amazon.com/images/I/71rBq9X3vHL._AC_SL1500_.jpg"
        },
        {
            "nome": "Mouse Sem Fio Logitech G305",
            "preco": 230.50,
            "categoria": "Mouse",
            "quantidade": 50,
            "descricao": "Mouse gaming sem fio com sensor HERO 12K e até 250 horas de autonomia.",
            "imagem": "https://m.media-amazon.com/images/I/51A2kP0tH8L._AC_SL1500_.jpg"
        },
        {
            "nome": "Notebook Dell Inspiron 15",
            "preco": 3800.00,
            "categoria": "Notebook",
            "quantidade": 12,
            "descricao": "Portátil com processador Intel Core i5 de 12ª geração, 8GB de RAM e 256GB SSD NVMe.",
            "imagem": "https://m.media-amazon.com/images/I/61pBvlYFAsL._AC_SL1500_.jpg"
        },
        {
            "nome": "Smartphone Samsung Galaxy S23",
            "preco": 4200.00,
            "categoria": "Celular",
            "quantidade": 25,
            "descricao": "Telemóvel 5G com 256GB de armazenamento, ecrã AMOLED de 120Hz e câmara de 50MP.",
            "imagem": "https://m.media-amazon.com/images/I/71DdwNshg4L._AC_SL1500_.jpg"
        },
        {
            "nome": "Monitor Gamer AOC Hero 24\" 144Hz",
            "preco": 999.00,
            "categoria": "Monitor",
            "quantidade": 20,
            "descricao": "Monitor de 24 polegadas com taxa de atualização de 144Hz e 1ms de tempo de resposta.",
            "imagem": "https://m.media-amazon.com/images/I/612QyL2XU6L._AC_SL1000_.jpg"
        }
    ]

    print("A ligar à base de dados MongoDB Atlas...")
    
    # Opcional: Descomente a linha abaixo se quiser apagar os produtos antigos antes de inserir os novos
    # await db.techs.delete_many({})
    
    # Insere todos os produtos de uma vez usando insert_many()
    resultado = await db.techs.insert_many(produtos_iniciais)
    
    print(f"Sucesso! {len(resultado.inserted_ids)} novos produtos foram adicionados à sua loja.")

if __name__ == "__main__":
    asyncio.run(popular_base_de_dados())
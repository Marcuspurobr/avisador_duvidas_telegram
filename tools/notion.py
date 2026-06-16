from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

async def checar_duvidas(bot):
    resultado = notion.databases.query(
    **{
        "database_id": os.getenv("NOTION_DATABASE_ID"),
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "status": {"equals": "Travado / Com Dúvida"}
                },
                {
                    "property": "Alerta Enviado",
                    "checkbox": {"equals": False}
                }
            ]
        }
    }
    )
    
    tasks = resultado.get("results", [])
    
    for task in tasks:
        titulo = task["properties"]["Nome"]["title"][0]["text"]["content"]
        pessoas = task["properties"]["Responsável"]["people"]
        if pessoas:
            nome_responsavel = pessoas[0]["name"]
        else:
            nome_responsavel = "Sem responsável"
        await bot.send_message(chat_id=os.getenv("CHAT_ID"), text=f"O(a) coordenador(a) {nome_responsavel} está com dúvida na demada: {titulo}, da um helpzinho lá :)")
        notion.pages.update(
            page_id=task["id"],
            properties={
                "Alerta Enviado": {
                    "checkbox": True
                }
            }
        )

async def checar_duvidas_tiradas(bot):
    resultado = notion.databases.query(
    **{
        "database_id": os.getenv("NOTION_DATABASE_ID"),
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Travado / Com Dúvida"}
                },
                {
                    "property": "Alerta Enviado",
                    "checkbox": {"equals": True}
                }
            ]
        }
    }
    )   

    tasks = resultado.get("results", [])
    for task in tasks:
        notion.pages.update(
                page_id=task["id"],
                properties={
                    "Alerta Enviado": {
                        "checkbox": False
                    }
                }
            )

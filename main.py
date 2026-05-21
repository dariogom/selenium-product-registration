import pandas as pd
import config
from automation import BotEstoque

#função carregar produtos
def carregar_produtos(caminho: str) -> list[dict]:
    df = pd.read_csv(caminho)
    return df.to_dict(orient="records")

#função principal do programa
def main():
    produtos = carregar_produtos(config.CSV_PATH)
    #mostra quatidade de produtos
    print(f"📦 {len(produtos)} produtos encontrados.")
#criação do objeto da classe botestoque
    bot = BotEstoque()
#tenta executar o codigo
    try:
        bot.fazer_login_sistema()
#contadores
        sucesso, falha = 0, 0
#loop principal
        for produto in produtos:
            if bot.cadastrar_produto(produto):
                sucesso += 1
            else:
                falha += 1

        print(f"\nConcluído: {sucesso} cadastrados |  Falhas: {falha}")
#O finnaly SEMPRE executa 
    finally:
        bot.fechar()


if __name__ == "__main__":
    main()
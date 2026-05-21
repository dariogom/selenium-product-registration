import logging
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log")
    ]
)


class BotEstoque:

    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait   = WebDriverWait(self.driver, timeout=10)

    def _preencher_campo(self, locator: tuple, valor: str) -> None:
        campo = self.wait.until(EC.presence_of_element_located(locator))
        campo.clear()
            #digita letra por letra com pausa entre acada uma
        for letra in str(valor):   
            campo.send_keys(letra)
            time.sleep(0.1)
            time.sleep(config.PAUSA_ENTRE_CAMPOS)

    def _clicar(self, locator: tuple) -> None:
        elemento = self.wait.until(EC.element_to_be_clickable(locator))
        elemento.click()

  
    #login do techstock
    def fazer_login_sistema(self) -> None:
       
        logging.info("Abrindo TechStock...")
        self.driver.get(config.SISTEMA_URL)

        # Preenche o formulário de login
        self._preencher_campo((By.ID, "email"), config.EMAIL_SISTEMA)
        self._preencher_campo((By.ID, "senha"), config.SENHA_SISTEMA)

        # Clica no botão "Entrar no sistema" (type="submit" dentro do form-login)
        self._clicar((By.CSS_SELECTOR, "#form-login button[type='submit']"))

        # Espera o formulário de produto ficar visível antes de continuar.
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-produto")))
        logging.info("Login no TechStock realizado.")

   
    # CADASTRAR PRODUTO
    def cadastrar_produto(self, produto: dict) -> bool:
        """
        Preenche o formulário usando os IDs do seu index.html:
        id="codigo", id="marca", id="tipo", id="categoria",
        id="preco_unitario", id="custo", id="obs"
        """
        try:
            logging.info(f"Cadastrando: {produto.get('codigo')} — {produto.get('marca')}")

            # Campos obrigatórios — IDs
            self._preencher_campo((By.ID, "codigo"),         produto["codigo"])
            self._preencher_campo((By.ID, "marca"),          produto["marca"])
            self._preencher_campo((By.ID, "tipo"),           produto["tipo"])
            self._preencher_campo((By.ID, "categoria"),      produto["categoria"])
            self._preencher_campo((By.ID, "preco_unitario"), produto["preco_unitario"])
            self._preencher_campo((By.ID, "custo"),          produto["custo"])

            # OBS é opcional — o HTML não tem required nesse campo
            obs = produto.get("obs", "")
            if pd.notna(obs) and str(obs).strip():
                self._preencher_campo((By.ID, "obs"), obs)

            # Clica em "Cadastrar Produto"
            self._clicar((By.CSS_SELECTOR, "#form-produto button[type='submit']"))

            # Após o cadastro o JS chama e.target.reset() e foca no campo codigo.
            # Espera o campo codigo ficar vazio (reset) antes de ir pro próximo.
            self.wait.until(
                lambda d: d.find_element(By.ID, "codigo").get_attribute("value") == ""
            )

            return True

        except Exception as erro:
            logging.error(f"Erro ao cadastrar {produto.get('codigo')}: {erro}")
            return False

    def fechar(self) -> None:
        self.driver.quit()
        logging.info("Navegador fechado.")
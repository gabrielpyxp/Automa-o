import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def fill_date_safely(driver, field_id, date):
    try:
        driver.execute_script(f"document.getElementById('{field_id}').value = '{date}';")
        time.sleep(0.5)
        element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, field_id)))
        element.clear()
        for char in date:
            element.send_keys(char)
            time.sleep(0.05)
        driver.execute_script(f"""
            var el = document.getElementById('{field_id}');
            el.dispatchEvent(new Event('change'));
            el.dispatchEvent(new Event('blur'));
        """)
        return True
    except Exception as e:
        print(f"Erro ao preencher {field_id}: {e}")
        return False

def wait_for_download_complete(download_folder, timeout=30, check_interval=1):
    print("⏳ Aguardando conclusão do download...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not any(f.endswith('.crdownload') for f in os.listdir(download_folder)):
            if any(f.lower().endswith('.xlsx') for f in os.listdir(download_folder)):
                return True
        time.sleep(check_interval)
    return False

def main():
    # ─── Lê datas de config.txt ─────────────────────────────────────────
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            lines = [l.strip() for l in f.read().splitlines() if l.strip()]
        if len(lines) >= 2:
            dataDe, dataAte = lines[0], lines[1]
        else:
            print("⚠️ config.txt sem datas válidas; usando padrão")
            dataDe = dataAte = "26/06/2025"
    else:
        print("⚠️ config.txt não encontrado; usando padrão")
        dataDe = dataAte = "26/06/2025"

    DOWNLOAD_FOLDER = os.path.abspath("downloads")
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # ─── Configurações do Chrome ────────────────────────────────────────
    options = Options()
    options.add_argument("--start-maximized")
    prefs = {
        "download.default_directory": DOWNLOAD_FOLDER,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True
    }
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # ─── Login ─────────────────────────────────────────────────────────
        driver.get("https://gestao.onitel.com.br/app/login")
        wait.until(EC.presence_of_element_located((By.ID, 'email')))\
            .send_keys("" + Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.ID, 'password')))\
            .send_keys("" + Keys.RETURN)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "vg-button#btn-enter-login"))).click()
        try:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Lembrar-me em 10 dias")]')
            )).click()
        except TimeoutException:
            pass
        wait.until(EC.url_contains("/adm.php"))

        # ─── Navegação até Ordens de Serviço ───────────────────────────────
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submenu_title"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Suporte']"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@rel, \"cria_grid('#1_grid','su_oss_chamado'\")]")
        )).click()
        time.sleep(1)

        # ─── Filtrar assunto ───────────────────────────────────────────────
        campo_busca = wait.until(EC.presence_of_element_located((By.ID, 'assunto')))
        campo_busca.clear()
        campo_busca.send_keys("instalação" + Keys.RETURN)
        time.sleep(1)

        # ─── Preencher datas ───────────────────────────────────────────────
        if not fill_date_safely(driver, 'dataDe', dataDe):
            raise Exception("Falha ao preencher data inicial")
        if not fill_date_safely(driver, 'dataAte', dataAte):
            raise Exception("Falha ao preencher data final")

        # ─── Aplicar filtro ────────────────────────────────────────────────
        campo_int = wait.until(EC.presence_of_element_located((By.ID, 'su_oss_chamado_apply_filter')))
        campo_int.send_keys("Aplicar" + Keys.RETURN)
        time.sleep(1)

        # ─── Limpar pasta de download ──────────────────────────────────────
        for f in os.listdir(DOWNLOAD_FOLDER):
            if f.lower().endswith(('.xlsx', '.crdownload')):
                os.remove(os.path.join(DOWNLOAD_FOLDER, f))

        # ─── Solicitar download ────────────────────────────────────────────
        btn_menu = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".downloadQueryTriggerIcon .fa-download")
        ))
        driver.execute_script("arguments[0].click()", btn_menu)
        time.sleep(1)
        opcao_xls = wait.until(EC.element_to_be_clickable((
            By.XPATH, 
            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'baixar consulta em xls')]"
        )))
        opcao_xls.click()

        # ─── Aguardar download e renomear ──────────────────────────────────
        if wait_for_download_complete(DOWNLOAD_FOLDER, timeout=20):
            xlsx_files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.lower().endswith('.xlsx')]
            latest = max(
                (os.path.join(DOWNLOAD_FOLDER, f) for f in xlsx_files),
                key=os.path.getctime
            )
            target = os.path.join(DOWNLOAD_FOLDER, "resultado.xlsx")
            shutil.move(latest, target)
            print(f"✅ Arquivo salvo em: {target}")
        else:
            print("❌ Download não finalizado a tempo")

    except Exception as e:
        print(f"❌ Erro geral: {e}")
        driver.save_screenshot("erro_zap.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

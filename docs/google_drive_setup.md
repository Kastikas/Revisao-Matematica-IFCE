# Guia de Configuração e Uso: Google Drive API (Service Account)

Este guia orienta a configuração completa da integração entre a plataforma **PartiuIF** e o **Google Drive** utilizando **Service Account** (sem necessidade de login interativo no navegador).

---

## 1. Visão Geral da Arquitetura

```text
[Imagem Local: assets/img/questoes/<if>/] 
          ↓ (manage_mathdata.py drive-upload / drive-sync)
[Google Drive API v3 (Service Account)]
          ↓ (Upload multipart)
[Pasta Compartilhada no seu Google Drive (PartiuIF_Imagens)]
          ↓ (Criação de subpasta por IF e permissão pública de leitura)
[Link Compartilhável: https://drive.google.com/file/d/<ID>/view?usp=sharing]
          ↓ (Opcional: --update-mathdata)
[mathData.json atualizado e compilado no site]
```

---

## 2. Passo a Passo no Google Cloud Console

### Passo 1: Criar ou Selecionar um Projeto no Google Cloud
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. No menu superior, selecione o menu de projetos e clique em **New Project** (Novo Projeto).
3. Dê um nome (ex: `partiuif-drive`) e clique em **Create** (Criar).

### Passo 2: Ativar a Google Drive API
1. No menu lateral esquerdo (ou na barra de busca superior), acesse **APIs & Services** > **Enabled APIs & Services**.
2. Clique no botão **+ ENABLE APIS AND SERVICES** no topo.
3. Pesquise por **Google Drive API**.
4. Clique na API e em seguida no botão azul **Enable** (Ativar).

### Passo 3: Criar uma Conta de Serviço (Service Account)
1. No menu lateral, acesse **IAM & Admin** > **Service Accounts** (Contas de Serviço).
2. Clique em **+ CREATE SERVICE ACCOUNT** no topo.
3. Preencha os detalhes:
   - **Service account name**: `partiuif-image-uploader`
   - **Service account ID**: gerado automaticamente
   - **Service account description**: `Upload automatizado de imagens de questões do PartiuIF`
4. Clique em **Create and Continue**.
5. Na etapa de permissões do projeto (*Grant this service account access to project*), você pode deixar sem papel ou selecionar `Viewer` e clicar em **Continue** e **Done**.
6. **Copie o e-mail da Service Account** gerado (ex.: `partiuif-image-uploader@seu-projeto.iam.gserviceaccount.com`). Você precisará dele no Passo 5!

### Passo 4: Gerar e Baixar a Chave Privada (JSON)
1. Na lista de Contas de Serviço, clique na conta que você acabou de criar.
2. Acesse a aba **Keys** (Chaves).
3. Clique em **Add Key** > **Create new key**.
4. Escolha o formato **JSON** e clique em **Create**.
5. O download do arquivo JSON será iniciado no seu computador.
6. Mova este arquivo para a raiz do projeto com o nome:
   ```text
   service_account.json
   ```
   *(Nota: O arquivo `.gitignore` já está configurado para garantir que esta chave nunca seja comitada no Git).*

### Passo 5: Criar e Compartilhar a Pasta no seu Google Drive Pessoal
> [!IMPORTANT]
> A Service Account possui um espaço próprio isolado. Para que as imagens fiquem salvas na sua conta pessoal do Google Drive:
1. Abra o seu [Google Drive](https://drive.google.com/).
2. Crie uma pasta dedicada para o projeto (ex.: `PartiuIF_Imagens`).
3. Clique com o botão direito na pasta e selecione **Compartilhar** > **Compartilhar**.
4. Cole o **e-mail da Service Account** (copiado no Passo 3.6).
5. Certifique-se de que a função selecionada seja **Editor** (para permitir envio e criação de subpastas).
6. Desmarque a opção "Notificar pessoas" (pois é um robô de serviço) e clique em **Compartilhar**.

### Passo 6: Obter o ID da Pasta e Configurar o `.env`
1. Abra a pasta recém-criada no Google Drive.
2. Observe a URL no navegador:
   `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0jKlMnOpQrStUvWx`
3. O código alfanumérico após `folders/` é o seu **FOLDER_ID**.
4. Crie ou edite o arquivo `.env` na raiz do projeto (baseando-se no `.env.example`):
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
   GOOGLE_DRIVE_FOLDER_ID="seu_folder_id_aqui"
   ```

---

## 3. Comandos e Exemplos de Uso

### 1. Testar Conexão e Permissões
Verifica se as credenciais são válidas e se a Service Account consegue gravar na pasta:
```bash
python3 scripts/manage_mathdata.py drive-test
```
*Saída esperada:*
```text
🔌 Testando autenticação com a Google Drive API...
✅ Credenciais carregadas com sucesso de: /.../service_account.json
👤 Service Account: partiuif-image-uploader@...iam.gserviceaccount.com
🌐 Conexão com Google Drive API estabelecida
📁 Verificando acesso à pasta remota (ID: ...)...
🎉 Acesso concedido com permissão de escrita!
   • Nome da pasta: PartiuIF_Imagens
```

---

### 2. Upload de Imagem Avulsa
Envia uma imagem local diretamente para o Drive (alocando na subpasta do IF):
```bash
python3 scripts/manage_mathdata.py drive-upload -f assets/img/questoes/ifmg/ifmg-2025-1-q17.png
```
*Gera o link público e exibe:*
```text
🎉 Upload realizado com sucesso!
   • Nome: ifmg-2025-1-q17.png
   • Subpasta remota: [ifmg/]
   • Link público: https://drive.google.com/file/d/1abc.../view?usp=sharing
```

---

### 3. Sincronização em Lote (Dry Run)
Simula a sincronização de todas as 107 imagens locais sem realizar uploads reais:
```bash
python3 scripts/manage_mathdata.py drive-sync --dry-run
```

---

### 4. Sincronização Real e Atualização Automática do `mathData.json`
Envia todas as imagens pendentes para o Drive, salva os links no cache local (`assets/img/drive_sync_cache.json`), atualiza os campos `"src"` no `mathData.json` e recompila o site:
```bash
python3 scripts/manage_mathdata.py drive-sync --update-mathdata --build
```

---

### 5. Recorte Integrado de Imagem de PDF
Ao recortar uma figura de prova com `crop-image`, faça o upload imediato com `--upload-drive`:
```bash
python3 scripts/manage_mathdata.py crop-image -p caderno.pdf --page 5 --rect 100 200 450 500 -o assets/img/questoes/ifmg/fig.png --upload-drive
```

---

### 6. Extração de PDF com Auto-Crop e Upload Automático
Extrai o exame completo do PDF, recorta as figuras detectadas e já hospeda no Google Drive:
```bash
python3 scripts/manage_mathdata.py parse-pdf -p caderno.pdf --auto-crop --upload-drive --import-to-block 8 --build
```

---

## 4. Solução de Problemas (Troubleshooting)

- **`Arquivo de credenciais da Service Account não encontrado!`**
  - Certifique-se de que o arquivo `service_account.json` está na raiz do projeto ou defina `GOOGLE_APPLICATION_CREDENTIALS` no `.env`.
- **`A Service Account tem acesso à pasta '...', mas NÃO possui permissão de escrita`**
  - No Google Drive, abra o menu Compartilhar da pasta e certifique-se de que o papel da conta de serviço seja **Editor** e não apenas Leitor.
- **`Erro 404: File not found` ao acessar a pasta raiz**
  - A Service Account só enxerga pastas que foram explicitamente compartilhadas com o e-mail dela. Verifique se o e-mail foi digitado corretamente no compartilhamento.

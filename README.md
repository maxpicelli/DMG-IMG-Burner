# DMG Burner - Gravador de Imagens IMG/DMG para USB

<p align="center">
  <img src="dmg-burner-icon.icns" alt="DMG Burner Icon" width="128" height="128">
</p>

Um aplicativo macOS simples e poderoso para gravar imagens IMG/DMG em pendrives USB, com interface via Terminal.

## 📋 Índice

- [Características](#-características)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Funcionalidades](#-funcionalidades)
- [Construir o App](#-construir-o-app)
- [Resolução de Problemas](#-resolução-de-problemas)
- [Avisos Importantes](#-avisos-importantes)
- [Licença](#-licença)

## ✨ Características

- 🔥 Gravação direta de imagens IMG/DMG em pendrives USB
- 🔄 Conversão de DMG para IMG (compatível com Balena Etcher)
- 📁 Suporte a Drag & Drop de arquivos
- 📊 Barra de progresso em tempo real durante a gravação
- 🔍 Detecção automática de dispositivos USB
- 🛡️ Confirmação de segurança antes de operações destrutivas
- 💻 Interface amigável via Terminal
- 🎨 Ícone personalizado e integração nativa com macOS

## 💻 Requisitos do Sistema

### Sistema Operacional
- **macOS 10.13 (High Sierra) ou superior**
- Recomendado: macOS 10.15 (Catalina) ou superior

### Python 3

O aplicativo requer **Python 3** instalado no sistema. O macOS 10.15+ já vem com Python 3 pré-instalado.

#### Verificar se o Python 3 está instalado:

```bash
python3 --version
```

Se você vir algo como `Python 3.x.x`, está pronto para usar!

#### Se o Python 3 não estiver instalado:

##### Opção 1: Anaconda Python (Recomendado)

1. **Baixar o Anaconda** - Escolha conforme seu Mac:

   **Para Mac com Apple Silicon (M1/M2/M3/M4):**
   ```bash
   curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-arm64.pkg
   open Anaconda3-2024.10-1-MacOSX-arm64.pkg
   ```
   Ou baixe direto: [Anaconda ARM64](https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-arm64.pkg)

   **Para Mac com Intel:**
   ```bash
   curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-x86_64.pkg
   open Anaconda3-2024.10-1-MacOSX-x86_64.pkg
   ```
   Ou baixe direto: [Anaconda Intel](https://repo.anaconda.com/archive/Anaconda3-2024.10-1-MacOSX-x86_64.pkg)

   **Não sabe qual Mac tem?** Execute no Terminal:
   ```bash
   uname -m
   # arm64 = Apple Silicon (M1/M2/M3/M4)
   # x86_64 = Intel
   ```

2. **Instalar o Anaconda**:
   - Execute o instalador baixado (.pkg)
   - Siga as instruções do instalador
   - Aceite os termos e escolha o local de instalação

3. **Configurar o Terminal** (após instalação):
   ```bash
   source ~/anaconda3/bin/activate
   conda init zsh
   ```

4. **Verificar a instalação**:
   ```bash
   python3 --version
   ```

5. **Vantagens do Anaconda**:
   - ✅ Inclui Python 3 + centenas de pacotes científicos
   - ✅ Gerenciador de ambientes virtuais (conda)
   - ✅ Jupyter Notebook incluído
   - ✅ Fácil atualização: `conda update python`
   - ✅ Otimizado para Apple Silicon (ARM64)

##### Opção 2: Download do Site Oficial Python

1. Acesse: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe o instalador mais recente do Python 3 para macOS
3. Execute o instalador (.pkg) e siga as instruções
4. Reinicie o Terminal e verifique: `python3 --version`

##### Opção 3: Via Command Line Tools do Xcode

```bash
xcode-select --install
```

Isso instalará as ferramentas de linha de comando incluindo o Python 3.

## 📥 Instalação

### Método 1: Instalação Rápida (Uma Linha)

Execute este comando no Terminal para instalar automaticamente:

```bash
curl -fsSL https://raw.githubusercontent.com/maxpicelli/DMG-IMG-Burner/main/install.sh | bash
```

Este comando irá:
- ✅ Baixar o repositório completo do GitHub
- ✅ Criar o aplicativo `DMG Burner.app`
- ✅ Mover para o Desktop
- ✅ Abrir o aplicativo automaticamente

### Método 2: Clone Manual do Repositório

1. **Clone este repositório**:
```bash
git clone https://github.com/maxpicelli/DMG-IMG-Burner.git
cd DMG-IMG-Burner
```

2. **Construir o aplicativo**:
```bash
chmod +x make-app.sh
./make-app.sh
```

3. **Mover para a pasta de Aplicativos** (opcional):
```bash
mv "DMG Burner.app" /Applications/
```

### Método 3: Download Direto

Baixe o ZIP do repositório e construa:
```bash
curl -L https://github.com/maxpicelli/DMG-IMG-Burner/archive/refs/heads/main.zip -o DMG-IMG-Burner.zip
unzip DMG-IMG-Burner.zip
cd DMG-IMG-Burner-main
chmod +x make-app.sh
./make-app.sh
```

### Primeira Execução

Na primeira vez que executar o app, o macOS pode bloquear por questões de segurança (Gatekeeper):

1. **Clique com botão direito** no `DMG Burner.app`
2. Selecione **"Abrir"**
3. Clique em **"Abrir"** na janela de confirmação

Após a primeira execução, você pode abrir normalmente com duplo-clique.

## 🚀 Como Usar

### Iniciar o Aplicativo

Duplo-clique em **DMG Burner.app**. O aplicativo abrirá uma janela do Terminal.

### Menu Principal

```
╔═══════════════════════════════════════════════════════════╗
║    IMG/DMG to USB Burner - macOS Terminal Version        ║
╚═══════════════════════════════════════════════════════════╝

Opções:
1. Selecionar imagem IMG/DMG
2. Listar dispositivos USB
3. Gravar imagem no pendrive
4. Converter DMG para IMG (USB compatível)
5. Ajuda
0. Sair
```

### Passo a Passo para Gravar um Pendrive

#### 1️⃣ Selecionar a Imagem

- Escolha a opção **1** no menu
- Você pode:
  - **Arrastar e soltar** o arquivo no Terminal
  - **Digitar o caminho** completo
  - **Procurar** em Downloads, Desktop ou pasta atual

#### 2️⃣ Verificar Dispositivos USB

- Escolha a opção **2** para listar dispositivos detectados
- Anote o identificador do seu pendrive (ex: `/dev/disk3`)

#### 3️⃣ Gravar a Imagem

- Escolha a opção **3**
- Selecione o dispositivo USB da lista
- **⚠️ ATENÇÃO**: Confirme que selecionou o dispositivo correto!
- Digite sua senha de administrador
- Aguarde a conclusão da gravação

#### 4️⃣ Ejetar com Segurança

Após a gravação, ejete o pendrive pelo Finder antes de removê-lo fisicamente.

## 🛠 Funcionalidades

### 1. Seleção de Imagem IMG/DMG

Múltiplas opções para selecionar sua imagem:
- 📎 Drag & Drop (arraste e solte)
- ⌨️ Digitação manual do caminho
- 🔍 Busca em pastas comuns (Downloads, Desktop, atual)

### 2. Listagem de Dispositivos USB

- Detecta automaticamente todos os dispositivos USB conectados
- Mostra informações detalhadas:
  - Nome do dispositivo
  - Identificador (/dev/diskX)
  - Tamanho
  - Status de montagem

### 3. Gravação de Imagem

- Usa o comando `dd` do sistema para gravação confiável
- Barra de progresso em tempo real
- Estatísticas de velocidade e tempo estimado
- Confirmação de segurança obrigatória
- Requer senha de administrador

### 4. Conversão DMG para IMG

Converte arquivos DMG para formato IMG compatível com ferramentas como Balena Etcher:

- **Método 1 (UDTO)**: Conversão RAW rápida
- **Método 2 (UDRW)**: Formato Read/Write
- **Método 3 (2 passos)**: Máxima compatibilidade

Suporta até mesmo arrastar o instalador `.app` do macOS!

## 🔨 Construir o App

Para recriar o aplicativo bundle a partir do código fonte:

```bash
./make-app.sh
```

O script irá:
1. ✅ Validar arquivos necessários
2. 🗑️ Limpar bundle existente (se houver)
3. 📁 Criar estrutura do bundle
4. 📄 Copiar script Python
5. 🚀 Criar launcher script
6. 🎨 Copiar ícone
7. ⚙️ Gerar Info.plist

### Estrutura do Bundle

```
DMG Burner.app/
├── Contents/
    ├── Info.plist
    ├── MacOS/
    │   ├── DMG Burner (launcher)
    │   └── DMG-terminal.py (script principal)
    └── Resources/
        └── dmg-burner-icon.icns
```

## 🔧 Resolução de Problemas

### Erro: "Python 3 is required but not installed"

**Solução**: Instale o Python 3 seguindo as instruções em [Requisitos do Sistema](#-requisitos-do-sistema).

### Erro: "Permission denied"

**Solução**: Certifique-se de que o script tem permissão de execução:
```bash
chmod +x "DMG Burner.app/Contents/MacOS/DMG Burner"
chmod +x DMG-terminal.py
```

### O app não abre ou não aparece o ícone

**Solução 1**: Reinicie o Finder
```bash
killall Finder
```

**Solução 2**: Limpe o cache de ícones
```bash
rm -rf /Library/Caches/com.apple.iconservices.store
sudo find /private/var/folders/ -name com.apple.iconservices -exec rm -rf {} \;
killall Finder
```

### Erro: "Operation not permitted" durante a gravação

**Solução**: O Terminal precisa de permissões de disco completo:
1. Vá em **Preferências do Sistema** > **Segurança e Privacidade**
2. Aba **Privacidade** > **Acesso Total ao Disco**
3. Adicione o **Terminal.app**

### Nenhum dispositivo USB encontrado

**Verificações**:
- ✅ Pendrive está conectado?
- ✅ Pendrive está funcionando em outro computador?
- ✅ Tente reconectar o dispositivo
- ✅ Verifique com: `diskutil list`

### Gravação muito lenta

**Dicas**:
- Use portas USB 3.0 (azuis) quando possível
- Evite usar hubs USB
- Certifique-se de que o pendrive suporta altas velocidades
- Velocidades típicas: 10-25 MB/s (USB 2.0), 40-100 MB/s (USB 3.0)

### Arquivo DMG não compatível

**Solução**: Use a opção **4** do menu para converter o DMG para IMG:
- Escolha o método de conversão adequado
- Depois use o arquivo `.img` gerado para gravar

## ⚠️ Avisos Importantes

### 🚨 OPERAÇÃO DESTRUTIVA

> **ATENÇÃO**: Gravar uma imagem em um dispositivo USB irá **APAGAR COMPLETAMENTE** todo o conteúdo existente no dispositivo. Esta operação é **IRREVERSÍVEL**.

### ✅ Antes de Gravar:

1. ✅ **Certifique-se** de ter selecionado o dispositivo correto
2. ✅ **Faça backup** de dados importantes do pendrive
3. ✅ **Verifique** se a imagem está íntegra e não corrompida
4. ✅ **Confirme** que o pendrive tem capacidade suficiente

### 🔐 Permissões de Administrador

Este aplicativo requer senha de administrador porque:
- Acessa dispositivos de armazenamento em baixo nível
- Desmonta volumes do sistema
- Executa comandos privilegiados (`sudo dd`)

### 🔌 Após a Gravação

1. **Aguarde** a mensagem de conclusão
2. **Ejete** o dispositivo pelo Finder
3. **Aguarde** a luz do pendrive parar de piscar
4. **Remova** o dispositivo com segurança

## 📝 Casos de Uso

### Criar Pendrive Bootável do macOS

1. Baixe o instalador do macOS da App Store
2. Use a opção 4 para converter o DMG interno do instalador
3. Grave o IMG resultante em um pendrive de 16GB+ (USB 3.0 recomendado)
4. Use para instalação limpa ou recuperação

### Criar Pendrive Linux Bootável

1. Baixe a imagem ISO/IMG da sua distribuição Linux
2. Use a opção 1 para selecionar a imagem
3. Grave em um pendrive de 4GB+
4. Boot pelo pendrive para testar ou instalar Linux

### Backup de Sistema

1. Crie uma imagem do seu sistema com Disk Utility
2. Converta para IMG se necessário (opção 4)
3. Grave em pendrive de emergência

## 🧪 Desenvolvido e Testado

- ✅ macOS 10.15 Catalina
- ✅ macOS 11 Big Sur
- ✅ macOS 12 Monterey
- ✅ macOS 13 Ventura
- ✅ macOS 14 Sonoma
- ✅ macOS 15 Sequoia

## 🛠 Tecnologias

- **Python 3** - Linguagem principal
- **Bash** - Scripts de build e launcher
- **diskutil** - Gerenciamento de discos macOS
- **dd** - Gravação de imagens em baixo nível
- **hdiutil** - Conversão de formatos DMG/IMG

## 📄 Licença

Copyright © 2025 M4Pro. Todos os direitos reservados.

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

---

## 🤝 Contribuições

Contribuições, issues e feature requests são bem-vindos!

## 📧 Suporte

Se você tiver problemas ou dúvidas:
1. Verifique a seção [Resolução de Problemas](#-resolução-de-problemas)
2. Consulte a opção **5 (Ajuda)** no menu do aplicativo
3. Abra uma issue no GitHub

---

<p align="center">
  Feito com ❤️ para a comunidade macOS
</p>

<p align="center">
  ⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!
</p>


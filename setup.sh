#!/bin/bash

################################################################################
# DMG Burner - Setup Script
# Instalador automático baseado no Clover Compiler Builder
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              DMG Burner - Setup Automático                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não está instalado!${NC}"
    echo ""
    echo -e "${YELLOW}Por favor, instale o Python 3 primeiro:${NC}"
    echo "  • Via Anaconda (Recomendado): https://www.anaconda.com/download"
    echo "  • Via site oficial: https://www.python.org/downloads/"
    echo "  • Via Xcode Tools: xcode-select --install"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 encontrado: $(python3 --version)${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não está instalado!${NC}"
    echo ""
    echo -e "${YELLOW}Instalando Git...${NC}"
    xcode-select --install
    exit 1
fi

# User directory
INSTALL_DIR="$HOME/DMG-IMG-Burner"

# Remove existing directory if it exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Removendo instalação anterior...${NC}"
    rm -rf "$INSTALL_DIR"
fi

echo -e "${YELLOW}[1/4]${NC} Baixando DMG-IMG-Burner do GitHub..."
git clone https://github.com/maxpicelli/DMG-IMG-Burner.git "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo -e "${YELLOW}[2/4]${NC} Preparando instalação..."
chmod +x make-app.sh

# Verificar se todos os arquivos necessários estão presentes
echo "Verificando arquivos necessários..."
if [ ! -f "DMG-terminal.py" ]; then
    echo -e "${RED}❌ Erro: DMG-terminal.py não encontrado!${NC}"
    exit 1
fi
if [ ! -f "dmg-burner-icon.icns" ]; then
    echo -e "${RED}❌ Erro: dmg-burner-icon.icns não encontrado!${NC}"
    exit 1
fi
if [ ! -f "make-app.sh" ]; then
    echo -e "${RED}❌ Erro: make-app.sh não encontrado!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Todos os arquivos necessários encontrados${NC}"

echo -e "${YELLOW}[3/4]${NC} Criando aplicativo..."
./make-app.sh

# Verificar se o app foi criado
if [ ! -d "DMG Burner.app" ]; then
    echo -e "${RED}❌ Erro: Aplicativo não foi criado!${NC}"
    echo "Verificando arquivos necessários..."
    ls -la
    exit 1
fi

echo -e "${GREEN}✓ Aplicativo criado com sucesso!${NC}"

echo -e "${YELLOW}[4/4]${NC} Abrindo pasta de instalação..."
open "$INSTALL_DIR"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📁 Pasta de instalação:${NC} ${INSTALL_DIR}"
echo -e "${BLUE}📱 Aplicativo criado:${NC} ${INSTALL_DIR}/DMG Burner.app"
echo ""

# Ask if user wants to open the app
echo -e "${YELLOW}Deseja abrir o aplicativo agora?${NC}"
echo -e "${BLUE}Digite 's' para sim ou 'n' para não (s/N):${NC}"
read -r response

if [[ "$response" =~ ^[Ss]$ ]] || [[ -z "$response" ]]; then
    echo -e "${GREEN}Abrindo aplicativo...${NC}"
    open "${INSTALL_DIR}/DMG Burner.app"
    echo -e "${YELLOW}Se aparecer aviso de segurança:${NC}"
    echo "  1. Clique com botão direito no app"
    echo "  2. Selecione 'Abrir'"
    echo "  3. Confirme 'Abrir' novamente"
else
    echo -e "${BLUE}Para usar o aplicativo:${NC}"
    echo "  1. Vá para a pasta que foi aberta"
    echo "  2. Duplo-clique em 'DMG Burner.app'"
fi

echo ""
echo -e "${YELLOW}Para mover para Applications:${NC}"
echo "  mv '${INSTALL_DIR}/DMG Burner.app' /Applications/"
echo ""
echo -e "${GREEN}✓ Setup finalizado!${NC}"

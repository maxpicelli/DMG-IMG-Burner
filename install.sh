#!/bin/bash

################################################################################
# DMG Burner - Quick Installer
# Instalador rápido para DMG-IMG-Burner
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           DMG Burner - Instalador Rápido                       ║${NC}"
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
echo ""

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

echo -e "${YELLOW}[4/4]${NC} Movendo para o Desktop..."
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR/DMG Burner.app" ]; then
    rm -rf "$DESKTOP_DIR/DMG Burner.app"
fi
mv "DMG Burner.app" "$DESKTOP_DIR/"

# Verificar se o app foi movido
if [ ! -d "$DESKTOP_DIR/DMG Burner.app" ]; then
    echo -e "${RED}❌ Erro: Falha ao mover aplicativo para o Desktop!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Aplicativo criado em:${NC} ${DESKTOP_DIR}/DMG Burner.app"
echo -e "${BLUE}📁 Código fonte em:${NC} ${INSTALL_DIR}"
echo ""
echo -e "${YELLOW}Para usar:${NC}"
echo "  1. Vá para o Desktop"
echo "  2. Duplo-clique em 'DMG Burner.app'"
echo "  3. Se necessário, clique com botão direito > Abrir (primeira vez)"
echo ""
echo -e "${YELLOW}Para mover para Applications:${NC}"
echo "  mv ~/Desktop/DMG\\ Burner.app /Applications/"
echo ""
echo -e "${YELLOW}Para limpar o código fonte:${NC}"
echo "  rm -rf ${INSTALL_DIR}"
echo ""
echo -e "${GREEN}✓ Instalação finalizada!${NC}"


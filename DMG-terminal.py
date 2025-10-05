#!/usr/bin/env python3
"""
IMG to USB Burner - Terminal Version
Gravador de imagens IMG/DMG para pendrives via terminal
"""
import sys
import subprocess
import os
import time
import re
import getpass

class ImgUsbBurner:
    def __init__(self):
        self.selected_img = None
        self.selected_device = None

    # >>> CORREÇÃO MÍNIMA: normalização de caminho (Drag & Drop/entrada manual)
    def _normalize_path(self, raw: str) -> str:
        if raw is None:
            return ""
        s = raw.strip()
        # Remove aspas externas
        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            s = s[1:-1].strip()
        # Desescapa padrões comuns do Finder no Terminal
        s = s.replace("\\ ", " ")
        for ch in "()[]{}&'\"":
            s = s.replace("\\" + ch, ch)
        # Expande ~ e $VARS
        s = os.path.expandvars(os.path.expanduser(s))
        return s
    # <<<

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear')
        
    def print_header(self):
        """Print application header"""
        self.clear_screen()
        print("=" * 60)
        print("    IMG/DMG to USB Burner - macOS Terminal Version")
        print("=" * 60)
        print()
        
    def print_menu(self):
        """Print main menu"""
        print("Opções:")
        print("1. Selecionar imagem IMG/DMG")
        print("2. Listar dispositivos USB")
        print("3. Gravar imagem no pendrive")
        print("4. Converter DMG para IMG (USB compatível)")
        print("5. Ajuda")
        print("0. Sair")
        print()
        
    def select_image(self):
        """Select IMG/DMG file"""
        print("=" * 60)
        print("Seleção de Imagem")
        print("=" * 60)
        
        while True:
            print("\nOpções:")
            print("1. Drag & Drop - Arraste o arquivo aqui")
            print("2. Digitar caminho completo")
            print("3. Procurar na pasta atual")
            print("4. Procurar na pasta Downloads")
            print("5. Procurar na pasta Desktop")
            print("0. Voltar ao menu principal")
            
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == "0":
                return
            elif choice == "1":
                print("\n🎯 DRAG & DROP MODE")
                print("─" * 40)
                print("Arraste o arquivo IMG/DMG aqui e pressione Enter:")
                print("(ou digite 'cancelar' para voltar)")
                print()
                
                raw = input("➤ ")
                path = self._normalize_path(raw)  # <<< CORREÇÃO: normaliza
                if path.lower() == 'cancelar':
                    continue
                if self.validate_image(path):
                    self.selected_img = path
                    print(f"✓ Imagem selecionada: {os.path.basename(path)}")
                    input("Pressione Enter para continuar...")
                    return
            elif choice == "2":
                raw = input("Digite o caminho completo da imagem: ").strip()
                path = self._normalize_path(raw)  # <<< CORREÇÃO: normaliza
                if self.validate_image(path):
                    self.selected_img = path
                    print(f"✓ Imagem selecionada: {os.path.basename(path)}")
                    input("Pressione Enter para continuar...")
                    return
            elif choice in ["3", "4", "5"]:
                if choice == "3":
                    search_path = os.getcwd()
                elif choice == "4":
                    search_path = os.path.expanduser("~/Downloads")
                else:
                    search_path = os.path.expanduser("~/Desktop")
                
                self.browse_folder(search_path)
                if self.selected_img:
                    return
            else:
                print("Opção inválida!")
                
    def browse_folder(self, folder_path):
        """Browse folder for IMG/DMG files"""
        if not os.path.exists(folder_path):
            print(f"Pasta não encontrada: {folder_path}")
            input("Pressione Enter para continuar...")
            return
            
        print(f"\nProcurando arquivos IMG/DMG em: {folder_path}")
        
        img_files = []
        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.img', '.dmg')):
                    full_path = os.path.join(folder_path, file)
                    img_files.append((file, full_path))
        except PermissionError:
            print("Erro: Sem permissão para acessar esta pasta")
            input("Pressione Enter para continuar...")
            return
            
        if not img_files:
            print("Nenhum arquivo IMG/DMG encontrado nesta pasta")
            input("Pressione Enter para continuar...")
            return
            
        print(f"\nEncontrados {len(img_files)} arquivo(s):")
        for i, (filename, _) in enumerate(img_files, 1):
            size = self.get_file_size(os.path.join(folder_path, filename))
            print(f"{i}. {filename} ({size})")
            
        print("0. Voltar")
        
        while True:
            try:
                choice = int(input(f"\nSelecione um arquivo (1-{len(img_files)}): "))
                if choice == 0:
                    return
                elif 1 <= choice <= len(img_files):
                    selected_file = img_files[choice - 1]
                    self.selected_img = selected_file[1]
                    print(f"✓ Imagem selecionada: {selected_file[0]}")
                    input("Pressione Enter para continuar...")
                    return
                else:
                    print("Número inválido!")
            except ValueError:
                print("Digite um número válido!")
            except KeyboardInterrupt:
                print("\n\nOperação cancelada!")
                return
            except Exception as e:
                print(f"Erro: {e}")
                
    def validate_image(self, path):
        """Validate if file is a valid image"""
        if not os.path.exists(path):
            print("Erro: Arquivo não encontrado!")
            return False
            
        if not path.lower().endswith(('.img', '.dmg')):
            print("Aviso: Arquivo não é .img ou .dmg")
            choice = input("Continuar mesmo assim? (s/N): ").lower()
            if choice != 's':
                return False
                
        file_size = os.path.getsize(path)
        if file_size == 0:
            print("Erro: Arquivo está vazio!")
            return False
            
        return True
        
    def get_file_size(self, path):
        """Get human readable file size"""
        try:
            size = os.path.getsize(path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except Exception:
            return "Unknown"
            
    def list_usb_devices(self):
        """List available USB devices"""
        print("=" * 60)
        print("Dispositivos USB Disponíveis")
        print("=" * 60)
        
        try:
            result = subprocess.run(['diskutil', 'list'],
                                  capture_output=True, text=True, check=True)
            
            devices = []
            lines = result.stdout.split('\n')
            
            print("Procurando dispositivos USB...")
            
            for line in lines:
                if '/dev/disk' in line and ('external' in line.lower() or 'usb' in line.lower()):
                    disk_id = line.split()[0]
                    
                    try:
                        # Get detailed info
                        info_result = subprocess.run(['diskutil', 'info', disk_id],
                                                   capture_output=True, text=True, check=True)
                        
                        info_lines = info_result.stdout.split('\n')
                        is_usb = False
                        device_name = "Dispositivo USB"
                        size = "Unknown"
                        mount_point = "Não montado"
                        
                        for info_line in info_lines:
                            if 'Protocol:' in info_line and 'USB' in info_line:
                                is_usb = True
                            elif 'Device / Media Name:' in info_line:
                                device_name = info_line.split(':', 1)[1].strip()
                            elif 'Disk Size:' in info_line:
                                size_part = info_line.split(':', 1)[1].strip()
                                size_match = re.search(r'(\d+\.?\d*\s*[KMGT]B)', size_part)
                                if size_match:
                                    size = size_match.group(1)
                            elif 'Mount Point:' in info_line:
                                mount_part = info_line.split(':', 1)[1].strip()
                                if mount_part and mount_part != "Not applicable (no file system)":
                                    mount_point = mount_part
                        
                        if is_usb:
                            devices.append({
                                'id': disk_id,
                                'name': device_name,
                                'size': size,
                                'mount': mount_point
                            })
                            
                    except subprocess.CalledProcessError:
                        continue
                        
            if not devices:
                print("❌ Nenhum dispositivo USB encontrado!")
                print("\nDicas:")
                print("- Certifique-se de que o pendrive está conectado")
                print("- Tente desconectar e reconectar o dispositivo")
                print("- Verifique se o dispositivo está funcionando")
            else:
                print(f"✅ Encontrados {len(devices)} dispositivo(s) USB:\n")
                for i, device in enumerate(devices, 1):
                    print(f"{i}. {device['id']} - {device['name']}")
                    print(f"   Tamanho: {device['size']}")
                    print(f"   Status: {device['mount']}")
                    print()
                    
                print("⚠️  ATENÇÃO: Gravar uma imagem irá APAGAR TODOS os dados do dispositivo!")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao listar dispositivos: {e}")
            
        input("\nPressione Enter para continuar...")
        
    def burn_image(self):
        """Burn image to USB device"""
        print("=" * 60)
        print("Gravação de Imagem")
        print("=" * 60)
        
        if not self.selected_img:
            print("❌ Nenhuma imagem selecionada!")
            print("Primeiro selecione uma imagem no menu principal.")
            input("Pressione Enter para continuar...")
            return
            
        print(f"📁 Imagem selecionada: {os.path.basename(self.selected_img)}")
        print(f"📍 Caminho: {self.selected_img}")
        print(f"📏 Tamanho: {self.get_file_size(self.selected_img)}")
        print()
        
        # List devices for selection
        try:
            result = subprocess.run(['diskutil', 'list'],
                                  capture_output=True, text=True, check=True)
            
            devices = []
            lines = result.stdout.split('\n')
            
            for line in lines:
                if '/dev/disk' in line and ('external' in line.lower() or 'usb' in line.lower()):
                    disk_id = line.split()[0]
                    
                    try:
                        info_result = subprocess.run(['diskutil', 'info', disk_id],
                                                   capture_output=True, text=True, check=True)
                        
                        if 'USB' in info_result.stdout:
                            info_lines = info_result.stdout.split('\n')
                            device_name = "Dispositivo USB"
                            size = "Unknown"
                            
                            for info_line in info_lines:
                                if 'Device / Media Name:' in info_line:
                                    device_name = info_line.split(':', 1)[1].strip()
                                elif 'Disk Size:' in info_line:
                                    size_part = info_line.split(':', 1)[1].strip()
                                    size_match = re.search(r'(\d+\.?\d*\s*[KMGT]B)', size_part)
                                    if size_match:
                                        size = size_match.group(1)
                            
                            devices.append({
                                'id': disk_id,
                                'name': device_name,
                                'size': size
                            })
                            
                    except subprocess.CalledProcessError:
                        continue
                        
            if not devices:
                print("❌ Nenhum dispositivo USB encontrado!")
                input("Pressione Enter para continuar...")
                return
                
            print("Dispositivos USB disponíveis:")
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device['id']} - {device['name']} ({device['size']})")
            print("0. Cancelar")
            
            while True:
                try:
                    choice = int(input(f"\nSelecione o dispositivo (1-{len(devices)}): "))
                    if choice == 0:
                        return
                    elif 1 <= choice <= len(devices):
                        selected_device = devices[choice - 1]
                        break
                    else:
                        print("Número inválido!")
                except ValueError:
                    print("Digite um número válido!")
                    
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao listar dispositivos: {e}")
            input("Pressione Enter para continuar...")
            return
            
        # Confirmation
        print("\n" + "⚠️ " * 20)
        print("🚨 ATENÇÃO: OPERAÇÃO DESTRUTIVA! 🚨")
        print("⚠️ " * 20)
        print(f"\nEsta operação irá APAGAR COMPLETAMENTE todo o conteúdo de:")
        print(f"📱 Dispositivo: {selected_device['id']}")
        print(f"🏷️  Nome: {selected_device['name']}")
        print(f"💾 Tamanho: {selected_device['size']}")
        print(f"\n📁 Com a imagem: {os.path.basename(self.selected_img)}")
        print(f"📏 Tamanho: {self.get_file_size(self.selected_img)}")
        
        print("\n❌ TODOS OS DADOS DO DISPOSITIVO SERÃO PERDIDOS!")
        print("✅ Certifique-se de ter backup de dados importantes!")
        
        confirm = input("\n⚠️  Deseja continuar? (S/n - Enter = Sim): ").strip().lower()
        if confirm in ['n', 'no', 'não']:
            print("❌ Operação cancelada!")
            input("Pressione Enter para continuar...")
            return
            
        # Get password
        password = self.get_password()
        if not password:
            print("❌ Senha necessária para continuar!")
            input("Pressione Enter para continuar...")
            return
            
        # Start burning process
        self.perform_burn(selected_device['id'], password)
        
    def get_password(self):
        """Get sudo password"""
        try:
            password = getpass.getpass("🔐 Digite sua senha de administrador: ")
            
            # Test password
            test_cmd = ['sudo', '-S', 'echo', 'test']
            result = subprocess.run(test_cmd, input=password + '\n',
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return password
            else:
                print("❌ Senha incorreta!")
                return None
                
        except KeyboardInterrupt:
            print("\n❌ Operação cancelada pelo usuário!")
            return None
        except Exception as e:
            print(f"❌ Erro ao obter senha: {e}")
            return None
            
    def perform_burn(self, device, password):
        """Perform the actual burning process"""
        print("\n" + "=" * 60)
        print("🔥 INICIANDO GRAVAÇÃO")
        print("=" * 60)
        
        try:
            # Step 1: Unmount device
            print("📤 Desmontando dispositivo...")
            unmount_result = subprocess.run(['sudo', '-S', 'diskutil', 'unmountDisk', device],
                                          input=password + '\n', text=True, capture_output=True)
            
            if unmount_result.returncode == 0:
                print("✅ Dispositivo desmontado com sucesso")
            else:
                print(f"⚠️  Aviso: {unmount_result.stderr}")
                
            # Step 2: Get file info
            file_size = os.path.getsize(self.selected_img)
            file_size_mb = file_size / (1024 * 1024)
            file_size_gb = file_size / (1024 * 1024 * 1024)
            
            print(f"📏 Tamanho do arquivo: {file_size_mb:.1f} MB ({file_size_gb:.2f} GB)")
            
            # Step 3: Start dd process
            print("🔥 Iniciando gravação com dd...")
            
            dd_cmd = ['sudo', '-S', 'dd', f'if={self.selected_img}', f'of={device}', 'bs=1m']
            
            print(f"🚀 Executando: dd if={os.path.basename(self.selected_img)} of={device} bs=1m")
            print("📊 Monitoramento de progresso ativo...")
            print()
            
            start_time = time.time()
            
            process = subprocess.Popen(dd_cmd, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True)
            try:
                process.stdin.write(password + '\n')
                process.stdin.flush()
                process.stdin.close()
            except Exception:
                pass
            
            print("📈 Progresso:")
            print("-" * 60)
            while process.poll() is None:
                try:
                    current_time = time.time()
                    elapsed = current_time - start_time
                    # Estimativa conservadora
                    estimated_speed_mb_s = 12
                    estimated_written = min(elapsed * estimated_speed_mb_s * 1024 * 1024, file_size)
                    progress_percent = min((estimated_written / file_size) * 100, 99)
                    written_mb = estimated_written / (1024 * 1024)
                    speed_mb_s = written_mb / max(elapsed, 1)
                    remaining_mb = (file_size - estimated_written) / (1024 * 1024)
                    eta_minutes = remaining_mb / max(speed_mb_s, 1) / 60
                    progress_bar = self.create_progress_bar(progress_percent, 40)
                    print(f"\r[{progress_bar}] {progress_percent:.1f}% | "
                          f"{written_mb:.0f}/{file_size_mb:.0f} MB | "
                          f"{speed_mb_s:.1f} MB/s | "
                          f"ETA: {eta_minutes:.1f}min", end='', flush=True)
                    time.sleep(1)
                except Exception:
                    time.sleep(1)
            
            try:
                stdout, stderr = process.communicate(timeout=10)
                _ = stderr if stderr else stdout
            except Exception:
                pass
                
            elapsed_time = time.time() - start_time
            print()
            
            if process.returncode == 0:
                print("\n🎉✅ GRAVAÇÃO CONCLUÍDA COM SUCESSO!")
                avg_speed = file_size_mb / elapsed_time if elapsed_time > 0 else 0
                print(f"\n📊 Estatísticas:")
                print(f"   ⏱️  Tempo total: {elapsed_time/60:.1f} min")
                print(f"   📏 Dados: {file_size_mb:.1f} MB")
                print(f"   🚀 Média: {avg_speed:.1f} MB/s")
                print("\nUse 'Ejetar' no Finder antes de remover o pendrive.")
            else:
                print("\n❌ ERRO NA GRAVAÇÃO!")
                print(f"Código de erro: {process.returncode}")
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação interrompida pelo usuário! A gravação pode estar incompleta.")
            try:
                if 'process' in locals():
                    process.terminate()
                    time.sleep(2)
                    if process.poll() is None:
                        process.kill()
                subprocess.run(['sudo', 'pkill', 'dd'], capture_output=True, timeout=5)
            except Exception:
                pass
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Detalhes técnicos: Falha na comunicação com processo dd")
        input("\nPressione Enter para continuar...")
        
    def create_progress_bar(self, percent, width=40):
        """Create a visual progress bar"""
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"{bar}"
        
    def convert_dmg_to_img(self):
        """Convert DMG to IMG with USB-compatible partition scheme"""
        print("=" * 60)
        print("Conversão DMG para IMG (USB Compatível)")
        print("=" * 60)

        # Se já houver DMG selecionado anteriormente, oferecer atalho
        path = None
        if self.selected_img and str(self.selected_img).lower().endswith(".dmg") and os.path.exists(self.selected_img):
            print(f"📁 DMG já selecionado anteriormente: {os.path.basename(self.selected_img)}")
            use_it = input("Usar este arquivo? (S/n): ").strip().lower()
            if use_it in ("", "s", "sim", "y", "yes"):
                path = self.selected_img

        if not path:
            print("\n📁 Seleção do arquivo DMG:")
            print("1. Drag & Drop - Arraste o arquivo DMG (ou o .app do instalador) aqui")
            print("0. Voltar ao menu principal")
            while True:
                choice = input("\nEscolha uma opção: ").strip()
                if choice in ("0", "voltar", "cancelar", "sair"):
                    return
                if choice == "1":
                    print("\n🎯 DRAG & DROP MODE")
                    print("─" * 40)
                    print("Arraste o arquivo DMG ou o .app aqui e pressione Enter:")
                    print("(ou digite 'cancelar' para voltar)")
                    raw = input("➤ ")
                    raw = self._normalize_path(raw)  # <<< CORREÇÃO: normaliza
                    if raw.lower() in ("cancelar", "voltar", "0", "sair"):
                        continue
                    if not os.path.exists(raw):
                        print("❌ Arquivo não encontrado! Tente novamente.")
                        continue
                    # >>> CORREÇÃO: aceitar .app e localizar .dmg interno
                    if raw.lower().endswith(".app"):
                        shared = os.path.join(raw, 'Contents', 'SharedSupport')
                        candidate = None
                        if os.path.isdir(shared):
                            for n in ['SharedSupport.dmg', 'InstallESD.dmg', 'BaseSystem.dmg']:
                                p = os.path.join(shared, n)
                                if os.path.exists(p):
                                    candidate = p
                                    break
                            if candidate is None:
                                for entry in os.listdir(shared):
                                    if entry.lower().endswith('.dmg'):
                                        candidate = os.path.join(shared, entry)
                                        break
                        if candidate and os.path.exists(candidate):
                            print(f"Encontrado DMG dentro do app: {os.path.basename(candidate)}")
                            path = candidate
                        else:
                            print("❌ Nenhum .dmg encontrado em Contents/SharedSupport dentro do .app")
                            input("Pressione Enter para continuar...")
                            return
                    else:
                        if not raw.lower().endswith(".dmg"):
                            print("❌ O arquivo deve ser um DMG (ou arraste o .app do instalador).")
                            continue
                        path = raw
                    # <<<
                    break
                else:
                    print("Opção inválida! Use 1 ou 0.")

        dmg_dir = os.path.dirname(path)
        dmg_name = os.path.basename(path)
        img_name = dmg_name.replace('.dmg', '_USB_Compatible.img')
        output_base = os.path.join(dmg_dir, img_name[:-4])  # hdiutil acrescenta extensão

        print(f"\n📁 Arquivo DMG: {dmg_name}")
        print(f"📏 Tamanho: {self.get_file_size(path)}")
        print(f"📤 Será convertido para: {img_name}")
        print(f"📍 Local: {dmg_dir}")
        
        print("\n🔧 Opções de conversão:")
        print("1. Conversão RAW (Balena Etcher compatível) [UDTO → .cdr → .img]")
        print("2. Formato Read/Write (UDRW) [gera .img RW]")
        print("3. Máxima compatibilidade (2 passos: UDTO→UDRW)")
        print("0. Voltar ao menu principal")

        while True:
            conv_choice = input("Escolha o método de conversão: ").strip()
            if conv_choice in ("0", "voltar", "cancelar", "sair"):
                return
            if conv_choice in ("1", "2", "3"):
                break
            print("Opção inválida!")

        print(f"\n⚠️  Confirma a conversão?\nDe: {dmg_name}\nPara: {img_name}")
        confirm = input("(S/n - Enter = Sim | 0/voltar/cancelar para sair): ").strip().lower()
        if confirm in ('n', 'no', 'não', 'nao', '0', 'voltar', 'cancelar', 'sair'):
            print("❌ Conversão cancelada!")
            input("Pressione Enter para continuar...")
            return
            
        self.perform_conversion(path, output_base, conv_choice)
        
    def perform_conversion(self, dmg_path, output_base, method):
        """Perform the actual DMG to IMG conversion"""
        print("\n" + "=" * 60)
        print("🔄 INICIANDO CONVERSÃO")
        print("=" * 60)
        
        start_time = time.time()
        created_paths = []
        try:
            if method == "1":
                # UDTO → .cdr → renomear .img
                print("🔄 Convertendo DMG para IMG RAW (UDTO)...")
                cmd = ['hdiutil', 'convert', dmg_path, '-format', 'UDTO', '-o', output_base]
                p = subprocess.run(cmd, capture_output=True, text=True)
                if p.returncode != 0:
                    print("❌ Erro na conversão (UDTO)")
                    if p.stderr:
                        print(f"Detalhes: {p.stderr.strip()}")
                    input("\nPressione Enter para continuar...")
                    return
                out_cdr = output_base + ".cdr"
                final_img = output_base + ".img"
                if not os.path.exists(out_cdr):
                    print("❌ Saída .cdr não encontrada.")
                    input("\nPressione Enter para continuar...")
                    return
                try:
                    if os.path.exists(final_img):
                        os.remove(final_img)
                except Exception:
                    pass
                os.rename(out_cdr, final_img)
                created_paths.append(final_img)

            elif method == "2":
                # UDRW → .img (ou .dmg em algumas versões → renomear para .img)
                print("🔄 Convertendo DMG para IMG (UDRW)...")
                cmd = ['hdiutil', 'convert', dmg_path, '-format', 'UDRW', '-o', output_base]
                p = subprocess.run(cmd, capture_output=True, text=True)
                if p.returncode != 0:
                    print("❌ Erro na conversão (UDRW)")
                    if p.stderr:
                        print(f"Detalhes: {p.stderr.strip()}")
                    input("\nPressione Enter para continuar...")
                    return
                out_img = output_base + ".img"
                out_dmg = output_base + ".dmg"
                if os.path.exists(out_img):
                    created_paths.append(out_img)
                elif os.path.exists(out_dmg):
                    final_img = output_base + ".img"
                    try:
                        if os.path.exists(final_img):
                            os.remove(final_img)
                    except Exception:
                        pass
                    os.rename(out_dmg, final_img)
                    created_paths.append(final_img)
                else:
                    print("⚠️ Não encontrei .img/.dmg após UDRW.")
                    input("\nPressione Enter para continuar...")
                    return

            elif method == "3":
                # Dois passos: UDTO e depois UDRW por cima do .cdr
                print("🔄 Passo 1/2: DMG → UDTO (.cdr)...")
                cmd1 = ['hdiutil', 'convert', dmg_path, '-format', 'UDTO', '-o', output_base]
                p1 = subprocess.run(cmd1, capture_output=True, text=True)
                if p1.returncode != 0:
                    print("❌ Erro no passo 1 (UDTO)")
                    if p1.stderr:
                        print(f"Detalhes: {p1.stderr.strip()}")
                    input("\nPressione Enter para continuar...")
                    return
                cdr = output_base + ".cdr"
                if not os.path.exists(cdr):
                    print("❌ Saída .cdr não encontrada.")
                    input("\nPressione Enter para continuar...")
                    return
                print("🔄 Passo 2/2: UDTO (.cdr) → UDRW (.img)...")
                cmd2 = ['hdiutil', 'convert', cdr, '-format', 'UDRW', '-o', output_base]
                p2 = subprocess.run(cmd2, capture_output=True, text=True)
                if p2.returncode != 0:
                    print("❌ Erro no passo 2 (UDRW)")
                    if p2.stderr:
                        print(f"Detalhes: {p2.stderr.strip()}")
                    input("\nPressione Enter para continuar...")
                    return
                out_img = output_base + ".img"
                out_dmg = output_base + ".dmg"
                if os.path.exists(out_img):
                    created_paths.append(out_img)
                elif os.path.exists(out_dmg):
                    final_img = output_base + ".img"
                    try:
                        if os.path.exists(final_img):
                            os.remove(final_img)
                    except Exception:
                        pass
                    os.rename(out_dmg, final_img)
                    created_paths.append(final_img)
                else:
                    print("⚠️ Não encontrei arquivo final após 2 passos.")
                    input("\nPressione Enter para continuar...")
                    return
            else:
                print("❌ Método inválido.")
                input("\nPressione Enter para continuar...")
                return

            elapsed = time.time() - start_time
            final_file = created_paths[-1] if created_paths else None
            print("\n🎉 Conversão concluída com sucesso!")
            if final_file:
                print(f"📦 Saída: {os.path.basename(final_file)}")
                print(f"📍 Local: {os.path.dirname(final_file)}")
                print(f"⏱️ Tempo total: {elapsed:.1f}s")
            else:
                print("⚠️ Conversão reportou sucesso, mas não encontrei o arquivo final.")
        except KeyboardInterrupt:
            print("\n❌ Conversão interrompida pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado durante a conversão: {e}")
        input("\nPressione Enter para continuar...")
        
    def show_help(self):
        """Show help information"""
        print("=" * 60)
        print("Ajuda")
        print("=" * 60)
        print("""
Este utilitário permite:
1) Selecionar uma imagem .img ou .dmg
2) Listar dispositivos USB detectados no sistema
3) Gravar a imagem selecionada em um pendrive (operação destrutiva)
4) Converter um arquivo .dmg para .img compatível com escrita RAW

ATENÇÃO:
- A gravação APAGA COMPLETAMENTE o conteúdo do dispositivo escolhido.
- Certifique-se de selecionar o disco correto (ex.: /dev/disk3).
- No macOS, use 'Ejetar' no Finder após finalizar, antes de remover o pendrive.

Dicas:
- Método 1 (UDTO) gera .cdr que é renomeado para .img (compatível com Etcher).
- Método 2 (UDRW) gera .img de leitura/escrita.
- Método 3 faz 2 passos para máxima compatibilidade.
- Na conversão (opção 4), você pode arrastar o .dmg **ou** o .app do instalador:
  o script localiza o .dmg em Contents/SharedSupport.
        """)
        input("Pressione Enter para voltar ao menu...")
        

def main():
    app = ImgUsbBurner()
    while True:
        app.print_header()
        app.print_menu()
        choice = input("Selecione uma opção: ").strip()
        
        if choice == "1":
            app.select_image()
        elif choice == "2":
            app.list_usb_devices()
        elif choice == "3":
            app.burn_image()
        elif choice == "4":
            app.convert_dmg_to_img()
        elif choice == "5":
            app.show_help()
        elif choice == "0":
            print("Saindo...")
            time.sleep(0.3)
            break
        else:
            print("Opção inválida!")
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")


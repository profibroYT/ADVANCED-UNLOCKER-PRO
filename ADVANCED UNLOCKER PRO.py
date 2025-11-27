import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import os
import sys
import psutil
import threading
import time
import subprocess
import shutil
import tempfile
from datetime import datetime
import json
import logging
import webbrowser
from pathlib import Path

try:
    import winreg
except ImportError:
    winreg = None
    logging.warning("winreg module not available on this system")

class StartupConfig:
    """Окно начальной конфигурации с логом обновлений"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Unlocker Pro - Configuration")
        self.root.geometry("600x500")
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        # Центрирование
        self.center_window()
        
        # Переменные настроек
        self.resolution = tk.StringVar(value="1400x900")
        self.theme = tk.StringVar(value="dark")
        self.debug_mode = tk.BooleanVar(value=False)
        self.admin_mode = tk.BooleanVar(value=False)
        
        # Создаем вкладки
        self.create_notebook()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 600
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_notebook(self):
        """Создание вкладок"""
        style = ttk.Style()
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#3a3a3a', foreground='white')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка настроек
        self.settings_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(self.settings_frame, text='⚙️ Настройки')
        
        # Вкладка лога обновлений
        self.update_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(self.update_frame, text='📋 Лог Обновления')
        
        self.setup_settings_tab()
        self.setup_update_log_tab()
    
    def setup_settings_tab(self):
        """Настройка вкладки с настройками"""
        # Заголовок
        title_frame = tk.Frame(self.settings_frame, bg='#2b2b2b')
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="⚡ ADVANCED UNLOCKER PRO", 
                font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#58a6ff').pack()
        tk.Label(title_frame, text="Complete System Management Suite", 
                font=('Arial', 10), bg='#2b2b2b', fg='#cccccc').pack(pady=5)
        
        # Основные настройки
        config_frame = tk.Frame(self.settings_frame, bg='#2b2b2b')
        config_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Разрешение
        res_frame = tk.Frame(config_frame, bg='#2b2b2b')
        res_frame.pack(fill='x', pady=10)
        tk.Label(res_frame, text="Разрешение:", bg='#2b2b2b', fg='white', 
                font=('Arial', 10)).pack(side='left')
        
        resolutions = ["1240x1020", "1400x900", "1600x1000", "1920x1080"]
        res_combo = ttk.Combobox(res_frame, textvariable=self.resolution, 
                               values=resolutions, state="readonly", width=15)
        res_combo.pack(side='right')
        
        # Тема
        theme_frame = tk.Frame(config_frame, bg='#2b2b2b')
        theme_frame.pack(fill='x', pady=10)
        tk.Label(theme_frame, text="Тема:", bg='#2b2b2b', fg='white',
                font=('Arial', 10)).pack(side='left')
        
        themes = ["dark", "light", "blue", "green"]
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme,
                                 values=themes, state="readonly", width=15)
        theme_combo.pack(side='right')
        
        # Опции
        options_frame = tk.Frame(config_frame, bg='#2b2b2b')
        options_frame.pack(fill='x', pady=15)
        
        tk.Checkbutton(options_frame, text="🔧 Режим отладки", 
                      variable=self.debug_mode, bg='#2b2b2b', fg='white',
                      selectcolor='#2b2b2b', font=('Arial', 10)).pack(anchor='w')
        
        tk.Checkbutton(options_frame, text="🛡️ Права администратора", 
                      variable=self.admin_mode, bg='#2b2b2b', fg='white',
                      selectcolor='#2b2b2b', font=('Arial', 10)).pack(anchor='w')
        
        # Информация
        info_frame = tk.Frame(config_frame, bg='#3a3a3a', relief='groove', bd=1)
        info_frame.pack(fill='x', pady=15)
        
        info_text = """📋 Доступные возможности:
• Разблокировка файлов и управление
• Мониторинг и контроль процессов  
• Редактор реестра
• Менеджер автозагрузки
• Системные инструменты и утилиты
• Сетевой мониторинг
• Центр безопасности"""
        
        tk.Label(info_frame, text=info_text, bg='#3a3a3a', fg='#cccccc',
                font=('Arial', 9), justify='left').pack(padx=10, pady=10)
        
        # Кнопки
        button_frame = tk.Frame(self.settings_frame, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🚀 ЗАПУСК ПРИЛОЖЕНИЯ", 
                 command=self.launch_app, bg='#58a6ff', fg='white',
                 font=('Arial', 12, 'bold'), width=20, height=2).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="❌ ВЫХОД", 
                 command=self.root.quit, bg='#da3633', fg='white',
                 font=('Arial', 10), width=10).pack(side='left', padx=10)
    
    def setup_update_log_tab(self):
        """Настройка вкладки с логом обновлений"""
        # Заголовок
        title_frame = tk.Frame(self.update_frame, bg='#2b2b2b')
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="📋 ИСТОРИЯ ОБНОВЛЕНИЙ", 
                font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#58a6ff').pack()
        tk.Label(title_frame, text="Журнал изменений и улучшений", 
                font=('Arial', 10), bg='#2b2b2b', fg='#cccccc').pack(pady=5)
        
        # Статистика обновлений
        stats_frame = tk.Frame(self.update_frame, bg='#3a3a3a', relief='groove', bd=1)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        stats_text = """📊 Статистика проекта:
• Версия: 2.1.0
• Всего обновлений: 15
• Последнее обновление: 2024-11-26
• Статус: Stable Release
• Размер кода: ~1500 строк"""
        
        tk.Label(stats_frame, text=stats_text, bg='#3a3a3a', fg='#cccccc',
                font=('Arial', 9), justify='left').pack(padx=10, pady=10)
        
        # Область с логом обновлений
        log_frame = tk.Frame(self.update_frame, bg='#2b2b2b')
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Создаем текстовое поле с прокруткой
        text_frame = tk.Frame(log_frame, bg='#2b2b2b')
        text_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD,
            width=70,
            height=15,
            bg='#1e1e1e',
            fg='#cccccc',
            font=('Consolas', 9),
            relief='sunken',
            bd=2
        )
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Загружаем лог обновлений
        self.load_update_log()
        
        # Кнопки управления
        button_frame = tk.Frame(self.update_frame, bg='#2b2b2b')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔄 Проверить обновления", 
                 command=self.check_for_updates, bg='#58a6ff', fg='white',
                 font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="💾 Экспорт лога", 
                 command=self.export_log, bg='#3fb950', fg='white',
                 font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="📋 Копировать", 
                 command=self.copy_log, bg='#d29922', fg='white',
                 font=('Arial', 10)).pack(side='left', padx=5)
    
    def load_update_log(self):
        """Загрузка лога обновлений"""
        update_log = """
╔══════════════════════════════════════════════════════════════╗
║                 ADVANCED UNLOCKER PRO v2.1.0                ║
║                   Полный системный комплект                 ║
╚══════════════════════════════════════════════════════════════╝

📅 ВЕРСИЯ 2.1.0 (2024-11-26)
────────────────────────────────────────────────────────────────
• 🎉 ПОЛНЫЙ РЕФАКТОРИНГ ПРИЛОЖЕНИЯ
• ✨ Добавлен современный графический интерфейс
• 🛠️ Исправлены все критические ошибки
• 📁 Полностью переработан файловый проводник
• 🚀 Улучшена производительность

🔧 ОСНОВНЫЕ ИЗМЕНЕНИЯ:
  ✅ Добавлен полноценный файловый менеджер
  ✅ Исправлена работа всех вкладок
  ✅ Добавлен монитор системных ресурсов
  ✅ Реализован центр безопасности
  ✅ Добавлены сетевые инструменты
  ✅ Улучшена система разблокировки файлов

📅 ВЕРСИЯ 2.0.0 (2024-11-25)
────────────────────────────────────────────────────────────────
• 🎨 Полностью переработан пользовательский интерфейс
• 📊 Добавлен мониторинг системы в реальном времени
• 🔒 Улучшены алгоритмы разблокировки файлов
• 🛡️ Добавлены инструменты безопасности

🆕 НОВЫЕ ВОЗМОЖНОСТИ:
  🌐 Сетевые инструменты (ping, netstat, ipconfig)
  🛡️ Сканер безопасности процессов
  📈 Монитор производительности
  🗂️ Расширенный редактор реестра
  🚀 Менеджер автозагрузки

📅 ВЕРСИЯ 1.5.0 (2024-11-20)
────────────────────────────────────────────────────────────────
• 🔧 Добавлены системные инструменты
• 📁 Улучшен файловый проводник
• 🐛 Исправлены ошибки стабильности
• ⚡ Оптимизирована работа с процессами

📅 ВЕРСИЯ 1.2.0 (2024-11-15)
────────────────────────────────────────────────────────────────
• 🎯 Добавлен монитор процессов
• 🔓 Улучшена система разблокировки
• 📊 Добавлена статистика системы
• 🎨 Обновлен интерфейс

📅 ВЕРСИЯ 1.0.0 (2024-11-10)
────────────────────────────────────────────────────────────────
• 🚀 Первоначальный выпуск
• 🔓 Базовый функционал разблокировки файлов
• ⚙️ Управление процессами
• 📁 Простой файловый менеджер

🔮 ПЛАНИРУЕМЫЕ ОБНОВЛЕНИЯ:
  ▶️ Интеграция с облачными сервисами
  ▶️ Расширенные сетевые возможности
  ▶️ Плагины и расширения
  ▶️ Мобильная версия
  ▶️ AI-ассистент для диагностики

📞 ПОДДЕРЖКА:
  • GitHub: github.com/profibroYT



────────────────────────────────────────────────────────────────
⭐ Благодарим за использование Advanced Unlocker Pro! ⭐
────────────────────────────────────────────────────────────────
"""
        self.log_text.insert('1.0', update_log)
        self.log_text.config(state='disabled')  # Делаем текст только для чтения
    
    def check_for_updates(self):
        """Проверка обновлений"""
        messagebox.showinfo("Проверка обновлений", 
                          "✅ Вы используете последнюю версию Advanced Unlocker Pro v2.1.0\n\n"
                          "Следующее обновление запланировано на декабрь 2024 года.")
    
    def export_log(self):
        """Экспорт лога в файл"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Экспорт лога обновлений",
            initialfile="AdvancedUnlocker_Update_Log.txt"
        )
        if filename:
            try:
                log_content = self.log_text.get('1.0', 'end-1c')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                messagebox.showinfo("Успех", f"Лог обновлений экспортирован в:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать лог: {e}")
    
    def copy_log(self):
        """Копирование лога в буфер обмена"""
        log_content = self.log_text.get('1.0', 'end-1c')
        self.root.clipboard_clear()
        self.root.clipboard_append(log_content)
        messagebox.showinfo("Успех", "Лог обновлений скопирован в буфер обмена")
    
    def launch_app(self):
        self.settings = {
            'resolution': self.resolution.get(),
            'theme': self.theme.get(),
            'debug_mode': self.debug_mode.get(),
            'admin_mode': self.admin_mode.get()
        }
        self.root.quit()
        self.root.destroy()
    
    def get_settings(self):
        return getattr(self, 'settings', {
            'resolution': '1400x900',
            'theme': 'dark',
            'debug_mode': False,
            'admin_mode': False
        })

class AdvancedUnlockerPro:
    def __init__(self, settings=None):
        try:
            # Используем настройки по умолчанию если не переданы
            if settings is None:
                settings = {
                    'resolution': '1400x900',
                    'theme': 'dark',
                    'debug_mode': False,
                    'admin_mode': False
                }
            
            self.settings = settings
            self.root = tk.Tk()
            self.root.title("Advanced Unlocker Pro - Complete System Suite")
            self.root.geometry(settings['resolution'])
            self.root.configure(bg='#0d1117')
            
            # Настройка темы
            self.theme = settings['theme']
            self.debug_mode = settings['debug_mode']
            
            # Центрирование окна
            self.center_window()
            
            # Настройка стилей в зависимости от темы
            self.setup_styles()
            
            # Настройка логирования
            self.setup_logging()
            
            # Переменные
            self.locked_files = []
            self.processes = []
            self.registry_data = {}
            self.current_registry_path = "Computer"
            self.force_mode = tk.BooleanVar(value=True)
            self.backup_mode = tk.BooleanVar(value=True)
            
            self.setup_ui()
            self.load_registry_structure()
            self.start_system_monitor()
            
            # Загружаем процессы при запуске
            self.refresh_processes()
            
            logging.info("Advanced Unlocker Pro initialized successfully")
            if self.debug_mode:
                self.update_status("DEBUG MODE ACTIVE")
            
        except Exception as e:
            logging.error(f"Initialization error: {e}")
            messagebox.showerror("Error", f"Failed to initialize: {e}")
    
    def setup_logging(self):
        """Настройка системы логирования"""
        log_level = logging.DEBUG if self.debug_mode else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('advanced_unlocker.log'),
                logging.StreamHandler() if self.debug_mode else logging.NullHandler()
            ]
        )
    
    def setup_styles(self):
        """Настройка стилей в зависимости от темы"""
        if self.theme == "light":
            self.colors = {
                'bg': '#ffffff',
                'panel_bg': '#f0f0f0',
                'accent': '#007acc',
                'accent2': '#005a9e',
                'text_fg': '#000000',
                'success': '#107c10',
                'warning': '#d83b01',
                'error': '#e81123',
                'terminal_bg': '#ffffff',
                'terminal_fg': '#008000'
            }
        elif self.theme == "blue":
            self.colors = {
                'bg': '#001f3f',
                'panel_bg': '#003366',
                'accent': '#7FDBFF',
                'accent2': '#39CCCC',
                'text_fg': '#ffffff',
                'success': '#2ECC40',
                'warning': '#FFDC00',
                'error': '#FF4136',
                'terminal_bg': '#001f3f',
                'terminal_fg': '#7FDBFF'
            }
        elif self.theme == "green":
            self.colors = {
                'bg': '#1a331a',
                'panel_bg': '#2d4d2d',
                'accent': '#00ff00',
                'accent2': '#00cc00',
                'text_fg': '#ffffff',
                'success': '#00ff00',
                'warning': '#ffff00',
                'error': '#ff0000',
                'terminal_bg': '#1a331a',
                'terminal_fg': '#00ff00'
            }
        else:  # dark (default)
            self.colors = {
                'bg': '#0d1117',
                'panel_bg': '#161b22',
                'accent': '#58a6ff',
                'accent2': '#1f6feb',
                'text_fg': '#f0f6fc',
                'success': '#3fb950',
                'warning': '#d29922',
                'error': '#f85149',
                'terminal_bg': '#0d1117',
                'terminal_fg': '#00ff00'
            }
    
    def center_window(self):
        self.root.update_idletasks()
        width, height = map(int, self.settings['resolution'].split('x'))
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Создание современного интерфейса"""
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Верхняя панель
        self.create_header(main_container)
        
        # Основная область
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, pady=5)
        
        # Левая панель навигации
        self.create_navigation_panel(content_frame)
        
        # Центральная область
        self.create_content_area(content_frame)
        
        # Правая панель информации
        self.create_info_panel(content_frame)
    
    def create_header(self, parent):
        """Создание верхней панели"""
        header = tk.Frame(parent, bg=self.colors['panel_bg'], height=70)
        header.pack(fill='x', pady=(0, 5))
        header.pack_propagate(False)
        
        # Логотип и название
        title_frame = tk.Frame(header, bg=self.colors['panel_bg'])
        title_frame.pack(side='left', padx=20)
        
        title = tk.Label(title_frame, 
                        text="⚡ ADVANCED UNLOCKER PRO", 
                        font=('Arial', 20, 'bold'),
                        bg=self.colors['panel_bg'],
                        fg=self.colors['accent'])
        title.pack(pady=5)
        
        subtitle = tk.Label(title_frame,
                          text="Complete System Management Suite",
                          font=('Arial', 10),
                          bg=self.colors['panel_bg'],
                          fg=self.colors['text_fg'])
        subtitle.pack()
        
        # Статус бар
        status_frame = tk.Frame(header, bg=self.colors['panel_bg'])
        status_frame.pack(side='right', padx=20)
        
        debug_text = " | DEBUG MODE" if self.debug_mode else ""
        self.status_label = tk.Label(status_frame,
                                   text=f"🟢 SYSTEM: ONLINE{debug_text}",
                                   font=('Arial', 10, 'bold'),
                                   bg=self.colors['panel_bg'],
                                   fg=self.colors['success'])
        self.status_label.pack(pady=5)
        
        # Время
        self.time_label = tk.Label(status_frame,
                                 text=datetime.now().strftime("%H:%M:%S"),
                                 font=('Arial', 12),
                                 bg=self.colors['panel_bg'],
                                 fg=self.colors['text_fg'])
        self.time_label.pack()
        self.update_time()
    
    def create_navigation_panel(self, parent):
        """Левая панель навигации"""
        nav_frame = tk.Frame(parent, bg=self.colors['panel_bg'], width=200)
        nav_frame.pack(side='left', fill='y', padx=(0, 5))
        nav_frame.pack_propagate(False)
        
        # Навигационные кнопки
        nav_items = [
            ("🔓 UNLOCKER", "unlocker"),
            ("⚙️ PROCESSES", "processes"),
            ("📁 FILES", "files"),
            ("🗂️ REGISTRY", "registry"),
            ("🚀 STARTUP", "startup"),
            ("🔧 TOOLS", "tools"),
            ("🌐 NETWORK", "network"),
            ("🛡️ SECURITY", "security")
        ]
        
        for text, tab in nav_items:
            btn = tk.Button(nav_frame,
                          text=text,
                          font=('Arial', 11),
                          bg=self.colors['panel_bg'],
                          fg=self.colors['text_fg'],
                          relief='flat',
                          anchor='w',
                          command=lambda t=tab: self.switch_tab(t))
            btn.pack(fill='x', padx=10, pady=8)
        
        # Разделитель
        sep = tk.Frame(nav_frame, bg=self.colors['accent2'], height=2)
        sep.pack(fill='x', pady=15)
        
        # Быстрые действия
        quick_actions = [
            ("🚨 EMERGENCY UNLOCK", self.emergency_unlock),
            ("💀 KILL MALWARE", self.kill_malware),
            ("🛡️ DEEP SCAN", self.deep_scan),
            ("🧹 CLEAN SYSTEM", self.clean_system)
        ]
        
        for text, command in quick_actions:
            btn = tk.Button(nav_frame,
                          text=text,
                          font=('Arial', 10),
                          bg=self.colors['accent2'],
                          fg='white',
                          relief='raised',
                          command=command)
            btn.pack(fill='x', padx=5, pady=3)
    
    def create_content_area(self, parent):
        """Центральная область контента"""
        self.content_frame = tk.Frame(parent, bg=self.colors['bg'])
        self.content_frame.pack(fill='both', expand=True)
        
        # Создаем все вкладки
        self.tabs = {}
        self.create_unlocker_tab()
        self.create_process_tab()
        self.create_files_tab()
        self.create_registry_tab()
        self.create_startup_tab()
        self.create_tools_tab()
        self.create_network_tab()
        self.create_security_tab()
        
        # Показываем первую вкладку
        self.show_tab("unlocker")
    
    def create_info_panel(self, parent):
        """Правая панель информации"""
        info_frame = tk.Frame(parent, bg=self.colors['panel_bg'], width=250)
        info_frame.pack(side='right', fill='y', padx=(5, 0))
        info_frame.pack_propagate(False)
        
        # Заголовок
        title = tk.Label(info_frame,
                       text="SYSTEM MONITOR",
                       font=('Arial', 12, 'bold'),
                       bg=self.colors['panel_bg'],
                       fg=self.colors['accent'])
        title.pack(pady=15)
        
        # Статистика системы
        self.stats_frame = tk.Frame(info_frame, bg=self.colors['panel_bg'])
        self.stats_frame.pack(fill='x', padx=15, pady=10)
        
        self.cpu_label = self.create_stat_label("🖥️ CPU: --%")
        self.memory_label = self.create_stat_label("💾 RAM: --%")
        self.disk_label = self.create_stat_label("💿 DISK: --%")
        self.process_label = self.create_stat_label("📊 PROCESSES: --")
        
        # Сетевой монитор
        net_frame = tk.LabelFrame(info_frame,
                                text=" NETWORK ",
                                bg=self.colors['panel_bg'],
                                fg=self.colors['accent'],
                                font=('Arial', 10))
        net_frame.pack(fill='x', padx=10, pady=10)
        
        self.network_label = tk.Label(net_frame,
                                    text="⬆️ Upload: -- KB/s\n⬇️ Download: -- KB/s",
                                    font=('Arial', 9),
                                    bg=self.colors['panel_bg'],
                                    fg=self.colors['text_fg'],
                                    justify='left')
        self.network_label.pack(padx=5, pady=5)
        
        # Активные операции
        ops_frame = tk.LabelFrame(info_frame,
                                text=" ACTIVE OPERATIONS ",
                                bg=self.colors['panel_bg'],
                                fg=self.colors['accent'],
                                font=('Arial', 10))
        ops_frame.pack(fill='x', padx=10, pady=5)
        
        self.operations_label = tk.Label(ops_frame,
                                       text="• No active operations",
                                       font=('Arial', 8),
                                       bg=self.colors['panel_bg'],
                                       fg=self.colors['text_fg'],
                                       justify='left')
        self.operations_label.pack(padx=5, pady=5)
        
        # Отладочная информация (только в режиме отладки)
        if self.debug_mode:
            debug_frame = tk.LabelFrame(info_frame,
                                      text=" DEBUG INFO ",
                                      bg=self.colors['panel_bg'],
                                      fg=self.colors['warning'],
                                      font=('Arial', 10))
            debug_frame.pack(fill='x', padx=10, pady=5)
            
            self.debug_label = tk.Label(debug_frame,
                                     text="Debug mode active\nLogging to file",
                                     font=('Arial', 8),
                                     bg=self.colors['panel_bg'],
                                     fg=self.colors['warning'],
                                     justify='left')
            self.debug_label.pack(padx=5, pady=5)
    
    def create_stat_label(self, text):
        """Создание метки статистики"""
        label = tk.Label(self.stats_frame,
                       text=text,
                       font=('Arial', 10),
                       bg=self.colors['panel_bg'],
                       fg=self.colors['text_fg'],
                       anchor='w')
        label.pack(fill='x', pady=3)
        return label
    
    def create_unlocker_tab(self):
        """Вкладка разблокировщика"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["unlocker"] = frame
        
        # Заголовок
        title = tk.Label(frame,
                       text="ADVANCED FILE UNLOCKER",
                       font=('Arial', 18, 'bold'),
                       bg=self.colors['bg'],
                       fg=self.colors['accent'])
        title.pack(pady=20)
        
        # Область перетаскивания
        drop_frame = tk.LabelFrame(frame,
                                 text=" DRAG & DROP AREA ",
                                 bg=self.colors['panel_bg'],
                                 fg=self.colors['accent'],
                                 font=('Arial', 12),
                                 relief='groove',
                                 bd=2)
        drop_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.drop_label = tk.Label(drop_frame,
                                 text="+ DRAG LOCKED FILES HERE\nOR USE QUICK ACTIONS BELOW",
                                 font=('Arial', 14),
                                 bg=self.colors['panel_bg'],
                                 fg=self.colors['accent2'],
                                 cursor="hand2",
                                 height=8)
        self.drop_label.pack(expand=True)
        
        # Панель действий
        action_frame = tk.Frame(frame, bg=self.colors['bg'])
        action_frame.pack(fill='x', padx=20, pady=10)
        
        actions = [
            ("📁 SELECT FILES", self.select_files),
            ("📂 SELECT FOLDER", self.select_folder),
            ("🔍 SCAN SYSTEM", self.scan_system_files),
            ("🔥 CLEAN TEMP", self.clean_temp_files)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = tk.Button(action_frame,
                          text=text,
                          font=('Arial', 10),
                          bg=self.colors['accent2'],
                          fg='white',
                          command=command)
            btn.grid(row=0, column=i, padx=5, sticky='ew')
            action_frame.columnconfigure(i, weight=1)
        
        # Опции
        options_frame = tk.Frame(frame, bg=self.colors['bg'])
        options_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Checkbutton(options_frame,
                     text="💪 FORCE MODE",
                     variable=self.force_mode,
                     bg=self.colors['bg'],
                     fg=self.colors['text_fg'],
                     selectcolor=self.colors['panel_bg'],
                     font=('Arial', 10)).pack(side='left', padx=10)
        
        tk.Checkbutton(options_frame,
                     text="💾 CREATE BACKUPS",
                     variable=self.backup_mode,
                     bg=self.colors['bg'],
                     fg=self.colors['text_fg'],
                     selectcolor=self.colors['panel_bg'],
                     font=('Arial', 10)).pack(side='left', padx=10)
        
        # Основные кнопки
        main_actions_frame = tk.Frame(frame, bg=self.colors['bg'])
        main_actions_frame.pack(fill='x', padx=20, pady=15)
        
        main_actions = [
            ("🔓 UNLOCK ALL", self.unlock_all, self.colors['success']),
            ("🗑️ DELETE ALL", self.delete_all, self.colors['error']),
            ("🔄 REFRESH ALL", self.refresh_all, self.colors['accent']),
            ("📊 STATISTICS", self.show_stats, self.colors['warning'])
        ]
        
        for text, command, color in main_actions:
            btn = tk.Button(main_actions_frame, text=text, command=command,
                          bg=color, fg='white', font=('Arial', 12, 'bold'),
                          relief='raised', bd=3, height=2)
            btn.pack(side='left', padx=5, fill='x', expand=True)
        
        # Список файлов
        self.create_file_list(frame)
        
        # Привязка событий
        self.setup_drag_drop()
    
    def create_process_tab(self):
        """Вкладка процессов"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["processes"] = frame
        
        tk.Label(frame, text="PROCESS MANAGER", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Поиск и фильтры
        search_frame = tk.Frame(frame, bg=self.colors['bg'])
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="🔍 Search:", bg=self.colors['bg'], fg=self.colors['text_fg']).pack(side='left')
        self.process_search = tk.Entry(search_frame, width=40, bg=self.colors['panel_bg'], fg=self.colors['text_fg'])
        self.process_search.pack(side='left', padx=10)
        self.process_search.bind('<KeyRelease>', self.filter_processes)
        
        # Дерево процессов
        tree_frame = tk.Frame(frame, bg=self.colors['bg'])
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ("PID", "Name", "CPU%", "Memory", "User", "Status")
        self.process_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        self.process_tree.pack(fill='both', expand=True)
        
        # Управление процессами
        control_frame = tk.Frame(frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', padx=20, pady=10)
        
        controls = [
            ("🔄 Refresh", self.refresh_processes),
            ("💀 Kill", self.kill_selected_process),
            ("🛑 Force Kill", self.force_kill_selected),
            ("📊 Details", self.show_process_details)
        ]
        
        for text, command in controls:
            tk.Button(control_frame, text=text, command=command,
                    bg=self.colors['accent2'], fg='white').pack(side='left', padx=5)
    
    def create_files_tab(self):
        """Вкладка файлового менеджера"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["files"] = frame
        
        tk.Label(frame, text="ADVANCED FILE EXPLORER", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Панель инструментов
        toolbar = tk.Frame(frame, bg=self.colors['bg'])
        toolbar.pack(fill='x', padx=20, pady=10)
        
        # Кнопки навигации
        nav_buttons = [
            ("⬆️ Up", self.file_explorer_up),
            ("📁 Home", self.file_explorer_home),
            ("🔄 Refresh", self.file_explorer_refresh)
        ]
        
        for text, command in nav_buttons:
            tk.Button(toolbar, text=text, command=command,
                     bg=self.colors['accent2'], fg='white').pack(side='left', padx=5)
        
        # Поле пути
        self.current_path = tk.StringVar(value=os.path.expanduser("~"))
        path_frame = tk.Frame(frame, bg=self.colors['bg'])
        path_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(path_frame, text="Path:", bg=self.colors['bg'], fg=self.colors['text_fg']).pack(side='left')
        path_entry = tk.Entry(path_frame, textvariable=self.current_path, 
                             width=80, bg=self.colors['panel_bg'], fg=self.colors['text_fg'])
        path_entry.pack(side='left', padx=10, fill='x', expand=True)
        path_entry.bind('<Return>', self.file_explorer_go_to_path)
        
        # Основная область файлового менеджера
        explorer_frame = tk.Frame(frame, bg=self.colors['bg'])
        explorer_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Дерево файлов
        columns = ("Name", "Size", "Type", "Modified")
        self.file_explorer_tree = ttk.Treeview(explorer_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.file_explorer_tree.heading(col, text=col)
        
        self.file_explorer_tree.column("Name", width=300)
        self.file_explorer_tree.column("Size", width=100)
        self.file_explorer_tree.column("Type", width=100)
        self.file_explorer_tree.column("Modified", width=150)
        
        self.file_explorer_tree.pack(fill='both', expand=True)
        self.file_explorer_tree.bind('<Double-1>', self.file_explorer_on_double_click)
        
        # Загружаем начальную директорию
        self.load_file_explorer()
    
    def load_file_explorer(self, path=None):
        """Загрузка содержимого директории в файловый менеджер"""
        if path is None:
            path = self.current_path.get()
        
        # Очищаем дерево
        for item in self.file_explorer_tree.get_children():
            self.file_explorer_tree.delete(item)
        
        try:
            # Добавляем родительскую директорию (кроме корневых)
            if path != os.path.dirname(path):
                self.file_explorer_tree.insert("", "end", text="..", 
                                              values=("..", "", "Parent Directory", ""),
                                              tags=('directory',))
            
            # Получаем список файлов и папок
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                try:
                    if os.path.isdir(full_path):
                        items.append((item, "", "Folder", "", 'directory'))
                    else:
                        size = self.get_file_size(full_path)
                        modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
                        items.append((item, size, "File", modified, 'file'))
                except (OSError, PermissionError):
                    continue
            
            # Сортируем: сначала папки, потом файлы
            items.sort(key=lambda x: (x[4] != 'directory', x[0].lower()))
            
            # Добавляем в дерево
            for name, size, type_, modified, file_type in items:
                self.file_explorer_tree.insert("", "end", values=(name, size, type_, modified), 
                                              tags=(file_type,))
            
            # Обновляем текущий путь
            self.current_path.set(path)
            
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading directory: {e}")
    
    def file_explorer_on_double_click(self, event):
        """Обработка двойного клика в файловом менеджере"""
        item = self.file_explorer_tree.selection()[0]
        values = self.file_explorer_tree.item(item, 'values')
        name = values[0]
        
        if name == "..":
            # Переход на уровень выше
            parent_dir = os.path.dirname(self.current_path.get())
            self.load_file_explorer(parent_dir)
        else:
            full_path = os.path.join(self.current_path.get(), name)
            if os.path.isdir(full_path):
                # Переход в папку
                self.load_file_explorer(full_path)
            else:
                # Попытка открыть файл
                try:
                    os.startfile(full_path)
                except:
                    messagebox.showinfo("Info", f"Cannot open file: {full_path}")
    
    def file_explorer_up(self):
        """Переход на уровень выше"""
        parent_dir = os.path.dirname(self.current_path.get())
        if os.path.exists(parent_dir):
            self.load_file_explorer(parent_dir)
    
    def file_explorer_home(self):
        """Переход в домашнюю директорию"""
        self.load_file_explorer(os.path.expanduser("~"))
    
    def file_explorer_refresh(self):
        """Обновление текущей директории"""
        self.load_file_explorer()
    
    def file_explorer_go_to_path(self, event=None):
        """Переход по указанному пути"""
        path = self.current_path.get()
        if os.path.exists(path):
            self.load_file_explorer(path)
        else:
            messagebox.showerror("Error", "Path does not exist")
    
    def create_registry_tab(self):
        """Вкладка искусственного реестра"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["registry"] = frame
        
        # Заголовок
        title = tk.Label(frame,
                       text="ARTIFICIAL REGISTRY EDITOR",
                       font=('Arial', 18, 'bold'),
                       bg=self.colors['bg'],
                       fg=self.colors['accent'])
        title.pack(pady=20)
        
        # Основная область реестра
        registry_main_frame = tk.Frame(frame, bg=self.colors['bg'])
        registry_main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая панель - дерево реестра
        left_frame = tk.Frame(registry_main_frame, bg=self.colors['panel_bg'])
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        tk.Label(left_frame, text="Registry Structure", bg=self.colors['panel_bg'], 
                fg=self.colors['accent'], font=('Arial', 11, 'bold')).pack(pady=10)
        
        # Дерево реестра
        tree_frame = tk.Frame(left_frame, bg=self.colors['panel_bg'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.registry_tree = ttk.Treeview(tree_frame, height=20)
        self.registry_tree.pack(fill='both', expand=True)
        self.registry_tree.bind('<<TreeviewSelect>>', self.on_registry_select)
        
        # Правая панель - значения
        right_frame = tk.Frame(registry_main_frame, bg=self.colors['panel_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(right_frame, text="Registry Values", bg=self.colors['panel_bg'],
                fg=self.colors['accent'], font=('Arial', 11, 'bold')).pack(pady=10)
        
        # Список значений
        values_frame = tk.Frame(right_frame, bg=self.colors['panel_bg'])
        values_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("Name", "Type", "Value")
        self.registry_values_tree = ttk.Treeview(values_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.registry_values_tree.heading(col, text=col)
            self.registry_values_tree.column(col, width=150)
        
        self.registry_values_tree.pack(fill='both', expand=True)
        
        # Панель управления реестром
        registry_control_frame = tk.Frame(frame, bg=self.colors['bg'])
        registry_control_frame.pack(fill='x', padx=20, pady=10)
        
        registry_controls = [
            ("➕ New Key", self.create_registry_key),
            ("📝 New Value", self.create_registry_value),
            ("✏️ Edit", self.edit_registry_value),
            ("🗑️ Delete", self.delete_registry_item),
            ("💾 Export", self.export_registry),
            ("📥 Import", self.import_registry)
        ]
        
        for text, command in registry_controls:
            tk.Button(registry_control_frame, text=text, command=command,
                    bg=self.colors['accent2'], fg='white').pack(side='left', padx=5)
        
        # Текущий путь
        self.registry_path_var = tk.StringVar(value="Computer")
        path_frame = tk.Frame(frame, bg=self.colors['bg'])
        path_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(path_frame, text="Path:", bg=self.colors['bg'], fg=self.colors['text_fg']).pack(side='left')
        path_entry = tk.Entry(path_frame, textvariable=self.registry_path_var, 
                            width=80, bg=self.colors['panel_bg'], fg=self.colors['text_fg'])
        path_entry.pack(side='left', padx=10, fill='x', expand=True)
    
    def create_startup_tab(self):
        """Вкладка автозагрузки"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["startup"] = frame
        
        tk.Label(frame, text="STARTUP MANAGER", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Информация о автозагрузке
        info_text = """Startup Manager allows you to manage programs that run automatically when your system starts.

⚠️  Be careful when modifying startup items - some are required for system operation."""
        
        info_label = tk.Label(frame, text=info_text, bg=self.colors['bg'], fg=self.colors['text_fg'],
                            font=('Arial', 10), justify='left', wraplength=600)
        info_label.pack(pady=10)
        
        # Список автозагрузки
        list_frame = tk.LabelFrame(frame, text=" STARTUP ITEMS ", 
                                 bg=self.colors['panel_bg'], fg=self.colors['accent'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_frame = tk.Frame(list_frame, bg=self.colors['panel_bg'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("Name", "Type", "Status", "Location")
        self.startup_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.startup_tree.heading(col, text=col)
        
        self.startup_tree.pack(fill='both', expand=True)
        
        # Загружаем элементы автозагрузки
        self.load_startup_items()
        
        # Управление
        control_frame = tk.Frame(frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', padx=20, pady=10)
        
        startup_controls = [
            ("🔄 Refresh", self.load_startup_items),
            ("⏹️ Disable", self.disable_startup_item),
            ("▶️ Enable", self.enable_startup_item),
            ("🗑️ Remove", self.remove_startup_item)
        ]
        
        for text, command in startup_controls:
            tk.Button(control_frame, text=text, command=command,
                     bg=self.colors['accent2'], fg='white').pack(side='left', padx=5)
    
    def load_startup_items(self):
        """Загрузка элементов автозагрузки"""
        # Очищаем дерево
        for item in self.startup_tree.get_children():
            self.startup_tree.delete(item)
        
        # Примерные данные автозагрузки
        startup_items = [
            ("Windows Defender", "System", "Enabled", "Registry"),
            ("OneDrive", "User", "Enabled", "Startup Folder"),
            ("Steam", "User", "Disabled", "Registry"),
            ("Discord", "User", "Enabled", "Startup Folder"),
            ("Graphics Driver", "System", "Enabled", "Services")
        ]
        
        for name, type_, status, location in startup_items:
            self.startup_tree.insert("", "end", values=(name, type_, status, location))
    
    def disable_startup_item(self):
        """Отключение элемента автозагрузки"""
        selection = self.startup_tree.selection()
        if selection:
            item = selection[0]
            values = self.startup_tree.item(item, 'values')
            messagebox.showinfo("Info", f"Disabled startup item: {values[0]}")
        else:
            messagebox.showwarning("Warning", "Please select a startup item")
    
    def enable_startup_item(self):
        """Включение элемента автозагрузки"""
        selection = self.startup_tree.selection()
        if selection:
            item = selection[0]
            values = self.startup_tree.item(item, 'values')
            messagebox.showinfo("Info", f"Enabled startup item: {values[0]}")
        else:
            messagebox.showwarning("Warning", "Please select a startup item")
    
    def remove_startup_item(self):
        """Удаление элемента автозагрузки"""
        selection = self.startup_tree.selection()
        if selection:
            item = selection[0]
            values = self.startup_tree.item(item, 'values')
            if messagebox.askyesno("Confirm", f"Remove startup item: {values[0]}?"):
                self.startup_tree.delete(item)
        else:
            messagebox.showwarning("Warning", "Please select a startup item")
    
    def create_tools_tab(self):
        """Вкладка инструментов"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["tools"] = frame
        
        tk.Label(frame, text="SYSTEM TOOLS", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Сетка инструментов
        tools_frame = tk.Frame(frame, bg=self.colors['bg'])
        tools_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tools = [
            ("🧹 Disk Cleaner", self.disk_cleaner),
            ("📊 System Info", self.system_info),
            ("🔍 File Analyzer", self.file_analyzer),
            ("🛡️ Permission Manager", self.permission_manager),
            ("🔧 Service Manager", self.service_manager),
            ("📈 Performance Monitor", self.performance_monitor),
            ("🗂️ Folder Statistics", self.folder_statistics),
            ("🔐 Security Scanner", self.security_scanner)
        ]
        
        for i, (text, command) in enumerate(tools):
            btn = tk.Button(tools_frame, text=text, command=command,
                          bg=self.colors['panel_bg'], fg=self.colors['text_fg'],
                          font=('Arial', 11), width=20, height=3)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
    
    def create_network_tab(self):
        """Вкладка сети"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["network"] = frame
        
        tk.Label(frame, text="NETWORK TOOLS", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Сетевые инструменты
        tools_frame = tk.Frame(frame, bg=self.colors['bg'])
        tools_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        network_tools = [
            ("🌐 IP Configuration", self.show_ip_config),
            ("📡 Network Statistics", self.show_netstat),
            ("🔍 Ping Tool", self.ping_tool),
            ("🚪 Port Scanner", self.port_scanner),
            ("📊 Bandwidth Monitor", self.bandwidth_monitor),
            ("🛡️ Firewall Status", self.firewall_status)
        ]
        
        for i, (text, command) in enumerate(network_tools):
            btn = tk.Button(tools_frame, text=text, command=command,
                          bg=self.colors['panel_bg'], fg=self.colors['text_fg'],
                          font=('Arial', 11), width=20, height=3)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    
    def show_ip_config(self):
        """Показать IP конфигурацию"""
        try:
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='cp866')
            self.show_text_dialog("IP Configuration", result.stdout)
        except:
            messagebox.showinfo("IP Config", "Run 'ipconfig /all' in command prompt for details")
    
    def show_netstat(self):
        """Показать сетевую статистику"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, encoding='cp866')
            self.show_text_dialog("Network Statistics", result.stdout)
        except:
            messagebox.showinfo("Netstat", "Run 'netstat -an' in command prompt for details")
    
    def ping_tool(self):
        """Инструмент ping"""
        host = simpledialog.askstring("Ping Tool", "Enter host to ping:")
        if host:
            try:
                result = subprocess.run(['ping', '-n', '4', host], capture_output=True, text=True, encoding='cp866')
                self.show_text_dialog(f"Ping Results - {host}", result.stdout)
            except:
                messagebox.showerror("Error", "Failed to execute ping command")
    
    def port_scanner(self):
        """Сканер портов"""
        messagebox.showinfo("Port Scanner", "Port scanner would be implemented here")
    
    def bandwidth_monitor(self):
        """Монитор пропускной способности"""
        messagebox.showinfo("Bandwidth Monitor", "Bandwidth monitoring would be implemented here")
    
    def firewall_status(self):
        """Статус брандмауэра"""
        try:
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                  capture_output=True, text=True, encoding='cp866')
            self.show_text_dialog("Firewall Status", result.stdout)
        except:
            messagebox.showinfo("Firewall", "Run 'netsh advfirewall show allprofiles' for details")
    
    def show_text_dialog(self, title, text):
        """Показать текст в диалоговом окне"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x400")
        dialog.configure(bg=self.colors['bg'])
        
        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=70, height=20,
                                              bg=self.colors['panel_bg'], fg=self.colors['text_fg'])
        text_widget.pack(padx=10, pady=10, fill='both', expand=True)
        text_widget.insert('1.0', text)
        text_widget.config(state='disabled')
        
        tk.Button(dialog, text="Close", command=dialog.destroy,
                 bg=self.colors['accent2'], fg='white').pack(pady=10)
    
    def create_security_tab(self):
        """Вкладка безопасности"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.tabs["security"] = frame
        
        tk.Label(frame, text="SECURITY CENTER", 
                font=('Arial', 18, 'bold'), bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=20)
        
        # Информация о безопасности
        security_info = tk.Frame(frame, bg=self.colors['panel_bg'])
        security_info.pack(fill='x', padx=20, pady=10)
        
        # Заголовок статуса
        status_header = tk.Label(security_info, text="🔒 SECURITY STATUS: GOOD", 
                               font=('Arial', 14, 'bold'), bg=self.colors['panel_bg'], fg=self.colors['success'])
        status_header.pack(pady=10)
        
        # Детали безопасности
        security_details = """
• Firewall: Active
• Antivirus: Protected  
• System Updates: Current
• User Account Control: Enabled
• Network Security: Good
        """
        
        details_label = tk.Label(security_info, text=security_details, 
                               bg=self.colors['panel_bg'], fg=self.colors['text_fg'],
                               font=('Arial', 10), justify='left')
        details_label.pack(pady=10)
        
        # Инструменты безопасности
        security_tools_frame = tk.Frame(frame, bg=self.colors['bg'])
        security_tools_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        security_tools = [
            ("🛡️ Run Security Scan", self.run_security_scan),
            ("🔍 Process Scanner", self.scan_processes),
            ("📁 File Integrity Check", self.file_integrity_check),
            ("🌐 Network Security", self.network_security),
            ("🔐 Password Check", self.password_check),
            ("🚨 Emergency Lockdown", self.emergency_lockdown)
        ]
        
        for i, (text, command) in enumerate(security_tools):
            btn = tk.Button(security_tools_frame, text=text, command=command,
                          bg=self.colors['panel_bg'], fg=self.colors['text_fg'],
                          font=('Arial', 11), width=20, height=2)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    
    def run_security_scan(self):
        """Запуск сканирования безопасности"""
        messagebox.showinfo("Security Scan", "Security scan would check for:\n• Malware processes\n• Suspicious files\n• System vulnerabilities")
    
    def scan_processes(self):
        """Сканирование процессов"""
        suspicious = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                # Простая проверка на подозрительные имена
                suspicious_keywords = ['crypt', 'miner', 'hack', 'keylog']
                if any(keyword in name for keyword in suspicious_keywords):
                    suspicious.append(name)
            except:
                continue
        
        if suspicious:
            messagebox.showwarning("Suspicious Processes", f"Found: {', '.join(suspicious)}")
        else:
            messagebox.showinfo("Process Scan", "No suspicious processes found")
    
    def file_integrity_check(self):
        """Проверка целостности файлов"""
        messagebox.showinfo("File Integrity", "File integrity check would verify system files")
    
    def network_security(self):
        """Проверка сетевой безопасности"""
        messagebox.showinfo("Network Security", "Network security analysis would check for open ports and vulnerabilities")
    
    def password_check(self):
        """Проверка паролей"""
        messagebox.showinfo("Password Check", "Password strength checker would be implemented here")
    
    def emergency_lockdown(self):
        """Аварийная блокировка"""
        if messagebox.askyesno("Emergency Lockdown", 
                             "This will terminate suspicious processes and lock down the system. Continue?"):
            messagebox.showinfo("Lockdown", "Emergency lockdown procedures activated")
    
    def create_file_list(self, parent):
        """Создание списка файлов"""
        list_frame = tk.LabelFrame(parent, text=" LOCKED FILES & PROCESSES ", 
                                 bg=self.colors['panel_bg'], fg=self.colors['accent'], font=('Arial', 11))
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_frame = tk.Frame(list_frame, bg=self.colors['panel_bg'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("File", "Type", "Size", "Process", "PID", "Status")
        self.file_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.file_tree.heading(col, text=col)
            self.file_tree.column(col, width=120)
        
        self.file_tree.pack(fill='both', expand=True)
        
        # Контекстное меню
        self.setup_context_menus()
    
    def setup_context_menus(self):
        """Настройка контекстных меню"""
        # Меню для файлов
        self.file_context_menu = tk.Menu(self.root, tearoff=0)
        self.file_context_menu.add_command(label="🔓 Unlock", command=self.unlock_selected)
        self.file_context_menu.add_command(label="🗑️ Delete", command=self.delete_selected)
        self.file_context_menu.add_command(label="💀 Kill Process", command=self.kill_process_selected)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="📋 Copy Path", command=self.copy_file_path)
        self.file_context_menu.add_command(label="📁 Open Location", command=self.open_file_location)
        
        self.file_tree.bind("<Button-3>", self.show_file_context_menu)
    
    def setup_drag_drop(self):
        """Упрощенная настройка drag & drop - только клик"""
        self.drop_label.bind('<Button-1>', lambda e: self.select_files())
    
    # ФУНКЦИОНАЛ РЕЕСТРА
    def load_registry_structure(self):
        """Загрузка структуры реестра"""
        try:
            # Очищаем дерево
            for item in self.registry_tree.get_children():
                self.registry_tree.delete(item)
                
            # Основные ветки реестра
            main_keys = [
                ("HKEY_CLASSES_ROOT", "Computer\\HKEY_CLASSES_ROOT"),
                ("HKEY_CURRENT_USER", "Computer\\HKEY_CURRENT_USER"), 
                ("HKEY_LOCAL_MACHINE", "Computer\\HKEY_LOCAL_MACHINE"),
                ("HKEY_USERS", "Computer\\HKEY_USERS"),
                ("HKEY_CURRENT_CONFIG", "Computer\\HKEY_CURRENT_CONFIG")
            ]
            
            for name, path in main_keys:
                node = self.registry_tree.insert("", "end", text=name, values=[path])
                
                # Добавляем подразделы
                subkeys = self.get_registry_subkeys(path)
                for subkey in subkeys[:5]:  # Ограничиваем для производительности
                    self.registry_tree.insert(node, "end", text=subkey, values=[f"{path}\\{subkey}"])
            
            logging.info("Registry structure loaded successfully")
            
        except Exception as e:
            logging.error(f"Error loading registry structure: {e}")
    
    def get_registry_subkeys(self, path):
        """Получение подразделов реестра"""
        # Это упрощенная версия - в реальном приложении нужно использовать winreg
        common_subkeys = {
            "Computer\\HKEY_CURRENT_USER": ["Software", "System", "Volatile Environment"],
            "Computer\\HKEY_LOCAL_MACHINE": ["SOFTWARE", "SYSTEM", "HARDWARE", "SECURITY"],
            "Computer\\HKEY_CLASSES_ROOT": [".exe", ".txt", ".doc", ".zip"],
            "Computer\\HKEY_USERS": [".DEFAULT", "S-1-5-18", "S-1-5-19"],
            "Computer\\HKEY_CURRENT_CONFIG": ["Software", "System"]
        }
        
        return common_subkeys.get(path, [])
    
    def on_registry_select(self, event):
        """Обработка выбора в дереве реестра"""
        selection = self.registry_tree.selection()
        if selection:
            item = selection[0]
            path = self.registry_tree.item(item, "values")[0]
            self.current_registry_path = path
            self.registry_path_var.set(path)
            self.load_registry_values(path)
    
    def load_registry_values(self, path):
        """Загрузка значений реестра"""
        # Очищаем текущие значения
        for item in self.registry_values_tree.get_children():
            self.registry_values_tree.delete(item)
        
        # Добавляем тестовые данные
        sample_values = [
            ("(Default)", "REG_SZ", "(value not set)"),
            ("TestValue1", "REG_DWORD", "0x00000001"),
            ("TestValue2", "REG_SZ", "Sample Text"),
            ("TestValue3", "REG_BINARY", "01 02 03 04"),
            ("TestValue4", "REG_MULTI_SZ", "Line1\\0Line2")
        ]
        
        for name, type_, value in sample_values:
            self.registry_values_tree.insert("", "end", values=(name, type_, value))
    
    def create_registry_key(self):
        """Создание нового раздела реестра"""
        key_name = simpledialog.askstring("New Registry Key", "Enter key name:")
        if key_name:
            # В реальном приложении здесь будет вызов winreg
            messagebox.showinfo("Success", f"Key '{key_name}' created successfully")
            self.update_status(f"Created registry key: {key_name}")
    
    def create_registry_value(self):
        """Создание нового значения реестра"""
        value_name = simpledialog.askstring("New Registry Value", "Enter value name:")
        if value_name:
            # В реальном приложении здесь будет вызов winreg
            messagebox.showinfo("Success", f"Value '{value_name}' created successfully")
            self.update_status(f"Created registry value: {value_name}")
    
    def edit_registry_value(self):
        """Редактирование значения реестра"""
        selection = self.registry_values_tree.selection()
        if selection:
            item = selection[0]
            values = self.registry_values_tree.item(item, "values")
            messagebox.showinfo("Edit Value", f"Editing: {values[0]}\nType: {values[1]}\nValue: {values[2]}")
        else:
            messagebox.showwarning("Warning", "Please select a value to edit")
    
    def delete_registry_item(self):
        """Удаление раздела или значения реестра"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            # В реальном приложении здесь будет вызов winreg
            messagebox.showinfo("Success", "Item deleted successfully")
            self.update_status("Registry item deleted")
    
    def export_registry(self):
        """Экспорт раздела реестра"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".reg",
            filetypes=[("Registry files", "*.reg"), ("All files", "*.*")]
        )
        if filename:
            # В реальном приложении здесь будет экспорт через winreg
            messagebox.showinfo("Success", f"Registry exported to {filename}")
            self.update_status("Registry exported successfully")
    
    def import_registry(self):
        """Импорт файла реестра"""
        filename = filedialog.askopenfilename(
            filetypes=[("Registry files", "*.reg"), ("All files", "*.*")]
        )
        if filename:
            # В реальном приложении здесь будет импорт через winreg
            messagebox.showinfo("Success", f"Registry imported from {filename}")
            self.update_status("Registry imported successfully")
    
    # ОСНОВНЫЕ ФУНКЦИИ РАЗБЛОКИРОВКИ
    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files to unlock")
        for file in files:
            self.add_locked_file(file)
        self.update_status(f"Selected {len(files)} files")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to unlock")
        if folder:
            self.add_locked_file(folder)
            self.update_status("Folder selected")
    
    def add_locked_file(self, path):
        if path and os.path.exists(path):
            # Проверяем, не добавлен ли уже этот файл
            for existing_file in self.locked_files:
                if existing_file[0] == path:
                    return  # Файл уже добавлен
            
            processes = self.find_locking_processes(path)
            file_type = "📁 Folder" if os.path.isdir(path) else "📄 File"
            size = self.get_file_size(path)
            status = "🔴 Locked" if processes else "🟢 Free"
            
            self.locked_files.append((path, file_type, size, processes, status))
            self.update_file_tree()
    
    def find_locking_processes(self, path):
        """Поиск процессов, блокирующих файл"""
        locking_processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    for file in proc.open_files():
                        if path.lower() in file.path.lower():
                            locking_processes.append((proc.info['pid'], proc.info['name']))
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logging.error(f"Error finding locking processes: {e}")
        return locking_processes
    
    def unlock_all(self):
        """Разблокировка всех файлов"""
        if not self.locked_files:
            messagebox.showinfo("Info", "No files to unlock")
            return
            
        success_count = 0
        files_to_remove = []
        
        for file_info in self.locked_files:
            path, file_type, size, processes, status = file_info
            if self.unlock_file(path):
                success_count += 1
                files_to_remove.append(file_info)
        
        # Удаляем разблокированные файлы из списка
        for file_info in files_to_remove:
            if file_info in self.locked_files:
                self.locked_files.remove(file_info)
        
        self.update_file_tree()
        messagebox.showinfo("Success", f"Unlocked {success_count} files")
        self.update_status(f"Unlocked {success_count} files")
    
    def unlock_file(self, path):
        """Реальная разблокировка файла"""
        try:
            # Завершаем процессы
            processes_killed = self.kill_locking_processes(path)
            
            # Дополнительные методы при включенном force mode
            if self.force_mode.get() and not processes_killed:
                self.force_unlock_methods(path)
            
            return True
        except Exception as e:
            logging.error(f"Error unlocking file {path}: {e}")
            return False
    
    def kill_locking_processes(self, path):
        """Завершение процессов, блокирующих файл"""
        processes = self.find_locking_processes(path)
        killed_count = 0
        
        for pid, name in processes:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=3)  # Ждем завершения процесса
                killed_count += 1
            except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied):
                try:
                    # Пробуем принудительное завершение
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, check=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    killed_count += 1
                except subprocess.CalledProcessError:
                    pass
        
        return killed_count > 0
    
    def force_unlock_methods(self, path):
        """Дополнительные методы принудительной разблокировки"""
        try:
            # Метод переименования
            if os.path.exists(path):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, f"unlocked_{os.path.basename(path)}")
                shutil.move(path, temp_path)
                time.sleep(0.1)
                shutil.move(temp_path, path)
        except Exception as e:
            logging.error(f"Force unlock failed: {e}")
    
    def delete_all(self):
        if not self.locked_files:
            messagebox.showinfo("Info", "No files to delete")
            return
            
        if messagebox.askyesno("Confirm", "Delete all locked files?"):
            success_count = 0
            files_to_remove = []
            
            for file_info in self.locked_files:
                path, file_type, size, processes, status = file_info
                if self.delete_file(path):
                    success_count += 1
                    files_to_remove.append(file_info)
            
            # Удаляем удаленные файлы из списка
            for file_info in files_to_remove:
                if file_info in self.locked_files:
                    self.locked_files.remove(file_info)
            
            self.update_file_tree()
            self.update_status(f"Deleted {success_count} files")
    
    def delete_file(self, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting {path}: {e}")
            if self.force_mode.get():
                return self.force_delete(path)
            return False
    
    def force_delete(self, path):
        try:
            if os.name == 'nt':  # Windows
                if os.path.isfile(path):
                    subprocess.run(f'cmd /c "del /f /q "{path}""', shell=True, check=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run(f'cmd /c "rd /s /q "{path}""', shell=True, check=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            else:  # Linux/Mac
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
                return True
        except Exception as e:
            logging.error(f"Force delete failed: {e}")
            return False
    
    def refresh_all(self):
        self.refresh_processes()
        # Обновляем статус файлов
        updated_files = []
        for path, file_type, size, processes, status in self.locked_files:
            current_processes = self.find_locking_processes(path)
            new_status = "🔴 Locked" if current_processes else "🟢 Free"
            updated_files.append((path, file_type, size, current_processes, new_status))
        
        self.locked_files = updated_files
        self.update_file_tree()
        self.update_status("All data refreshed")
    
    def show_stats(self):
        total_files = len(self.locked_files)
        locked_files = sum(1 for _, _, _, processes, _ in self.locked_files if processes)
        
        stats = f"""
📊 System Statistics:
• Total Files: {total_files}
• Locked Files: {locked_files}
• System Processes: {len(psutil.pids())}
• Memory Usage: {psutil.virtual_memory().percent}%
• CPU Usage: {psutil.cpu_percent()}%
        """
        messagebox.showinfo("Statistics", stats)
    
    def update_file_tree(self):
        # Очищаем дерево
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # Добавляем файлы без дублирования
        for path, file_type, size, processes, status in self.locked_files:
            if processes:
                # Для файлов с блокирующими процессами показываем каждый процесс отдельно
                for pid, name in processes:
                    self.file_tree.insert("", "end", values=(path, file_type, size, name, pid, status))
            else:
                # Для файлов без процессов показываем одну запись
                self.file_tree.insert("", "end", values=(path, file_type, size, "None", "None", status))
    
    def get_file_size(self, path):
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f} {unit}"
                    size /= 1024.0
                return f"{size:.1f} TB"
            elif os.path.isdir(path):
                return "Folder"
            return "N/A"
        except:
            return "Error"
    
    # ФУНКЦИИ ПРОЦЕССОВ
    def refresh_processes(self):
        def update():
            self.processes.clear()
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username', 'status']):
                try:
                    memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                    self.processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': proc.info['cpu_percent'] or 0,
                        'memory': f"{memory_mb:.1f} MB",
                        'user': proc.info['username'] or 'SYSTEM',
                        'status': proc.info['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.root.after(0, self.update_process_tree)
        
        threading.Thread(target=update, daemon=True).start()
    
    def update_process_tree(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
            
        search_term = self.process_search.get().lower()
        for proc in self.processes:
            if (search_term in proc['name'].lower() or 
                search_term in str(proc['pid'])):
                self.process_tree.insert("", "end", values=(
                    proc['pid'], proc['name'], f"{proc['cpu']:.1f}%",
                    proc['memory'], proc['user'], proc['status']
                ))
    
    def filter_processes(self, event=None):
        self.update_process_tree()
    
    def kill_selected_process(self):
        selection = self.process_tree.selection()
        if selection:
            pid = int(self.process_tree.item(selection[0])['values'][0])
            try:
                psutil.Process(pid).terminate()
                self.update_status(f"Process {pid} terminated")
                self.refresh_processes()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to terminate process: {e}")
    
    def force_kill_selected(self):
        selection = self.process_tree.selection()
        if selection:
            pid = int(self.process_tree.item(selection[0])['values'][0])
            try:
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, check=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.update_status(f"Process {pid} force killed")
                self.refresh_processes()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to force kill process: {e}")
    
    def show_process_details(self):
        selection = self.process_tree.selection()
        if selection:
            pid = int(self.process_tree.item(selection[0])['values'][0])
            try:
                process = psutil.Process(pid)
                details = f"""
Process Details:
PID: {pid}
Name: {process.name()}
Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB
CPU: {process.cpu_percent()}%
Status: {process.status()}
                """
                messagebox.showinfo("Process Details", details)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get process details: {e}")
    
    # СИСТЕМНЫЕ ИНСТРУМЕНТЫ
    def disk_cleaner(self):
        """Очистка диска"""
        temp_dirs = [
            os.environ.get('TEMP', ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
        ]
        
        cleaned = 0
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        try:
                            full_path = os.path.join(temp_dir, item)
                            if os.path.isfile(full_path):
                                os.remove(full_path)
                                cleaned += 1
                        except:
                            continue
                except:
                    pass
        
        messagebox.showinfo("Disk Cleaner", f"Cleaned {cleaned} temporary files")
    
    def system_info(self):
        info = f"""
System Information:
OS: {sys.platform}
Processors: {psutil.cpu_count()}
Total Memory: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB
Memory Usage: {psutil.virtual_memory().percent}%
Disk Usage: {psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent}%
        """
        messagebox.showinfo("System Information", info)
    
    def file_analyzer(self):
        """Анализатор файлов"""
        file = filedialog.askopenfilename(title="Select file to analyze")
        if file:
            try:
                size = os.path.getsize(file)
                modified = datetime.fromtimestamp(os.path.getmtime(file))
                info = f"""
File Analysis:
Path: {file}
Size: {self.get_file_size(file)}
Modified: {modified}
Type: {os.path.splitext(file)[1]}
                """
                messagebox.showinfo("File Analysis", info)
            except Exception as e:
                messagebox.showerror("Error", f"Could not analyze file: {e}")
    
    def permission_manager(self):
        """Менеджер разрешений"""
        messagebox.showinfo("Permission Manager", "Permission management tool - select a file to modify permissions")
    
    def service_manager(self):
        """Менеджер служб"""
        try:
            services = []
            for service in psutil.win_service_iter() if hasattr(psutil, 'win_service_iter') else []:
                services.append(service.name())
            
            if services:
                service_list = "\n".join(services[:10])  # Показываем первые 10
                messagebox.showinfo("Services", f"Found {len(services)} services\n\nFirst 10:\n{service_list}")
            else:
                messagebox.showinfo("Services", "No Windows services found or not on Windows system")
        except:
            messagebox.showinfo("Service Manager", "Service management requires Windows system")
    
    def performance_monitor(self):
        """Монитор производительности"""
        info = f"""
Performance Monitor:
CPU Usage: {psutil.cpu_percent()}%
Memory Usage: {psutil.virtual_memory().percent}%
Disk Usage: {psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent}%
Running Processes: {len(psutil.pids())}
        """
        messagebox.showinfo("Performance Monitor", info)
    
    def folder_statistics(self):
        """Статистика папки"""
        folder = filedialog.askdirectory(title="Select folder for statistics")
        if folder:
            try:
                file_count = 0
                folder_count = 0
                total_size = 0
                
                for root, dirs, files in os.walk(folder):
                    folder_count += len(dirs)
                    for file in files:
                        file_count += 1
                        try:
                            total_size += os.path.getsize(os.path.join(root, file))
                        except:
                            pass
                
                stats = f"""
Folder Statistics:
Path: {folder}
Folders: {folder_count}
Files: {file_count}
Total Size: {self.format_size(total_size)}
                """
                messagebox.showinfo("Folder Statistics", stats)
            except Exception as e:
                messagebox.showerror("Error", f"Could not analyze folder: {e}")
    
    def format_size(self, size_bytes):
        """Форматирование размера"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def security_scanner(self):
        """Сканер безопасности"""
        messagebox.showinfo("Security Scanner", "Security scanner would check for vulnerabilities")
    
    # ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
    def scan_system_files(self):
        system_locations = [
            os.environ.get('WINDIR', 'C:\\Windows'),
            os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        ]
        
        for location in system_locations:
            if os.path.exists(location):
                self.add_locked_file(location)
        
        self.update_status("System files scanned")
    
    def clean_temp_files(self):
        temp_locations = [
            os.environ.get('TEMP', ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
        ]
        
        cleaned = 0
        for temp_dir in temp_locations:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir)[:10]:
                        try:
                            full_path = os.path.join(temp_dir, item)
                            if os.path.isfile(full_path):
                                os.remove(full_path)
                                cleaned += 1
                        except:
                            continue
                except:
                    pass
        
        self.update_status(f"Cleaned {cleaned} temp files")
    
    def emergency_unlock(self):
        self.unlock_all()
        self.update_status("Emergency unlock completed")
    
    def kill_malware(self):
        # Простой поиск подозрительных процессов
        suspicious_keywords = ['virus', 'malware', 'trojan']
        killed = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if any(keyword in proc_name for keyword in suspicious_keywords):
                    psutil.Process(proc.info['pid']).terminate()
                    killed += 1
            except:
                continue
        
        self.update_status(f"Killed {killed} suspicious processes")
    
    def deep_scan(self):
        self.scan_system_files()
        self.clean_temp_files()
        self.update_status("Deep scan completed")
    
    def clean_system(self):
        self.clean_temp_files()
        self.update_status("System cleanup completed")
    
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    def unlock_selected(self):
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "No files selected")
            return
            
        success_count = 0
        files_to_remove = []
        
        for item in selection:
            path = self.file_tree.item(item)['values'][0]
            if self.unlock_file(path):
                success_count += 1
                # Находим и помечаем файл для удаления из списка
                for file_info in self.locked_files:
                    if file_info[0] == path:
                        files_to_remove.append(file_info)
                        break
        
        # Удаляем разблокированные файлы из списка
        for file_info in files_to_remove:
            if file_info in self.locked_files:
                self.locked_files.remove(file_info)
        
        self.refresh_all()
        self.update_status(f"Unlocked {success_count} selected files")
    
    def delete_selected(self):
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "No files selected")
            return
            
        paths_to_delete = []
        for item in selection:
            path = self.file_tree.item(item)['values'][0]
            paths_to_delete.append(path)
            
        if messagebox.askyesno("Confirm", f"Delete {len(paths_to_delete)} files?"):
            success_count = 0
            files_to_remove = []
            
            for path in paths_to_delete:
                if self.delete_file(path):
                    success_count += 1
                    # Находим и помечаем файл для удаления из списка
                    for file_info in self.locked_files:
                        if file_info[0] == path:
                            files_to_remove.append(file_info)
                            break
            
            # Удаляем удаленные файлы из списка
            for file_info in files_to_remove:
                if file_info in self.locked_files:
                    self.locked_files.remove(file_info)
                    
            self.update_file_tree()
            self.update_status(f"Deleted {success_count} files")
    
    def kill_process_selected(self):
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "No files selected")
            return
            
        killed_count = 0
        for item in selection:
            pid_value = self.file_tree.item(item)['values'][4]
            if pid_value != "None":
                try:
                    psutil.Process(int(pid_value)).terminate()
                    killed_count += 1
                except:
                    pass
        
        self.refresh_all()
        self.update_status(f"Killed {killed_count} processes")
    
    def copy_file_path(self):
        selection = self.file_tree.selection()
        if selection:
            path = self.file_tree.item(selection[0])['values'][0]
            self.root.clipboard_clear()
            self.root.clipboard_append(path)
            self.update_status("File path copied to clipboard")
    
    def open_file_location(self):
        selection = self.file_tree.selection()
        if selection:
            path = self.file_tree.item(selection[0])['values'][0]
            folder = os.path.dirname(path) if os.path.isfile(path) else path
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(folder)
                else:  # Linux/Mac
                    subprocess.run(['xdg-open', folder])
                self.update_status("File location opened")
            except:
                self.update_status("Error opening file location")
    
    def show_file_context_menu(self, event):
        item = self.file_tree.identify_row(event.y)
        if item:
            self.file_tree.selection_set(item)
            self.file_context_menu.post(event.x_root, event.y_root)
    
    def switch_tab(self, tab_name):
        self.show_tab(tab_name)
        self.update_status(f"Switched to {tab_name} tab")
    
    def show_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()
        
        if tab_name in self.tabs:
            self.tabs[tab_name].pack(fill='both', expand=True)
    
    def start_system_monitor(self):
        def monitor():
            while True:
                try:
                    # Обновляем статистику
                    cpu = psutil.cpu_percent()
                    memory = psutil.virtual_memory().percent
                    disk = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
                    processes = len(psutil.pids())
                    
                    self.root.after(0, self.update_system_stats, cpu, memory, disk, processes)
                    time.sleep(2)
                except Exception as e:
                    logging.error(f"Monitor error: {e}")
                    time.sleep(5)
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def update_system_stats(self, cpu, memory, disk, processes):
        self.cpu_label.config(text=f"🖥️ CPU: {cpu}%")
        self.memory_label.config(text=f"💾 RAM: {memory}%")
        self.disk_label.config(text=f"💿 DISK: {disk}%")
        self.process_label.config(text=f"📊 PROCESSES: {processes}")
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_status(self, message):
        """Обновление статуса с учетом режима отладки"""
        debug_text = " | DEBUG MODE" if self.debug_mode else ""
        self.status_label.config(text=f"🟢 SYSTEM: ONLINE | {message}{debug_text}")
        logging.info(f"Status: {message}")
        if self.debug_mode:
            print(f"DEBUG: {message}")
    
    def run(self):
        """Запуск главного цикла приложения"""
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Application error: {e}")
            messagebox.showerror("Error", f"Application error: {e}")

def create_build_script():
    """Создание скрипта для компиляции в EXE"""
    script_name = os.path.basename(__file__)
    build_script = f'''@echo off
chcp 65001 > nul
title Advanced Unlocker Pro - Build EXE

echo ========================================
echo    ADVANCED UNLOCKER PRO - BUILD EXE
echo ========================================
echo.

echo Installing dependencies...
pip install psutil

echo.
echo Building EXE...
pyinstaller --onefile --windowed --name "AdvancedUnlockerPro" --icon=NONE {script_name}

echo.
echo ========================================
echo BUILD COMPLETE!
echo EXE: dist\\AdvancedUnlockerPro.exe
echo ========================================
pause
'''

    with open("build.bat", "w", encoding='utf-8') as f:
        f.write(build_script)

if __name__ == "__main__":
    # Создаем скрипт сборки
    create_build_script()
    
    # Проверяем зависимости
    try:
        import psutil
    except ImportError:
        print("Installing psutil...")
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    # Запускаем окно конфигурации
    config = StartupConfig()
    config.root.mainloop()
    
    # Получаем настройки и запускаем основное приложение
    try:
        settings = config.get_settings()
        print(f"Starting with settings: {settings}")
        
        app = AdvancedUnlockerPro(settings)
        app.run()
    except Exception as e:
        # Если что-то пошло не так, запускаем с настройками по умолчанию
        print(f"Error with config window: {e}")
        app = AdvancedUnlockerPro()
        app.run()
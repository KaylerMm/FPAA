from typing import List, Tuple
from abc import ABC, abstractmethod
import random
import time
import threading

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class Grid:
    def __init__(self, rows: int, cols: int, data: List[List[int]]):
        self.rows = rows
        self.cols = cols
        self.data = data
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def get_value(self, x: int, y: int) -> int:
        if self.is_valid_position(x, y):
            return self.data[x][y]
        return -1
    
    def set_value(self, x: int, y: int, value: int):
        if self.is_valid_position(x, y):
            self.data[x][y] = value
    
    def display(self):
        for row in self.data:
            print(' '.join(map(str, row)))
        print()
    
    def find_next_navigable_cell(self) -> Tuple[int, int]:
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] == 0:
                    return (i, j)
        return (-1, -1)


class FloodFillStrategy(ABC):
    @abstractmethod
    def fill(self, grid: Grid, start_x: int, start_y: int, color: int):
        pass


class RecursiveFloodFill(FloodFillStrategy):
    def fill(self, grid: Grid, start_x: int, start_y: int, color: int):
        if not grid.is_valid_position(start_x, start_y):
            return
        
        if grid.get_value(start_x, start_y) != 0:
            return
        
        grid.set_value(start_x, start_y, color)
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            self.fill(grid, start_x + dx, start_y + dy, color)


class IterativeFloodFill(FloodFillStrategy):
    def fill(self, grid: Grid, start_x: int, start_y: int, color: int):
        if not grid.is_valid_position(start_x, start_y):
            return
        
        if grid.get_value(start_x, start_y) != 0:
            return
        
        stack = [(start_x, start_y)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while stack:
            x, y = stack.pop()
            
            if not grid.is_valid_position(x, y) or grid.get_value(x, y) != 0:
                continue
            
            grid.set_value(x, y, color)
            
            for dx, dy in directions:
                stack.append((x + dx, y + dy))


class TerrainMapper:
    def __init__(self, strategy: FloodFillStrategy):
        self.strategy = strategy
        self.current_color = 2
    
    def fill_region(self, grid: Grid, start_x: int, start_y: int):
        self.strategy.fill(grid, start_x, start_y, self.current_color)
        self.current_color += 1
    
    def map_all_regions(self, grid: Grid):
        while True:
            next_x, next_y = grid.find_next_navigable_cell()
            if next_x == -1:
                break
            
            print(f"Preenchendo região iniciando em ({next_x}, {next_y}) com cor {self.current_color}")
            self.fill_region(grid, next_x, next_y)
            grid.display()


class GridInputHandler:
    @staticmethod
    def get_grid_dimensions() -> Tuple[int, int]:
        try:
            rows = int(input("Digite o número de linhas: "))
            cols = int(input("Digite o número de colunas: "))
            
            if rows <= 0 or cols <= 0:
                raise ValueError("As dimensões devem ser positivas")
            
            return rows, cols
        except ValueError as e:
            print(f"Erro: {e}")
            return GridInputHandler.get_grid_dimensions()
    
    @staticmethod
    def get_grid_data(rows: int, cols: int) -> List[List[int]]:
        print(f"Digite {rows} linhas com {cols} números inteiros cada (0=navegável, 1=obstáculo):")
        data = []
        
        for i in range(rows):
            try:
                row_input = input(f"Linha {i + 1}: ")
                row = [int(x) for x in row_input.split()]
                
                if len(row) != cols:
                    raise ValueError(f"A linha deve ter exatamente {cols} elementos")
                
                data.append(row)
            except ValueError as e:
                print(f"Erro: {e}")
                return GridInputHandler.get_grid_data(rows, cols)
        
        return data
    
    @staticmethod
    def get_starting_coordinates(rows: int, cols: int) -> Tuple[int, int]:
        try:
            x = int(input(f"Digite a linha inicial (0-{rows-1}): "))
            y = int(input(f"Digite a coluna inicial (0-{cols-1}): "))
            
            if x < 0 or x >= rows or y < 0 or y >= cols:
                raise ValueError("Coordenadas fora dos limites")
            
            return x, y
        except ValueError as e:
            print(f"Erro: {e}")
            return GridInputHandler.get_starting_coordinates(rows, cols)


class RandomGridGenerator:
    @staticmethod
    def generate_grid(rows: int, cols: int, obstacle_probability: float = 0.3) -> Grid:
        print(f"Gerando grade {rows}x{cols} com {obstacle_probability*100:.0f}% de obstáculos...")
        data = []
        for i in range(rows):
            row = []
            for j in range(cols):
                if random.random() < obstacle_probability:
                    row.append(1)
                else:
                    row.append(0)
            data.append(row)
        return Grid(rows, cols, data)


class AnimatedFloodFill(FloodFillStrategy):
    def __init__(self, gui_callback=None, delay=0.1):
        self.gui_callback = gui_callback
        self.delay = delay
    
    def fill(self, grid: Grid, start_x: int, start_y: int, color: int):
        if not grid.is_valid_position(start_x, start_y):
            return
        
        if grid.get_value(start_x, start_y) != 0:
            return
        
        stack = [(start_x, start_y)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while stack:
            x, y = stack.pop()
            
            if not grid.is_valid_position(x, y) or grid.get_value(x, y) != 0:
                continue
            
            grid.set_value(x, y, color)
            
            if self.gui_callback:
                self.gui_callback(x, y, color)
                time.sleep(self.delay)
            
            for dx, dy in directions:
                stack.append((x + dx, y + dy))


class FloodFillGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FloodFill - Terrain Mapping Visualizer")
        self.root.geometry("800x600")
        
        self.grid = None
        self.canvas = None
        self.cell_size = 30
        self.colors = {
            0: "white",
            1: "black", 
            2: "red",
            3: "orange",
            4: "yellow",
            5: "green",
            6: "blue",
            7: "purple",
            8: "pink",
            9: "brown"
        }
        
        self.strategy = AnimatedFloodFill(self.update_cell, 0.05)
        self.mapper = TerrainMapper(self.strategy)
        self.is_running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Label(control_frame, text="Linhas:").grid(row=0, column=0, padx=5)
        self.rows_var = tk.StringVar(value="8")
        ttk.Entry(control_frame, textvariable=self.rows_var, width=5).grid(row=0, column=1, padx=5)
        
        ttk.Label(control_frame, text="Colunas:").grid(row=0, column=2, padx=5)
        self.cols_var = tk.StringVar(value="10")
        ttk.Entry(control_frame, textvariable=self.cols_var, width=5).grid(row=0, column=3, padx=5)
        
        ttk.Label(control_frame, text="% Obstáculos:").grid(row=0, column=4, padx=5)
        self.obstacle_var = tk.StringVar(value="30")
        ttk.Entry(control_frame, textvariable=self.obstacle_var, width=5).grid(row=0, column=5, padx=5)
        
        ttk.Button(control_frame, text="Gerar Grade Aleatória", 
                  command=self.generate_random_grid).grid(row=0, column=6, padx=5)
        
        ttk.Button(control_frame, text="Carregar Grade Exemplo", 
                  command=self.load_sample_grid).grid(row=0, column=7, padx=5)
        
        control_frame2 = ttk.Frame(self.root)
        control_frame2.pack(pady=5)
        
        ttk.Button(control_frame2, text="Iniciar FloodFill", 
                  command=self.start_flood_fill).grid(row=0, column=0, padx=5)
        
        ttk.Button(control_frame2, text="Resetar", 
                  command=self.reset_grid).grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame2, text="Limpar Seleção", 
                  command=self.clear_selection).grid(row=0, column=2, padx=5)
        
        legend_frame = ttk.LabelFrame(self.root, text="Legenda de Cores", padding=10)
        legend_frame.pack(pady=5)
        
        legend_colors = [
            ("0 - Branco (Navegável)", "white", "black"),
            ("1 - Preto (Obstáculo)", "black", "white"),
            ("2 - Vermelho", "red", "white"),
            ("3 - Laranja", "orange", "black"),
            ("4 - Amarelo", "yellow", "black"),
            ("5 - Verde", "green", "white")
        ]
        
        for i, (text, bg, fg) in enumerate(legend_colors):
            label = tk.Label(legend_frame, text=text, bg=bg, fg=fg, padx=10, pady=2)
            label.grid(row=0, column=i, padx=2)
        
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.status_var = tk.StringVar(value="Pronto - Gere uma grade para começar")
        status_label = ttk.Label(self.root, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        self.selected_cell = None
        self.load_sample_grid()
    
    def generate_random_grid(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            obstacle_prob = float(self.obstacle_var.get()) / 100
            
            if rows <= 0 or cols <= 0 or not (0 <= obstacle_prob <= 1):
                raise ValueError("Invalid parameters")
            
            self.grid = RandomGridGenerator.generate_grid(rows, cols, obstacle_prob)
            self.mapper = TerrainMapper(self.strategy)
            self.draw_grid()
            self.status_var.set(f"Grade aleatória {rows}x{cols} gerada com {obstacle_prob*100:.0f}% de obstáculos")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira parâmetros válidos")
    
    def load_sample_grid(self):
        sample_data = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0]
        ]
        self.grid = Grid(4, 5, sample_data)
        self.mapper = TerrainMapper(self.strategy)
        self.draw_grid()
        self.status_var.set("Grade de exemplo carregada - Clique em uma célula para iniciar o flood fill")
    
    def draw_grid(self):
        if self.canvas:
            self.canvas.destroy()
        
        canvas_width = self.grid.cols * self.cell_size
        canvas_height = self.grid.rows * self.cell_size
        
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg="gray")
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_cell_click)
        
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.draw_cell(i, j, self.grid.get_value(i, j))
    
    def draw_cell(self, row, col, value):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        color = self.colors.get(value, "gray")
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", width=1, 
                                   tags=f"cell_{row}_{col}")
        
        if value > 0:
            self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, 
                                  text=str(value), fill="white" if value == 1 else "black",
                                  font=("Arial", 8, "bold"), tags=f"text_{row}_{col}")
    
    def update_cell(self, row, col, color):
        if self.canvas:
            self.root.after(0, lambda: self.draw_cell(row, col, color))
            self.root.update()
    
    def on_cell_click(self, event):
        if self.is_running:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if self.grid and self.grid.is_valid_position(row, col):
            if self.grid.get_value(row, col) != 0:
                messagebox.showwarning("Seleção Inválida", 
                                     "Por favor, selecione uma célula navegável (branca, valor 0)")
                return
            
            self.selected_cell = (row, col)
            self.highlight_selected_cell(row, col)
            self.status_var.set(f"Célula ({row}, {col}) selecionada - Clique em 'Iniciar FloodFill' para começar")
    
    def highlight_selected_cell(self, row, col):
        self.canvas.delete("selection")
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3, tags="selection")
    
    def clear_selection(self):
        if self.canvas:
            self.canvas.delete("selection")
        self.selected_cell = None
        self.status_var.set("Seleção limpa - Clique em uma célula para selecionar a posição inicial")
    
    def start_flood_fill(self):
        if not self.grid or not self.selected_cell or self.is_running:
            if not self.selected_cell:
                messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma célula inicial primeiro")
            return
        
        self.is_running = True
        row, col = self.selected_cell
        
        def run_fill():
            try:
                self.status_var.set(f"Preenchendo região a partir de ({row}, {col})...")
                self.mapper.fill_region(self.grid, row, col)
                
                time.sleep(0.5)
                
                self.status_var.set("Mapeando todas as regiões restantes...")
                self.mapper.map_all_regions(self.grid)
                
                self.status_var.set("FloodFill concluído!")
            finally:
                self.is_running = False
        
        thread = threading.Thread(target=run_fill)
        thread.daemon = True
        thread.start()
    
    def reset_grid(self):
        if not self.is_running and self.grid:
            original_data = []
            for i in range(self.grid.rows):
                row = []
                for j in range(self.grid.cols):
                    value = self.grid.get_value(i, j)
                    if value > 1:
                        row.append(0)
                    else:
                        row.append(value)
                original_data.append(row)
            
            self.grid = Grid(self.grid.rows, self.grid.cols, original_data)
            self.mapper = TerrainMapper(self.strategy)
            self.draw_grid()
            self.clear_selection()
            self.status_var.set("Grade resetada - Clique em uma célula para iniciar o flood fill")
    
    def run(self):
        self.root.mainloop()


class FloodFillApp:
    def __init__(self):
        self.strategy = IterativeFloodFill()
        self.mapper = TerrainMapper(self.strategy)
    
    def create_sample_grid(self) -> Grid:
        sample_data = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0]
        ]
        return Grid(4, 5, sample_data)
    
    def run_sample(self):
        print("Executando demonstração de exemplo:")
        print("=" * 50)
        
        grid = self.create_sample_grid()
        
        print("Grade inicial:")
        grid.display()
        
        print("Iniciando flood fill da posição (0, 0)")
        self.mapper.fill_region(grid, 0, 0)
        grid.display()
        
        print("Mapeando todas as regiões restantes:")
        self.mapper.map_all_regions(grid)
        
        print("Grade final:")
        grid.display()
    
    def run_interactive(self):
        print("FloodFill Interativo - Mapeamento de Terreno")
        print("=" * 50)
        
        rows, cols = GridInputHandler.get_grid_dimensions()
        data = GridInputHandler.get_grid_data(rows, cols)
        start_x, start_y = GridInputHandler.get_starting_coordinates(rows, cols)
        
        grid = Grid(rows, cols, data)
        
        print("\nGrade inicial:")
        grid.display()
        
        print(f"Iniciando flood fill da posição ({start_x}, {start_y})")
        self.mapper.fill_region(grid, start_x, start_y)
        grid.display()
        
        print("Mapeando todas as regiões restantes:")
        self.mapper.map_all_regions(grid)
        
        print("Grade final:")
        grid.display()
    
    def run_random_demo(self):
        print("Demonstração de FloodFill com Grade Aleatória")
        print("=" * 50)
        
        try:
            rows = int(input("Digite o número de linhas (padrão 6): ") or "6")
            cols = int(input("Digite o número de colunas (padrão 8): ") or "8")
            obstacle_prob = float(input("Digite a porcentagem de obstáculos 0-100 (padrão 25): ") or "25") / 100
            
            if rows <= 0 or cols <= 0 or not (0 <= obstacle_prob <= 1):
                raise ValueError("Parâmetros inválidos")
                
        except ValueError:
            print("Usando valores padrão: grade 6x8 com 25% de obstáculos")
            rows, cols, obstacle_prob = 6, 8, 0.25
        
        grid = RandomGridGenerator.generate_grid(rows, cols, obstacle_prob)
        animated_strategy = AnimatedFloodFill(delay=0.1)
        mapper = TerrainMapper(animated_strategy)
        
        print("\nGrade aleatória gerada:")
        grid.display()
        
        print("Legenda de Cores:")
        print("0 - Branco (Terreno navegável)")
        print("1 - Preto (Obstáculo)")
        print("2 - Vermelho (Primeira região)")
        print("3 - Laranja (Segunda região)") 
        print("4 - Amarelo (Terceira região)")
        print("5+ - Cores adicionais\n")
        
        print("Iniciando flood fill automático...")
        mapper.map_all_regions(grid)
        
        print("Grade final com todas as regiões preenchidas:")
        grid.display()
    
    def run_gui(self):
        if not GUI_AVAILABLE:
            print("Erro: Interface gráfica não disponível. Módulo tkinter não encontrado.")
            print("Executando demonstração de exemplo...")
            self.run_sample()
            return
            
        gui = FloodFillGUI()
        gui.run()
    
    def run(self):
        print("Algoritmo FloodFill - Sistema de Mapeamento de Terreno")
        print("=" * 60)
        print("1. Executar demonstração de exemplo")
        print("2. Entrada interativa") 
        print("3. Demonstração de grade aleatória")
        if GUI_AVAILABLE:
            print("4. Interface gráfica")
        else:
            print("4. Interface gráfica (indisponível - tkinter não instalado)")
        
        choice = input("Escolha uma opção (1, 2, 3, ou 4): ").strip()
        
        if choice == "1":
            self.run_sample()
        elif choice == "2":
            self.run_interactive()
        elif choice == "3":
            self.run_random_demo()
        elif choice == "4":
            if GUI_AVAILABLE:
                self.run_gui()
            else:
                print("Interface gráfica não disponível. Executando demonstração de exemplo.")
                self.run_sample()
        else:
            print("Opção inválida. Executando demonstração de exemplo.")
            self.run_sample()


if __name__ == "__main__":
    app = FloodFillApp()
    app.run()
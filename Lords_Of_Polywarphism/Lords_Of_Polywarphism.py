import pygame
import sys
import random
from abc import ABC, abstractmethod

def get_world_size():
    while True:
        try:
            input_str = input("Oyun boyutunu girin (örneğin, 16x16 veya 8x8): ")
            rows, cols = map(int, input_str.split('x'))

            if 8 <= rows <= 32 and 8 <= cols <= 32:
                return rows, cols
            else:
                print("Geçersiz dünya boyutu. Lütfen 8 ile 32 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz bir değer girdiniz. Lütfen iki sayıyı 'x' işareti ile ayırarak girin.")


def draw_grid(window, rows, cols, window_size, players, available_positions):
    square_size = window_size // rows
    line_color = (255, 255, 255)  # Çizgileri beyaz renkte çiz

    # Satır çizgilerini çiz
    for i in range(1, rows):
        pygame.draw.line(window, line_color, (0, i * square_size), (window_size, i * square_size))

    # Sütun çizgilerini çiz
    for i in range(1, cols):
        pygame.draw.line(window, line_color, (i * square_size, 0), (i * square_size, window_size))

    # Karelerin ortasına beyaz nokta ekle
    for i in range(rows):
        for j in range(cols):
            if any(player['guard_position'] == (i, j) for player in players.values()):
                continue  # Bu nokta bir muhafızın altında, boş bırak
            if any(player['warrior_position'] == (i, j) for player in players.values()):
                continue
            pygame.draw.circle(window, line_color,(i * square_size + square_size // 2, j * square_size + square_size // 2), 3)

    # Savaşçı sembollerini çiz
    for player_id, player_info in players.items():
        warrior_position = player_info['warrior_position']
        if warrior_position:
            warrior_name = player_info['warrior_name']
            draw_warrior(window, warrior_position, square_size, player_info['color'], f"{warrior_name}{player_id}")


def place_guards(players, rows, cols):
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]

    for player in players:
        random_corner = random.choice(corners)
        players[player]['guard_position'] = random_corner  # Köşeden rastgele bir muhafız yerleştir
        corners.remove(random_corner)  # Aynı köşeyi bir daha seçilmemesi için listeden çıkar


def ask_for_fighter_choice(player_id):
    while True:
        try:
            choice = int(
                input(f"{player_id}. oyuncu, savaşçı seçin (1: Muhafız, 2: Okçu, 3: Topçu, 4: Atlı, 5: Sağlıkçı): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Geçersiz savaşçı seçimi. Lütfen 1 ile 5 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz bir değer girdiniz. Lütfen bir sayı girin.")


def ask_for_fighter_count(player_id):
    while True:
        try:
            count = int(input(f"{player_id}. oyuncu, kaç savaşçı seçeceksiniz? (0-2): "))
            if 0 <= count <= 2:
                return count
            elif count == 0:
                print()
                return count
            else:
                print("Geçersiz savaşçı sayısı. Lütfen 0 ile 2 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz bir değer girdiniz. Lütfen bir sayı girin.")


def ask_for_next_round():
    while True:
        user_input = input("Bir sonraki tura geçilsin mi? (evet/hayır): ").lower()
        if user_input == 'evet':
            return True
        elif user_input == 'hayır':
            sys.exit()
        else:
            print("Geçersiz giriş. Lütfen 'evet' veya 'hayır' olarak yanıt verin.")


def draw_warrior(screen, position, square_size, color, warrior_name):
    font = pygame.font.Font(None, 36)
    text = font.render(warrior_name, True, color)
    text_rect = text.get_rect(center=(position[0] * square_size + square_size // 2, 
    position[1] * square_size + square_size // 2))
    screen.blit(text, text_rect)


def place_potential_guards(players, rows, cols):
    potential_positions = []
    for player_id, player in players.items():
        guard_position = player['guard_position']
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    new_pos = (guard_position[0] + i, guard_position[1] + j, player_id)
                    if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
                        potential_positions.append(new_pos)
    return potential_positions


def get_valid_placement_guard_positions(player_id, rows, cols, guard_position):
    potential_positions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                new_pos = (guard_position[0] + i, guard_position[1] + j)
                if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
                    potential_positions.append(new_pos)
    return potential_positions


def get_valid_placement_warrior_positions(player_id, rows, cols, warrior_position):
    potential_warrior_positions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                new_pos = (warrior_position[1] + i, warrior_position[0] + j)
                if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
                    potential_warrior_positions.append(new_pos)
    return potential_warrior_positions


def place_potential_warriors(players, rows, cols):
    potential_warrior_positions = []
    for player_id, player in players.items():
        warrior_position = player['warrior_position']
        warrior_color = player['color']
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    if warrior_position:
                        new_pos = (warrior_position[1] + i, warrior_position[0] + j, player_id)
                        if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
                            potential_warrior_positions.append(new_pos)
    return potential_warrior_positions


def update_and_draw_potential_positions(screen, square_size, players, rows, cols):
    potential_warrior_positions = place_potential_warriors(players, rows, cols)

    # Potansiyel savaşçı pozisyonlarını ekrana çiz
    for player in players:
        for pos in potential_warrior_positions:
            player_id = pos[2]
            back_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170), 4: (242, 229, 111)}
            pygame.draw.rect(screen, back_color[player_id],(pos[1] * square_size, pos[0] * square_size, square_size, square_size))

    for player in players:
        guard_position = players[player]['guard_position']
        square_size = 640 // rows
        pygame.draw.rect(screen, players[player]['back_color'],(guard_position[1] * square_size, guard_position[0] * square_size, square_size, square_size))
        font = pygame.font.Font(None, 36)
        text = font.render(f"M{player}", True, players[player]['color'])
        screen.blit(text, (guard_position[1] * square_size + square_size // 2 - text.get_width() // 2,guard_position[0] * square_size + square_size // 2 - text.get_height() // 2))


def draw_resource_management(screen, players, rows):
    square_size = 640 // rows
    for i, player in enumerate(players, start=1):
        font = pygame.font.Font(None, 22)
        text = font.render(f"{i}. Oyuncu Kaynak: {players[player]['resources']}", True, players[player]['color'])
        source_position = (rows * square_size + 10, i * 40)
        screen.blit(text, source_position)


def update_resources(players, total_warriors):
    for player_id, player_info in players.items():  # Tur başlarında her oyuncunun kaynağına 10 kaynak ekle
        player_info['resources'] += 10

    for player_id, warrior_count in total_warriors.items():  # Her savaşçı için ek olarak 1 kaynak ekle
        players[player_id]['resources'] += 1
        players[player_id]['resources'] += warrior_count


def count_warriors(warriors_matrix):
    total_warriors = {}
    for row in warriors_matrix:
        for warrior in row:
            if warrior:
                player_id = warrior['player_id']
                total_warriors[player_id] = total_warriors.get(player_id, 0) + 1
    return total_warriors


def place_warrior_manually(player_id, players, warriors_matrix, available_positions):
    placed = False
    while not placed:
        try:
            y, x = map(int, input(f"{player_id}. oyuncu, savaşçıyı yerleştirmek istediğiniz konumu seçin (x y): ").split())
            x -= 1
            y -= 1
            if (x, y) in available_positions and warriors_matrix[x][y] is None:
                warrior_choice = ask_for_fighter_choice(player_id)
                if warrior_choice == 1:
                    warrior_name = "M"
                    player_info = players[player_id]
                    if player_info['resources'] >= 10:
                        players[player_id]['resources'] -= 10
                    else:
                        print("Yeterli kaynağınız yok. Muhafız yerleştiremezsiniz.")
                        continue
                elif warrior_choice == 2:
                    warrior_name = "O"
                    player_info = players[player_id]
                    if player_info['resources'] >= 20:
                        players[player_id]['resources'] -= 20
                    else:
                        print("Yeterli kaynağınız yok. Okçu yerleştiremezsiniz.")
                        continue
                elif warrior_choice == 3:
                    warrior_name = "T"
                    player_info = players[player_id]
                    if player_info['resources'] >= 50:
                        players[player_id]['resources'] -= 50
                    else:
                        print("Yeterli kaynağınız yok. Topçu yerleştiremezsiniz.")
                        continue
                elif warrior_choice == 4:
                    warrior_name = "A"
                    player_info = players[player_id]
                    if player_info['resources'] >= 30:
                        players[player_id]['resources'] -= 30
                    else:
                        print("Yeterli kaynağınız yok. Atlı yerleştiremezsiniz.")
                        continue
                else:
                    warrior_name = "S"
                    player_info = players[player_id]
                    if player_info['resources'] >= 10:
                        players[player_id]['resources'] -= 10
                    else:
                        print("Yeterli kaynağınız yok. Sağlıkçı yerleştiremezsiniz.")
                        continue
                players[player_id]['warrior_name'] = warrior_name
                players[player_id]['warrior_position'] = (x, y)
                warriors_matrix[x][y] = {'player_id': player_id,'player_name': players[player_id]['name'],'warrior_name': warrior_name,'color': players[player_id]['color']}
                available_positions.pop((x, y))
                placed = True
            else:
                print(
                    "Bu konum geçersiz veya başka bir savaşçı tarafından işgal edilmiş. Lütfen başka bir konum seçin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen x ve y koordinatlarını boşlukla ayırarak girin.")


def ai_place_warriors(player_id, players, rows, cols, valid_positions, warriors_matrix):
    # Muhtemel savaşçı pozisyonları
    potential_warrior_positions = []
    for row in range(rows):
        for col in range(cols):
            if (row, col) in valid_positions:
                potential_warrior_positions.append((row, col))

    # Savaşçıyı yerleştirilecek uygun pozisyonlar listesinden geçerli savaşçı pozisyonları
    current_warrior_positions = [player['warrior_position'] for player in players.values()]

    # Uygun pozisyonları güncel savaşçı pozisyonlarından filtreleme
    available_positions = [pos for pos in potential_warrior_positions if pos not in current_warrior_positions]

    # Rastgele bir savaşçı pozisyonu seç
    if available_positions:
        for pos in available_positions:
            x, y = pos
            adjacent_cells = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for adj_pos in adjacent_cells:
                adj_x, adj_y = adj_pos
                if 0 <= adj_x < rows and 0 <= adj_y < cols:
                    adj_warrior = warriors_matrix[adj_x][adj_y]
                    if adj_warrior and adj_warrior['player_id'] == player_id:
                        players[player_id]['warrior_position'] = (x, y)
                        players[player_id]['warrior_name'] = ("T")
                        warriors_matrix[x][y] = {'player_id': player_id, 'player_name': players[player_id]['name'], 'warrior_name': players[player_id]['warrior_name'], 'color': players[player_id]['color']}
                        return True

        random_position = random.choice(available_positions)
        y, x = random_position
        players[player_id]['warrior_name'] = "T"
        players[player_id]['warrior_position'] = (x, y)
        warriors_matrix[x][y] = {'player_id': player_id, 
        'player_name': players[player_id]['name'], 
        'warrior_name': "T", 'color': players[player_id]['color']}
        return True
    else:
        return False


def ask_for_ai_decision(player_id,players):
    decision = input(f"{player_id}. oyuncu, yapay zeka kullanılsın mı? (E/H): ")
    player_info = players[player_id]
    if decision == "E":
        if player_info['resources'] >= 50:
            players[player_id]['resources'] -= 50
        else:
            print("Yeterli kaynağınız yok. Sağlıkçı yerleştiremezsiniz.")
    return decision.upper() == "E"


class Savasci(ABC):
    def __init__(self, player_id, color, guard_position):
        self.player_id = player_id
        self.color = color
        self.guard_name = None
        self.guard_position = guard_position
        self.resource_cost = None
        self.health = None
        self.target_enemies = 3
        self.damage = None
        self.range_horizontal = None
        self.range_vertical = None
        self.range_diagonal = None

    @abstractmethod
    def draw(self, screen, square_size):
        pass

    def attack(self, enemies):
        pass


class Muhafiz(Savasci):
    def __init__(self, player_id, color, guard_position):
        super().__init__(player_id, color, guard_position)
        self.guard_name = "Muhafız"
        self.guard_position_symbol = "M"
        self.resource_cost = 10
        self.health = 80
        self.damage = 20
        self.range_horizontal = 1
        self.range_vertical = 1
        self.range_diagonal = 1

    def draw(self, screen, square_size, position):
        pygame.draw.rect(screen, self.color,
                         (position[0] * square_size, position[1] * square_size, square_size, square_size))
        draw_warrior(screen, position, square_size, self.color, self.guard_position_symbol)

    def attack(self, enemies, players):
        for enemy in enemies:
            enemy_x, enemy_y, enemy_player_id = enemy
            guard_x, guard_y = self.position

            if (abs(enemy_x - guard_x) <= self.range_horizontal and
                    abs(enemy_y - guard_y) <= self.range_vertical):
                players[enemy_player_id]['health'] += self.damage
                if players[enemy_player_id]['health'] <= 0:
                    del players[enemy_player_id]


class Okcu(Savasci):
    def __init__(self, player_id, color, guard_position):
        super().__init__(player_id, color, guard_position)
        self.guard_name = "Okçu"
        self.guard_position_symbol = "O"
        self.resource_cost = 20
        self.health = 30
        self.damage = 0.6
        self.range_horizontal = 2
        self.range_vertical = 2
        self.range_diagonal = 2

    def draw(self, screen, square_size, position):
        pygame.draw.rect(screen, self.color,(position[0] * square_size, position[1] * square_size, square_size, square_size))
        draw_warrior(screen, position, square_size, self.color, self.guard_position_symbol)

    def attack(self, enemies, players):
        for _ in range(3):
            max_health_enemy = max(enemies, key=lambda x: players[x[2]]['health'], default=None)
            if max_health_enemy:
                enemy_x, enemy_y, enemy_player_id = max_health_enemy
                archer_x, archer_y = self.position

                if (abs(enemy_x - archer_x) <= self.range_horizontal and abs(enemy_y - archer_y) <= self.range_vertical):
                    players[enemy_player_id]['health'] *= (1 + self.damage_percentage)
                    if players[enemy_player_id]['health'] <= 0:
                        del players[enemy_player_id]
                    enemies.remove(max_health_enemy)
                else:
                    break
            else:
                break


class Topcu(Savasci):
    def __init__(self, player_id, color, guard_position):
        super().__init__(player_id, color, guard_position)
        self.guard_name = "Topçu"
        self.guard_position_symbol = "T"
        self.resource_cost = 50
        self.health = 30
        self.damage = 100
        self.range_horizontal = 2
        self.range_vertical = 2
        self.range_diagonal = 0

    def draw(self, screen, square_size, position):
        pygame.draw.rect(screen, self.color,(position[0] * square_size, position[1] * square_size, square_size, square_size))
        draw_warrior(screen, position, square_size, self.color, self.guard_position_symbol)

    def attack(self, enemies, players):
        max_health_enemy = max(enemies, key=lambda x: players[x[2]]['health'], default=None)
        if max_health_enemy:
            enemy_x, enemy_y, enemy_player_id = max_health_enemy
            artillery_x, artillery_y = self.position

            if (abs(enemy_x - artillery_x) <= self.range_horizontal and abs(enemy_y - artillery_y) <= self.range_vertical):
                players[enemy_player_id]['health'] *= (1 + self.damage_percentage)
                if players[enemy_player_id]['health'] <= 0:
                    del players[enemy_player_id]
                enemies.remove(max_health_enemy)


class Atli(Savasci):
    def __init__(self, player_id, color, guard_position):
        super().__init__(player_id, color, guard_position)
        self.guard_name = "Atlı"
        self.guard_position_symbol = "A"
        self.resource_cost = 30
        self.health = 40
        self.damage = 30
        self.range_horizontal = 0
        self.range_vertical = 0
        self.range_diagonal = 3

    def draw(self, screen, square_size, position):
        pygame.draw.rect(screen, self.color,(position[0] * square_size, position[1] * square_size, square_size, square_size))
        draw_warrior(screen, position, square_size, self.color, self.guard_position_symbol)

    def attack(self, enemies, players):
        if len(enemies) >= 2:
            # Düşmanları kaynaklarına göre sırala
            enemies.sort(key=lambda x: players[x[2]]['resource'], reverse=True)

            # İlk iki düşmanı hedef al
            for enemy in enemies[:2]:
                enemy_x, enemy_y, enemy_player_id = enemy
                horseman_x, horseman_y = self.position

                # Çapraz menzilde mi kontrol et
                if (abs(enemy_x - horseman_x) <= self.range_diagonal and abs(enemy_y - horseman_y) <= self.range_diagonal and
                    (enemy_x != horseman_x or enemy_y != horseman_y)):
                    players[enemy_player_id]['health'] += self.damage
                    if players[enemy_player_id]['health'] <= 0:
                        del players[enemy_player_id]
                    enemies.remove(enemy)


class Saglikci(Savasci):
    def __init__(self, player_id, color, guard_position):
        super().__init__(player_id, color, guard_position)
        self.guard_name = "Sağlıkçı"
        self.guard_position_symbol = "S"
        self.resource_cost = 10
        self.health = 100
        self.damage = -50  # Can eklemek için negatif hasar kullanıyoruz
        self.range_horizontal = 0
        self.range_vertical = 2
        self.range_diagonal = 2

    def draw(self, screen, square_size, position):
        pygame.draw.rect(screen, self.color,(position[0] * square_size, position[1] * square_size, square_size, square_size))
        draw_warrior(screen, position, square_size, self.color, self.guard_position_symbol)

    def attack(self, allies, players):
        if allies:
            # En az cana sahip olan dost birliği bul
            min_health_ally = min(allies, key=lambda x: players[x[2]]['health'])
            ally_x, ally_y, ally_player_id = min_health_ally
            healer_x, healer_y = self.position

            # Menzilde mi kontrol et
            if (abs(ally_x - healer_x) <= self.range_horizontal and abs(ally_y - healer_y) <= self.range_vertical and
                (ally_x != healer_x or ally_y != healer_y)):
                players[ally_player_id]['health'] += self.damage


# Oyun ekranını oluştur
pygame.init()
width_height = (850, 640)
screen = pygame.display.set_mode((width_height))
pygame.display.set_caption("LORDS OF THE POLYWARPHISM")


def main():
    pygame.init()
    first_round = True  # İlk turu izlemek için bir bayrak

    while True:
        while True:
            try:
                num_players = int(input("Oyuncu sayısını girin (1-4): "))
                if 1 <= num_players <= 4:
                    break
                else:
                    print("Geçersiz oyuncu sayısı. Lütfen 1 ile 4 arasında bir değer girin.")
            except ValueError:
                print("Geçersiz bir değer girdiniz. Lütfen bir sayı girin.")

        # Dünya boyutunu al
        rows, cols = get_world_size()

        # Oyuncuları oluştur
        players = {}
        for i in range(1, num_players + 1):
            background_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170), 4: (242, 229, 111)}
            player_color = background_color[i]

            font_color = {1: (127, 0, 0), 2: (0, 0, 191), 3: (0, 127, 0), 4: (249, 187, 0)}
            player_second = font_color[i]

            players[i] = {'id': i, 'color': player_second, 'back_color': player_color, 'name': f"Oyuncu {i}", 'warrior_position': None, 'guard_name': f"M{i}", 'guard_position': None, 'resources': 201}

        place_guards(players, rows, cols)  # Oyuncu muhafızlarını yerleştir
        available_positions = {(x, y): None for x in range(rows) for y in range(cols)}  # Boş konumları belirlemek için bir liste oluştur
        warriors_matrix = [[None for _ in range(cols)] for _ in range(rows)]  # Oyuncu savaşçılarını saklamak için bir matris oluştur
        potential_positions = [[False for _ in range(cols)] for _ in range(rows)]  # Her bir karenin muhtemel bir yerleşim alanı olup olmadığını gösteren bir iki boyutlu liste oluştur

        # Oyun döngüsü
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))  # Ekranı temizle
            draw_grid(screen, rows, cols, 640, players, available_positions.keys())  # Izgara çizimini yap

            # Oyuncu muhafızlarını çiz
            for player in players:
                guard_position = players[player]['guard_position']
                square_size = 640 // rows
                font = pygame.font.Font(None, 36)
                text = font.render(f"M{player}", True, players[player]['color'])
                screen.blit(text, (guard_position[1] * square_size + square_size // 2 - text.get_width() // 2, guard_position[0] * square_size + square_size // 2 - text.get_height() // 2))

            # İlk turda ise, kullanıcıya bir sonraki tura geçilsin mi sor
            if first_round:
                draw_resource_management(screen, players, rows)
                pygame.display.flip()
                if ask_for_next_round():
                    first_round = False  # İlk tur bitti
                    for player in players:
                        guard_position = players[player]['guard_position']
                        square_size = 640 // rows
                        pygame.draw.rect(screen, players[player]['back_color'], (
                        guard_position[1] * square_size, guard_position[0] * square_size, square_size, square_size))
                        font = pygame.font.Font(None, 36)
                        text = font.render(f"M{player}", True, players[player]['color'])
                        screen.blit(text, (guard_position[1] * square_size + square_size // 2 - text.get_width() // 2,
                                           guard_position[0] * square_size + square_size // 2 - text.get_height() // 2))

                    # Potansiyel muhafız konumlarını al ve uygun arka plan rengiyle boyayın
                    potential_guard_positions = place_potential_guards(players, rows, cols)
                    for pos in potential_guard_positions:
                        player_id = pos[2]
                        back_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170),4: (242, 229, 111)}  
                        pygame.draw.rect(screen, back_color[player_id], (pos[1] * square_size, pos[0] * square_size, square_size, square_size))

                    draw_grid(screen, rows, cols, 640, players, available_positions.keys())
                    pygame.display.flip()
                else:
                    pygame.quit()
                    sys.exit()
            else:
                # İkinci turda, muhafızların olduğu karelerin arkaplanını boyadıktan sonra potansiyel yeni muhafız konumlarını belirleyin ve uygun arka plan renkleriyle boyayın
                for player in players:
                    guard_position = players[player]['guard_position']
                    square_size = 640 // rows
                    pygame.draw.rect(screen, players[player]['back_color'], (
                    guard_position[1] * square_size, guard_position[0] * square_size, square_size,
                    square_size))  # Muhtemel muhafız yerleştirildiğinde bu arka planı düzeltilcek
                    font = pygame.font.Font(None, 36)
                    text = font.render(f"M{player}", True, players[player]['color'])  # M'lerin rengi burdan güncellenecek
                    screen.blit(text, (guard_position[1] * square_size + square_size // 2 - text.get_width() // 2,
                                       guard_position[0] * square_size + square_size // 2 - text.get_height() // 2))

                # Potansiyel muhafız konumlarını al ve uygun arka plan rengiyle boyayın.
                potential_warrior_positions = place_potential_warriors(players, rows, cols)
                for pos in potential_guard_positions:
                    player_id = pos[2]
                    back_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170), 4: (242, 229, 111)} 
                    pygame.draw.rect(screen, back_color[player_id], (pos[1] * square_size, pos[0] * square_size, square_size, square_size))

                # Muhtemel yerleşim alanlarını çiz.Yani savaşçının çevresini çiziyor.
                for x in range(rows):
                    for y in range(cols):
                        player_id = pos[2]
                        back_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170), 4: (242, 229, 111)}  
                        if potential_positions[x][y]:
                            pygame.draw.rect(screen, ((back_color[player_id])), (
                            y * square_size, x * square_size, square_size, square_size))  # 255,255,255

                # Savaşçının bulunduğu karenin arka planını boyayın
                for player in players:
                    warrior_position = players[player]['warrior_position']  # Savaşçının pozisyonunu al
                    square_size = 640 // rows
                    pygame.draw.rect(screen, players[player]['back_color'], (warrior_position[0] * square_size, warrior_position[1] * square_size, square_size, square_size))

                # Potansiyel savaşçı pozisyonlarını al ve ekrana çiz
                potential_warrior_positions = place_potential_warriors(players, rows, cols)
                for pos in potential_warrior_positions:
                    player_id = pos[2]
                    back_color = {1: (255, 170, 170), 2: (170, 212, 255), 3: (170, 255, 170), 4: (242, 229, 111)}
                    pygame.draw.rect(screen, back_color[player_id],(pos[1] * square_size, pos[0] * square_size, square_size, square_size))
                    warrior_name = players[player_id]['warrior_name']
                    draw_warrior(screen, (pos[1], pos[0]), square_size, players[player_id]['color'],f"{warrior_name}{player_id}")

                for player in players:
                    guard_position = players[player]['guard_position']
                    square_size = 640 // rows
                    pygame.draw.rect(screen, players[player]['back_color'], (
                    guard_position[1] * square_size, guard_position[0] * square_size, square_size, square_size)) 
                    font = pygame.font.Font(None, 36)
                    text = font.render(f"M{player}", True, players[player]['color']) 
                    screen.blit(text, (guard_position[1] * square_size + square_size // 2 - text.get_width() // 2,
                                       guard_position[0] * square_size + square_size // 2 - text.get_height() // 2))

            # Oyuncuların savaşçılarını ekrana çiz
            for x in range(rows):
                for y in range(cols):
                    if warriors_matrix[x][y]:
                        player_id = warriors_matrix[x][y]['player_id']
                        color = warriors_matrix[x][y]['color']
                        warrior_name = warriors_matrix[x][y]['warrior_name']
                        pygame.draw.rect(screen, players[player_id]['back_color'],(x * square_size, y * square_size, square_size, square_size))
                        draw_warrior(screen, (x, y), 640 // rows, color, f"{warrior_name}{player_id}")

            # Savaşçıları matrise yerleştir
            for player_id, player_info in players.items():
                warrior_position = player_info['warrior_position']
                if warrior_position:
                    x, y = warrior_position
                    warriors_matrix[x][y] = {'player_id': player_id, 'player_name': player_info['name'], 'warrior_name': player_info['warrior_name'], 'color': player_info['color']}

            # Potansiyel pozisyonları güncelle ve ekrana çiz
            update_and_draw_potential_positions(screen, square_size, players, rows, cols)

            # Savaşçıları ekrana çiz
            for x in range(rows):
                for y in range(cols):
                    if warriors_matrix[x][y]:
                        warrior_info = warriors_matrix[x][y]
                        draw_warrior(screen, (x, y), square_size, warrior_info['color'], f"{warrior_info['warrior_name']}{warrior_info['player_id']}")

            update_and_draw_potential_positions(screen, square_size, players, rows, cols)  # Potansiyel pozisyonları güncelle ve ekrana çiz

            resource_management_area = (
            rows * square_size, 0, 210, rows * square_size)  # Kaynak yönetimi alanını belirle
            pygame.draw.rect(screen, (0, 0, 0),
                             resource_management_area)  # Kaynak bilgilerinin üst üste gelmemesi için siyaha boya

            total_warriors = count_warriors(warriors_matrix)  # Her tur başında savaşçı sayısını hesapla
            update_resources(players, total_warriors)  # Her tur başında kaynakları güncelle
            draw_resource_management(screen, players, rows)

            draw_grid(screen, rows, cols, 640, players, available_positions.keys())
            pygame.display.flip()

            # Kullanıcıya bir sonraki tura geçilsin mi sor
            if ask_for_next_round():
                for player_id in players:
                    fighter_count = ask_for_fighter_count(player_id)
                    # Potansiyel savaşçı konumlarını al ve uygun renkte çiz
                    potential_warrior_positions = place_potential_warriors(players, rows, cols)
                    for pos in potential_warrior_positions:
                        x, y, current_player_id = pos
                        potential_positions[x][y] = True
                    pygame.display.flip()
                    if ask_for_ai_decision(player_id, players):
                        valid_positions = get_valid_placement_guard_positions(player_id, rows, cols,players[player_id]['guard_position'])
                        ai_place_warriors(player_id, players, rows, cols, valid_positions, warriors_matrix)
                    else:
                        for _ in range(fighter_count):
                            place_warrior_manually(player_id, players, warriors_matrix, available_positions)

        pygame.quit()

if __name__ == "__main__":
    main()




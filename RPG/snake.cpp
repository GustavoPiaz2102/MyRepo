#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h> // Necessário para Sprites
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <ctime>

// ==========================================
// CONFIGURAÇÕES
// ==========================================
const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;
const int GRID_SIZE = 25; 
const int COLS = SCREEN_WIDTH / GRID_SIZE;
const int ROWS = SCREEN_HEIGHT / GRID_SIZE;

const std::string FONT_PATH = "/usr/share/fonts/TTF/DejaVuSans.ttf"; 
const std::string SHOP_FILE = "shop.json";
const std::string SAVE_FILE = "save.json";

// Cores Básicas
const SDL_Color CLR_BG = {20, 20, 20, 255};
const SDL_Color CLR_TEXT = {255, 255, 255, 255};
const SDL_Color CLR_HIGHLIGHT = {255, 215, 0, 255};

enum GameState { MENU, GAME, SHOP, GAME_OVER };
enum FruitType { TYPE_FOOD, TYPE_MONEY, TYPE_CHEST };
enum RenderMode { MODE_COLOR, MODE_CHAR, MODE_SPRITE };

// ==========================================
// ESTRUTURAS
// ==========================================
struct Item {
    std::string name;
    int price;
    bool owned;
    bool equipped;
    
    // Dados de Renderização
    RenderMode mode;
    SDL_Color color;      // Para MODE_COLOR e cor do texto em MODE_CHAR
    char character;       // Para MODE_CHAR
    std::string spritePath; // Para MODE_SPRITE
    SDL_Texture* texture;   // Textura carregada em memória
};

struct PlayerData {
    int points;
    std::vector<Item> inventory;
};

struct Point { 
    int x, y; 
    bool operator==(const Point& o) const { return x==o.x && y==o.y; }
};

// ==========================================
// GLOBAIS
// ==========================================
PlayerData player;
GameState currentState = MENU;
SDL_Window* window = nullptr;
SDL_Renderer* renderer = nullptr;
TTF_Font* font = nullptr;

Point fruitPos;
FruitType currentFruitType = TYPE_FOOD;
std::string notificationMsg = "";
Uint32 notificationTime = 0;

// ==========================================
// UTILITÁRIOS
// ==========================================

// Parse JSON manual (Simples)
std::string getJsonValue(std::string content, std::string key) {
    size_t keyPos = content.find("\"" + key + "\"");
    if (keyPos == std::string::npos) return "";
    size_t colonPos = content.find(":", keyPos);
    if (colonPos == std::string::npos) return "";
    size_t valueStart = content.find_first_not_of(" \t\n\r", colonPos + 1);
    
    if (content[valueStart] == '"') {
        size_t valueEnd = content.find("\"", valueStart + 1);
        return content.substr(valueStart + 1, valueEnd - valueStart - 1);
    }
    if (isdigit(content[valueStart]) || content[valueStart] == '-') {
        size_t valueEnd = content.find_first_not_of("0123456789-", valueStart);
        if (valueEnd == std::string::npos) return content.substr(valueStart);
        return content.substr(valueStart, valueEnd - valueStart);
    }
    return "";
}

SDL_Texture* LoadTexture(std::string path) {
    SDL_Surface* loadedSurface = IMG_Load(path.c_str());
    if (loadedSurface == NULL) {
        // Se falhar, retorna NULL (o jogo deve tratar desenhando cor ou char)
        return NULL; 
    }
    SDL_Texture* newTexture = SDL_CreateTextureFromSurface(renderer, loadedSurface);
    SDL_FreeSurface(loadedSurface);
    return newTexture;
}

void LoadShop() {
    player.inventory.clear();
    std::ifstream checkFile(SHOP_FILE);
    
    // Cria arquivo padrão com exemplos de COR, CHAR e SPRITE
    if (!checkFile.good()) {
        std::ofstream outfile(SHOP_FILE);
        // Exemplo Cor
        outfile << "{\"name\": \"Padrao\", \"type\": \"color\", \"r\": 0, \"g\": 255, \"b\": 0, \"price\": 0}\n";
        // Exemplo Char
        outfile << "{\"name\": \"OldSchool\", \"type\": \"char\", \"symbol\": \"#\", \"r\": 0, \"g\": 255, \"b\": 0, \"price\": 50}\n";
        outfile << "{\"name\": \"Matematica\", \"type\": \"char\", \"symbol\": \"Pi\", \"r\": 255, \"g\": 0, \"b\": 255, \"price\": 100}\n";
        // Exemplo Sprite (Precisa ter o arquivo snake.png na pasta, senao falha)
        outfile << "{\"name\": \"Realista\", \"type\": \"sprite\", \"path\": \"snake.png\", \"price\": 500}\n";
        // Mais Cores
        outfile << "{\"name\": \"Ouro\", \"type\": \"color\", \"r\": 255, \"g\": 215, \"b\": 0, \"price\": 200}\n";
        outfile.close();
    }
    checkFile.close();

    std::ifstream file(SHOP_FILE);
    std::string line;
    while (std::getline(file, line)) {
        if (line.find("{") != std::string::npos) {
            Item item;
            item.texture = nullptr;
            item.name = getJsonValue(line, "name");
            
            // Determina o Modo de Renderização
            std::string typeStr = getJsonValue(line, "type");
            if (typeStr == "sprite") item.mode = MODE_SPRITE;
            else if (typeStr == "char") item.mode = MODE_CHAR;
            else item.mode = MODE_COLOR;

            // Carrega Propriedades Específicas
            if (item.mode == MODE_SPRITE) {
                item.spritePath = getJsonValue(line, "path");
                item.texture = LoadTexture(item.spritePath);
                // Se falhar carregar a imagem, fallback para cor branca
                if (!item.texture) {
                    item.mode = MODE_COLOR;
                    item.color = {255, 255, 255, 255};
                }
            }
            
            if (item.mode == MODE_CHAR) {
                std::string s = getJsonValue(line, "symbol");
                item.character = s.empty() ? '?' : s[0];
            }

            // Lê cor (usada para o texto do char ou para o bloco de cor)
            std::string r = getJsonValue(line, "r");
            std::string g = getJsonValue(line, "g");
            std::string b = getJsonValue(line, "b");
            item.color = {(Uint8)(r.empty()?255:stoi(r)), (Uint8)(g.empty()?255:stoi(g)), (Uint8)(b.empty()?255:stoi(b)), 255};

            std::string priceStr = getJsonValue(line, "price");
            try { item.price = priceStr.empty() ? 0 : std::stoi(priceStr); } catch (...) { item.price = 999; }
            
            item.owned = (item.price == 0);
            item.equipped = (item.price == 0);
            player.inventory.push_back(item);
        }
    }
}

void SaveGame() {
    std::ofstream file(SAVE_FILE);
    file << "{\n  \"points\": " << player.points << ",\n  \"owned_items\": [";
    bool first = true;
    for (const auto& item : player.inventory) {
        if (item.owned) {
            if (!first) file << ",";
            file << "\"" << item.name << "\"";
            first = false;
        }
    }
    file << "],\n";
    std::string equippedName = "Padrao";
    for(const auto& item : player.inventory) if(item.equipped) equippedName = item.name;
    file << "  \"equipped\": \"" << equippedName << "\"\n}\n";
    file.close();
}

void LoadGame() {
    std::ifstream file(SAVE_FILE);
    player.points = 0;
    if (file.good()) {
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();
        std::string pStr = getJsonValue(content, "points");
        if (!pStr.empty()) try { player.points = std::stoi(pStr); } catch(...) {}
        
        std::string equippedName = getJsonValue(content, "equipped");
        for (auto& item : player.inventory) {
            if (content.find("\"" + item.name + "\"") != std::string::npos) item.owned = true;
            item.equipped = (item.name == equippedName);
        }
    }
}

// ==========================================
// RENDERIZAÇÃO
// ==========================================

void DrawText(std::string text, int x, int y, SDL_Color color, bool centered = false) {
    if (!font) return;
    SDL_Surface* surface = TTF_RenderText_Solid(font, text.c_str(), color);
    if (!surface) return;
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    SDL_Rect dstRect = { x, y, surface->w, surface->h };
    if (centered) dstRect.x -= surface->w / 2;
    SDL_RenderCopy(renderer, texture, NULL, &dstRect);
    SDL_FreeSurface(surface);
    SDL_DestroyTexture(texture);
}

// Função Genérica que decide como desenhar o Item
void DrawItem(int x, int y, const Item& item) {
    SDL_Rect rect = { x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE };

    if (item.mode == MODE_SPRITE && item.texture != nullptr) {
        SDL_RenderCopy(renderer, item.texture, NULL, &rect);
    } 
    else if (item.mode == MODE_CHAR) {
        // Desenha fundo preto pro char aparecer
        // SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        // SDL_RenderFillRect(renderer, &rect);
        std::string s(1, item.character);
        DrawText(s, x * GRID_SIZE + 5, y * GRID_SIZE, item.color);
    } 
    else { // MODE_COLOR
        SDL_SetRenderDrawColor(renderer, item.color.r, item.color.g, item.color.b, item.color.a);
        // Reduz um pixel para fazer borda
        rect.w -= 1; rect.h -= 1; 
        SDL_RenderFillRect(renderer, &rect);
    }
}

// ==========================================
// LÓGICA DO JOGO
// ==========================================
Point head = {COLS/2, ROWS/2}, dir = {0,0};
std::vector<Point> tail;
int sessionScore = 0;
Uint32 lastMoveTime = 0;
const int MOVE_DELAY = 100;

void SpawnFruit() {
    fruitPos = {rand() % COLS, rand() % ROWS};
    for(auto t : tail) if(t == fruitPos) SpawnFruit();
    if(head == fruitPos) SpawnFruit();

    int roll = rand() % 100;
    if (roll == 0) currentFruitType = TYPE_CHEST; 
    else if (roll < 5) currentFruitType = TYPE_MONEY;
    else currentFruitType = TYPE_FOOD;
}

void ResetGame() {
    head = {COLS/2, ROWS/2};
    dir = {0,0};
    tail.clear();
    sessionScore = 0;
    srand(time(0));
    SpawnFruit();
}

void UnlockRandomItem() {
    std::vector<int> notOwnedIndices;
    for(size_t i = 0; i < player.inventory.size(); i++) {
        if(!player.inventory[i].owned) notOwnedIndices.push_back(i);
    }

    if(!notOwnedIndices.empty()) {
        int idx = notOwnedIndices[rand() % notOwnedIndices.size()];
        player.inventory[idx].owned = true;
        notificationMsg = "Novo: " + player.inventory[idx].name + "!";
    } else {
        player.points += 500;
        notificationMsg = "Bau: +500 Pontos!";
    }
    notificationTime = SDL_GetTicks();
}

void UpdateGame() {
    Uint32 currentTime = SDL_GetTicks();
    if (currentTime - lastMoveTime < MOVE_DELAY) return;
    lastMoveTime = currentTime;

    if (dir.x == 0 && dir.y == 0) return;

    if (!tail.empty()) {
        for (size_t i = tail.size()-1; i > 0; i--) tail[i] = tail[i-1];
        tail[0] = head;
    }
    head.x += dir.x;
    head.y += dir.y;

    if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS) {
        SaveGame(); currentState = GAME_OVER; return;
    }
    for (auto t : tail) if (t == head) {
        SaveGame(); currentState = GAME_OVER; return;
    }

    if (head.x == fruitPos.x && head.y == fruitPos.y) {
        tail.push_back({-1,-1}); 
        if (currentFruitType == TYPE_FOOD) { sessionScore += 10; player.points += 10; } 
        else if (currentFruitType == TYPE_MONEY) { sessionScore += 100; player.points += 100; notificationMsg = "Bonus! +100"; notificationTime = SDL_GetTicks();}
        else if (currentFruitType == TYPE_CHEST) { UnlockRandomItem(); }
        SpawnFruit();
    }
}

// ==========================================
// RENDERIZAÇÃO DE TELAS
// ==========================================
int menuSelection = 0;

void RenderMenu() {
    DrawText("SNAKE RPG ULTIMATE", SCREEN_WIDTH/2, 100, CLR_HIGHLIGHT, true);
    DrawText("Pontos: " + std::to_string(player.points), SCREEN_WIDTH/2, 150, CLR_TEXT, true);

    std::string opts[] = { "JOGAR", "LOJA", "SAIR" };
    for (int i = 0; i < 3; i++) {
        SDL_Color c = (i == menuSelection) ? CLR_HIGHLIGHT : CLR_TEXT;
        std::string prefix = (i == menuSelection) ? "> " : "  ";
        DrawText(prefix + opts[i], SCREEN_WIDTH/2, 250 + (i * 50), c, true);
    }
}

void RenderShop() {
    DrawText("LOJA HIBRIDA", SCREEN_WIDTH/2, 30, CLR_HIGHLIGHT, true);
    DrawText("Pontos: " + std::to_string(player.points), SCREEN_WIDTH/2, 70, CLR_TEXT, true);

    int startY = 120;
    // Paginação simples se tiver muitos itens
    int maxItems = 10;
    int startIdx = (menuSelection / maxItems) * maxItems;
    
    for (size_t i = startIdx; i < player.inventory.size() && i < startIdx + maxItems; i++) {
        Item& it = player.inventory[i];
        SDL_Color c = ((int)i == menuSelection) ? CLR_HIGHLIGHT : CLR_TEXT;
        
        int drawY = startY + ((int)i - startIdx) * 40;

        // Preview do Item (Usa a mesma lógica do jogo)
        // Criamos um item temporário com posição 0,0 relativa ao menu
        SDL_Rect previewRect = { 200, drawY, 20, 20 };
        if (it.mode == MODE_SPRITE && it.texture) SDL_RenderCopy(renderer, it.texture, NULL, &previewRect);
        else if (it.mode == MODE_COLOR) {
            SDL_SetRenderDrawColor(renderer, it.color.r, it.color.g, it.color.b, 255);
            SDL_RenderFillRect(renderer, &previewRect);
        }
        else if (it.mode == MODE_CHAR) {
            std::string s(1, it.character);
            DrawText(s, 205, drawY, it.color);
        }

        std::string status;
        if (it.owned) status = it.equipped ? "[EQUIPADO]" : "[COMPRADO]";
        else status = "$" + std::to_string(it.price);

        std::string typeInfo = (it.mode == MODE_SPRITE) ? "(IMG)" : (it.mode == MODE_CHAR ? "(TXT)" : "(COR)");

        DrawText(it.name + " " + typeInfo + "  " + status, 240, drawY, c);
        if ((int)i == menuSelection) DrawText(">", 180, drawY, CLR_HIGHLIGHT);
    }
    DrawText("[X] Voltar", SCREEN_WIDTH/2, 560, {150,150,150,255}, true);
}

void RenderGameLoop() {
    // Fruta
    if (currentFruitType == TYPE_FOOD) DrawText("@", fruitPos.x * GRID_SIZE + 5, fruitPos.y * GRID_SIZE, {255, 50, 50, 255}); 
    else if (currentFruitType == TYPE_MONEY) DrawText("$", fruitPos.x * GRID_SIZE + 5, fruitPos.y * GRID_SIZE, {50, 255, 50, 255});
    else if (currentFruitType == TYPE_CHEST) {
        SDL_SetRenderDrawColor(renderer, 255, 215, 0, 255);
        SDL_Rect r = {fruitPos.x * GRID_SIZE, fruitPos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE};
        SDL_RenderDrawRect(renderer, &r);
        DrawText("?", fruitPos.x * GRID_SIZE + 5, fruitPos.y * GRID_SIZE, {100, 100, 255, 255});
    }

    // Desenha Cobra com o Item Equipado
    Item* equippedItem = nullptr;
    for(auto& i : player.inventory) if(i.equipped) equippedItem = &i;

    if (equippedItem) {
        DrawItem(head.x, head.y, *equippedItem);
        for (auto& t : tail) DrawItem(t.x, t.y, *equippedItem);
    } else {
        // Fallback se nada equipado
        SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
        SDL_Rect r = {head.x*GRID_SIZE, head.y*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1};
        SDL_RenderFillRect(renderer, &r);
    }

    DrawText("Score: " + std::to_string(sessionScore), 10, 10, CLR_TEXT);
    if (SDL_GetTicks() - notificationTime < 2000) DrawText(notificationMsg, SCREEN_WIDTH/2, 50, CLR_HIGHLIGHT, true);
}

// ==========================================
// MAIN
// ==========================================
int main(int argc, char* args[]) {
    // Inicializa Video e Fontes e Imagens (PNG/JPG)
    if (SDL_Init(SDL_INIT_VIDEO) < 0) return 1;
    if (TTF_Init() < 0) return 1;
    if (IMG_Init(IMG_INIT_PNG) == 0) return 1; // Inicializa loader de imagens

    window = SDL_CreateWindow("Snake RPG Ultimate", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    font = TTF_OpenFont(FONT_PATH.c_str(), 20);
    if (!font) std::cerr << "ERRO FONTE: Instale ttf-dejavu." << std::endl;

    LoadShop();
    LoadGame();

    bool running = true;
    SDL_Event e;

    while (running) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) running = false;
            
            if (e.type == SDL_KEYDOWN) {
                switch (currentState) {
                    case MENU:
                        if (e.key.keysym.sym == SDLK_UP && menuSelection > 0) menuSelection--;
                        if (e.key.keysym.sym == SDLK_DOWN && menuSelection < 2) menuSelection++;
                        if (e.key.keysym.sym == SDLK_RETURN) {
                            if (menuSelection == 0) { ResetGame(); currentState = GAME; }
                            if (menuSelection == 1) { 
                                menuSelection = 0; // RESETANDO SELECAO AO ENTRAR
                                currentState = SHOP; 
                            }
                            if (menuSelection == 2) running = false;
                        }
                        break;

                    case SHOP:
                        if (e.key.keysym.sym == SDLK_UP && menuSelection > 0) menuSelection--;
                        if (e.key.keysym.sym == SDLK_DOWN && menuSelection < (int)player.inventory.size() - 1) menuSelection++;
                        
                        // CORREÇÃO DO BUG AQUI:
                        if (e.key.keysym.sym == SDLK_x) { 
                            menuSelection = 0; // RESETANDO SELECAO AO SAIR
                            currentState = MENU; 
                        }
                        
                        if (e.key.keysym.sym == SDLK_RETURN) {
                            Item& it = player.inventory[menuSelection];
                            if (it.owned) {
                                for(auto& i : player.inventory) i.equipped = false;
                                it.equipped = true;
                                SaveGame();
                            } else if (player.points >= it.price) {
                                player.points -= it.price;
                                it.owned = true;
                                for(auto& i : player.inventory) i.equipped = false;
                                it.equipped = true;
                                SaveGame();
                            }
                        }
                        break;

                    case GAME:
                        if (e.key.keysym.sym == SDLK_UP && dir.y != 1) dir = {0, -1};
                        if (e.key.keysym.sym == SDLK_DOWN && dir.y != -1) dir = {0, 1};
                        if (e.key.keysym.sym == SDLK_LEFT && dir.x != 1) dir = {-1, 0};
                        if (e.key.keysym.sym == SDLK_RIGHT && dir.x != -1) dir = {1, 0};
                        if (e.key.keysym.sym == SDLK_x) { 
                            SaveGame(); 
                            menuSelection = 0; // RESET
                            currentState = MENU; 
                        }
                        break;
                    
                    case GAME_OVER:
                        if (e.key.keysym.sym == SDLK_RETURN) {
                            menuSelection = 0; // RESET
                            currentState = MENU;
                        }
                        break;
                }
            }
        }

        if (currentState == GAME) UpdateGame();

        SDL_SetRenderDrawColor(renderer, CLR_BG.r, CLR_BG.g, CLR_BG.b, 255);
        SDL_RenderClear(renderer);

        if (currentState == MENU) RenderMenu();
        else if (currentState == SHOP) RenderShop();
        else if (currentState == GAME) RenderGameLoop();
        else if (currentState == GAME_OVER) {
            DrawText("GAME OVER", SCREEN_WIDTH/2, 200, {255,0,0,255}, true);
            DrawText("Score Final: " + std::to_string(sessionScore), SCREEN_WIDTH/2, 250, CLR_TEXT, true);
            DrawText("ENTER para voltar", SCREEN_WIDTH/2, 400, CLR_TEXT, true);
        }

        SDL_RenderPresent(renderer);
    }

    if (font) TTF_CloseFont(font);
    // Limpar texturas
    for(auto& i : player.inventory) if(i.texture) SDL_DestroyTexture(i.texture);
    
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    TTF_Quit();
    SDL_Quit();

    return 0;
}
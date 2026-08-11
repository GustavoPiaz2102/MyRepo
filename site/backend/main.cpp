#include "httplib.h"
#include <fstream>
#include <iostream>
#include <sstream>

int main() {
	httplib::Server svr;

	// Servir a pasta frontend/ inteira como arquivos estáticos (CSS, JS, HTML)
	if (!svr.set_mount_point("/", "./frontend")) {
		std::cerr << "Erro: Pasta ./frontend não encontrada. Execute o programa da raiz do projeto." << std::endl;
		return 1;
	}

	// Criar a rota /api/horarios que lê o JSON da pasta data/
	svr.Get("/api/horarios", [](const httplib::Request &req, httplib::Response &res) {
		std::ifstream file("./data/horarios.json");

		if (file.is_open()) {
			std::stringstream buffer;
			buffer << file.rdbuf();
			res.set_content(buffer.str(), "application/json");
		} else {
			res.status = 500;
			res.set_content("{\"erro\": \"Arquivo data/horarios.json não encontrado\"}", "application/json");
		}
	});

	std::cout << "[Servidor C++] Rodando na porta 8080..." << std::endl;
	std::cout << "[Acesso] Abra http://localhost:8080 no seu navegador." << std::endl;

	svr.listen("localhost", 8080);

	return 0;
}
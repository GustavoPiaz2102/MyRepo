CXX = g++
CXXFLAGS = -O2 -std=c++11
LDFLAGS = -lpthread
TARGET = servidor
SRC = backend/main.cpp
HEADER = backend/httplib.h

all: $(HEADER) $(TARGET)

$(HEADER):
	@echo "Baixando httplib.h..."
	@wget -q -O $(HEADER) https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h || curl -s -o $(HEADER) https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h

$(TARGET): $(SRC)
	@echo "Compilando o backend..."
	$(CXX) $(CXXFLAGS) -Ibackend $(SRC) -o $(TARGET) $(LDFLAGS)
	@echo "Build concluído! Digite 'make run' para iniciar o servidor."

run: all
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all run clean
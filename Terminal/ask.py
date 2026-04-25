#!/usr/bin/env python3
"""
BIA — Interface Neural (Versão Corrigida)
"""

import sys, math, json, requests
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QTextEdit, QLineEdit, QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QTimer, QThread, Signal, QObject, QPointF, QRectF, QFile
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont,
    QRadialGradient, QPainterPath, QKeyEvent,
    QTextCursor, QPalette
)
from PySide6.QtUiTools import QUiLoader

# ─── Config ──────────────────────────────────────────────────────────────────

MODEL      = "bia"
OLLAMA_URL = "http://localhost:11434/api/chat"
HISTORY    = Path.home() / ".ollama_history.json"
UI_FILE    = Path(__file__).parent / "bia_layout.ui"

# ─── Paleta ──────────────────────────────────────────────────────────────────

BG     = QColor(6,   4,   2)
PANEL  = QColor(10,  7,   2)
BORDER = QColor(40,  25,  5)
GOLD   = QColor(255, 179,  0)
ORANGE = QColor(255, 109,  0)
EMBER  = QColor(255,  61,  0)
GLOW   = QColor(255, 248, 225)
DIM2   = QColor(100,  65, 15)

# ─── Worker Ollama ────────────────────────────────────────────────────────────

class OllamaWorker(QObject):
    finished = Signal(str)
    error    = Signal(str)

    def __init__(self, history: list):
        super().__init__()
        self.history = history

    def run(self):
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": self.history, "stream": False},
                timeout=120,
            )
            resp.raise_for_status()
            self.finished.emit(resp.json()["message"]["content"])
        except Exception as e:
            self.error.emit(str(e))

# ─── HUD (canvas animado) ────────────────────────────────────────────────────

class HUDWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle    = 0.0
        self.pulse    = 0.0
        self.thinking = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(280, 280)
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(33)

    def _tick(self):
        self.angle += 0.025
        self.pulse  = math.sin(self.angle * 3.0) * 0.5 + 0.5
        self.update()

    def set_thinking(self, v: bool):
        self.thinking = v

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h   = self.width(), self.height()
        cx, cy = w / 2, h / 2
        R      = min(w, h) * 0.42
        a      = self.angle
        pulse  = self.pulse

        v = QRadialGradient(cx, cy, R * 1.6)
        v.setColorAt(0.0, QColor(15, 10, 3, 180))
        v.setColorAt(1.0, QColor(0, 0, 0, 240))
        p.fillRect(0, 0, w, h, v)

        gc = QColor(255, 120, 0, 18 + int(pulse * 22))
        gg = QRadialGradient(cx, cy, R * 1.1)
        gg.setColorAt(0.0, gc)
        gg.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.setBrush(gg); p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx, cy), R * 1.1, R * 1.1)

        p.setPen(QPen(QColor(50, 32, 5, 120), 1.0, Qt.DotLine))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(cx, cy), R * 0.97, R * 0.97)

        # Anel 3
        r3_in, r3_out = R * 0.78, R * 0.88
        for i in range(36):
            frac     = i / 36
            base_ang = frac * 2 * math.pi + a * 0.6
            wave     = math.sin(frac * math.pi * 6 + a * 2.5)
            if wave < -0.3: continue
            intensity = max(0.0, wave)
            col = QColor(
                int(ORANGE.red() * 0.4 + GOLD.red() * 0.6 * intensity),
                int(ORANGE.green() * 0.4 + GOLD.green() * 0.6 * intensity),
                int(ORANGE.blue() * 0.4 + GOLD.blue() * 0.6 * intensity),
                int(80 + 160 * intensity),
            )
            pen = QPen(col, 2.8); pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            gap = 0.06
            p.drawLine(
                QPointF(cx + math.cos(base_ang + gap) * r3_in,  cy + math.sin(base_ang + gap) * r3_in),
                QPointF(cx + math.cos(base_ang + gap) * r3_out, cy + math.sin(base_ang + gap) * r3_out),
            )

        # Anel 2
        r2 = R * 0.62
        for i in range(24):
            frac     = i / 24
            base_ang = frac * 2 * math.pi - a * 1.4
            wave     = math.cos(frac * math.pi * 4 - a * 3.0)
            if wave < 0.0: continue
            col = QColor(255, 179, 0, int(60 + 180 * wave))
            pen = QPen(col, 2.2); pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            span = 0.18
            path = QPainterPath()
            path.moveTo(cx + math.cos(base_ang - span) * (r2 - 5), cy + math.sin(base_ang - span) * (r2 - 5))
            path.lineTo(cx + math.cos(base_ang) * (r2 + 5), cy + math.sin(base_ang) * (r2 + 5))
            path.lineTo(cx + math.cos(base_ang + span) * (r2 - 5), cy + math.sin(base_ang + span) * (r2 - 5))
            p.drawPath(path)

        # Anel 1
        r1 = R * 0.38
        for i in range(12):
            frac     = i / 12
            base_ang = frac * 2 * math.pi + a * 2.8
            wave     = math.sin(frac * math.pi * 12 + a * 5)
            alpha    = int(80 + 170 * max(0, wave))
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 80, 0, alpha))
            path = QPainterPath()
            path.moveTo(cx + math.cos(base_ang) * (r1 + 8), cy + math.sin(base_ang) * (r1 + 8))
            path.lineTo(cx + math.cos(base_ang + 0.25) * (r1 - 6), cy + math.sin(base_ang + 0.25) * (r1 - 6))
            path.lineTo(cx + math.cos(base_ang - 0.25) * (r1 - 6), cy + math.sin(base_ang - 0.25) * (r1 - 6))
            path.closeSubpath()
            p.drawPath(path)

        # Núcleo
        core_r = R * 0.18
        if self.thinking:
            for layer in range(4):
                lr   = core_r * (0.5 + layer * 0.3) * (0.8 + 0.2 * pulse)
                bang = a * (3 + layer) + layer * math.pi / 3
                col  = QColor(255, 60 + layer * 30, 0, int(200 - layer * 35))
                g = QRadialGradient(cx + math.cos(bang) * lr * 0.3, cy + math.sin(bang) * lr * 0.3, lr)
                g.setColorAt(0.0, col)
                g.setColorAt(1.0, QColor(0, 0, 0, 0))
                p.setBrush(g); p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(cx, cy), lr, lr)
        else:
            for layer in range(3):
                lr  = core_r * (1.0 - layer * 0.25) * (0.75 + 0.25 * pulse)
                t   = 1.0 - layer / 3
                col = QColor(255, int(220*t + 179*(1-t)), int(200*t), int(220*t))
                g = QRadialGradient(cx, cy, lr)
                g.setColorAt(0.0, col)
                g.setColorAt(0.6, QColor(255, 140, 0, int(80*t)))
                g.setColorAt(1.0, QColor(0, 0, 0, 0))
                p.setBrush(g); p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(cx, cy), lr, lr)

        p.setPen(QPen(QColor(0, 0, 0, 18), 1))
        for y in range(0, h, 3): p.drawLine(0, y, w, y)

        font = QFont("monospace", 8)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.setPen(EMBER if self.thinking else GOLD)
        label = "● PROCESSANDO" if self.thinking else "● ONLINE"
        p.drawText(QRectF(0, h - 26, w, 20), Qt.AlignCenter, label)
        p.end()

# ─── Chat Display ─────────────────────────────────────────────────────────────

class ChatDisplay(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                color: {GLOW.name()};
                font-family: 'JetBrains Mono', 'Fira Code', monospace;
                font-size: 13px;
                padding: 8px 12px;
                selection-background-color: {GOLD.name()};
            }}
            QScrollBar:vertical {{ background: {BG.name()}; width: 6px; border: none; }}
            QScrollBar::handle:vertical {{ background: {DIM2.name()}; border-radius: 3px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

    def append_user(self, text: str):
        self.moveCursor(QTextCursor.End)
        self.insertHtml(f'<p style="margin:4px 0;"><span style="color:{GOLD.name()};font-weight:bold;">▸ Gustavo</span><span style="color:{DIM2.name()};">  ──  </span><span style="color:{GLOW.name()};">{text}</span></p>')
        self._bottom()

    def append_bia(self, text: str):
        safe = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
        self.moveCursor(QTextCursor.End)
        self.insertHtml(f'<p style="margin:4px 0 12px 0;"><span style="color:{ORANGE.name()};font-weight:bold;">◈ Bia</span><span style="color:{DIM2.name()};">  ──  </span><span style="color:{GLOW.name()};">{safe}</span></p>')
        self._bottom()

    def append_system(self, text: str):
        self.moveCursor(QTextCursor.End)
        self.insertHtml(f'<p style="margin:2px 0;color:{DIM2.name()};font-size:11px;">{text}</p>')
        self._bottom()

    def append_error(self, text: str):
        self.moveCursor(QTextCursor.End)
        self.insertHtml(f'<p style="margin:4px 0;color:{EMBER.name()};"><b>✗ Erro:</b> {text}</p>')
        self._bottom()

    def _bottom(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

# ─── Input Bar ────────────────────────────────────────────────────────────────

class InputBar(QWidget):
    submitted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(52)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        
        self.label = QLabel("GUSTAVO ›› ")
        self.label.setStyleSheet(f"color:{GOLD.name()}; font-family:monospace; font-size:13px; font-weight:bold;")
        layout.addWidget(self.label)

        self.field = QLineEdit()
        self.field.setFrame(False)
        self.field.setStyleSheet(f"QLineEdit {{ background:transparent; color:{GLOW.name()}; font-family:monospace; font-size:13px; }}")
        self.field.returnPressed.connect(self._submit)
        layout.addWidget(self.field)

        self.setStyleSheet(f"InputBar {{ background:{QColor(12,8,2).name()}; border-top:1px solid {ORANGE.name()}; }}")

    def _submit(self):
        t = self.field.text().strip()
        if t:
            self.submitted.emit(t)
            self.field.clear()

    def set_enabled(self, v: bool):
        self.field.setEnabled(v)
        self.label.setStyleSheet(f"color:{GOLD.name() if v else DIM2.name()}; font-family:monospace; font-size:13px; font-weight:bold;")

    def focus(self): self.field.setFocus()

# ─── Info Bar ─────────────────────────────────────────────────────────────────

class InfoBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        t = QTimer(self)
        t.timeout.connect(self.update)
        t.start(1000)

    def paintEvent(self, _):
        p = QPainter(self)
        p.fillRect(self.rect(), PANEL)
        font = QFont("monospace", 9)
        p.setFont(font)
        now = datetime.now()
        items = [(GOLD, "BIA NEURAL INTERFACE"), (DIM2, "  │  "), (ORANGE, "HORA "), (GLOW, now.strftime("%H:%M:%S"))]
        x = 14
        for col, txt in items:
            p.setPen(col)
            p.drawText(x, 24, txt)
            x += p.fontMetrics().horizontalAdvance(txt)
        p.end()

# ─── Janela Principal ─────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    _reply_ready = Signal(str)
    _error_ready = Signal(str)

    def __init__(self):
        super().__init__()
        self.history = self._load_history()

        # Registro e Carregamento do UI
        loader = QUiLoader()
        loader.registerCustomWidget(HUDWidget)
        loader.registerCustomWidget(ChatDisplay)
        loader.registerCustomWidget(InputBar)
        loader.registerCustomWidget(InfoBar)

        qfile = QFile(str(UI_FILE))
        if not qfile.open(QFile.ReadOnly):
            raise RuntimeError(f"Não abriu {UI_FILE}")
        
        # IMPORTANTE: Carregamos o container sem passar 'self' como parent inicial
        ui_container = loader.load(qfile)
        qfile.close()

        # DEFINE O CENTRAL WIDGET CORRETAMENTE
        self.setCentralWidget(ui_container.centralwidget)
        self.setWindowTitle("BIA — Interface Neural")
        self.resize(1200, 720)

        # Busca referências dentro do centralWidget
        self.hud       = self.findChild(HUDWidget, "hud")
        self.chat      = self.findChild(ChatDisplay, "chat")
        self.input_bar = self.findChild(InputBar, "input_bar")

        self._apply_styles()

        self._reply_ready.connect(self._on_reply)
        self._error_ready.connect(self._on_error)
        self.input_bar.submitted.connect(self._on_submit)

        self._load_history_to_chat()
        self.input_bar.focus()

    def _apply_styles(self):
        # Seletores específicos usando o nome do objeto (#) evitam que tudo fique preto
        self.setStyleSheet(f"QMainWindow {{ background:{BG.name()}; }}")
        
        lp = self.findChild(QWidget, "left_panel")
        if lp: lp.setStyleSheet(f"QWidget#left_panel {{ background:{PANEL.name()}; border-right:1px solid {BORDER.name()}; }}")
        
        rp = self.findChild(QWidget, "right_panel")
        if rp: rp.setStyleSheet(f"QWidget#right_panel {{ background:{BG.name()}; }}")

    def _load_history(self) -> list:
        return json.load(open(HISTORY)) if HISTORY.exists() else []

    def _save_history(self):
        json.dump(self.history, open(HISTORY, "w"))

    def _load_history_to_chat(self):
        self.chat.append_system(f"BIA Neural Interface  ·  modelo: {MODEL}")
        for msg in self.history[-10:]:
            if msg["role"] == "user": self.chat.append_user(msg["content"])
            else: self.chat.append_bia(msg["content"])

    def _on_submit(self, text: str):
        self.chat.append_user(text)
        self.history.append({"role": "user", "content": text})
        self.input_bar.set_enabled(False)
        self.hud.set_thinking(True)

        self.worker = OllamaWorker(list(self.history))  # <-- self.worker, não local
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._reply_ready.emit)
        self.worker.error.connect(self._error_ready.emit)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)  # <-- limpa depois
        self.thread.start()

    def _on_reply(self, text: str):
        self.history.append({"role": "assistant", "content": text})
        self._save_history()
        self.chat.append_bia(text)
        self.input_bar.set_enabled(True)
        self.hud.set_thinking(False)
        self.input_bar.focus()

    def _on_error(self, err: str):
        self.chat.append_error(err)
        self.input_bar.set_enabled(True)
        self.hud.set_thinking(False)

    def keyPressEvent(self, e: QKeyEvent):
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_L:
            self.history = []; self._save_history(); self.chat.clear()
        super().keyPressEvent(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
